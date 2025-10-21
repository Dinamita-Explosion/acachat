import os
from dotenv import load_dotenv

# Carga las variables del archivo .env en el entorno
load_dotenv()


class Config:
    # Clave secreta para la aplicación Flask (usada para sesiones, etc.)
    SECRET_KEY = os.environ.get("SECRET_KEY") or "una-clave-secreta-por-defecto"

    # Configuración de la base de datos desde el .env
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    # Desactiva una advertencia de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clave secreta para los tokens JWT desde el .env
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
