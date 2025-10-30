"""Utilidades para manejo de archivos."""
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename: str, file_type: str = 'documents') -> bool:
    """
    Verifica si la extensión del archivo es permitida.

    Args:
        filename: Nombre del archivo
        file_type: Tipo de archivo ('images', 'documents', 'archives')

    Returns:
        True si el archivo es permitido, False en caso contrario
    """
    if not filename or '.' not in filename:
        return False

    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS'].get(file_type, set())
    ext = filename.rsplit('.', 1)[1].lower()

    return ext in allowed_extensions


def is_allowed_extension(filename: str) -> bool:
    """
    Verifica si la extensión está permitida en cualquier categoría.

    Args:
        filename: Nombre del archivo

    Returns:
        True si el archivo es permitido en alguna categoría
    """
    if not filename or '.' not in filename:
        return False

    ext = filename.rsplit('.', 1)[1].lower()
    all_extensions = set()

    for extensions in current_app.config['ALLOWED_EXTENSIONS'].values():
        all_extensions.update(extensions)

    return ext in all_extensions


def save_file(file, folder: str, file_type: str = 'documents') -> tuple:
    """
    Guarda un archivo y retorna información del mismo.

    Args:
        file: FileStorage object de Flask
        folder: Subcarpeta donde guardar (ej: 'institutions/logos' o 'courses/1')
        file_type: Tipo de archivo para validación

    Returns:
        tuple: (filepath, original_filename, filesize, mimetype)

    Raises:
        ValueError: Si el tipo de archivo no está permitido
    """
    if not file or not file.filename:
        raise ValueError("No se proporcionó un archivo válido")

    if not is_allowed_extension(file.filename):
        raise ValueError(f"Tipo de archivo no permitido: {file.filename}")

    # Obtener extensión
    ext = file.filename.rsplit('.', 1)[1].lower()

    # Generar nombre único
    unique_filename = f"{uuid.uuid4().hex}.{ext}"

    # Crear directorio si no existe
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
    os.makedirs(upload_path, exist_ok=True)

    # Path relativo y path completo
    relative_path = os.path.join(folder, unique_filename)
    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], relative_path)

    # Guardar archivo
    file.save(full_path)

    # Obtener tamaño
    filesize = os.path.getsize(full_path)

    return (relative_path, file.filename, filesize, file.content_type or 'application/octet-stream')


def delete_file(filepath: str) -> bool:
    """
    Elimina un archivo del storage.

    Args:
        filepath: Path relativo del archivo (ej: 'institutions/logos/abc123.png')

    Returns:
        True si se eliminó correctamente, False si no existía
    """
    if not filepath:
        return False

    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filepath)

    if os.path.exists(full_path):
        try:
            os.remove(full_path)
            return True
        except Exception:
            return False

    return False


def get_file_path(filepath: str) -> str:
    """
    Obtiene el path completo de un archivo.

    Args:
        filepath: Path relativo del archivo

    Returns:
        Path absoluto del archivo
    """
    return os.path.join(current_app.config['UPLOAD_FOLDER'], filepath)


def file_exists(filepath: str) -> bool:
    """
    Verifica si un archivo existe.

    Args:
        filepath: Path relativo del archivo

    Returns:
        True si el archivo existe, False en caso contrario
    """
    full_path = get_file_path(filepath)
    return os.path.exists(full_path)


def format_file_size(size_bytes: int) -> str:
    """
    Formatea el tamaño de un archivo a formato legible.

    Args:
        size_bytes: Tamaño en bytes

    Returns:
        String formateado (ej: '1.5 MB')
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
