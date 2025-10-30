"""
MÓDULO: GESTIÓN DE ARCHIVOS DE CURSOS
======================================

Endpoints para subir, descargar y eliminar archivos de cursos.

Endpoints:
- GET    /courses/:id/files          - Listar archivos de un curso
- POST   /courses/:id/files          - Subir archivo a un curso (profesor/admin)
- GET    /files/:id/download         - Descargar un archivo
- DELETE /files/:id                  - Eliminar un archivo (profesor/admin)
"""

from flask import Blueprint, request, jsonify, current_app, send_file
from flask_jwt_extended import jwt_required
from datetime import datetime
import os

from .. import db
from ..models import CourseFile, Course, UserCourse
from ..schemas import CourseFileSchema
from ..exceptions import (
    ValidationError,
    ResourceNotFoundError,
    DatabaseError,
    AuthorizationError
)
from ..decorators import (
    get_current_user,
    course_access_required,
    course_teacher_or_admin_required
)
from ..utils.file_handler import save_file, delete_file, get_file_path, file_exists
from ..utils.file_parser import parse_file_to_text, can_parse_file

# Blueprint
files_bp = Blueprint('files', __name__, url_prefix='/api')

# Schema
course_file_schema = CourseFileSchema()


@files_bp.route("/courses/<int:course_id>/files", methods=["GET"])
@jwt_required()
@course_access_required(course_id_param='course_id')
def list_course_files(course_id):
    """
    Listar todos los archivos de un curso.

    El usuario debe estar inscrito en el curso O ser admin.

    Path params:
        - course_id: ID del curso

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Lista de archivos
        403: No tiene acceso al curso
        404: Curso no encontrado
    """
    course = Course.query.get(course_id)
    if not course:
        raise ResourceNotFoundError("Curso no encontrado")

    files = CourseFile.query.filter_by(course_id=course_id).order_by(
        CourseFile.uploaded_at.desc()
    ).all()

    return jsonify({
        "course": {
            "id": course.id,
            "nombre": course.nombre
        },
        "files": [file.to_dict() for file in files],
        "total": len(files)
    }), 200


@files_bp.route("/courses/<int:course_id>/files", methods=["POST"])
@jwt_required()
@course_teacher_or_admin_required(course_id_param='course_id')
def upload_course_file(course_id):
    """
    Subir un archivo a un curso.

    Solo profesores del curso o administradores pueden subir archivos.

    Path params:
        - course_id: ID del curso

    Form data (multipart/form-data):
        - file: archivo (requerido)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        201: Archivo subido exitosamente
        400: No se proporcionó archivo o tipo no permitido
        403: No autorizado
        404: Curso no encontrado
    """
    user = get_current_user()
    course = Course.query.get(course_id)

    if not course:
        raise ResourceNotFoundError("Curso no encontrado")

    # Verificar que se proporcionó un archivo
    if 'file' not in request.files:
        raise ValidationError("No se proporcionó ningún archivo")

    file = request.files['file']

    if not file or not file.filename:
        raise ValidationError("Archivo inválido")

    try:
        # Guardar archivo
        filepath, original_filename, filesize, mimetype = save_file(
            file,
            f'courses/{course_id}'  # Carpeta específica del curso
        )

        # Crear registro en BD
        course_file = CourseFile(
            course_id=course_id,
            filename=original_filename,
            filepath=filepath,
            filesize=filesize,
            mimetype=mimetype,
            uploaded_by=user.id
        )

        db.session.add(course_file)
        db.session.commit()

        # NUEVO: Parsear archivo automáticamente para chatbot
        if can_parse_file(original_filename):
            try:
                full_path = get_file_path(filepath)
                parsed_content = parse_file_to_text(full_path)

                if parsed_content:
                    course_file.parsed_content = parsed_content
                    course_file.parsed_at = datetime.utcnow()
                    db.session.commit()

                    current_app.logger.info(
                        f"Archivo parseado: {original_filename} ({len(parsed_content)} caracteres)"
                    )
                else:
                    current_app.logger.warning(
                        f"Archivo parseado pero contenido vacío: {original_filename}"
                    )

            except Exception as e:
                # Si falla el parseo, solo registrar warning pero no fallar el upload
                current_app.logger.warning(
                    f"No se pudo parsear archivo {original_filename}: {str(e)}"
                )
        else:
            current_app.logger.info(
                f"Archivo {original_filename} no es parseable (tipo no soportado)"
            )

        current_app.logger.info(
            f"Archivo subido: {original_filename} al curso {course.nombre} por {user.email}"
        )

        return jsonify({
            "msg": "Archivo subido exitosamente",
            "file": course_file.to_dict()
        }), 201

    except ValueError as e:
        # Error de validación de tipo de archivo
        raise ValidationError(str(e))
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al subir archivo: {str(e)}")
        raise DatabaseError("Error al subir el archivo")


