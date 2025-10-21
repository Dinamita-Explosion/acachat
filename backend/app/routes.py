from flask import request, jsonify, Blueprint
from . import db
from .models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# 1. Crea un Blueprint
# El primer argumento es el nombre del blueprint.
# El segundo es el nombre del módulo o paquete, para que Flask sepa dónde encontrar plantillas y archivos estáticos.
# El tercer argumento es el prefijo de la URL para todas las rutas de este blueprint.
api = Blueprint("api", __name__, url_prefix="/api")


# 2. Usa el blueprint para definir las rutas
@api.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Validación simple (en una app real, usa Marshmallow como dicen los docs)
    required_fields = ["rut", "username", "email", "region", "comuna", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Faltan datos requeridos"}), 400

    # Verifica si el email o RUT ya existen
    if User.query.filter(
        (User.email == data["email"]) | (User.rut == data["rut"])
    ).first():
        return jsonify({"msg": "Email o RUT ya están registrados"}), 409

    # Crea un nuevo usuario
    user = User(
        rut=data["rut"],
        username=data["username"],
        email=data["email"],
        region=data["region"],
        comuna=data["comuna"],
    )
    user.set_password(data["password"])

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error al registrar: {str(e)}"}), 500

    return jsonify(
        {"msg": "Usuario registrado exitosamente"}
    ), 201  # 201 Created [cite: 431, 1392]


@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"msg": "Faltan email o contraseña"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    # Verifica el usuario y la contraseña
    if user and user.check_password(data["password"]):
        # Crea el token JWT
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)

    return jsonify(
        {"msg": "Credenciales incorrectas"}
    ), 401  # 401 Unauthorized [cite: 433, 1332]


@api.route("/profile", methods=["GET"])
@jwt_required()  # Protege esta ruta
def profile():
    # Obtiene la identidad del usuario desde el token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    return jsonify(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "rut": user.rut,
            "region": user.region,
            "comuna": user.comuna,
        }
    )
