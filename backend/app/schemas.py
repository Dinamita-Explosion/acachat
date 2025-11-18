"""Schemas de validación usando Marshmallow."""
from marshmallow import Schema, fields, validates, ValidationError, validate, validates_schema
from .utils.validators import validate_rut, validate_password_strength
import re


# ==========================================
# SCHEMAS DE GRADO (Grade)
# ==========================================

class GradeSchema(Schema):
    """Schema para serializar un grado educativo (respuesta)."""

    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    order = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class GradeCreateSchema(Schema):
    """Schema para crear un grado educativo."""

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50),
        error_messages={"required": "El nombre del grado es obligatorio"}
    )
    order = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=100),
        error_messages={"required": "El orden es obligatorio"}
    )


class GradeUpdateSchema(Schema):
    """Schema para actualizar un grado educativo."""

    name = fields.Str(
        validate=validate.Length(min=1, max=50)
    )
    order = fields.Int(
        validate=validate.Range(min=1, max=100)
    )


# ==========================================
# SCHEMAS DE USUARIO (User)
# ==========================================

class RegisterSchema(Schema):
    """Schema para validar el registro de usuarios."""

    rut = fields.Str(required=True, error_messages={
        "required": "El RUT es obligatorio"
    })
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80),
        error_messages={
            "required": "El nombre de usuario es obligatorio"
        }
    )
    email = fields.Email(required=True, error_messages={
        "required": "El email es obligatorio",
        "invalid": "El email no es válido"
    })
    region = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "La región es obligatoria"}
    )
    comuna = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "La comuna es obligatoria"}
    )
    password = fields.Str(
        required=True,
        load_only=True,
        error_messages={"required": "La contraseña es obligatoria"}
    )
    institution_id = fields.Int(
        required=True,
        error_messages={"required": "La institución es obligatoria"}
    )
    grade_id = fields.Int(allow_none=True)
    role = fields.Str(
        validate=validate.OneOf(['student', 'teacher', 'admin']),
        missing='student',  # Por defecto 'student'
        error_messages={"validator_failed": "El rol debe ser student, teacher o admin"}
    )

    @validates("rut")
    def validate_rut_field(self, value):
        """Valida el formato y dígito verificador del RUT."""
        if not validate_rut(value):
            raise ValidationError("El RUT no es válido")

    @validates("password")
    def validate_password_field(self, value):
        """Valida la fortaleza de la contraseña."""
        is_valid, error_message = validate_password_strength(value)
        if not is_valid:
            raise ValidationError(error_message)


class ProfileUpdateSchema(Schema):
    """Schema para actualizar el perfil del usuario autenticado."""

    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80),
        error_messages={
            "required": "El nombre de usuario es obligatorio"
        }
    )


class PasswordChangeSchema(Schema):
    """Schema para cambio de contraseña usando email y contraseña actual."""

    email = fields.Email(required=True, error_messages={
        "required": "El email es obligatorio",
        "invalid": "El email no es válido"
    })
    old_password = fields.Str(
        required=True,
        load_only=True,
        error_messages={"required": "La contraseña actual es obligatoria"}
    )
    new_password = fields.Str(
        required=True,
        load_only=True,
        error_messages={"required": "La nueva contraseña es obligatoria"}
    )

    @validates("new_password")
    def validate_new_password(self, value):
        is_valid, error_message = validate_password_strength(value)
        if not is_valid:
            raise ValidationError(error_message)

    @validates_schema
    def ensure_passwords_differ(self, data, **_):
        if data.get('old_password') and data.get('new_password'):
            if data['old_password'] == data['new_password']:
                raise ValidationError("La nueva contraseña debe ser distinta a la actual.")


class LoginSchema(Schema):
    """Schema para validar el login."""

    email = fields.Email(required=True, error_messages={
        "required": "El email es obligatorio",
        "invalid": "El email no es válido"
    })
    password = fields.Str(required=True, error_messages={
        "required": "La contraseña es obligatoria"
    })


class UserSchema(Schema):
    """Schema para serializar datos de usuario (respuestas)."""

    id = fields.Int(dump_only=True)
    rut = fields.Str(dump_only=True)
    username = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    region = fields.Str(dump_only=True)
    comuna = fields.Str(dump_only=True)
    role = fields.Str(dump_only=True)
    institution_id = fields.Int(dump_only=True)
    institution = fields.Nested("InstitutionSchema", dump_only=True, allow_none=True)
    grade_id = fields.Int(dump_only=True)
    grade = fields.Nested("GradeSchema", dump_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_active = fields.Bool(dump_only=True)


class UpdateRoleSchema(Schema):
    """Schema para actualizar el rol de un usuario."""

    role = fields.Str(
        required=True,
        validate=validate.OneOf(['student', 'teacher', 'admin']),
        error_messages={
            "required": "El rol es obligatorio",
            "validator_failed": "El rol debe ser student, teacher o admin"
        }
    )


# ==========================================
# SCHEMAS DE INSTITUCIÓN (Institution)
# ==========================================

class InstitutionCreateSchema(Schema):
    """Schema para crear una institución."""

    nombre = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200),
        error_messages={"required": "El nombre es obligatorio"}
    )
    direccion = fields.Str(
        allow_none=True,
        validate=validate.Length(max=300)
    )
    fundacion = fields.Date(
        allow_none=True,
        error_messages={"invalid": "Formato de fecha inválido (YYYY-MM-DD)"}
    )
    paginaweb = fields.Url(
        allow_none=True,
        error_messages={"invalid": "URL inválida"}
    )
    colorinstitucional = fields.Str(
        allow_none=True,
        validate=validate.Regexp(
            r'^#[0-9A-Fa-f]{6}$',
            error='El color debe estar en formato hexadecimal (#RRGGBB)'
        )
    )


