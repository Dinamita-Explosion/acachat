"""
MÓDULO: AUTENTICACIÓN Y GESTIÓN DE USUARIOS
===========================================

Endpoints para registro, login, gestión de usuarios y roles.

Endpoints:
- POST   /auth/register          - Registrar nuevo usuario
- POST   /auth/login             - Iniciar sesión
- POST   /auth/refresh           - Refrescar token
- GET    /auth/profile           - Obtener perfil del usuario actual
- GET    /auth/users             - Listar usuarios (admin only)
- GET    /auth/users/:id         - Obtener usuario por ID (admin only)
- PUT    /auth/users/:id         - Actualizar usuario (admin only)
- DELETE /auth/users/:id         - Eliminar usuario (admin only)
- PUT    /auth/users/:id/role    - Cambiar rol de usuario (admin only)
- GET    /auth/health            - Health check
"""

from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError as MarshmallowValidationError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from sqlalchemy.exc import IntegrityError

from .. import db, limiter
from ..models import User, Institution, Grade
from ..schemas import (
    RegisterSchema,
    LoginSchema,
    UserSchema,
    UpdateRoleSchema,
    ProfileUpdateSchema,
    PasswordChangeSchema,
)
from ..exceptions import (
    ValidationError,
    AuthenticationError,
    ResourceNotFoundError,
    ConflictError,
    DatabaseError
)
from ..utils.validators import normalize_rut
from ..decorators import admin_required, get_current_user

# Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Schemas
register_schema = RegisterSchema()
login_schema = LoginSchema()
user_schema = UserSchema()
update_role_schema = UpdateRoleSchema()
profile_update_schema = ProfileUpdateSchema()
password_change_schema = PasswordChangeSchema()


