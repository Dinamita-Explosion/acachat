"""
MÓDULO: GESTIÓN DE CURSOS
==========================

Endpoints para CRUD de cursos con permisos basados en roles.

Endpoints:
- GET    /courses                - Listar cursos (filtrado según rol)
- POST   /courses                - Crear curso (admin only)
- GET    /courses/my-courses     - Obtener mis cursos
- GET    /courses/:id            - Obtener un curso
- PUT    /courses/:id            - Actualizar curso (profesor del curso o admin)
- DELETE /courses/:id            - Eliminar curso (admin only)
"""

from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError as MarshmallowValidationError
from flask_jwt_extended import jwt_required

from .. import db
from ..models import Course, Institution, Grade, UserCourse
from ..schemas import (
    CourseCreateSchema,
    CourseUpdateSchema,
    CourseSchema
)
from ..exceptions import (
    ValidationError,
    ResourceNotFoundError,
    DatabaseError,
    AuthorizationError
)
from ..decorators import (
    admin_required,
    get_current_user,
    course_teacher_or_admin_required
)

# Blueprint
courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

# Schemas
course_create_schema = CourseCreateSchema()
course_update_schema = CourseUpdateSchema()
course_schema = CourseSchema()


@courses_bp.route("", methods=["GET"])
@jwt_required()
def list_courses():
    """
    Listar cursos según el rol del usuario.

    - Estudiantes: Solo ven sus cursos inscritos
    - Profesores: Ven sus cursos + todos los activos
    - Admins: Ven todos los cursos

    Query params:
        - institution_id: filtrar por institución
        - year: filtrar por año de inscripción
        - my_courses: true/false (solo mis cursos)
        - is_active: true/false (solo cursos activos/inactivos)
        - page: número de página (default: 1)
        - per_page: resultados por página (default: 20, max: 100)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Lista de cursos
    """
    user = get_current_user()

    # Parámetros de consulta
    institution_id = request.args.get('institution_id', type=int)
    year = request.args.get('year', type=int)
    my_courses_only = request.args.get('my_courses', 'false').lower() == 'true'
    is_active_filter = request.args.get('is_active')
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)

    # Query base según rol
    if my_courses_only or user.is_student():
        # Obtener IDs de cursos del usuario
        enrollments = UserCourse.query.filter_by(user_id=user.id)
        if year:
            enrollments = enrollments.filter_by(year=year)

        course_ids = [e.course_id for e in enrollments.all()]
        query = Course.query.filter(Course.id.in_(course_ids)) if course_ids else Course.query.filter(Course.id == -1)
    else:
        # Profesores y admins ven todos
        query = Course.query

    # Aplicar filtros
    if institution_id:
        query = query.filter_by(institution_id=institution_id)

    if is_active_filter is not None:
        is_active = is_active_filter.lower() == 'true'
        query = query.filter_by(is_active=is_active)
    else:
        # Por defecto solo mostrar activos (excepto para admins)
        if not user.is_admin():
            query = query.filter_by(is_active=True)

    # Paginación
    pagination = query.order_by(Course.nombre).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "courses": [course.to_dict() for course in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "per_page": pagination.per_page
    }), 200


@courses_bp.route("/my-courses", methods=["GET"])
@jwt_required()
def my_courses():
    """
    Obtener cursos del usuario actual (donde está inscrito o es profesor).

    Query params:
        - year: filtrar por año (opcional)
        - role_in_course: filtrar por rol en curso (student/teacher, opcional)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Lista de matrículas con cursos
    """
    user = get_current_user()

    # Parámetros
    year = request.args.get('year', type=int)
    role_in_course = request.args.get('role_in_course')

    # Query de inscripciones
    query = UserCourse.query.filter_by(user_id=user.id)

    if year:
        query = query.filter_by(year=year)

    if role_in_course and role_in_course in ['student', 'teacher']:
        query = query.filter_by(role_in_course=role_in_course)

    enrollments = query.order_by(UserCourse.enrolled_at.desc()).all()

    return jsonify({
        "enrollments": [enrollment.to_dict(include_course=True) for enrollment in enrollments]
    }), 200


