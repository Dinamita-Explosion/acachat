"""
MÓDULO: CHATBOT POR CURSO CON GEMINI
=====================================

Endpoints para interactuar con el chatbot de cada curso usando Gemini AI.
El chatbot tiene acceso al prompt del curso y al contenido de todos los archivos
parseados asociados al curso.

Endpoints:
- POST   /courses/:id/chat           - Enviar mensaje al chatbot del curso
- GET    /courses/:id/chat/context   - Obtener información del contexto disponible
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
import google.generativeai as genai

from .. import db
from ..models import Course, CourseFile, UserCourse
from ..decorators import get_current_user, course_access_required
from ..exceptions import (
    ValidationError,
    ResourceNotFoundError,
    DatabaseError,
    AuthorizationError
)
from ..utils.file_parser import estimate_token_count, truncate_text

# Blueprint
chat_bp = Blueprint('chat', __name__, url_prefix='/api')


def initialize_gemini():
    """Inicializa el cliente de Gemini con la API key."""
    api_key = current_app.config.get('GEMINI_API_KEY')
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        raise ValueError("GEMINI_API_KEY no está configurada correctamente en .env")
    genai.configure(api_key=api_key)


def build_course_context(course_id: int, max_tokens: int = None) -> str:
    """
    Construye el contexto del curso a partir de archivos parseados.

    Args:
        course_id: ID del curso
        max_tokens: Límite máximo de tokens para el contexto

    Returns:
        str: Contexto formateado con todos los archivos del curso
    """
    if max_tokens is None:
        max_tokens = current_app.config.get('GEMINI_MAX_CONTEXT_TOKENS', 30000)

    files = CourseFile.query.filter_by(course_id=course_id).order_by(
        CourseFile.uploaded_at.desc()
    ).all()

    context_parts = []
    total_tokens = 0

    for file in files:
        if not file.parsed_content:
            continue

        # Estimar tokens del contenido del archivo
        file_tokens = estimate_token_count(file.parsed_content)

        # Si agregar este archivo excede el límite, truncarlo o saltar
        if total_tokens + file_tokens > max_tokens:
            remaining_tokens = max_tokens - total_tokens
            if remaining_tokens > 500:  # Solo incluir si quedan al menos 500 tokens
                truncated = truncate_text(file.parsed_content, remaining_tokens)
                context_parts.append(
                    f"## Archivo: {file.filename}\n\n{truncated}"
                )
                total_tokens += remaining_tokens
            break
        else:
            context_parts.append(
                f"## Archivo: {file.filename}\n\n{file.parsed_content}"
            )
            total_tokens += file_tokens

    if not context_parts:
        return "[No hay archivos parseados disponibles para este curso]"

    return "\n\n---\n\n".join(context_parts)


def build_system_prompt(course: Course) -> str:
    """
    Construye el prompt del sistema para el chatbot del curso.

    Args:
        course: Objeto Course con el prompt configurado

    Returns:
        str: Prompt del sistema completo
    """
    base_prompt = course.prompt or "Eres un asistente educativo útil que responde preguntas sobre el curso."

    context = build_course_context(course.id)

    full_prompt = f"""{base_prompt}

# CONTEXTO DEL CURSO
Tienes acceso a los siguientes materiales del curso para responder preguntas:

{context}

