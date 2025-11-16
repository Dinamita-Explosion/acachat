const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const MIN_PASSWORD_LENGTH = 8;
export const MAX_PASSWORD_LENGTH = 64;

export interface PasswordValidationOptions {
  enforceComplexity?: boolean;
}

export function validateEmail(email: string | null | undefined): boolean {
  if (!email) {
    return false;
  }
  return emailRegex.test(email.trim());
}

export function validateRut(rawValue: string | null | undefined): boolean {
  if (!rawValue) {
    return false;
  }

  const normalized = rawValue.replace(/\./g, '').replace(/-/g, '').toUpperCase();

  if (!/^\d{7,8}[0-9K]$/.test(normalized)) {
    return false;
  }

  const rutNumber = normalized.slice(0, -1);
  const digit = normalized.slice(-1);

  let sum = 0;
  let multiplier = 2;

  for (let i = rutNumber.length - 1; i >= 0; i--) {
    sum += Number(rutNumber[i]) * multiplier;
    multiplier = multiplier === 7 ? 2 : multiplier + 1;
  }

  const remainder = sum % 11;
  const verificationDigit = 11 - remainder;
  let expected: string;

  if (verificationDigit === 11) {
    expected = '0';
  } else if (verificationDigit === 10) {
    expected = 'K';
  } else {
    expected = String(verificationDigit);
  }

  return digit === expected;
}

export function validatePassword(
  password: string | null | undefined,
  options?: PasswordValidationOptions,
): string | null {
  const enforceComplexity = options?.enforceComplexity ?? true;
  const value = password ?? '';
  const trimmed = value.trim();

  if (!trimmed) {
    return 'La contraseña es obligatoria.';
  }

  if (value.length < MIN_PASSWORD_LENGTH) {
    return `La contraseña debe tener al menos ${MIN_PASSWORD_LENGTH} caracteres.`;
  }

  if (value.length > MAX_PASSWORD_LENGTH) {
    return `La contraseña no puede superar los ${MAX_PASSWORD_LENGTH} caracteres.`;
  }

  if (!enforceComplexity) {
    return null;
  }

  if (!/[A-Z]/.test(value)) {
    return 'La contraseña debe incluir al menos una mayúscula.';
  }

  if (!/[a-z]/.test(value)) {
    return 'La contraseña debe incluir al menos una minúscula.';
  }

  if (!/\d/.test(value)) {
    return 'La contraseña debe incluir al menos un número.';
  }

  return null;
}
