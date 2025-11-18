from . import db
from datetime import datetime
import bcrypt


class Grade(db.Model):
    """Modelo de nivel educativo (grado escolar)."""

    __tablename__ = "grades"

    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    # Ej: "1ro Básico", "2do Básico", ..., "4to Medio"

    order = db.Column(db.Integer, nullable=False, unique=True, index=True)
    # Para ordenar: 1 = 1ro básico, 12 = 4to medio

    # Campos de auditoría
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relaciones
    users = db.relationship('User', back_populates='grade')
    courses = db.relationship('Course', back_populates='grade')

    def to_dict(self) -> dict:
        """Serializa el grado a un diccionario."""
        return {
            "id": self.id,
            "name": self.name,
            "order": self.order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f"<Grade {self.name}>"


class User(db.Model):
    """Modelo de usuario con autenticación, roles y auditoría."""

    __tablename__ = "users"

    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(12), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    region = db.Column(db.String(100), nullable=False)
    comuna = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Rol del usuario
    role = db.Column(
        db.String(20),
        nullable=False,
        default='student',
        index=True
    )  # student, teacher, admin

    # Relación con institución y grado
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'), nullable=True, index=True)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'), nullable=True, index=True)

    # Campos de auditoría
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relaciones
    institution = db.relationship('Institution', back_populates='users')
    grade = db.relationship('Grade', back_populates='users')
    enrollments = db.relationship('UserCourse', back_populates='user', cascade='all, delete-orphan')
    uploaded_files = db.relationship('CourseFile', back_populates='uploader', foreign_keys='CourseFile.uploaded_by')

    def set_password(self, password: str) -> None:
        """
        Encripta la contraseña usando bcrypt.

        Args:
            password: Contraseña en texto plano
        """
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """
        Verifica si la contraseña proporcionada coincide con el hash.

        Args:
            password: Contraseña a verificar

        Returns:
            True si la contraseña es correcta, False en caso contrario
        """
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )

    def is_student(self) -> bool:
        """Verifica si el usuario es estudiante."""
        return self.role == 'student'

    def is_teacher(self) -> bool:
        """Verifica si el usuario es profesor."""
        return self.role == 'teacher'

    def is_admin(self) -> bool:
        """Verifica si el usuario es administrador."""
        return self.role == 'admin'

    def to_dict(self) -> dict:
        """
        Serializa el usuario a un diccionario (sin password_hash).

        Returns:
            Diccionario con los datos del usuario
        """
        return {
            "id": self.id,
            "rut": self.rut,
            "username": self.username,
            "email": self.email,
            "region": self.region,
            "comuna": self.comuna,
            "role": self.role,
            "institution_id": self.institution_id,
            "institution": {
                "id": self.institution.id,
                "nombre": self.institution.nombre,
                "colorinstitucional": self.institution.colorinstitucional
            } if self.institution else None,
            "grade_id": self.grade_id,
            "grade": self.grade.to_dict() if self.grade else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active
        }

    def __repr__(self) -> str:
        return f"<User {self.username} ({self.role})>"


