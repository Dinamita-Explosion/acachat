from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .config import config_by_name
from .utils.db import ensure_database_exists
import os

# Inicializa las extensiones
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)


def create_app(config_name=None):
    """
    Factory para crear la aplicación Flask.

    Args:
        config_name: Nombre de la configuración ('development', 'production', 'testing')
                     Si no se especifica, se usa la variable de entorno FLASK_ENV

    Returns:
        Instancia configurada de Flask
    """
    # Determina el entorno
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    # Crea la aplicación
    app = Flask(__name__)

    # Carga la configuración según el entorno
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    # Garantiza que la base de datos exista antes de inicializar SQLAlchemy
    ensure_database_exists(app.config["SQLALCHEMY_DATABASE_URI"])

    # Inicializa las extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Configura CORS con orígenes desde la configuración
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": app.config["CORS_ORIGINS"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
    )

    # Configura el logging
    from .logger import setup_logger

    setup_logger(app)

    # Inicializa el rate limiter
    limiter.init_app(app)

    # Registra los blueprints modulares
    from .routes import (
        auth_bp,
        institutions_bp,
        grades_bp,
        courses_bp,
        enrollments_bp,
        files_bp,
        chat_bp,
        admin_bp,
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(institutions_bp)
    app.register_blueprint(grades_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(enrollments_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(admin_bp)

    @app.route('/uploads/<path:filename>')
    def serve_uploads(filename: str):
        """Sirve los archivos subidos (logos, materiales, etc.)."""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Importa los modelos para que SQLAlchemy los reconozca
    with app.app_context():
        from . import models

    app.logger.info(f"Aplicación iniciada en modo: {config_name}")

    @app.cli.command("seed-db")
    def seed_db_command():
        """Poblar la base de datos con datos de ejemplo."""
        from .seed_data import seed_database

        seed_database(app)

    return app