@auth_bp.route("/health", methods=["GET"])
def health():
    """
    Health check del sistema.

    Returns:
        200: Sistema funcionando correctamente
    """
    try:
        db.session.execute(db.text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return jsonify({
        "status": "healthy",
        "database": db_status
    }), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registrar un nuevo usuario.

    Body (JSON):
        - rut: string (formato chileno con validación)
        - username: string (3-80 caracteres)
        - email: string (formato email válido)
        - region: string
        - comuna: string
        - password: string (min 8 chars, 1 mayúscula, 1 minúscula, 1 número)
        - role: string (opcional, default: 'student') - 'student', 'teacher', 'admin'

    Returns:
        201: Usuario creado exitosamente
        400: Datos inválidos
        409: Email o RUT ya registrado
        500: Error del servidor
    """
    try:
        # Validar datos de entrada
        data = register_schema.load(request.get_json())
    except MarshmallowValidationError as e:
        current_app.logger.warning(f"Error de validación en registro: {e.messages}")
        raise ValidationError(str(e.messages))

    # Normalizar RUT
    normalized_rut = normalize_rut(data["rut"])

    # Verificar si el email o RUT ya existen
    existing_user = User.query.filter(
        (User.email == data["email"].lower()) | (User.rut == normalized_rut)
    ).first()

    if existing_user:
        if existing_user.email == data["email"].lower():
            raise ConflictError("El email ya está registrado")
        else:
            raise ConflictError("El RUT ya está registrado")

    # Verificar que el username sea único
    existing_username = User.query.filter(
        db.func.lower(User.username) == data["username"].lower()
    ).first()
    if existing_username:
        raise ConflictError("El nombre de usuario ya está registrado")

    # Verificar que la institución existe
    institution = Institution.query.get(data["institution_id"])
    if not institution:
        raise ValidationError("La institución seleccionada no existe")

    # Determinar el grado y estado del usuario según configuración o solicitud
    grade_obj = None
    grade_id = None
    is_active = False

    requested_grade_id = data.get("grade_id")
    if requested_grade_id is not None:
        grade_obj = Grade.query.get(requested_grade_id)
        if not grade_obj:
            raise ValidationError("El grado seleccionado no existe")
        grade_id = grade_obj.id
        is_active = True  # El admin asignó grado manualmente
        current_app.logger.info(f"Grado asignado manualmente: {grade_obj.name}")
    elif current_app.config.get('AUTO_ASSIGN_GRADE', False):
        # Auto-asignar grado según configuración
        grade_name = current_app.config.get('AUTO_ASSIGN_GRADE_NAME', '4to Medio')
        grade_obj = Grade.query.filter_by(name=grade_name).first()

        if grade_obj:
            grade_id = grade_obj.id
            is_active = True
            current_app.logger.info(f"Grado auto-asignado: {grade_name}")
        else:
            current_app.logger.warning(f"Grado configurado '{grade_name}' no existe en la BD")
            # Usuario queda inactivo hasta que admin asigne grado
            is_active = False
    else:
        # Sin auto-asignación, usuario queda inactivo hasta aprobación
        current_app.logger.info("Auto-asignación deshabilitada, usuario queda inactivo")
        is_active = False

    # Crear el nuevo usuario
    try:
        user = User(
            rut=normalized_rut,
            username=data["username"],
            email=data["email"].lower(),
            region=data["region"],
            comuna=data["comuna"],
            institution_id=data["institution_id"],
            grade_id=grade_id,
            role=data.get("role", "student"),  # Por defecto 'student'
            is_active=is_active
        )
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        current_app.logger.info(
            f"Usuario registrado: {user.email} (rol: {user.role}, "
            f"institución: {institution.nombre}, grado: {grade_obj.name if grade_obj else 'No asignado'}, "
            f"activo: {is_active})"
        )

        message = "Usuario registrado exitosamente"
        if not is_active:
            message += ". Tu cuenta está pendiente de activación por un administrador."

        return jsonify({
            "msg": message,
            "user": user_schema.dump(user),
            "requires_activation": not is_active
        }), 201

    except IntegrityError as exc:
        db.session.rollback()
        error_text = str(getattr(exc, "orig", exc)).lower()
        current_app.logger.error(f"Error de integridad al registrar usuario: {exc}")
        if "username" in error_text:
            raise ConflictError("El nombre de usuario ya está registrado")
        if "email" in error_text:
            raise ConflictError("El email ya está registrado")
        if "rut" in error_text:
            raise ConflictError("El RUT ya está registrado")
        raise DatabaseError("Error al crear el usuario") from exc
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al registrar usuario: {str(e)}")
        raise DatabaseError("Error al crear el usuario")


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Iniciar sesión.

    Body (JSON):
        - email: string
        - password: string

    Returns:
        200: Login exitoso con tokens
        400: Datos inválidos
        401: Credenciales incorrectas
    """
    try:
        # Validar datos de entrada
        data = login_schema.load(request.get_json())
    except MarshmallowValidationError as e:
        current_app.logger.warning(f"Error de validación en login: {e.messages}")
        raise ValidationError(str(e.messages))

    # Buscar usuario por email (solo activos)
    user = User.query.filter_by(email=data["email"].lower(), is_active=True).first()

    # Verificar credenciales
    if not user or not user.check_password(data["password"]):
        current_app.logger.warning(f"Intento de login fallido: {data['email']}")
        raise AuthenticationError()

    # Crear tokens (identity debe ser string)
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    current_app.logger.info(f"Login exitoso: {user.email} (rol: {user.role})")

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user_schema.dump(user)
    }), 200


