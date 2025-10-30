"""
Módulo de rutas modular.

Este paquete contiene todos los endpoints de la API organizados por funcionalidad:
- auth.py: Autenticación y gestión de usuarios
- institutions.py: CRUD de instituciones
- grades.py: Listado de grados educativos
- courses.py: CRUD de cursos
- enrollments.py: Matrícula y asignaciones
- files.py: Gestión de archivos de cursos
- chat.py: Chatbot con Gemini AI por curso
- admin.py: Panel de administración HTML
"""

from .auth import auth_bp
from .institutions import institutions_bp
from .grades import grades_bp
from .courses import courses_bp
from .enrollments import enrollments_bp
from .files import files_bp
from .chat import chat_bp
from .admin import admin_bp

__all__ = [
    "auth_bp",
    "institutions_bp",
    "grades_bp",
    "courses_bp",
    "enrollments_bp",
    "files_bp",
    "chat_bp",
    "admin_bp",
]
