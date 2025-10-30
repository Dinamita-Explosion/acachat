"""
MÓDULO: GESTIÓN DE MATRÍCULAS
==============================

Endpoints para inscripción de estudiantes y asignación de profesores.

Endpoints:
- POST   /enrollments                - Inscribir estudiante a curso
- POST   /enrollments/assign-teacher - Asignar profesor a curso (admin only)
- GET    /enrollments/course/:id     - Ver inscripciones de un curso (profesor/admin)
- DELETE /enrollments/:id            - Eliminar inscripción
"""

from datetime import datetime

from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError as MarshmallowValidationError
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from .. import db
from ..models import UserCourse, Course, User
from ..schemas import (
    EnrollmentCreateSchema,
    AssignTeacherSchema,
    EnrollmentSchema,
    BulkEnrollmentSchema,
)
from ..exceptions import (
    ValidationError,
    ResourceNotFoundError,
    DatabaseError,
    ConflictError,
    AuthorizationError
)
from ..decorators import (
    admin_required,
    get_current_user,
    course_teacher_or_admin_required
)

# Blueprint
enrollments_bp = Blueprint('enrollments', __name__, url_prefix='/api/enrollments')

# Schemas
enrollment_create_schema = EnrollmentCreateSchema()
assign_teacher_schema = AssignTeacherSchema()
enrollment_schema = EnrollmentSchema()
bulk_enrollment_schema = BulkEnrollmentSchema()


