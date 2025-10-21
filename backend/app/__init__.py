from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import Config

# 1. Inicializa las extensiones (sin una app todavía)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_class=Config):
    # 2. Crea la instancia de la aplicación Flask
    app = Flask(__name__)

    # 3. Carga la configuración desde el objeto Config
    app.config.from_object(config_class)

    # 4. Vincula las extensiones con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # 5. Configura CORS para permitir peticiones desde tu app Ionic [cite: 2611]
    # Esto es crucial para que Ionic (localhost:8100) pueda hablar con Flask (localhost:5000)
    CORS(app, resources={r"/*": {"origins": "http://localhost:8100"}})

    # 6. Registra el blueprint
    from .routes import api as api_blueprint

    app.register_blueprint(api_blueprint)

    # 7. Importa los modelos para que SQLAlchemy los reconozca
    with app.app_context():
        from . import models

    return app