class InstitutionUpdateSchema(Schema):
    """Schema para actualizar una institución."""

    nombre = fields.Str(
        validate=validate.Length(min=1, max=200)
    )
    direccion = fields.Str(
        allow_none=True,
        validate=validate.Length(max=300)
    )
    fundacion = fields.Date(
        allow_none=True,
        error_messages={"invalid": "Formato de fecha inválido (YYYY-MM-DD)"}
    )
    paginaweb = fields.Url(
        allow_none=True,
        error_messages={"invalid": "URL inválida"}
    )
    colorinstitucional = fields.Str(
        allow_none=True,
        validate=validate.Regexp(
            r'^#[0-9A-Fa-f]{6}$',
            error='El color debe estar en formato hexadecimal (#RRGGBB)'
        )
    )


class InstitutionSchema(Schema):
    """Schema para serializar una institución (respuesta)."""

    id = fields.Int(dump_only=True)
    nombre = fields.Str(dump_only=True)
    direccion = fields.Str(dump_only=True)
    fundacion = fields.Date(dump_only=True)
    paginaweb = fields.Str(dump_only=True)
    logotipo = fields.Str(dump_only=True)
    colorinstitucional = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    courses_count = fields.Int(dump_only=True)


# ==========================================
# SCHEMAS DE CURSO (Course)
# ==========================================

class CourseCreateSchema(Schema):
    """Schema para crear un curso."""

    nombre = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200),
        error_messages={"required": "El nombre del curso es obligatorio"}
    )
    prompt = fields.Str(
        allow_none=True
    )
    emoji = fields.Str(
        allow_none=True,
        validate=validate.Length(min=1, max=16)
    )
    institution_id = fields.Int(
        required=True,
        error_messages={"required": "El ID de la institución es obligatorio"}
    )
    grade_id = fields.Int(
        required=True,
        error_messages={"required": "El ID del grado es obligatorio"}
    )


class CourseUpdateSchema(Schema):
    """Schema para actualizar un curso."""

    nombre = fields.Str(
        validate=validate.Length(min=1, max=200)
    )
    prompt = fields.Str(
        allow_none=True
    )
    emoji = fields.Str(
        allow_none=True,
        validate=validate.Length(min=1, max=16)
    )
    institution_id = fields.Int()
    grade_id = fields.Int()
    is_active = fields.Bool()
    chat_hidden_for_students = fields.Bool()


class CourseSchema(Schema):
    """Schema para serializar un curso (respuesta)."""

    id = fields.Int(dump_only=True)
    nombre = fields.Str(dump_only=True)
    prompt = fields.Str(dump_only=True)
    emoji = fields.Str(dump_only=True)
    institution_id = fields.Int(dump_only=True)
    institution = fields.Nested(InstitutionSchema, dump_only=True, only=['id', 'nombre', 'colorinstitucional'])
    grade_id = fields.Int(dump_only=True)
    grade = fields.Nested(GradeSchema, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    files_count = fields.Int(dump_only=True)
    students_count = fields.Int(dump_only=True)
    teachers_count = fields.Int(dump_only=True)
    chat_hidden_for_students = fields.Bool(dump_only=True)


# ==========================================
# SCHEMAS DE MATRÍCULA (UserCourse)
# ==========================================

class EnrollmentCreateSchema(Schema):
    """Schema para inscribir un estudiante a un curso."""

    course_id = fields.Int(
        required=True,
        error_messages={"required": "El ID del curso es obligatorio"}
    )
    year = fields.Int(
        required=True,
        validate=validate.Range(min=2000, max=2100),
        error_messages={"required": "El año es obligatorio"}
    )


class AssignTeacherSchema(Schema):
    """Schema para asignar un profesor a un curso."""

    user_id = fields.Int(
        required=True,
        error_messages={"required": "El ID del usuario es obligatorio"}
    )
    course_id = fields.Int(
        required=True,
        error_messages={"required": "El ID del curso es obligatorio"}
    )
    year = fields.Int(
        required=True,
        validate=validate.Range(min=2000, max=2100),
        error_messages={"required": "El año es obligatorio"}
    )


class EnrollmentSchema(Schema):
    """Schema para serializar una matrícula (respuesta)."""

    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    course_id = fields.Int(dump_only=True)
    year = fields.Int(dump_only=True)
    role_in_course = fields.Str(dump_only=True)
    enrolled_at = fields.DateTime(dump_only=True)
    course = fields.Nested(CourseSchema, dump_only=True)
    user = fields.Nested(UserSchema, dump_only=True, only=['id', 'username', 'email', 'role'])


# ==========================================
# SCHEMAS DE ARCHIVO (CourseFile)
# ==========================================

class CourseFileSchema(Schema):
    """Schema para serializar un archivo de curso (respuesta)."""

    id = fields.Int(dump_only=True)
    course_id = fields.Int(dump_only=True)
    filename = fields.Str(dump_only=True)
    filepath = fields.Str(dump_only=True)
    filesize = fields.Int(dump_only=True)
    mimetype = fields.Str(dump_only=True)
    uploaded_by = fields.Int(dump_only=True)
    uploader = fields.Nested(UserSchema, dump_only=True, only=['id', 'username'])
    uploaded_at = fields.DateTime(dump_only=True)


class BulkEnrollmentSchema(Schema):
    """Schema para inscribir múltiples estudiantes."""

    course_id = fields.Int(required=True, error_messages={"required": "El ID del curso es obligatorio"})
    year = fields.Int(
        required=False,
        validate=validate.Range(min=2000, max=2100),
    )
    user_ids = fields.List(fields.Int(), required=False)
    grade_id = fields.Int(required=False, allow_none=True)
