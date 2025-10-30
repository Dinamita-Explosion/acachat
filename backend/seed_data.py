"""
Script para poblar la base de datos con datos de prueba.
"""

from datetime import date

from app import create_app, db
from app.models import User, Institution, Course, UserCourse, Grade


def seed_database(app=None):
    """Poblar la base de datos con datos de prueba."""
    app = app or create_app()

    with app.app_context():
        print("Iniciando seed de datos de prueba...")

        # 1. CREAR GRADOS EDUCATIVOS (Niveles escolares chilenos)
        print("\nCreando grados educativos chilenos...")
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
                db.session.commit()
                print(f"   Grado creado: {grade.name} (Orden: {grade.order})")
            else:
                print(f"    Grado ya existe: {grade.name}")
            grades_dict[grade.name] = grade

        # 2. CREAR ADMINISTRADOR
        print("\n Creando usuario administrador...")
        admin = User.query.filter_by(email="admin@example.com").first()

        if not admin:
            admin = User(
                rut="11111111-1",
                username="Administrador",
                email="admin@example.com",
                region="Metropolitana",
                comuna="Santiago",
                role="admin",
            )
            admin.set_password("Admin1234")
            db.session.add(admin)
            db.session.commit()
            print(f"    Admin creado: {admin.email} (ID: {admin.id})")
        else:
            print(f"     Admin ya existe: {admin.email} (ID: {admin.id})")

        # 3. CREAR INSTITUTO NACIONAL
        print("\n Creando institución de ejemplo...")
        instituto = Institution.query.filter_by(nombre="Academia Nacional").first()

        if not instituto:
            instituto = Institution(
                nombre="Academia Nacional",
                direccion="Av. Educadores 123, Santiago, Región Metropolitana",
                fundacion=date(1985, 3, 15),
                paginaweb="https://www.academianacional.cl",
                colorinstitucional="#0052A3",
            )
            db.session.add(instituto)
            db.session.commit()
            print(f"    Institución creada: {instituto.nombre} (ID: {instituto.id})")
        else:
            print(
                f"     Institución ya existe: {instituto.nombre} (ID: {instituto.id})"
            )

        # 4. CREAR ALGUNOS PROFESORES
        print("\n4️⃣ Creando profesores de ejemplo...")
        profesores_data = [
            {
                "rut": "12345678-5",
                "username": "María Torres",
                "email": "maria.torres@academianacional.cl",
                "region": "Metropolitana",
                "comuna": "Santiago",
                "role": "teacher",
                "password": "Teacher1234",
                "grade": "4to Medio",
            },
            {
                "rut": "23456789-6",
                "username": "Luis Fernández",
                "email": "luis.fernandez@academianacional.cl",
                "region": "Metropolitana",
                "comuna": "Santiago",
                "role": "teacher",
                "password": "Teacher1234",
                "grade": "3ro Medio",
            },
        ]

        profesores = []
        for prof_data in profesores_data:
            profesor = User.query.filter_by(email=prof_data["email"]).first()
            if not profesor:
                profesor = User(
                    rut=prof_data["rut"],
                    username=prof_data["username"],
                    email=prof_data["email"],
                    region=prof_data["region"],
                    comuna=prof_data["comuna"],
                    role=prof_data["role"],
                    institution_id=instituto.id,
                    grade_id=grades_dict[prof_data["grade"]].id,
                )
                profesor.set_password(prof_data["password"])
                db.session.add(profesor)
                db.session.commit()
                print(
                    f"    Profesor creado: {profesor.email} (ID: {profesor.id}, Grado: {prof_data['grade']})"
                )
            else:
                print(f"     Profesor ya existe: {profesor.email} (ID: {profesor.id})")
            profesores.append(profesor)

        # 5. CREAR ESTUDIANTES
        print("\n5️⃣ Creando estudiantes de ejemplo...")
        estudiantes_data = [
            {
                "rut": "20111222-3",
                "username": "Juan Pérez",
                "email": "juan.perez@estudiante.cl",
                "region": "Metropolitana",
                "comuna": "Santiago",
                "role": "student",
                "password": "Student1234",
                "grade": "4to Medio",  # Estudiante de 4to Medio
            },
            {
                "rut": "20222333-4",
                "username": "María González",
                "email": "maria.gonzalez@estudiante.cl",
                "region": "Metropolitana",
                "comuna": "Providencia",
                "role": "student",
                "password": "Student1234",
                "grade": "4to Medio",  # Estudiante de 4to Medio
            },
            {
                "rut": "20333444-5",
                "username": "Pedro Silva",
                "email": "pedro.silva@estudiante.cl",
                "region": "Metropolitana",
                "comuna": "Las Condes",
                "role": "student",
                "password": "Student1234",
                "grade": "3ro Medio",  # Estudiante de 3ro Medio
            },
        ]

        estudiantes = []
        for est_data in estudiantes_data:
            estudiante = User.query.filter_by(email=est_data["email"]).first()
            if not estudiante:
                estudiante = User(
                    rut=est_data["rut"],
                    username=est_data["username"],
                    email=est_data["email"],
                    region=est_data["region"],
                    comuna=est_data["comuna"],
                    role=est_data["role"],
                    institution_id=instituto.id,
                    grade_id=grades_dict[est_data["grade"]].id,
                )
                estudiante.set_password(est_data["password"])
                db.session.add(estudiante)
                db.session.commit()
                print(
                    f"    Estudiante creado: {estudiante.email} (ID: {estudiante.id}, Grado: {est_data['grade']})"
                )
            else:
                print(
                    f"     Estudiante ya existe: {estudiante.email} (ID: {estudiante.id})"
                )
            estudiantes.append(estudiante)

        # 6. CREAR CURSOS
        print("\n Creando cursos...")
        cursos_data = [
            {
                "nombre": "Matemáticas 4° Medio",
                "prompt": "Curso de matemáticas avanzadas para cuarto año medio. Incluye cálculo, álgebra avanzada y estadística.",
                "institution_id": instituto.id,
                "grade": "4to Medio",
            },
            {
                "nombre": "Historia y Ciencias Sociales 3° Medio",
                "prompt": "Historia de Chile y América Latina en el contexto mundial. Análisis de procesos históricos contemporáneos.",
                "institution_id": instituto.id,
                "grade": "3ro Medio",
            },
            {
                "nombre": "Física 4° Medio",
                "prompt": "Física avanzada con énfasis en mecánica cuántica y termodinámica.",
                "institution_id": instituto.id,
                "grade": "4to Medio",
            },
        ]

        cursos = []
        for curso_data in cursos_data:
            curso = Course.query.filter_by(
                nombre=curso_data["nombre"], institution_id=curso_data["institution_id"]
            ).first()

            if not curso:
                curso = Course(
                    nombre=curso_data["nombre"],
                    prompt=curso_data["prompt"],
                    institution_id=curso_data["institution_id"],
                    grade_id=grades_dict[curso_data["grade"]].id,
                )
                db.session.add(curso)
                db.session.commit()
                print(
                    f"    Curso creado: {curso.nombre} (ID: {curso.id}, Grado: {curso_data['grade']})"
                )
            else:
                print(f"     Curso ya existe: {curso.nombre} (ID: {curso.id})")
            cursos.append(curso)

        # 7. ASIGNAR PROFESORES A CURSOS
        print("\n Asignando profesores a cursos...")
        if len(profesores) >= 2 and len(cursos) >= 2:
            # Asignar profesor de matemáticas
            enrollment1 = UserCourse.query.filter_by(
                user_id=profesores[0].id, course_id=cursos[0].id, year=2025
            ).first()

            if not enrollment1:
                enrollment1 = UserCourse(
                    user_id=profesores[0].id,
                    course_id=cursos[0].id,
                    year=2025,
                    role_in_course="teacher",
                )
                db.session.add(enrollment1)
                print(f"    {profesores[0].username} asignado a {cursos[0].nombre}")
            else:
                print(
                    f"     Asignación ya existe: {profesores[0].username} → {cursos[0].nombre}"
                )

            # Asignar profesora de historia
            enrollment2 = UserCourse.query.filter_by(
                user_id=profesores[1].id, course_id=cursos[1].id, year=2025
            ).first()

            if not enrollment2:
                enrollment2 = UserCourse(
                    user_id=profesores[1].id,
                    course_id=cursos[1].id,
                    year=2025,
                    role_in_course="teacher",
                )
                db.session.add(enrollment2)
                print(f"    {profesores[1].username} asignado a {cursos[1].nombre}")
            else:
                print(
                    f"     Asignación ya existe: {profesores[1].username} → {cursos[1].nombre}"
                )

            db.session.commit()

        # 8. INSCRIBIR ESTUDIANTES EN CURSOS
        print("\n Inscribiendo estudiantes en cursos...")
        for estudiante in estudiantes:
            for i, curso in enumerate(cursos[:2]):  # Inscribir en los primeros 2 cursos
                enrollment = UserCourse.query.filter_by(
                    user_id=estudiante.id, course_id=curso.id, year=2025
                ).first()

                if not enrollment:
                    enrollment = UserCourse(
                        user_id=estudiante.id,
                        course_id=curso.id,
                        year=2025,
                        role_in_course="student",
                    )
                    db.session.add(enrollment)
                    print(f"    {estudiante.username} inscrito en {curso.nombre}")
                else:
                    print(
                        f"     Inscripción ya existe: {estudiante.username} → {curso.nombre}"
                    )

        db.session.commit()

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

        print("\n CREDENCIALES DE ACCESO:")
        print(f"   Admin: admin@example.com / Admin1234")
        print(f"   Profesor: maria.torres@academianacional.cl / Teacher1234")
        print(f"   Estudiante: juan.perez@estudiante.cl / Student1234")
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    seed_database()
