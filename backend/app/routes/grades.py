"""
Rutas para grados educativos.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError as MarshmallowValidationError

from .. import db
from ..models import Grade
from ..schemas import GradeSchema, GradeCreateSchema, GradeUpdateSchema
from ..exceptions import (
    ValidationError,
    ConflictError,
    DatabaseError,
    ResourceNotFoundError,
)
from ..decorators import admin_required

grades_bp = Blueprint('grades', __name__, url_prefix='/api/grades')

grade_schema = GradeSchema()
grade_create_schema = GradeCreateSchema()
grade_update_schema = GradeUpdateSchema()


@grades_bp.route("", methods=["GET"])
def list_grades():
    """
    Listar todos los grados educativos ordenados por nivel.

    Query params:
        - page: número de página (default: 1)
        - per_page: resultados por página (default: 50, max: 100)

    Returns:
        200: Lista de grados
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 50, type=int), 100)

    pagination = Grade.query.order_by(Grade.order).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "grades": [grade.to_dict() for grade in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "per_page": pagination.per_page
    }), 200


@grades_bp.route("", methods=["POST"])
@jwt_required()
@admin_required
def create_grade():
    """
    Crear un grado educativo (solo administradores).

    Body (JSON):
        - name: string (requerido)
        - order: int (requerido)
    """
    try:
        data = grade_create_schema.load(request.get_json() or {})
    except MarshmallowValidationError as e:
        raise ValidationError(str(e.messages))

    # Validar duplicados
    existing = Grade.query.filter(
        (db.func.lower(Grade.name) == data["name"].lower()) | (Grade.order == data["order"])
    ).first()
    if existing:
        if existing.name.lower() == data["name"].lower():
            raise ConflictError("Ya existe un grado con ese nombre")
        raise ConflictError("Ya existe un grado con ese orden")

    grade = Grade(name=data["name"], order=data["order"])

    try:
        db.session.add(grade)
        db.session.commit()
        return jsonify({
            "msg": "Grado creado exitosamente",
            "grade": grade_schema.dump(grade)
        }), 201
    except Exception as exc:
        db.session.rollback()
        raise DatabaseError("Error al crear el grado") from exc


@grades_bp.route("/<int:grade_id>", methods=["GET"])
def get_grade(grade_id):
    """Obtener un grado por ID."""
    grade = Grade.query.get(grade_id)
    if not grade:
        raise ResourceNotFoundError("Grado no encontrado")
    return jsonify(grade.to_dict()), 200


@grades_bp.route("/<int:grade_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_grade(grade_id):
    """
    Actualizar un grado educativo (solo administradores).
    """
    grade = Grade.query.get(grade_id)
    if not grade:
        raise ResourceNotFoundError("Grado no encontrado")

    try:
        data = grade_update_schema.load(request.get_json() or {})
    except MarshmallowValidationError as e:
        raise ValidationError(str(e.messages))

    if "name" in data and data["name"] != grade.name:
        duplicate = Grade.query.filter(
            Grade.id != grade_id,
            db.func.lower(Grade.name) == data["name"].lower()
        ).first()
        if duplicate:
            raise ConflictError("Ya existe un grado con ese nombre")
        grade.name = data["name"]

    if "order" in data and data["order"] != grade.order:
        duplicate = Grade.query.filter(
            Grade.id != grade_id,
            Grade.order == data["order"]
        ).first()
        if duplicate:
            raise ConflictError("Ya existe un grado con ese orden")
        grade.order = data["order"]

    try:
        db.session.commit()
        return jsonify({
            "msg": "Grado actualizado exitosamente",
            "grade": grade_schema.dump(grade)
        }), 200
    except Exception as exc:
        db.session.rollback()
        raise DatabaseError("Error al actualizar el grado") from exc


@grades_bp.route("/<int:grade_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_grade(grade_id):
    """
    Eliminar un grado educativo (solo administradores).
    """
    grade = Grade.query.get(grade_id)
    if not grade:
        raise ResourceNotFoundError("Grado no encontrado")

    if grade.courses:
        raise ConflictError("No puedes eliminar el grado porque tiene cursos asociados")

    if grade.users:
        raise ConflictError("No puedes eliminar el grado porque tiene usuarios asociados")

    try:
        db.session.delete(grade)
        db.session.commit()
        return jsonify({"msg": "Grado eliminado exitosamente"}), 200
    except Exception as exc:
        db.session.rollback()
        raise DatabaseError("Error al eliminar el grado") from exc
