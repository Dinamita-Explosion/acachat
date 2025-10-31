import os
from dotenv import load_dotenv
from datetime import timedelta

# Carga las variables del archivo .env en el entorno
load_dotenv()


class Config:
    """Configuración base de la aplicación."""

    # Claves secretas
    SECRET_KEY = os.environ.get("SECRET_KEY") or "una-clave-secreta-por-defecto"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-secret-key-change-in-production"

    # Base de datos
    @staticmethod
    def _build_database_uri():
        """Construye la URI de la base de datos a partir de variables separadas o DATABASE_URL."""
        # Si existe DATABASE_URL, usarla directamente (compatibilidad hacia atrás)
        database_url = os.environ.get("DATABASE_URL")
        if database_url:
            return database_url

        # Si no, construir desde variables separadas
        db_connection = os.environ.get("DB_CONNECTION", "mysql")
        db_host = os.environ.get("DB_HOST", "localhost")
        db_port = os.environ.get("DB_PORT", "3306")
        db_database = os.environ.get("DB_DATABASE", "")
        db_username = os.environ.get("DB_USERNAME", "")
        db_password = os.environ.get("DB_PASSWORD", "")

        # Mapeo de drivers según el tipo de conexión
        driver_map = {
            "mysql": "mysql+pymysql",
            "postgresql": "postgresql",
            "sqlite": "sqlite"
        }

        driver = driver_map.get(db_connection, "mysql+pymysql")

        # Construcción de la URL según el tipo de BD
        if db_connection == "sqlite":
            # SQLite no necesita host, port, user, password
            return f"{driver}:///{db_database}"
        else:
            # MySQL, PostgreSQL, etc.
            auth = f"{db_username}:{db_password}@" if db_username else ""
            port = f":{db_port}" if db_port else ""
            return f"{driver}://{auth}{db_host}{port}/{db_database}"

    SQLALCHEMY_DATABASE_URI = _build_database_uri.__func__()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,  # Verifica conexiones antes de usarlas
        "pool_recycle": 300,    # Recicla conexiones cada 5 minutos
    }

    # JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    # CORS
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:8100").split(",")

    # Rate Limiting
    RATELIMIT_STORAGE_URI = "memory://"
    RATELIMIT_DEFAULT = "100 per hour"

    # Archivos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max por archivo
    ALLOWED_EXTENSIONS = {
        'images': {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'},
        'documents': {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'md'},
        'archives': {'zip', 'rar', '7z'}
    }

    # Gemini AI (Chatbot)
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
    GEMINI_TEMPERATURE = float(os.environ.get("GEMINI_TEMPERATURE", "0.7"))
    GEMINI_MAX_OUTPUT_TOKENS = int(os.environ.get("GEMINI_MAX_OUTPUT_TOKENS", "2048"))
    GEMINI_MAX_CONTEXT_TOKENS = int(os.environ.get("GEMINI_MAX_CONTEXT_TOKENS", "30000"))  # Tokens máx de contexto de archivos

    # Auto-asignación de grado
    AUTO_ASSIGN_GRADE = os.environ.get("AUTO_ASSIGN_GRADE", "true").lower() == "true"
    AUTO_ASSIGN_GRADE_NAME = os.environ.get("AUTO_ASSIGN_GRADE_NAME", "4to Medio")


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""

    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuración para producción."""

    DEBUG = False
    TESTING = False
    # En producción, estas claves DEBEN venir del entorno
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)


class TestingConfig(Config):
    """Configuración para testing."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Base de datos en memoria para tests


# Mapa de configuraciones
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