@auth_bp.route("/change-password", methods=["POST"])
def change_password():
    """Permite actualizar la contraseña usando email y contraseña actual."""

    try:
        data = password_change_schema.load(request.get_json())
    except MarshmallowValidationError as e:
        current_app.logger.warning(f"Error de validación en cambio de contraseña: {e.messages}")
        raise ValidationError(str(e.messages))

    email = data["email"].lower()
    user = User.query.filter_by(email=email, is_active=True).first()

    if not user or not user.check_password(data['old_password']):
        current_app.logger.warning(f"Intento de cambio de contraseña fallido para {email}")
        raise AuthenticationError("Las credenciales proporcionadas no son válidas")

    user.set_password(data['new_password'])

    try:
        db.session.commit()
        current_app.logger.info(f"Usuario {user.email} actualizó su contraseña")
        return jsonify({"msg": "Contraseña actualizada correctamente"}), 200
    except Exception as exc:
        db.session.rollback()
        current_app.logger.error(f"Error al actualizar contraseña: {exc}")
        raise DatabaseError("No se pudo actualizar la contraseña")


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    Refrescar access token usando refresh token.

    Headers:
        Authorization: Bearer <refresh_token>

    Returns:
        200: Nuevo access token
        401: Refresh token inválido o expirado
    """
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)

    return jsonify({
        "access_token": access_token
    }), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    """
    Obtener perfil del usuario actual.

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Datos del usuario
        404: Usuario no encontrado
    """
    user = get_current_user()
    return jsonify(user_schema.dump(user)), 200


@auth_bp.route("/profile", methods=["PATCH"])
@jwt_required()
def update_profile():
    """
    Actualizar el perfil del usuario autenticado.

    Actualmente solo permite modificar el nombre de usuario.
    """
    user = get_current_user()

    try:
        data = profile_update_schema.load(request.get_json() or {})
    except MarshmallowValidationError as exc:
        raise ValidationError(str(exc.messages))

    new_username = data.get("username", "").strip()
    if not new_username:
        raise ValidationError("El nombre de usuario es obligatorio")

    if new_username.lower() == user.username.lower():
        return jsonify({
            "msg": "No hay cambios para aplicar",
            "user": user_schema.dump(user)
        }), 200

    # Validar que el nombre no esté en uso
    existing_username = User.query.filter(
        db.func.lower(User.username) == new_username.lower(),
        User.id != user.id
    ).first()
    if existing_username:
        raise ConflictError("El nombre de usuario ya está ocupado")

    user.username = new_username

    try:
        db.session.commit()
        current_app.logger.info(f"Usuario {user.id} actualizó su nombre a {user.username}")
        return jsonify({
            "msg": "Perfil actualizado correctamente",
            "user": user_schema.dump(user)
        }), 200
    except IntegrityError as exc:
        db.session.rollback()
        current_app.logger.error(f"Error de integridad al actualizar perfil: {exc}")
        raise ConflictError("El nombre de usuario ya está ocupado")
    except Exception as exc:
        db.session.rollback()
        current_app.logger.error(f"Error al actualizar perfil: {exc}")
        raise DatabaseError("No se pudo actualizar el perfil")


@auth_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_required
def list_users():
    """
    Listar todos los usuarios (solo administradores).

    Query params:
        - role: filtrar por rol (student, teacher, admin)
        - is_active: filtrar por estado (true, false)
        - page: número de página (default: 1)
        - per_page: resultados por página (default: 20, max: 100)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Lista de usuarios
        401: No autenticado
        403: No autorizado (no es admin)
    """
    # Parámetros de consulta
    role_filter = request.args.get('role')
    is_active_filter = request.args.get('is_active')
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)

    # Query base
    query = User.query

    # Aplicar filtros
    if role_filter and role_filter in ['student', 'teacher', 'admin']:
        query = query.filter_by(role=role_filter)

    if is_active_filter is not None:
        is_active = is_active_filter.lower() == 'true'
        query = query.filter_by(is_active=is_active)

    # Paginación
    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "users": [user.to_dict() for user in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "per_page": pagination.per_page
    }), 200


@auth_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
@admin_required
def get_user(user_id):
    """
    Obtener un usuario por ID (solo administradores).

    Path params:
        - user_id: ID del usuario

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Datos del usuario
        404: Usuario no encontrado
        403: No autorizado
    """
    user = User.query.get(user_id)
    if not user:
        raise ResourceNotFoundError("Usuario no encontrado")

    return jsonify(user_schema.dump(user)), 200


@auth_bp.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_user(user_id):
    """
    Actualizar un usuario (solo administradores).

    Path params:
        - user_id: ID del usuario

    Body (JSON):
        - rut: string (opcional)
        - username: string (opcional)
        - email: string (opcional)
        - region: string (opcional)
        - comuna: string (opcional)
        - role: string (opcional)
        - is_active: boolean (opcional)
        - password: string (opcional)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Usuario actualizado
        400: Datos inválidos
        404: Usuario no encontrado
        403: No autorizado
    """
    user = User.query.get(user_id)
    if not user:
        raise ResourceNotFoundError("Usuario no encontrado")

    data = request.get_json()

    try:
        # Actualizar campos si están presentes
        if 'rut' in data:
            user.rut = normalize_rut(data['rut'])
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email'].lower()
        if 'region' in data:
            user.region = data['region']
        if 'comuna' in data:
            user.comuna = data['comuna']
        if 'role' in data:
            user.role = data['role']
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'institution_id' in data:
            user.institution_id = data['institution_id']
        if 'grade_id' in data:
            user.grade_id = data['grade_id']
        if 'password' in data and data['password']:
            user.set_password(data['password'])

        db.session.commit()
        current_app.logger.info(f"Usuario {user.email} actualizado")

        return jsonify({
            "msg": "Usuario actualizado exitosamente",
            "user": user_schema.dump(user)
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al actualizar usuario: {str(e)}")
        raise DatabaseError("Error al actualizar el usuario")


@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_user(user_id):
    """
    Eliminar un usuario (solo administradores).

    Path params:
        - user_id: ID del usuario

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Usuario eliminado
        404: Usuario no encontrado
        403: No autorizado
    """
    user = User.query.get(user_id)
    if not user:
        raise ResourceNotFoundError("Usuario no encontrado")

    try:
        db.session.delete(user)
        db.session.commit()
        current_app.logger.info(f"Usuario {user.email} eliminado")

        return jsonify({"msg": "Usuario eliminado exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al eliminar usuario: {str(e)}")
        raise DatabaseError("Error al eliminar el usuario")


@auth_bp.route("/users/<int:user_id>/role", methods=["PUT"])
@jwt_required()
@admin_required
def update_user_role(user_id):
    """
    Cambiar el rol de un usuario (solo administradores).

    Path params:
        - user_id: ID del usuario

    Body (JSON):
        - role: string ('student', 'teacher', 'admin')

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Rol actualizado
        400: Datos inválidos
        404: Usuario no encontrado
        403: No autorizado
    """
    try:
        # Validar datos de entrada
        data = update_role_schema.load(request.get_json())
    except MarshmallowValidationError as e:
        raise ValidationError(str(e.messages))

    # Buscar usuario
    user = User.query.get(user_id)
    if not user:
        raise ResourceNotFoundError("Usuario no encontrado")

    # Actualizar rol
    old_role = user.role
    user.role = data["role"]

    try:
        db.session.commit()
        current_app.logger.info(
            f"Rol de usuario {user.email} cambiado de {old_role} a {user.role}"
        )

        return jsonify({
            "msg": "Rol actualizado exitosamente",
            "user": user_schema.dump(user)
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al actualizar rol: {str(e)}")
        raise DatabaseError("Error al actualizar el rol del usuario")


# ==========================================
# ERROR HANDLERS
# ==========================================

@auth_bp.errorhandler(ValidationError)
@auth_bp.errorhandler(AuthenticationError)
@auth_bp.errorhandler(ResourceNotFoundError)
@auth_bp.errorhandler(ConflictError)
@auth_bp.errorhandler(DatabaseError)
def handle_app_error(error):
    """Maneja las excepciones personalizadas de la aplicación."""
    return jsonify({"msg": error.message}), error.status_code


@auth_bp.errorhandler(Exception)
def handle_unexpected_error(error):
    """Maneja errores inesperados."""
    current_app.logger.error(f"Error inesperado: {str(error)}", exc_info=True)
    return jsonify({"msg": "Error interno del servidor"}), 500