class Institution(db.Model):
    """Modelo de institución educativa."""

    __tablename__ = "institutions"

    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    direccion = db.Column(db.String(300), nullable=True)
    fundacion = db.Column(db.Date, nullable=True)
    paginaweb = db.Column(db.String(200), nullable=True)
    logotipo = db.Column(db.String(500), nullable=True)  # Path del archivo
    colorinstitucional = db.Column(db.String(7), nullable=True)  # Formato: #RRGGBB

    # Campos de auditoría
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relaciones
    users = db.relationship('User', back_populates='institution')
    courses = db.relationship('Course', back_populates='institution', cascade='all, delete-orphan')

    def to_dict(self) -> dict:
        """Serializa la institución a un diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "fundacion": self.fundacion.isoformat() if self.fundacion else None,
            "paginaweb": self.paginaweb,
            "logotipo": self.logotipo,
            "colorinstitucional": self.colorinstitucional,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "courses_count": len(self.courses) if self.courses else 0
        }

    def __repr__(self) -> str:
        return f"<Institution {self.nombre}>"


class Course(db.Model):
    """Modelo de curso."""

    __tablename__ = "courses"

    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    prompt = db.Column(db.Text, nullable=True)  # Descripción/instrucciones del curso
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'), nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'), nullable=False, index=True)
    emoji = db.Column(db.String(16), nullable=True, default='📘')

    # Campos de auditoría
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # Soft delete
    chat_hidden_for_students = db.Column(db.Boolean, default=False, nullable=False)

    # Relaciones
    institution = db.relationship('Institution', back_populates='courses')
    grade = db.relationship('Grade', back_populates='courses')
    files = db.relationship('CourseFile', back_populates='course', cascade='all, delete-orphan')
    enrollments = db.relationship('UserCourse', back_populates='course', cascade='all, delete-orphan')

    def get_teachers(self):
        """Obtiene todos los profesores del curso."""
        return [
            enrollment.user for enrollment in self.enrollments
            if enrollment.role_in_course == 'teacher'
        ]

    def get_students(self):
        """Obtiene todos los estudiantes del curso."""
        return [
            enrollment.user for enrollment in self.enrollments
            if enrollment.role_in_course == 'student'
        ]

    def to_dict(self, include_institution=True, include_stats=True) -> dict:
        """Serializa el curso a un diccionario."""
        data = {
            "id": self.id,
            "nombre": self.nombre,
            "prompt": self.prompt,
            "emoji": self.emoji or '📘',
            "institution_id": self.institution_id,
            "grade_id": self.grade_id,
            "grade": self.grade.to_dict() if self.grade else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
            "chat_hidden_for_students": self.chat_hidden_for_students
        }

        if include_institution and self.institution:
            data["institution"] = {
                "id": self.institution.id,
                "nombre": self.institution.nombre,
                "colorinstitucional": self.institution.colorinstitucional
            }

        if include_stats:
            data["files_count"] = len(self.files) if self.files else 0
            data["students_count"] = len(self.get_students())
            data["teachers_count"] = len(self.get_teachers())

        return data

    def __repr__(self) -> str:
        return f"<Course {self.nombre}>"


class CourseFile(db.Model):
    """Modelo de archivos de cursos."""

    __tablename__ = "course_files"

    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)  # Nombre original
    filepath = db.Column(db.String(500), nullable=False)  # Path en storage
    filesize = db.Column(db.Integer, nullable=False)  # Tamaño en bytes
    mimetype = db.Column(db.String(100), nullable=False)  # Tipo MIME

    # Usuario que subió el archivo
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Contenido parseado para chatbot
    parsed_content = db.Column(db.Text, nullable=True)  # Contenido del archivo en texto/markdown
    parsed_at = db.Column(db.DateTime, nullable=True)  # Cuándo se parseó el archivo

    # Relaciones
    course = db.relationship('Course', back_populates='files')
    uploader = db.relationship('User', back_populates='uploaded_files', foreign_keys=[uploaded_by])

    def to_dict(self, include_parsed_content=False) -> dict:
        """Serializa el archivo a un diccionario."""
        data = {
            "id": self.id,
            "course_id": self.course_id,
            "filename": self.filename,
            "filepath": self.filepath,
            "filesize": self.filesize,
            "mimetype": self.mimetype,
            "uploaded_by": self.uploaded_by,
            "uploader": {
                "id": self.uploader.id,
                "username": self.uploader.username
            } if self.uploader else None,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
            "has_parsed_content": self.parsed_content is not None,
            "parsed_at": self.parsed_at.isoformat() if self.parsed_at else None
        }

        # Solo incluir el contenido parseado si se solicita explícitamente
        if include_parsed_content and self.parsed_content:
            data["parsed_content"] = self.parsed_content

        return data

    def __repr__(self) -> str:
        return f"<CourseFile {self.filename}>"


class UserCourse(db.Model):
    """Modelo de matrícula (tabla intermedia entre User y Course)."""

    __tablename__ = "user_courses"

    # Campos principales
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)  # Año académico (ej: 2025)
    role_in_course = db.Column(
        db.String(20),
        nullable=False
    )  # student o teacher
    enrolled_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Constraint: Un usuario no puede inscribirse dos veces al mismo curso en el mismo año
    __table_args__ = (
        db.UniqueConstraint('user_id', 'course_id', 'year', name='unique_user_course_year'),
    )

    # Relaciones
    user = db.relationship('User', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')

    def to_dict(self, include_course=True, include_user=False) -> dict:
        """Serializa la matrícula a un diccionario."""
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "course_id": self.course_id,
            "year": self.year,
            "role_in_course": self.role_in_course,
            "enrolled_at": self.enrolled_at.isoformat() if self.enrolled_at else None
        }

        if include_course and self.course:
            data["course"] = self.course.to_dict(include_stats=False)

        if include_user and self.user:
            data["user"] = {
                "id": self.user.id,
                "username": self.user.username,
                "email": self.user.email,
                "role": self.user.role
            }

        return data

    def __repr__(self) -> str:
        return f"<UserCourse user_id={self.user_id} course_id={self.course_id} year={self.year}>"
