"""Configuración de logging para la aplicación."""
import logging
import sys
from logging.handlers import RotatingFileHandler
import os


def setup_logger(app):
    """
    Configura el sistema de logging para la aplicación.

    Args:
        app: Instancia de Flask
    """
    # Nivel de logging según el entorno
    log_level = logging.DEBUG if app.config.get("DEBUG") else logging.INFO

    # Formato del log
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Handler para archivo (si estamos en producción)
    if not app.config.get("DEBUG"):
        if not os.path.exists("logs"):
            os.mkdir("logs")

        file_handler = RotatingFileHandler(
            "logs/app.log", maxBytes=10240000, backupCount=10
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)
    app.logger.info("Logging configurado correctamente")
