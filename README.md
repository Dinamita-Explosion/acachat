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

- **Profesor**: Puede gestionar los documentos usados en cada materia donde imparte.
- **Estudiante**: Puede ver los materias que se le asignaron y usar el chat de los cursos.

### Requerimientos Funcionales por Rol

#### Rol-Profesor

- **RF-PRO-01**: El profesor puede visualizar las materias donde imparte clases.
- **RF-PRO-02**: El profesor puede ver el listado de estudiantes de una materia en específico.
- **RF-PRO-03**: El profesor puede gestionar el material que usará el chatbot.
- **RF-PRO-04**: El profesor puede filtrar palabras o frases que no se podrán usar dentro de los chats de una materia en específico.
- **RF-PRO-05**: El profesor puede ocultar el chat de una materia en específico a los estudiantes inscritos.

#### Rol-Estudiante

- **RF-EST-01**: El estudiante puede visualizar las materias en los que está inscrito.
- **RF-EST-02**: El estudiante puede conversar con el chatbot asignado a un curso.
- **RF-EST-03**: El estudiante puede vaciar el chat de una materia en específico.
- **RF-EST-04**: El estudiante puede exportar a un texto el chat de una materia en específico.

### Requerimientos No Funcionales

- **RNF-01:** El sistema deberá tener disponiblilidad del 99.5% del tiempo de un mes
- **RNF-02:** El sitema debe ser utilizado por usuarios autenticados anteriormente.
- **RNF-03:** El sistema debe de soportar más de mil usuarios al mismo tiempo sin pérdida notable de rendimiento.
- **RNF-04:** El sistema debe restringir acceso de funciones según el rol.
- **RNF-05:** La base de datos debe poder gestionar un crecimineto de un 500% sin que el rendimineto se vea perjudicado.
- **RNF-06:** El sistema debe tener una interfaz intuitiva y fácil de usar.
- **RNF-07:** El sistema debe ser capaz de realizar funciones con un ancho de banda bajo.

---

## Principios de Experiencia de Usuario (UX) y Patrones de Diseño

* Arquitectura de Componentes Reutilizables
* Navegación Intuitiva y Estándar
* Jerarquía Visual Clara
* Feedback Inmediato
* Buen contraste de colores para Accesibilidad


## Arquitectura de la información

<p align="center">
  <img src="https://i.postimg.cc/GmfNkk20/image-3.png" alt="Imagen 1" width="350"/>
  <br>
  <img src="https://i.postimg.cc/N0rnb59q/image-4.png" alt="Imagen 2" width="350"/>
  <br><br>
  <a href="https://whimsical.com/GTT4RKXKGvJMUkVdoTcEVg" target="_blank">
    <img src="https://img.shields.io/badge/Ver%20Diagramas-Click%20Aquí-blue?style=for-the-badge" alt="Ver Diagramas">
  </a>
</p>

## Librerias usadas con Angular

 ![@angular/localize](https://img.shields.io/badge/@angular%2Flocalize%20v20.3.0-EE2F2F?style=flat&logo=angular&logoColor=white) <br> Utilizado para generar una traducción al texto implementado en las vistas.

## Diseño de prototipos

<div align="center">

[![Figma](https://img.shields.io/badge/Figma-000000?style=flat&logo=figma&logoColor=white)](https://www.figma.com/design/1GNS37vGlElebS0W7YCuaH/WyM?node-id=48-324&t=DrgJfPm5505lGtZ7-1)  
</div>

## Tecnologías
<div align="center">

![Ionic](https://img.shields.io/badge/Ionic%20v8.0+-3880FF?style=flat&logo=ionic&logoColor=white)
[![Angular](https://img.shields.io/badge/Angular%20v15.0+-DD0031?style=flat&logo=angular&logoColor=white)](#)  
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS%20v4.0-06B6D4?style=flat&logo=tailwind-css&logoColor=white)](#)
</div>