@courses_bp.route("", methods=["POST"])
@jwt_required()
@admin_required
def create_course():
    """
    Crear un nuevo curso (solo administradores).

    Body (JSON):
        - nombre: string (requerido)
        - prompt: string (opcional)
        - institution_id: int (requerido)
        - grade_id: int (requerido)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        201: Curso creado
        400: Datos inválidos
        404: Institución no encontrada
        403: No autorizado
    """
    try:
        # Validar datos
        data = course_create_schema.load(request.get_json())
    except MarshmallowValidationError as e:
        current_app.logger.warning(f"Error de validación en creación de curso: {e.messages}")
        raise ValidationError(str(e.messages))

    # Verificar que la institución existe
    institution = Institution.query.get(data["institution_id"])
    if not institution:
        raise ResourceNotFoundError("Institución no encontrada")

    # Verificar que el grado existe
    grade = Grade.query.get(data["grade_id"])
    if not grade:
        raise ResourceNotFoundError("Grado no encontrado")

    # Crear curso
    course = Course(
        nombre=data["nombre"],
        prompt=data.get("prompt"),
        institution_id=data["institution_id"],
        grade_id=data["grade_id"],
        emoji=data.get("emoji") or '📘'
    )

    try:
        db.session.add(course)
        db.session.commit()

        current_app.logger.info(
            f"Curso creado: {course.nombre} (Institución: {institution.nombre}, Grado: {grade.name})"
        )

        return jsonify({
            "msg": "Curso creado exitosamente",
            "course": course.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al crear curso: {str(e)}")
        raise DatabaseError("Error al crear el curso")


@courses_bp.route("/<int:course_id>", methods=["GET"])
@jwt_required()
def get_course(course_id):
    """
    Obtener un curso por ID.

    El usuario debe estar inscrito en el curso O ser admin.

    Path params:
        - course_id: ID del curso

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Datos del curso
        403: No tiene acceso al curso
        404: Curso no encontrado
    """
    user = get_current_user()
    course = Course.query.get(course_id)

    if not course:
        raise ResourceNotFoundError("Curso no encontrado")

    # Verificar acceso
    if not user.is_admin():
        # Verificar si está inscrito
        enrollment = UserCourse.query.filter_by(
            user_id=user.id,
            course_id=course_id
        ).first()

        if not enrollment:
            raise AuthorizationError("No tienes acceso a este curso")

    return jsonify(course.to_dict()), 200


@courses_bp.route("/<int:course_id>", methods=["PUT"])
@jwt_required()
@course_teacher_or_admin_required(course_id_param='course_id')
def update_course(course_id):
    """
    Actualizar un curso.

    Solo el profesor del curso o un administrador puede hacerlo.

    Path params:
        - course_id: ID del curso

    Body (JSON):
        - nombre: string (opcional)
        - prompt: string (opcional)
        - institution_id: int (opcional)
        - grade_id: int (opcional)
        - is_active: bool (opcional, solo admin)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Curso actualizado
        400: Datos inválidos
        403: No autorizado
        404: Curso no encontrado
    """
    user = get_current_user()
    course = Course.query.get(course_id)

    if not course:
        raise ResourceNotFoundError("Curso no encontrado")

    try:
        # Validar datos
        data = course_update_schema.load(request.get_json() or {})
    except MarshmallowValidationError as e:
        raise ValidationError(str(e.messages))

    # Actualizar campos
    if "nombre" in data:
        course.nombre = data["nombre"]

    if "prompt" in data:
        course.prompt = data["prompt"]

    if "emoji" in data:
        course.emoji = data["emoji"] or '📘'

    if "institution_id" in data:
        # Verificar que la institución existe
        institution = Institution.query.get(data["institution_id"])
        if not institution:
            raise ResourceNotFoundError("Institución no encontrada")
        course.institution_id = data["institution_id"]

    if "grade_id" in data:
        grade = Grade.query.get(data["grade_id"])
        if not grade:
            raise ResourceNotFoundError("Grado no encontrado")
        course.grade_id = data["grade_id"]

    # Solo admins pueden cambiar is_active
    if "is_active" in data and user.is_admin():
        course.is_active = data["is_active"]

    try:
        db.session.commit()
        current_app.logger.info(f"Curso actualizado: {course.nombre}")

        return jsonify({
            "msg": "Curso actualizado exitosamente",
            "course": course.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al actualizar curso: {str(e)}")
        raise DatabaseError("Error al actualizar el curso")


@courses_bp.route("/<int:course_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_course(course_id):
    """
    Eliminar un curso (solo administradores).

    Nota: Esto es un soft delete (cambia is_active a False).
    También elimina todas las matrículas asociadas.

    Path params:
        - course_id: ID del curso

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Curso eliminado
        403: No autorizado
        404: Curso no encontrado
    """
    course = Course.query.get(course_id)

    if not course:
        raise ResourceNotFoundError("Curso no encontrado")

    try:
        # Soft delete
        course.is_active = False
        db.session.commit()

        current_app.logger.info(f"Curso desactivado (soft delete): {course.nombre}")

        return jsonify({
            "msg": "Curso eliminado exitosamente"
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al eliminar curso: {str(e)}")
        raise DatabaseError("Error al eliminar el curso")


# ==========================================
# ERROR HANDLERS
# ==========================================

@courses_bp.errorhandler(ValidationError)
@courses_bp.errorhandler(ResourceNotFoundError)
@courses_bp.errorhandler(DatabaseError)
@courses_bp.errorhandler(AuthorizationError)
def handle_app_error(error):
    """Maneja las excepciones personalizadas."""
    return jsonify({"msg": error.message}), error.status_code


@courses_bp.errorhandler(Exception)
def handle_unexpected_error(error):
    """Maneja errores inesperados."""
    current_app.logger.error(f"Error inesperado: {str(error)}", exc_info=True)
    return jsonify({"msg": "Error interno del servidor"}), 500
