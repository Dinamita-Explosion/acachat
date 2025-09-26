<img src="./src/assets/icon/readmeicon.png" alt="logo" width="100" />

# Acachat 

**Presentado por:**
- Giovanni Ahumada
- Matías Díaz
- Daniel Saavedra

##  Índice
1. [Resumen del Proyecto](#resumen-del-proyecto)
2. [Requerimientos](#requerimientos)
3. [Librerias usadas con Angular](#librerias-usadas-con-angular)
3. [Diseño de prototipos](#diseño-de-prototipos)
4. [Tecnologías](#tecnologías)

## Resumen del proyecto

**Acachat** es una aplicación móvil cuya finalidad es ofrecer y hacer mas amigable el uso de IA's generativas (LLM) dentro de establecimientos academicos, ofreciendo un uso personalizado para estudiantes y profesores, con contenido creado y diseñado para cada asignatura.


## Requerimientos

### Roles del sistema

- **Administrador**: Tiene control total del sistema.
- **Profesor**: Puede agregar, eliminar y modificar nuevos cursos y añadir o quitar estudiantes de los cursos.
- **Estudiante**: Puede ver los cursos que se le asignaron y usar el chat de los cursos.

### Requerimientos Funcionales por Rol

#### Rol-Administrador

- **RF-ADM-01**: El administrador puede gestionar usuarios y asignar roles.
- **RF-ADM-02**: El administrador puede cambiar las instituciones acádemicas de los usuarios.
- **RF-ADM-03**: El administrador puede gestionar las intituciones acádemicas asociadas.

#### Rol-Profesor

- **RF-PRO-01**: El profesor puede gestionar cursos.
- **RF-PRO-02**: El profesor puede asignar estudiantes a uno o a más cursos.
- **RF-PRO-03**: El profesor puede gestionar el material que usará el chatbot.

#### Rol-Estudiante

- **RF-EST-01**: El estudiante puede visualizar los cursos en los que está inscrito.
- **RF-EST-02**: El estudiante puede chatear con el chatbot asignado a un curso.

### Requerimientos No Funcionales

- **RNF-01:** El sistema deberá tener disponiblilidad del 99.5% del tiempo de un mes
- **RNF-02:** El sitema debe ser utilizado por usuarios autenticados anteriormente.
- **RNF-03:** El sistema debe de soportar más de mil usuarios al mismo tiempo sin pérdida notable de rendimiento.
- **RNF-04:** El sistema debe restringir acceso de funciones según el rol.
- **RNF-05:** La base de datos debe poder gestionar  un crecimineto de un 500% sin que el rendimineto se vea perjudicado.
- **RNF-06:** El sistema debe tener una interfaz intuitiva y fácil de usar.
- **RNF-07:** El sistema debe ser capaz de realizar funciones con un ancho de banda bajo.

---

## Librerias usadas con Angular

 ![@angular/localize](https://img.shields.io/badge/@angular%2Flocalize-EE2F2F?style=flat&logo=angular&logoColor=white) <br> Utilizado para generar una traducción al texto implementado en las vistas.

## Diseño de prototipos

<div align="center">

[![Figma](https://img.shields.io/badge/Figma-000000?style=flat&logo=figma&logoColor=white)](#)  
</div>

## Tecnologías
<div align="center">

[![Ionic](https://img.shields.io/badge/Ionic-3880FF?style=flat&logo=ionic&logoColor=white)](#)
[![Angular](https://img.shields.io/badge/Angular-DD0031?style=flat&logo=angular&logoColor=white)](#)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-06B6D4?style=flat&logo=tailwind-css&logoColor=white)](#)
</div>
