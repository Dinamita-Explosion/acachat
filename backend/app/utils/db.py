"""Utilidades relacionadas con la base de datos."""
from __future__ import annotations

import os
from contextlib import suppress

from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import OperationalError, ProgrammingError


def ensure_database_exists(database_uri: str) -> None:
    """
    Garantiza que la base de datos definida en la URI exista.

    Soporta motores comunes (MySQL, PostgreSQL, SQLite). Para SQLite simplemente
    se crea el directorio que contenga el fichero si fuese necesario.

    Args:
        database_uri: Cadena de conexión SQLAlchemy.
    """
    url = make_url(database_uri)

    if url.drivername.startswith("sqlite"):
        database = url.database
        if database and database != ":memory:":
            directory = os.path.dirname(os.path.abspath(database))
            if directory:
                os.makedirs(directory, exist_ok=True)
        return

    database = url.database
    if not database:
        return

    server_url = url.set(database=None)
    engine = create_engine(server_url, isolation_level="AUTOCOMMIT")
    try:
        with engine.connect() as connection:
            driver = url.drivername.split("+")[0]
            if driver in {"mysql", "mariadb"}:
                connection.execute(
                    text(f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                )
            elif driver in {"postgresql", "postgres"}:
                result = connection.execute(
                    text("SELECT 1 FROM pg_database WHERE datname = :name"),
                    {"name": database},
                )
                exists = result.scalar() is not None
                if not exists:
                    connection.execute(text(f'CREATE DATABASE "{database}"'))
            else:
                with suppress(ProgrammingError, OperationalError):
                    connection.execute(text(f"CREATE DATABASE {database}"))
    finally:
        engine.dispose()
