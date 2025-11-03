"""
Script para poblar la base de datos con datos de prueba.
"""

from datetime import date, datetime
import os
import re
import shutil
import unicodedata

from app import create_app, db
from app.models import User, Institution, Course, UserCourse, Grade, CourseFile

COURSE_TEMPLATES = [
    {
        "name": "Matemáticas Aplicadas",
        "focus": "Refuerzo de ejercicios tipo PAES y resolución de problemas contextualizados."
    },
    {
        "name": "Lenguaje y Comunicación",
        "focus": "Comprensión lectora avanzada, análisis de textos y preparación de ensayos argumentativos."
    },
    {
        "name": "Historia y Ciudadanía",
        "focus": "Procesos históricos del siglo XX, ciudadanía activa y debate informado."
    },
]

def seed_database(app=None):
    """Poblar la base de datos con datos de prueba."""
    app = app or create_app()

    with app.app_context():
        print("Iniciando seed de datos de prueba...")

        # 1. CREAR GRADOS EDUCATIVOS (Niveles escolares chilenos)
        print("\n1️⃣ Creando grados educativos chilenos...")
        grades_data = [
            {"name": "1ro Básico", "order": 1},
            {"name": "2do Básico", "order": 2},
            {"name": "3ro Básico", "order": 3},
            {"name": "4to Básico", "order": 4},
            {"name": "5to Básico", "order": 5},
            {"name": "6to Básico", "order": 6},
            {"name": "7mo Básico", "order": 7},
            {"name": "8vo Básico", "order": 8},
            {"name": "1ro Medio", "order": 9},
            {"name": "2do Medio", "order": 10},
            {"name": "3ro Medio", "order": 11},
            {"name": "4to Medio", "order": 12},
        ]

        grades_dict = {}
        for grade_data in grades_data:
            grade = Grade.query.filter_by(name=grade_data["name"]).first()
            if not grade:
                grade = Grade(name=grade_data["name"], order=grade_data["order"])
                db.session.add(grade)
                print(f'   Grado creado: {grade.name} (Orden: {grade.order})')
            else:
                print(f'   Grado ya existe: {grade.name}')
            grades_dict[grade.name] = grade
        db.session.commit()

        # 2. DATOS DE INSTITUCIONES Y USUARIOS
        institutions_data = [
            {
                "nombre": "Colegio Inglés de Quillota",
                "direccion": "José Miguel Carrera 550, Quillota",
                "fundacion": date(1933, 5, 16),
                "paginaweb": "https://colegioinglesquillota.cl/",
                "colorinstitucional": "#43569c",
                "logo_filename": "ingles.png",
                "student_domain": "inglesquillota.cl",
                "admin": {
                    "rut": "22038002-5",
                    "username": "Matias Diaz",
                    "email": "matias.diaz.c01@mail.pucv.cl",
                    "password": "Admin1234",
                    "region": "Valparaíso",
                    "comuna": "Quillota"
                },
                "teacher": {
                    "rut": "11111111-1",
                    "email": "matias.diaz@colegioinglesquillota.cl",
                    "password": "Profesor1234",
                    "region": "Valparaíso",
                    "comuna": "Quillota"
                }
            },
            {
                "nombre": "Liceo Gastronomía y Turismo",
                "direccion": "Diaguitas 1751, Quilpué",
                "fundacion": date(2003, 3, 3),
                "paginaweb": "https://liceogastronomiayturismo.webescuela.cl/",
                "colorinstitucional": "#69b1ab",
                "logo_filename": "lgt.png",
                "student_domain": "turismo.cl",
                "admin": {
                    "rut": "21523921-7",
                    "username": "Giovanni Ahumada",
                    "email": "giovanni.ahumada.t@mail.pucv.cl",
                    "password": "Admin1234",
                    "region": "Valparaíso",
                    "comuna": "Quilpué"
                },
                "teacher": {
                    "rut": "22222222-2",
                    "email": "giovanni.ahumada@lgt.cl",
                    "password": "Profesor1234",
                    "region": "Valparaíso",
                    "comuna": "Quilpué"
                }
            },
            {
                "nombre": "Instituto Rafael Ariztía",
                "direccion": "O\"Higgins 500, Quillota",
                "fundacion": date(1914, 3, 8),
                "paginaweb": "https://www.ira.maristas.cl/",
                "colorinstitucional": "#111d5c",
                "logo_filename": "ira.png",
                "student_domain": "maristas.cl",
                "admin": {
                    "rut": "21219402-6",
                    "username": "Daniel Saavedra",
                    "email": "daniel.saavedra.e@mail.pucv.cl",
                    "password": "Admin1234",
                    "region": "Valparaíso",
                    "comuna": "Quillota"
                },
                "teacher": {
                    "rut": "33333333-3",
                    "email": "daniel.saavedra@ira.cl",
                    "password": "Profesor1234",
                    "region": "Valparaíso",
                    "comuna": "Quillota"
                }
            }
        ]

        upload_folder = app.config["UPLOAD_FOLDER"]
        logos_dir = os.path.join(upload_folder, "institutions", "logos")
        seeder_assets_dir = os.path.join(os.path.dirname(__file__), "seeder")
        os.makedirs(logos_dir, exist_ok=True)

        print("\n2️⃣ Creando instituciones, administradores, profesores y alumnos...")

        def generate_fake_rut(institution_counter: int, student_counter: int) -> str:
            """
            Genera un RUT ficticio único por institución y estudiante.

            Formato: XX.XXX.XXX-D
            """
            base_number = institution_counter * 1_000_000 + student_counter * 10 + institution_counter
            base_str = f"{base_number:08d}"
            dv = (institution_counter + student_counter) % 10
            return f"{base_str[:2]}.{base_str[2:5]}.{base_str[5:8]}-{dv}"

        institution_context = {}
        cuarto_medio = grades_dict["4to Medio"]

        for inst_index, inst_data in enumerate(institutions_data, start=1):
            logo_filename = inst_data["logo_filename"]
            logo_rel_path = f"institutions/logos/{logo_filename}"
            logo_full_path = os.path.join(upload_folder, logo_rel_path)
            logo_source_path = os.path.join(seeder_assets_dir, logo_filename)

            try:
                if os.path.exists(logo_source_path):
                    shutil.copyfile(logo_source_path, logo_full_path)
                else:
                    print(f'  ⚠️ No se encontró el logo en {logo_source_path}, se dejará sin archivo.')
                    logo_rel_path = None
            except OSError as error:
                print(f'  ⚠️ No se pudo copiar el logo {logo_filename}: {error}')
                logo_rel_path = None

            # Crear o actualizar institución
            institution = Institution.query.filter_by(nombre=inst_data["nombre"]).first()
            if not institution:
                institution = Institution(
                    nombre=inst_data["nombre"],
                    direccion=inst_data["direccion"],
                    fundacion=inst_data["fundacion"],
                    paginaweb=inst_data["paginaweb"],
                    colorinstitucional=inst_data["colorinstitucional"],
                    logotipo=logo_rel_path
                )
                db.session.add(institution)
                db.session.flush()
                print(f'  Institución creada: {institution.nombre}')
            else:
                institution.direccion = inst_data["direccion"]
                institution.fundacion = inst_data["fundacion"]
                institution.paginaweb = inst_data["paginaweb"]
                institution.colorinstitucional = inst_data["colorinstitucional"]
                institution.logotipo = logo_rel_path
                print(f'  Institución actualizada: {institution.nombre}')

            # Crear o actualizar administrador
            admin_data = inst_data["admin"]
            admin = User.query.filter_by(email=admin_data["email"]).first()
            if not admin:
                admin = User(
                    rut=admin_data["rut"],
                    username=admin_data["username"],
                    email=admin_data["email"],
                    region=admin_data["region"],
                    comuna=admin_data["comuna"],
                    role="admin",
                    institution_id=institution.id
                )
                admin.set_password(admin_data["password"])
                db.session.add(admin)
                db.session.flush()
                print(f'    Admin creado: {admin.email}')
            else:
                admin.username = admin_data["username"]
                admin.region = admin_data["region"]
                admin.comuna = admin_data["comuna"]
                admin.role = "admin"
                admin.institution_id = institution.id
                print(f'    Admin actualizado: {admin.email}')

            # Crear o actualizar profesor con nombre alineado al admin
            teacher_data = inst_data["teacher"]
            teacher_name_base = admin_data["username"]
            teacher_username = teacher_name_base

            existing_same_name = User.query.filter_by(username=teacher_username).first()
            if existing_same_name and existing_same_name.email != teacher_data["email"]:
                teacher_username = f"{teacher_name_base} (Profesor)"

            teacher = User.query.filter_by(email=teacher_data["email"]).first()
            if not teacher:
                teacher = User(
                    rut=teacher_data["rut"],
                    username=teacher_username,
                    email=teacher_data["email"],
                    region=teacher_data["region"],
                    comuna=teacher_data["comuna"],
                    role="teacher",
                    institution_id=institution.id
                )
                teacher.set_password(teacher_data["password"])
                db.session.add(teacher)
                db.session.flush()
                print(f'    Profesor creado: {teacher.email}')
            else:
                teacher.username = teacher_username
                teacher.region = teacher_data["region"]
                teacher.comuna = teacher_data["comuna"]
                teacher.role = "teacher"
                teacher.institution_id = institution.id
                print(f'    Profesor actualizado: {teacher.email}')

            # Crear alumnos ficticios de 4to Medio
            for i in range(1, 6):
                student_email = f"alumno{i}@{inst_data['student_domain']}"
                student = User.query.filter_by(email=student_email).first()
                if not student:
                    student = User(
                        rut=generate_fake_rut(inst_index, i),
                        username=f"Alumno Falso {i} {institution.nombre.split(' ')[-1]}",
                        email=student_email,
                        region="Valparaíso",
                        comuna="Comuna Falsa",
                        role="student",
                        institution_id=institution.id,
                        grade_id=cuarto_medio.id
                    )
                    student.set_password("Alumno1234")
                    db.session.add(student)
                    print(f'    Estudiante creado: {student.email}')
                else:
                    student.grade_id = cuarto_medio.id
                    student.institution_id = institution.id
                    print(f'    Estudiante ya existe: {student.email}')

            db.session.flush()
            institution_context[institution.id] = {
                "institution": institution,
                "admin": admin,
                "teacher": teacher,
                "teacher_display_name": teacher_name_base
            }

        db.session.commit()

        print("\n3️⃣ Creando cursos de 4to Medio por institución...")
        courses_by_institution = {}
        course_template_map = {}

        for inst_data in institutions_data:
            institution = Institution.query.filter_by(nombre=inst_data["nombre"]).first()
            if not institution:
                continue

            for template in COURSE_TEMPLATES:
                course_name = f"{template['name']} {cuarto_medio.name}"
                prompt_text = (
                    f"Eres el docente de {course_name} en {institution.nombre}. "
                    f"{template['focus']} Mantén un tono cercano y coherente con el sello del establecimiento."
                )

                course = Course.query.filter_by(nombre=course_name, institution_id=institution.id).first()
                if not course:
                    course = Course(
                        nombre=course_name,
                        prompt=prompt_text,
                        institution_id=institution.id,
                        grade_id=cuarto_medio.id
                    )
                    db.session.add(course)
                    db.session.flush()
                    print(f'  Curso creado: "{course.nombre}" en {institution.nombre}')
                else:
                    course.prompt = prompt_text
                    course.grade_id = cuarto_medio.id
                    print(f'  Curso actualizado: "{course.nombre}" en {institution.nombre}')

                courses_by_institution.setdefault(institution.id, set()).add(course.id)
                course_template_map[course.id] = template

        db.session.commit()

        print("\n4️⃣ Inscribiendo profesores y alumnos en cursos...")
        current_year = date.today().year
        teacher_courses_assigned = set()

        for inst_id, context_data in institution_context.items():
            teacher = context_data["teacher"]
            admin = context_data["admin"]
            teacher_display_name = context_data["teacher_display_name"]

            course_ids = list(courses_by_institution.get(inst_id, []))
            if not course_ids:
                continue

            courses = (
                Course.query.filter(Course.id.in_(course_ids))
                .order_by(Course.id.asc())
                .all()
            )
            students = User.query.filter_by(
                institution_id=inst_id,
                role="student",
                grade_id=cuarto_medio.id
            ).all()

            for idx, course in enumerate(courses):
                if teacher and idx < 2:
                    enrollment = UserCourse.query.filter_by(
                        user_id=teacher.id,
                        course_id=course.id,
                        year=current_year
                    ).first()
                    if not enrollment:
                        enrollment = UserCourse(
                            user_id=teacher.id,
                            course_id=course.id,
                            year=current_year,
                            role_in_course="teacher"
                        )
                        db.session.add(enrollment)
                    teacher_courses_assigned.add(course.id)
                    print(f'  Profesor {teacher_display_name} asignado a {course.nombre}')
                else:
                    print(f'  Curso sin profesor asignado: {course.nombre}')

                for student in students:
                    enrollment = UserCourse.query.filter_by(
                        user_id=student.id,
                        course_id=course.id,
                        year=current_year
                    ).first()
                    if not enrollment:
                        enrollment = UserCourse(
                            user_id=student.id,
                            course_id=course.id,
                            year=current_year,
                            role_in_course="student"
                        )
                        db.session.add(enrollment)
                        print(f'    Estudiante {student.username} inscrito en {course.nombre}')

        db.session.commit()

        print("\n5️⃣ Generando archivos de referencia para los cursos...")

        def slugify(value: str) -> str:
            """Convierte texto en un slug ASCII seguro para nombres de archivo."""
            normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
            cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", normalized)
            return cleaned.strip("-").lower() or "curso"

        files_created = 0

        for inst_id, context_data in institution_context.items():
            teacher = context_data["teacher"]
            admin = context_data["admin"]
            teacher_display_name = context_data["teacher_display_name"]

            course_ids = list(courses_by_institution.get(inst_id, []))
            if not course_ids:
                continue

            courses = (
                Course.query.filter(Course.id.in_(course_ids))
                .order_by(Course.id.asc())
                .all()
            )

            for course in courses:
                template = course_template_map.get(course.id, {})
                subject_name = template.get("name", course.nombre.replace(f" {cuarto_medio.name}", "").strip())
                focus = template.get("focus", "Refuerzo de contenidos clave.")
                assigned_teacher_name = (
                    teacher_display_name if course.id in teacher_courses_assigned else "Por asignar"
                )

                uploader = teacher if (course.id in teacher_courses_assigned and teacher) else admin
                if not uploader:
                    continue  # No hay usuario disponible para asociar el archivo

                course_slug = slugify(course.nombre)
                course_dir = os.path.join(upload_folder, "courses", str(course.id))
                os.makedirs(course_dir, exist_ok=True)

                planning_content = (
                    f"# Planificación semanal de {subject_name}\n\n"
                    f"**Institución:** {course.institution.nombre}\n"
                    f"**Grado:** {cuarto_medio.name}\n"
                    f"**Curso:** {course.nombre}\n"
                    f"**Docente responsable:** {assigned_teacher_name}\n\n"
                    "## Objetivos de la semana\n"
                    f"- {focus}\n"
                    "- Promover el aprendizaje activo y colaborativo.\n"
                    "- Evaluar avances a través de actividades formativas.\n\n"
                    "## Actividades sugeridas\n"
                    "1. Diagnóstico inicial para activar conocimientos previos.\n"
                    f"2. Desarrollo guiado con ejercicios de {subject_name.lower()}.\n"
                    "3. Trabajo colaborativo en equipos heterogéneos.\n"
                    "4. Cierre reflexivo con salida escrita breve.\n\n"
                    "## Recursos para la semana\n"
                    "- Pizarra digital y material audiovisual.\n"
                    "- Cuaderno del estudiante y fichas de trabajo.\n"
                    "- Plataforma ACAChat para consultas asíncronas.\n"
                )

                guide_content = (
                    f"Guía de aprendizaje - {course.nombre}\n"
                    f"Institución: {course.institution.nombre}\n"
                    f"Grado: {cuarto_medio.name}\n"
                    f"Docente: {assigned_teacher_name}\n\n"
                    "Esta guía acompaña la planificación semanal y se apoya en el chatbot del curso.\n\n"
                    "Instrucciones para el estudiante:\n"
                    "1. Revisa la planificación y marca los objetivos que dominas.\n"
                    "2. Resuelve los ejercicios propuestos y valida tus respuestas con el chatbot.\n"
                    "3. Anota dudas específicas para llevar a la clase presencial.\n"
                    "4. Comparte un breve resumen de tu aprendizaje en el foro del curso.\n\n"
                    "Recuerda que el chatbot usa este material como contexto, por lo que puedes referenciarlo en tus preguntas."
                )

                sample_files = [
                    {
                        "filename": f"planificacion_{course_slug}.md",
                        "mimetype": "text/markdown",
                        "content": planning_content,
                    },
                    {
                        "filename": f"guia_aprendizaje_{course_slug}.txt",
                        "mimetype": "text/plain",
                        "content": guide_content,
                    },
                ]

                for sample in sample_files:
                    existing_file = CourseFile.query.filter_by(
                        course_id=course.id,
                        filename=sample["filename"]
                    ).first()

                    if existing_file:
                        continue

                    file_path = os.path.join(course_dir, sample["filename"])
                    if not os.path.exists(file_path):
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(sample["content"])

                    filesize = os.path.getsize(file_path)
                    relative_path = os.path.relpath(file_path, upload_folder).replace(os.sep, "/")

                    course_file = CourseFile(
                        course_id=course.id,
                        filename=sample["filename"],
                        filepath=relative_path,
                        filesize=filesize,
                        mimetype=sample["mimetype"],
                        uploaded_by=uploader.id,
                        uploaded_at=datetime.utcnow(),
                        parsed_content=sample["content"],
                        parsed_at=datetime.utcnow(),
                    )

                    db.session.add(course_file)
                    files_created += 1
                    print(f'  Archivo ficticio creado: {sample["filename"]} para {course.nombre}')

        if files_created:
            db.session.commit()
            print(f"\n   ✅ Archivos de curso generados: {files_created}")
        else:
            print("   ℹ️ No se agregaron nuevos archivos (ya existen).")


        # RESUMEN FINAL
        print("\n" + "=" * 60)
        print(" SEED COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print(f"\n RESUMEN:")
        print(f"   • Grados educativos: {Grade.query.count()}")
        print(f"   • Usuarios totales: {User.query.count()}")
        print(f"   • Administradores: {User.query.filter_by(role='admin').count()}")
        print(f"   • Profesores: {User.query.filter_by(role='teacher').count()}")
        print(f"   • Estudiantes: {User.query.filter_by(role='student').count()}")
        print(f"   • Instituciones: {Institution.query.count()}")
        print(f"   • Cursos: {Course.query.count()}")
        print(f"   • Matrículas: {UserCourse.query.count()}")
        print(f"   • Archivos de curso: {CourseFile.query.count()}")

        print("\n CREDENCIALES DE ACCESO (EJEMPLOS):")
        print(f"   Admin LGT: giovanni.ahumada.t@mail.pucv.cl / Admin1234")
        print(f"   Profesor LGT: giovanni.ahumada@lgt.cl / Profesor1234")
        print(f"   Estudiante LGT: alumno1@turismo.cl / Alumno1234")
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    seed_database()
