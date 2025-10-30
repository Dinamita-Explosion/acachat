"""Excepciones personalizadas para la aplicación."""


class AppException(Exception):
    """Excepción base para la aplicación."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ValidationError(AppException):
    """Error de validación de datos."""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class AuthenticationError(AppException):
    """Error de autenticación."""

    def __init__(self, message: str = "Credenciales incorrectas"):
        super().__init__(message, status_code=401)


class AuthorizationError(AppException):
    """Error de autorización (permisos insuficientes)."""

    def __init__(self, message: str = "No tienes permisos para realizar esta acción"):
        super().__init__(message, status_code=403)


class ResourceNotFoundError(AppException):
    """Recurso no encontrado."""

    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(message, status_code=404)


class ConflictError(AppException):
    """Conflicto de recursos (ej: duplicados)."""

    def __init__(self, message: str):
        super().__init__(message, status_code=409)


class DatabaseError(AppException):
    """Error de base de datos."""

    def __init__(self, message: str = "Error en la base de datos"):
        super().__init__(message, status_code=500)
