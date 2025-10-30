"""Decoradores para autorización basada en roles."""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from .models import User, UserCourse
from .exceptions import AuthorizationError


def role_required(*allowed_roles):
    """
    Decorador para requerir roles específicos.

    Uso:
        @role_required('admin')
        @role_required('admin', 'teacher')

    Args:
        *allowed_roles: Roles permitidos (student, teacher, admin)

    Raises:
        AuthorizationError: Si el usuario no tiene el rol requerido
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(int(current_user_id))

            if not user or not user.is_active:
                raise AuthorizationError("Usuario no encontrado o inactivo")

            if user.role not in allowed_roles:
                raise AuthorizationError(
                    f"Se requiere uno de los siguientes roles: {', '.join(allowed_roles)}"
                )

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """
    Decorador para requerir rol de administrador.

    Uso:
        @admin_required

    Raises:
        AuthorizationError: Si el usuario no es administrador
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user or not user.is_active:
            raise AuthorizationError("Usuario no encontrado o inactivo")

        if not user.is_admin():
            raise AuthorizationError("Se requiere rol de administrador")

        return f(*args, **kwargs)
    return decorated_function


def teacher_or_admin_required(f):
    """
    Decorador para requerir rol de profesor o administrador.

    Uso:
        @teacher_or_admin_required

    Raises:
        AuthorizationError: Si el usuario no es profesor ni administrador
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user or not user.is_active:
            raise AuthorizationError("Usuario no encontrado o inactivo")

        if not (user.is_teacher() or user.is_admin()):
            raise AuthorizationError("Se requiere rol de profesor o administrador")

        return f(*args, **kwargs)
    return decorated_function


def course_access_required(course_id_param='course_id'):
    """
    Decorador para verificar acceso a un curso específico.

    El usuario debe estar inscrito en el curso O ser administrador.

    Uso:
        @course_access_required()
        @course_access_required(course_id_param='id')

    Args:
        course_id_param: Nombre del parámetro que contiene el course_id

    Raises:
        AuthorizationError: Si el usuario no tiene acceso al curso
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(int(current_user_id))

            if not user or not user.is_active:
                raise AuthorizationError("Usuario no encontrado o inactivo")

            # Admins tienen acceso a todos los cursos
            if user.is_admin():
                return f(*args, **kwargs)

            # Obtener course_id de los parámetros
            course_id = kwargs.get(course_id_param)

            if not course_id:
                raise AuthorizationError("No se proporcionó ID de curso")

            # Verificar si el usuario está inscrito en el curso
            enrollment = UserCourse.query.filter_by(
                user_id=int(current_user_id),
                course_id=course_id
            ).first()

            if not enrollment:
                raise AuthorizationError("No tienes acceso a este curso")

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def course_teacher_or_admin_required(course_id_param='course_id'):
    """
    Decorador para verificar que el usuario sea profesor del curso o administrador.

    Uso:
        @course_teacher_or_admin_required()
        @course_teacher_or_admin_required(course_id_param='id')

    Args:
        course_id_param: Nombre del parámetro que contiene el course_id

    Raises:
        AuthorizationError: Si el usuario no es profesor del curso ni administrador
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(int(current_user_id))

            if not user or not user.is_active:
                raise AuthorizationError("Usuario no encontrado o inactivo")

            # Admins tienen acceso total
            if user.is_admin():
                return f(*args, **kwargs)

            # Obtener course_id de los parámetros
            course_id = kwargs.get(course_id_param)

            if not course_id:
                raise AuthorizationError("No se proporcionó ID de curso")

            # Verificar si es profesor del curso
            enrollment = UserCourse.query.filter_by(
                user_id=int(current_user_id),
                course_id=course_id,
                role_in_course='teacher'
            ).first()

            if not enrollment:
                raise AuthorizationError("No tienes permisos para modificar este curso")

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_current_user() -> User:
    """
    Obtiene el usuario actual desde el JWT token.

    Returns:
        Usuario autenticado

    Raises:
        AuthorizationError: Si no hay usuario autenticado
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))

    if not user or not user.is_active:
        raise AuthorizationError("Usuario no encontrado o inactivo")

    return user
