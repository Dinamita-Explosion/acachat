# Panel de Administración ACACHAT

## Descripción

El panel de administración es una interfaz web completamente independiente que permite gestionar todos los recursos de ACACHAT:

- 👥 **Usuarios**: Crear, editar y eliminar usuarios
- 🏛️ **Instituciones**: Administrar instituciones educativas
- 📚 **Cursos**: Gestionar cursos y asignaturas
- 📝 **Matrículas**: Administrar inscripciones de usuarios en cursos
- 📁 **Archivos**: Ver y eliminar archivos subidos

## Características

✅ **Autenticación segura con JWT**: Login con email y contraseña
✅ **Independiente del backend**: Si eliminas la vista, el backend sigue funcionando normalmente
✅ **Usa las APIs existentes**: Todas las operaciones se realizan mediante las APIs REST ya creadas
✅ **Manejo automático de tokens**: Refresco automático de tokens expirados
✅ **Interfaz responsive**: Funciona en desktop, tablet y móvil
✅ **Solo para administradores**: Requiere rol de admin para acceder

## Acceso

1. **URL**: `http://localhost:5000/admin`

2. **Credenciales**: Necesitas un usuario con rol `admin`

   Para crear un usuario admin, puedes usar el endpoint de registro con el campo `role: "admin"`, o promover un usuario existente mediante la base de datos.

## Funcionalidades

### Login
- Ingresa con tu email y contraseña de administrador
- El token se guarda automáticamente en localStorage
- Si el token expira, se intenta refrescar automáticamente

### Gestión de Usuarios
- **Listar**: Ver todos los usuarios del sistema
- **Crear**: Registrar nuevos usuarios (estudiantes, profesores, admins)
- **Editar**: Modificar información de usuarios existentes
- **Eliminar**: Borrar usuarios del sistema
- **Filtrar**: Por rol y estado activo/inactivo

### Gestión de Instituciones
- **Listar**: Ver todas las instituciones
- **Crear**: Agregar nuevas instituciones
- **Editar**: Modificar datos institucionales
- **Eliminar**: Borrar instituciones
- Gestión de datos como dirección, web, color institucional, etc.

### Gestión de Cursos
- **Listar**: Ver todos los cursos
- **Crear**: Crear nuevos cursos
- **Editar**: Modificar información de cursos
- **Eliminar**: Borrar cursos
- Ver estadísticas (archivos, estudiantes, profesores)

### Gestión de Matrículas
- **Listar**: Ver todas las inscripciones
- **Crear**: Inscribir usuarios en cursos
- **Eliminar**: Remover inscripciones
- Asignar roles en curso (estudiante/profesor)

### Gestión de Archivos
- **Listar**: Ver todos los archivos subidos
- **Eliminar**: Borrar archivos del sistema
- Ver metadatos (tamaño, tipo, fecha, uploader)

## Seguridad

- ✅ **Autenticación JWT obligatoria**: Todas las peticiones requieren token válido
- ✅ **Solo administradores**: Los endpoints verifican el rol de admin
- ✅ **Rate limiting**: Protección contra fuerza bruta en login
- ✅ **Tokens de refresco**: Para mantener sesiones seguras
- ✅ **Logout seguro**: Limpia todos los datos de sesión

## Arquitectura

La vista de admin es completamente independiente:

1. **Frontend**: Un único archivo HTML con CSS y JavaScript vanilla
2. **Sin dependencias**: No requiere frameworks ni librerías externas
3. **API REST**: Consume las mismas APIs que cualquier otra aplicación
4. **Desacoplado**: Si eliminas `/admin`, el backend sigue funcionando normalmente

## APIs Utilizadas

El panel utiliza estos endpoints del backend:

- `POST /api/auth/login` - Autenticación
- `POST /api/auth/refresh` - Refresco de token
- `GET /api/auth/users` - Listar usuarios
- `GET /api/auth/users/:id` - Obtener usuario
- `POST /api/auth/register` - Crear usuario
- `PUT /api/auth/users/:id` - Actualizar usuario
- `DELETE /api/auth/users/:id` - Eliminar usuario
- `GET /api/institutions` - Listar instituciones
- `GET /api/institutions/:id` - Obtener institución
- `POST /api/institutions` - Crear institución
- `PUT /api/institutions/:id` - Actualizar institución
- `DELETE /api/institutions/:id` - Eliminar institución
- `GET /api/courses` - Listar cursos
- `GET /api/courses/:id` - Obtener curso
- `POST /api/courses` - Crear curso
- `PUT /api/courses/:id` - Actualizar curso
- `DELETE /api/courses/:id` - Eliminar curso
- `GET /api/enrollments` - Listar matrículas
- `POST /api/enrollments` - Crear matrícula
- `DELETE /api/enrollments/:id` - Eliminar matrícula
- `GET /api/files` - Listar archivos
- `DELETE /api/files/:id` - Eliminar archivo

## Desarrollo

Para modificar la vista de admin, edita:
- **Archivo**: `backend/app/templates/admin.html`
- **Ruta**: `backend/app/routes/admin.py`

La ruta simplemente sirve el archivo HTML, toda la lógica está en el frontend.

## Notas

- El panel guarda el token en `localStorage`, así que persiste entre sesiones
- Si cierras el navegador y vuelves a abrir, seguirás logueado (hasta que expire el token)
- El botón "Cerrar Sesión" limpia todos los datos de autenticación
- Si hay problemas de CORS, verifica la configuración en `backend/app/__init__.py`