# INSTRUCCIONES
- Usa el contexto proporcionado para responder preguntas de manera precisa
- Si la respuesta está en los archivos, cita el nombre del archivo
- Si no tienes la información, sé honesto y dilo
- Responde en español de manera clara y educativa
- Si te preguntan sobre algo que no está en el contexto, usa tu conocimiento general pero aclara que no está en los materiales del curso
"""

    return full_prompt


@chat_bp.route("/courses/<int:course_id>/chat", methods=["POST"])
@jwt_required()
@course_access_required(course_id_param='course_id')
def chat_with_course(course_id):
    """
    Enviar un mensaje al chatbot del curso y recibir respuesta.

    El usuario debe estar inscrito en el curso o ser administrador.

    Path params:
        - course_id: ID del curso

    Body (JSON):
        - messages: array de mensajes [{role: 'user'/'model', content: '...'}]
        - temperature: float (opcional, default del config)
        - max_tokens: int (opcional, default del config)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Respuesta del chatbot
        400: Datos inválidos
        403: No tiene acceso al curso
        404: Curso no encontrado
        500: Error al procesar con Gemini
    """
    user = get_current_user()
    course = Course.query.get(course_id)

    if not course:
        raise ResourceNotFoundError("Curso no encontrado")

    # Validar body
    data = request.get_json()
    if not data or 'messages' not in data:
        raise ValidationError("Se requiere el campo 'messages'")

    messages = data.get('messages', [])
    if not isinstance(messages, list) or len(messages) == 0:
        raise ValidationError("El campo 'messages' debe ser un array no vacío")

    # Parámetros opcionales
    temperature = data.get('temperature', current_app.config.get('GEMINI_TEMPERATURE', 0.7))
    max_tokens = data.get('max_tokens', current_app.config.get('GEMINI_MAX_OUTPUT_TOKENS', 2048))

    try:
        # Inicializar Gemini
        initialize_gemini()

        # Construir el prompt del sistema
        system_prompt = build_system_prompt(course)

        # Configurar el modelo
        model_name = current_app.config.get('GEMINI_MODEL', 'gemini-1.5-flash')
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt
        )

        # Convertir mensajes al formato de Gemini
        gemini_messages = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')

            if not content:
                continue

            # Gemini usa 'user' y 'model' como roles
            if role in ['user', 'model']:
                gemini_messages.append({
                    'role': role,
                    'parts': [content]
                })

        if not gemini_messages:
            raise ValidationError("No hay mensajes válidos para procesar")

        # Configuración de generación
        generation_config = genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )

        # Generar respuesta
        chat = model.start_chat(history=gemini_messages[:-1])  # Historial sin el último mensaje
        response = chat.send_message(
            gemini_messages[-1]['parts'][0],
            generation_config=generation_config
        )

        # Extraer texto de la respuesta
        response_text = response.text

        current_app.logger.info(
            f"Chat con curso {course.nombre} por {user.email} - {len(messages)} mensajes"
        )

        return jsonify({
            "response": response_text,
            "model": model_name,
            "course": {
                "id": course.id,
                "nombre": course.nombre
            }
        }), 200

    except ValueError as e:
        # Error de configuración (API key, etc)
        current_app.logger.error(f"Error de configuración Gemini: {str(e)}")
        raise DatabaseError(f"Error de configuración del chatbot: {str(e)}")

    except Exception as e:
        # Error al llamar a la API de Gemini
        current_app.logger.error(f"Error al generar respuesta con Gemini: {str(e)}")
        raise DatabaseError(f"Error al procesar el mensaje: {str(e)}")


@chat_bp.route("/courses/<int:course_id>/chat/context", methods=["GET"])
@jwt_required()
@course_access_required(course_id_param='course_id')
def get_course_context(course_id):
    """
    Obtener información sobre el contexto disponible para el chatbot.

    Útil para que el frontend sepa qué archivos están disponibles.

    Path params:
        - course_id: ID del curso

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Información del contexto
        403: No tiene acceso al curso
        404: Curso no encontrado
    """
    course = Course.query.get(course_id)

    if not course:
        raise ResourceNotFoundError("Curso no encontrado")

    # Obtener archivos parseados
    files = CourseFile.query.filter_by(course_id=course_id).all()

    parsed_files = []
    total_characters = 0
    total_tokens = 0

    for file in files:
        file_info = {
            "id": file.id,
            "filename": file.filename,
            "has_parsed_content": file.parsed_content is not None,
            "parsed_at": file.parsed_at.isoformat() if file.parsed_at else None
        }

        if file.parsed_content:
            chars = len(file.parsed_content)
            tokens = estimate_token_count(file.parsed_content)
            file_info["characters"] = chars
            file_info["estimated_tokens"] = tokens
            total_characters += chars
            total_tokens += tokens

        parsed_files.append(file_info)

    return jsonify({
        "course": {
            "id": course.id,
            "nombre": course.nombre,
            "prompt": course.prompt
        },
        "files": parsed_files,
        "total_files": len(files),
        "parsed_files_count": sum(1 for f in files if f.parsed_content),
        "total_characters": total_characters,
        "estimated_total_tokens": total_tokens,
        "model": current_app.config.get('GEMINI_MODEL', 'gemini-1.5-flash'),
        "max_context_tokens": current_app.config.get('GEMINI_MAX_CONTEXT_TOKENS', 30000)
    }), 200


# ==========================================
# ERROR HANDLERS
# ==========================================

@chat_bp.errorhandler(ValidationError)
@chat_bp.errorhandler(ResourceNotFoundError)
@chat_bp.errorhandler(DatabaseError)
@chat_bp.errorhandler(AuthorizationError)
def handle_app_error(error):
    """Maneja las excepciones personalizadas."""
    return jsonify({"msg": error.message}), error.status_code


@chat_bp.errorhandler(Exception)
def handle_unexpected_error(error):
    """Maneja errores inesperados."""
    current_app.logger.error(f"Error inesperado en chat: {str(error)}", exc_info=True)
    return jsonify({"msg": "Error interno del servidor"}), 500