@files_bp.route("/files/<int:file_id>/download", methods=["GET"])
@jwt_required()
def download_file(file_id):
    """
    Descargar un archivo.

    El usuario debe tener acceso al curso del archivo.

    Path params:
        - file_id: ID del archivo

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Archivo descargado
        403: No tiene acceso al curso
        404: Archivo no encontrado
    """
    user = get_current_user()
    course_file = CourseFile.query.get(file_id)

    if not course_file:
        raise ResourceNotFoundError("Archivo no encontrado")

    # Verificar acceso al curso
    if not user.is_admin():
        enrollment = UserCourse.query.filter_by(
            user_id=user.id,
            course_id=course_file.course_id
        ).first()

        if not enrollment:
            raise AuthorizationError("No tienes acceso a este archivo")

    # Verificar que el archivo físico existe
    file_path = get_file_path(course_file.filepath)

    if not file_exists(course_file.filepath):
        current_app.logger.error(f"Archivo físico no encontrado: {file_path}")
        raise ResourceNotFoundError("Archivo físico no encontrado")

    try:
        # Enviar archivo
        return send_file(
            file_path,
            as_attachment=True,
            download_name=course_file.filename,
            mimetype=course_file.mimetype
        )

    except Exception as e:
        current_app.logger.error(f"Error al descargar archivo: {str(e)}")
        raise DatabaseError("Error al descargar el archivo")


@files_bp.route("/files/<int:file_id>", methods=["DELETE"])
@jwt_required()
def delete_course_file(file_id):
    """
    Eliminar un archivo de un curso.

    Solo el profesor del curso o un administrador pueden eliminar archivos.

    Path params:
        - file_id: ID del archivo

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Archivo eliminado
        403: No autorizado
        404: Archivo no encontrado
    """
    user = get_current_user()
    course_file = CourseFile.query.get(file_id)

    if not course_file:
        raise ResourceNotFoundError("Archivo no encontrado")

    # Verificar permisos
    if not user.is_admin():
        # Verificar si es profesor del curso
        enrollment = UserCourse.query.filter_by(
            user_id=user.id,
            course_id=course_file.course_id,
            role_in_course='teacher'
        ).first()

        if not enrollment:
            raise AuthorizationError("No tienes permisos para eliminar este archivo")

    # Eliminar archivo físico
    if course_file.filepath:
        delete_file(course_file.filepath)

    try:
        # Eliminar registro de BD
        filename = course_file.filename
        course_name = course_file.course.nombre if course_file.course else "Unknown"

        db.session.delete(course_file)
        db.session.commit()

        current_app.logger.info(
            f"Archivo eliminado: {filename} del curso {course_name} por {user.email}"
        )

        return jsonify({
            "msg": "Archivo eliminado exitosamente"
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al eliminar archivo: {str(e)}")
        raise DatabaseError("Error al eliminar el archivo")


# ==========================================
# ERROR HANDLERS
# ==========================================

@files_bp.errorhandler(ValidationError)
@files_bp.errorhandler(ResourceNotFoundError)
@files_bp.errorhandler(DatabaseError)
@files_bp.errorhandler(AuthorizationError)
def handle_app_error(error):
    """Maneja las excepciones personalizadas."""
    return jsonify({"msg": error.message}), error.status_code


@files_bp.errorhandler(Exception)
def handle_unexpected_error(error):
    """Maneja errores inesperados."""
    current_app.logger.error(f"Error inesperado: {str(error)}", exc_info=True)
    return jsonify({"msg": "Error interno del servidor"}), 500
