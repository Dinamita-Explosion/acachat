"""
Rutas para instituciones educativas.
"""

from datetime import datetime

from flask import Blueprint, current_app, jsonify, request
from marshmallow import ValidationError as MarshmallowValidationError
from flask_jwt_extended import jwt_required

from .. import db
from ..decorators import admin_required
from ..exceptions import DatabaseError, ValidationError, ResourceNotFoundError
from ..models import Institution
from ..schemas import InstitutionCreateSchema, InstitutionUpdateSchema
from ..utils.file_handler import save_file

institutions_bp = Blueprint('institutions', __name__, url_prefix='/api/institutions')

institution_create_schema = InstitutionCreateSchema()
institution_update_schema = InstitutionUpdateSchema()


@institutions_bp.route("", methods=["GET"])
def list_institutions():
    """
    Listar todas las instituciones.

    Query params:
        - page: número de página (default: 1)
        - per_page: resultados por página (default: 20, max: 100)

    Returns:
        200: Lista de instituciones
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)

    pagination = Institution.query.order_by(Institution.nombre).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "institutions": [institution.to_dict() for institution in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "per_page": pagination.per_page
    }), 200


@institutions_bp.route("", methods=["POST"])
@jwt_required()
@admin_required
def create_institution():
    """
    Crear una nueva institución (solo administradores).

    Soporta JSON o multipart/form-data para permitir subida de logotipo.

    Returns:
        201: Institución creada
        400: Datos inválidos
        403: No autorizado
    """
    try:
        payload = _extract_payload_from_request()
        validated_data = institution_create_schema.load(payload)
    except MarshmallowValidationError as exc:
        current_app.logger.warning("Error de validación en creación de institución: %s", exc.messages)
        raise ValidationError(str(exc.messages))

    institution = Institution(
        nombre=validated_data["nombre"],
        direccion=validated_data.get("direccion"),
        fundacion=validated_data.get("fundacion"),
        paginaweb=validated_data.get("paginaweb"),
        colorinstitucional=validated_data.get("colorinstitucional"),
    )

    # Manejo del logotipo únicamente si viene en la petición multipart
    if 'logotipo' in request.files:
        file = request.files['logotipo']
        if file and file.filename:
            try:
                filepath, *_ = save_file(
                    file,
                    'institutions/logos',
                    file_type='images'
                )
                institution.logotipo = filepath
                current_app.logger.info("Logotipo guardado: %s", filepath)
            except ValueError as exc:
                raise ValidationError(str(exc))

    try:
        db.session.add(institution)
        db.session.commit()
        current_app.logger.info("Institución creada: %s", institution.nombre)
        return jsonify({
            "msg": "Institución creada exitosamente",
            "institution": institution.to_dict()
        }), 201
    except Exception as exc:  # pylint: disable=broad-except
        db.session.rollback()
        current_app.logger.error("Error al crear institución: %s", exc)
        raise DatabaseError("Error al crear la institución")


@institutions_bp.route("/<int:institution_id>", methods=["GET"])
def get_institution(institution_id):
    """Obtener una institución por ID."""
    institution = Institution.query.get(institution_id)
    if not institution:
        raise ResourceNotFoundError("Institución no encontrada")
    return jsonify(institution.to_dict()), 200


@institutions_bp.route("/<int:institution_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_institution(institution_id):
    """Actualizar una institución (solo administradores)."""
    institution = Institution.query.get(institution_id)
    if not institution:
        raise ResourceNotFoundError("Institución no encontrada")

    try:
        payload = _extract_payload_from_request()
        validated_data = institution_update_schema.load(payload)
    except MarshmallowValidationError as exc:
        current_app.logger.warning("Error de validación en actualización de institución: %s", exc.messages)
        raise ValidationError(str(exc.messages))

    for key, value in validated_data.items():
        setattr(institution, key, value)

    if 'logotipo' in request.files:
        file = request.files['logotipo']
        if file and file.filename:
            try:
                filepath, *_ = save_file(
                    file,
                    'institutions/logos',
                    file_type='images'
                )
                institution.logotipo = filepath
                current_app.logger.info("Logotipo actualizado: %s", filepath)
            except ValueError as exc:
                raise ValidationError(str(exc))

    try:
        db.session.commit()
        current_app.logger.info("Institución actualizada: %s", institution.nombre)
        return jsonify({
            "msg": "Institución actualizada exitosamente",
            "institution": institution.to_dict()
        }), 200
    except Exception as exc:  # pylint: disable=broad-except
        db.session.rollback()
        current_app.logger.error("Error al actualizar institución: %s", exc)
        raise DatabaseError("Error al actualizar la institución")


def _extract_payload_from_request():
    """Extrae y normaliza los datos del request soportando JSON o multipart."""
    if request.files:
        data = request.form.to_dict()
    else:
        data = request.get_json(silent=True) or {}

    if not isinstance(data, dict):
        raise ValidationError("El cuerpo de la petición debe ser un objeto JSON")

    fundacion_str = data.get('fundacion')
    if fundacion_str:
        normalized = _normalize_date_string(fundacion_str)
        if not normalized:
            raise ValidationError("Formato de fecha inválido (YYYY-MM-DD)")
        data['fundacion'] = normalized

    paginaweb = data.get('paginaweb')
    if paginaweb:
        data['paginaweb'] = paginaweb.strip()

    return data


def _normalize_date_string(value: str):
    """Normaliza fechas aceptando distintos formatos comunes."""
    candidates = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"]
    for fmt in candidates:
        try:
            parsed = datetime.strptime(value, fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    try:
        parsed = datetime.fromisoformat(value)
        return parsed.strftime("%Y-%m-%d")
    except ValueError:
        return None
