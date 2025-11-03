"""Utilidades de validación para el backend."""
import re


def validate_rut(rut: str) -> bool:
    """
    Valida un RUT chileno con su dígito verificador.

    Acepta formatos:
    - 12345678-9
    - 12.345.678-9

    Args:
        rut: String con el RUT a validar

    Returns:
        True si el RUT es válido, False en caso contrario
    """
    if not rut:
        return False

    # Elimina puntos y guiones, convierte a mayúsculas
    rut = rut.replace(".", "").replace("-", "").upper()

    # Verifica formato básico (7-8 dígitos + verificador)
    if not re.match(r'^\d{7,8}[0-9K]$', rut):
        return False

    # Separa número y dígito verificador
    rut_numero = rut[:-1]
    dv = rut[-1]

    # Calcula el dígito verificador
    suma = 0
    multiplicador = 2

    for digito in reversed(rut_numero):
        suma += int(digito) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2

    resto = suma % 11
    dv_calculado = 11 - resto

    # Convierte el dígito verificador calculado
    if dv_calculado == 11:
        dv_esperado = '0'
    elif dv_calculado == 10:
        dv_esperado = 'K'
    else:
        dv_esperado = str(dv_calculado)

    return dv == dv_esperado


def normalize_rut(rut: str) -> str:
    """
    Normaliza un RUT al formato XX.XXX.XXX-X

    Args:
        rut: RUT a normalizar

    Returns:
        RUT normalizado
    """
    # Elimina puntos y guiones
    rut = rut.replace(".", "").replace("-", "").upper()

    # Separa número y dígito verificador
    rut_numero = rut[:-1]
    dv = rut[-1]

    # Formatea con puntos
    rut_formateado = ""
    for i, digito in enumerate(reversed(rut_numero)):
        if i > 0 and i % 3 == 0:
            rut_formateado = "." + rut_formateado
        rut_formateado = digito + rut_formateado

    return f"{rut_formateado}-{dv}"


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Valida la fortaleza de una contraseña.

    Requisitos:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número

    Args:
        password: Contraseña a validar

    Returns:
        Tupla (es_válida, mensaje_error)
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"

    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una mayúscula"

    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una minúscula"

    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número"

    return True, ""