@enrollments_bp.route("", methods=["GET"])
@jwt_required()
@admin_required
def list_all_enrollments():
    """
    Listar todas las matrículas (solo administradores).

    Query params:
        - year: filtrar por año (opcional)
        - role_in_course: filtrar por rol (student/teacher, opcional)
        - course_id: filtrar por curso (opcional)
        - page: número de página (default: 1)
        - per_page: resultados por página (default: 50, max: 100)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Lista de matrículas
        403: No autorizado
    """
    # Parámetros de consulta
    year = request.args.get('year', type=int)
    role_in_course = request.args.get('role_in_course')
    course_id = request.args.get('course_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 50, type=int), 100)

    # Query base
    query = UserCourse.query

    # Aplicar filtros
    if year:
        query = query.filter_by(year=year)
    if role_in_course and role_in_course in ['student', 'teacher']:
        query = query.filter_by(role_in_course=role_in_course)
    if course_id:
        query = query.filter_by(course_id=course_id)

    # Paginación
    pagination = query.order_by(UserCourse.enrolled_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "enrollments": [enrollment.to_dict(include_course=True, include_user=True) for enrollment in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "per_page": pagination.per_page
    }), 200


@enrollments_bp.route("", methods=["POST"])
@jwt_required()
def enroll_student():
    """
    Inscribir un estudiante a un curso.

    - Los estudiantes pueden inscribirse a sí mismos
    - Los admins pueden inscribir a cualquier estudiante

    Body (JSON):
        - course_id: int (requerido)
        - year: int (requerido, rango 2000-2100)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        201: Inscripción exitosa
        400: Datos inválidos
        404: Curso no encontrado
        409: Ya inscrito en ese curso para ese año
    """
    user = get_current_user()

    # Solo estudiantes y admins pueden inscribirse
    if user.is_teacher() and not user.is_admin():
        raise AuthorizationError("Los profesores no pueden inscribirse en cursos")

    try:
        # Validar datos
        data = enrollment_create_schema.load(request.get_json())
    except MarshmallowValidationError as e:
        current_app.logger.warning(f"Error de validación en inscripción: {e.messages}")
        raise ValidationError(str(e.messages))

    # Verificar que el curso existe y está activo
    course = Course.query.get(data["course_id"])
    if not course or not course.is_active:
        raise ResourceNotFoundError("Curso no encontrado o inactivo")

    # Verificar si ya está inscrito
    existing_enrollment = UserCourse.query.filter_by(
        user_id=user.id,
        course_id=data["course_id"],
        year=data["year"]
    ).first()

    if existing_enrollment:
        raise ConflictError("Ya estás inscrito en este curso para este año")

    # Crear inscripción
    enrollment = UserCourse(
        user_id=user.id,
        course_id=data["course_id"],
        year=data["year"],
        role_in_course='student'
    )

    try:
        db.session.add(enrollment)
        db.session.commit()

        current_app.logger.info(
            f"Estudiante {user.email} inscrito en curso {course.nombre} (año {data['year']})"
        )

        return jsonify({
            "msg": "Inscripción exitosa",
            "enrollment": enrollment.to_dict(include_course=True)
        }), 201

    except IntegrityError:
        db.session.rollback()
        raise ConflictError("Ya estás inscrito en este curso para este año")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al inscribir estudiante: {str(e)}")
        raise DatabaseError("Error al procesar la inscripción")


@enrollments_bp.route("/assign-teacher", methods=["POST"])
@jwt_required()
@admin_required
def assign_teacher():
    """
    Asignar un profesor a un curso (solo administradores).

    Body (JSON):
        - user_id: int (requerido, debe ser un usuario con rol 'teacher')
        - course_id: int (requerido)
        - year: int (requerido, rango 2000-2100)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        201: Asignación exitosa
        400: Datos inválidos / Usuario no es profesor
        404: Usuario o curso no encontrado
        409: Ya asignado a ese curso
    """
    try:
        # Validar datos
        data = assign_teacher_schema.load(request.get_json())
    except MarshmallowValidationError as e:
        current_app.logger.warning(f"Error de validación en asignación: {e.messages}")
        raise ValidationError(str(e.messages))

    # Verificar que el usuario existe y es profesor
    teacher = User.query.get(data["user_id"])
    if not teacher or not teacher.is_active:
        raise ResourceNotFoundError("Usuario no encontrado o inactivo")

    if not teacher.is_teacher() and not teacher.is_admin():
        raise ValidationError("El usuario debe tener rol de profesor")

    # Verificar que el curso existe y está activo
    course = Course.query.get(data["course_id"])
    if not course or not course.is_active:
        raise ResourceNotFoundError("Curso no encontrado o inactivo")

    # Verificar si ya está asignado
    existing_enrollment = UserCourse.query.filter_by(
        user_id=data["user_id"],
        course_id=data["course_id"],
        year=data["year"]
    ).first()

    if existing_enrollment:
        raise ConflictError("Este profesor ya está asignado a este curso para este año")

    # Crear asignación
    enrollment = UserCourse(
        user_id=data["user_id"],
        course_id=data["course_id"],
        year=data["year"],
        role_in_course='teacher'
    )

    try:
        db.session.add(enrollment)
        db.session.commit()

        current_app.logger.info(
            f"Profesor {teacher.email} asignado a curso {course.nombre} (año {data['year']})"
        )

        return jsonify({
            "msg": "Profesor asignado exitosamente",
            "enrollment": enrollment.to_dict(include_course=True, include_user=True)
        }), 201

    except IntegrityError:
        db.session.rollback()
        raise ConflictError("Este profesor ya está asignado a este curso para este año")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al asignar profesor: {str(e)}")
        raise DatabaseError("Error al procesar la asignación")


@enrollments_bp.route("/bulk", methods=["POST"])
@jwt_required()
@admin_required
def bulk_enroll_students():
    """Inscribir múltiples estudiantes a un curso."""
    try:
        data = bulk_enrollment_schema.load(request.get_json() or {})
    except MarshmallowValidationError as exc:
        current_app.logger.warning(f"Error de validación en inscripción masiva: {exc.messages}")
        raise ValidationError(str(exc.messages))

    course = Course.query.get(data["course_id"])
    if not course or not course.is_active:
        raise ResourceNotFoundError("Curso no encontrado o inactivo")

    provided_user_ids = set(data.get("user_ids") or [])
    grade_id = data.get("grade_id")

    if not provided_user_ids and not grade_id:
        raise ValidationError("Selecciona estudiantes específicos o un grado completo.")

    if grade_id:
        grade_students = User.query.filter_by(grade_id=grade_id, role='student').with_entities(User.id).all()
        provided_user_ids.update(user_id for (user_id,) in grade_students)

    if not provided_user_ids:
        raise ValidationError("No hay estudiantes válidos para inscribir.")

    students = User.query.filter(User.id.in_(provided_user_ids), User.role == 'student', User.is_active.is_(True)).all()
    valid_user_ids = {student.id for student in students}

    if not valid_user_ids:
        raise ValidationError("Los estudiantes seleccionados no son válidos.")

    year = data.get("year") or datetime.utcnow().year

    existing = UserCourse.query.filter(
        UserCourse.course_id == course.id,
        UserCourse.year == year,
        UserCourse.user_id.in_(valid_user_ids)
    ).with_entities(UserCourse.user_id).all()
    already_enrolled = {user_id for (user_id,) in existing}

    new_user_ids = valid_user_ids - already_enrolled
    enrollments = [
        UserCourse(
            user_id=user_id,
            course_id=course.id,
            year=year,
            role_in_course='student'
        )
        for user_id in new_user_ids
    ]

    if not enrollments:
        return jsonify({
            "msg": "No se inscribieron nuevos estudiantes (ya estaban inscritos).",
            "created": 0,
            "skipped": len(valid_user_ids)
        }), 200

    try:
        db.session.bulk_save_objects(enrollments)
        db.session.commit()
        current_app.logger.info(
            f"{len(enrollments)} estudiantes inscritos al curso {course.nombre} (año {year})"
        )
        return jsonify({
            "msg": f"{len(enrollments)} estudiantes inscritos correctamente.",
            "created": len(enrollments),
            "skipped": len(valid_user_ids) - len(enrollments)
        }), 201
    except Exception as exc:
        db.session.rollback()
        current_app.logger.error(f"Error al procesar inscripción masiva: {exc}")
        raise DatabaseError("No se pudo completar la inscripción masiva")


@enrollments_bp.route("/course/<int:course_id>", methods=["GET"])
@jwt_required()
@course_teacher_or_admin_required(course_id_param='course_id')
def get_course_enrollments(course_id):
    """
    Ver todas las inscripciones de un curso.

    Solo profesores del curso o administradores pueden ver esto.

    Path params:
        - course_id: ID del curso

    Query params:
        - year: filtrar por año (opcional)
        - role_in_course: filtrar por rol (student/teacher, opcional)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Lista de inscripciones
        403: No autorizado
        404: Curso no encontrado
    """
    course = Course.query.get(course_id)
    if not course:
        raise ResourceNotFoundError("Curso no encontrado")

    # Parámetros de consulta
    year = request.args.get('year', type=int)
    role_in_course = request.args.get('role_in_course')

    # Query de inscripciones
    query = UserCourse.query.filter_by(course_id=course_id)

    if year:
        query = query.filter_by(year=year)

    if role_in_course and role_in_course in ['student', 'teacher']:
        query = query.filter_by(role_in_course=role_in_course)

    enrollments = query.order_by(UserCourse.enrolled_at.desc()).all()

    return jsonify({
        "course": course.to_dict(include_stats=False),
        "enrollments": [enrollment.to_dict(include_course=False, include_user=True) for enrollment in enrollments],
        "total": len(enrollments)
    }), 200


@enrollments_bp.route("/<int:enrollment_id>", methods=["DELETE"])
@jwt_required()
def delete_enrollment(enrollment_id):
    """
    Eliminar una inscripción.

    - Los estudiantes pueden eliminar sus propias inscripciones
    - Los admins pueden eliminar cualquier inscripción

    Path params:
        - enrollment_id: ID de la inscripción

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Inscripción eliminada
        403: No autorizado
        404: Inscripción no encontrada
    """
    user = get_current_user()
    enrollment = UserCourse.query.get(enrollment_id)

    if not enrollment:
        raise ResourceNotFoundError("Inscripción no encontrada")

    # Verificar permisos
    if not user.is_admin() and enrollment.user_id != user.id:
        raise AuthorizationError("No tienes permisos para eliminar esta inscripción")

    try:
        course_name = enrollment.course.nombre if enrollment.course else "Unknown"
        user_email = enrollment.user.email if enrollment.user else "Unknown"

        db.session.delete(enrollment)
        db.session.commit()

        current_app.logger.info(
            f"Inscripción eliminada: {user_email} del curso {course_name}"
        )

        return jsonify({
            "msg": "Inscripción eliminada exitosamente"
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al eliminar inscripción: {str(e)}")
        raise DatabaseError("Error al eliminar la inscripción")


# ==========================================
# ERROR HANDLERS
# ==========================================

@enrollments_bp.errorhandler(ValidationError)
@enrollments_bp.errorhandler(ResourceNotFoundError)
@enrollments_bp.errorhandler(DatabaseError)
@enrollments_bp.errorhandler(ConflictError)
@enrollments_bp.errorhandler(AuthorizationError)
def handle_app_error(error):
    """Maneja las excepciones personalizadas."""
    return jsonify({"msg": error.message}), error.status_code


@enrollments_bp.errorhandler(Exception)
def handle_unexpected_error(error):
    """Maneja errores inesperados."""
    current_app.logger.error(f"Error inesperado: {str(error)}", exc_info=True)
    return jsonify({"msg": "Error interno del servidor"}), 500
