-- MySQL dump 10.13  Distrib 9.5.0, for macos26.0 (arm64)
--
-- Host: localhost    Database: acachat_db
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('6b6d8f2c24b2');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_files`
--

DROP TABLE IF EXISTS `course_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `filename` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `filepath` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `filesize` int NOT NULL,
  `mimetype` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uploaded_by` int NOT NULL,
  `uploaded_at` datetime NOT NULL,
  `parsed_content` text COLLATE utf8mb4_unicode_ci,
  `parsed_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  KEY `uploaded_by` (`uploaded_by`),
  CONSTRAINT `course_files_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `course_files_ibfk_2` FOREIGN KEY (`uploaded_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_files`
--

LOCK TABLES `course_files` WRITE;
/*!40000 ALTER TABLE `course_files` DISABLE KEYS */;
INSERT INTO `course_files` VALUES (1,1,'planificacion_matematicas-aplicadas-4to-medio.md','courses/1/planificacion_matematicas-aplicadas-4to-medio.md',822,'text/markdown',2,'2025-11-03 00:28:22','# Planificación semanal de Matemáticas Aplicadas\n\n**Institución:** Colegio Inglés de Quillota\n**Grado:** 4to Medio\n**Curso:** Matemáticas Aplicadas 4to Medio\n**Docente responsable:** Matias Diaz\n\n## Objetivos de la semana\n- Refuerzo de ejercicios tipo PAES y resolución de problemas contextualizados.\n- Promover el aprendizaje activo y colaborativo.\n- Evaluar avances a través de actividades formativas.\n\n## Actividades sugeridas\n1. Diagnóstico inicial para activar conocimientos previos.\n2. Desarrollo guiado con ejercicios de matemáticas aplicadas.\n3. Trabajo colaborativo en equipos heterogéneos.\n4. Cierre reflexivo con salida escrita breve.\n\n## Recursos para la semana\n- Pizarra digital y material audiovisual.\n- Cuaderno del estudiante y fichas de trabajo.\n- Plataforma ACAChat para consultas asíncronas.\n','2025-11-03 00:28:22'),(2,1,'guia_aprendizaje_matematicas-aplicadas-4to-medio.txt','courses/1/guia_aprendizaje_matematicas-aplicadas-4to-medio.txt',635,'text/plain',2,'2025-11-03 00:28:22','Guía de aprendizaje - Matemáticas Aplicadas 4to Medio\nInstitución: Colegio Inglés de Quillota\nGrado: 4to Medio\nDocente: Matias Diaz\n\nEsta guía acompaña la planificación semanal y se apoya en el chatbot del curso.\n\nInstrucciones para el estudiante:\n1. Revisa la planificación y marca los objetivos que dominas.\n2. Resuelve los ejercicios propuestos y valida tus respuestas con el chatbot.\n3. Anota dudas específicas para llevar a la clase presencial.\n4. Comparte un breve resumen de tu aprendizaje en el foro del curso.\n\nRecuerda que el chatbot usa este material como contexto, por lo que puedes referenciarlo en tus preguntas.','2025-11-03 00:28:22'),(3,2,'planificacion_lenguaje-y-comunicacion-4to-medio.md','courses/2/planificacion_lenguaje-y-comunicacion-4to-medio.md',843,'text/markdown',2,'2025-11-03 00:28:22','# Planificación semanal de Lenguaje y Comunicación\n\n**Institución:** Colegio Inglés de Quillota\n**Grado:** 4to Medio\n**Curso:** Lenguaje y Comunicación 4to Medio\n**Docente responsable:** Matias Diaz\n\n## Objetivos de la semana\n- Comprensión lectora avanzada, análisis de textos y preparación de ensayos argumentativos.\n- Promover el aprendizaje activo y colaborativo.\n- Evaluar avances a través de actividades formativas.\n\n## Actividades sugeridas\n1. Diagnóstico inicial para activar conocimientos previos.\n2. Desarrollo guiado con ejercicios de lenguaje y comunicación.\n3. Trabajo colaborativo en equipos heterogéneos.\n4. Cierre reflexivo con salida escrita breve.\n\n## Recursos para la semana\n- Pizarra digital y material audiovisual.\n- Cuaderno del estudiante y fichas de trabajo.\n- Plataforma ACAChat para consultas asíncronas.\n','2025-11-03 00:28:22'),(4,2,'guia_aprendizaje_lenguaje-y-comunicacion-4to-medio.txt','courses/2/guia_aprendizaje_lenguaje-y-comunicacion-4to-medio.txt',637,'text/plain',2,'2025-11-03 00:28:22','Guía de aprendizaje - Lenguaje y Comunicación 4to Medio\nInstitución: Colegio Inglés de Quillota\nGrado: 4to Medio\nDocente: Matias Diaz\n\nEsta guía acompaña la planificación semanal y se apoya en el chatbot del curso.\n\nInstrucciones para el estudiante:\n1. Revisa la planificación y marca los objetivos que dominas.\n2. Resuelve los ejercicios propuestos y valida tus respuestas con el chatbot.\n3. Anota dudas específicas para llevar a la clase presencial.\n4. Comparte un breve resumen de tu aprendizaje en el foro del curso.\n\nRecuerda que el chatbot usa este material como contexto, por lo que puedes referenciarlo en tus preguntas.','2025-11-03 00:28:22'),(5,3,'planificacion_historia-y-ciudadania-4to-medio.md','courses/3/planificacion_historia-y-ciudadania-4to-medio.md',818,'text/markdown',1,'2025-11-03 00:28:22','# Planificación semanal de Historia y Ciudadanía\n\n**Institución:** Colegio Inglés de Quillota\n**Grado:** 4to Medio\n**Curso:** Historia y Ciudadanía 4to Medio\n**Docente responsable:** Por asignar\n\n## Objetivos de la semana\n- Procesos históricos del siglo XX, ciudadanía activa y debate informado.\n- Promover el aprendizaje activo y colaborativo.\n- Evaluar avances a través de actividades formativas.\n\n## Actividades sugeridas\n1. Diagnóstico inicial para activar conocimientos previos.\n2. Desarrollo guiado con ejercicios de historia y ciudadanía.\n3. Trabajo colaborativo en equipos heterogéneos.\n4. Cierre reflexivo con salida escrita breve.\n\n## Recursos para la semana\n- Pizarra digital y material audiovisual.\n- Cuaderno del estudiante y fichas de trabajo.\n- Plataforma ACAChat para consultas asíncronas.\n','2025-11-03 00:28:22'),(6,3,'guia_aprendizaje_historia-y-ciudadania-4to-medio.txt','courses/3/guia_aprendizaje_historia-y-ciudadania-4to-medio.txt',635,'text/plain',1,'2025-11-03 00:28:22','Guía de aprendizaje - Historia y Ciudadanía 4to Medio\nInstitución: Colegio Inglés de Quillota\nGrado: 4to Medio\nDocente: Por asignar\n\nEsta guía acompaña la planificación semanal y se apoya en el chatbot del curso.\n\nInstrucciones para el estudiante:\n1. Revisa la planificación y marca los objetivos que dominas.\n2. Resuelve los ejercicios propuestos y valida tus respuestas con el chatbot.\n3. Anota dudas específicas para llevar a la clase presencial.\n4. Comparte un breve resumen de tu aprendizaje en el foro del curso.\n\nRecuerda que el chatbot usa este material como contexto, por lo que puedes referenciarlo en tus preguntas.','2025-11-03 00:28:22'),(7,4,'planificacion_matematicas-aplicadas-4to-medio.md','courses/4/planificacion_matematicas-aplicadas-4to-medio.md',828,'text/markdown',9,'2025-11-03 00:28:22','# Planificación semanal de Matemáticas Aplicadas\n\n**Institución:** Liceo Gastronomía y Turismo\n**Grado:** 4to Medio\n**Curso:** Matemáticas Aplicadas 4to Medio\n**Docente responsable:** Giovanni Ahumada\n\n## Objetivos de la semana\n- Refuerzo de ejercicios tipo PAES y resolución de problemas contextualizados.\n- Promover el aprendizaje activo y colaborativo.\n- Evaluar avances a través de actividades formativas.\n\n## Actividades sugeridas\n1. Diagnóstico inicial para activar conocimientos previos.\n2. Desarrollo guiado con ejercicios de matemáticas aplicadas.\n3. Trabajo colaborativo en equipos heterogéneos.\n4. Cierre reflexivo con salida escrita breve.\n\n## Recursos para la semana\n- Pizarra digital y material audiovisual.\n- Cuaderno del estudiante y fichas de trabajo.\n- Plataforma ACAChat para consultas asíncronas.\n','2025-11-03 00:28:22'),(8,4,'guia_aprendizaje_matematicas-aplicadas-4to-medio.txt','courses/4/guia_aprendizaje_matematicas-aplicadas-4to-medio.txt',641,'text/plain',9,'2025-11-03 00:28:22','Guía de aprendizaje - Matemáticas Aplicadas 4to Medio\nInstitución: Liceo Gastronomía y Turismo\nGrado: 4to Medio\nDocente: Giovanni Ahumada\n\nEsta guía acompaña la planificación semanal y se apoya en el chatbot del curso.\n\nInstrucciones para el estudiante:\n1. Revisa la planificación y marca los objetivos que dominas.\n2. Resuelve los ejercicios propuestos y valida tus respuestas con el chatbot.\n3. Anota dudas específicas para llevar a la clase presencial.\n4. Comparte un breve resumen de tu aprendizaje en el foro del curso.\n\nRecuerda que el chatbot usa este material como contexto, por lo que puedes referenciarlo en tus preguntas.','2025-11-03 00:28:22'),(9,5,'planificacion_lenguaje-y-comunicacion-4to-medio.md','courses/5/planificacion_lenguaje-y-comunicacion-4to-medio.md',849,'text/markdown',9,'2025-11-03 00:28:22','# Planificación semanal de Lenguaje y Comunicación\n\n**Institución:** Liceo Gastronomía y Turismo\n**Grado:** 4to Medio\n**Curso:** Lenguaje y Comunicación 4to Medio\n**Docente responsable:** Giovanni Ahumada\n\n## Objetivos de la semana\n- Comprensión lectora avanzada, análisis de textos y preparación de ensayos argumentativos.\n- Promover el aprendizaje activo y colaborativo.\n- Evaluar avances a través de actividades formativas.\n\n## Actividades sugeridas\n1. Diagnóstico inicial para activar conocimientos previos.\n2. Desarrollo guiado con ejercicios de lenguaje y comunicación.\n3. Trabajo colaborativo en equipos heterogéneos.\n4. Cierre reflexivo con salida escrita breve.\n\n## Recursos para la semana\n- Pizarra digital y material audiovisual.\n- Cuaderno del estudiante y fichas de trabajo.\n- Plataforma ACAChat para consultas asíncronas.\n','2025-11-03 00:28:22'),(10,5,'guia_aprendizaje_lenguaje-y-comunicacion-4to-medio.txt','courses/5/guia_aprendizaje_lenguaje-y-comunicacion-4to-medio.txt',643,'text/plain',9,'2025-11-03 00:28:22','Guía de aprendizaje - Lenguaje y Comunicación 4to Medio\nInstitución: Liceo Gastronomía y Turismo\nGrado: 4to Medio\nDocente: Giovanni Ahumada\n\nEsta guía acompaña la planificación semanal y se apoya en el chatbot del curso.\n\nInstrucciones para el estudiante:\n1. Revisa la planificación y marca los objetivos que dominas.\n2. Resuelve los ejercicios propuestos y valida tus respuestas con el chatbot.\n3. Anota dudas específicas para llevar a la clase presencial.\n4. Comparte un breve resumen de tu aprendizaje en el foro del curso.\n\nRecuerda que el chatbot usa este material como contexto, por lo que puedes referenciarlo en tus preguntas.','2025-11-03 00:28:22'),(11,6,'planificacion_historia-y-ciudadania-4to-medio.md','courses/6/planificacion_historia-y-ciudadania-4to-medio.md',819,'text/markdown',8,'2025-11-03 00:28:22','# Planificación semanal de Historia y Ciudadanía\n\n**Institución:** Liceo Gastronomía y Turismo\n**Grado:** 4to Medio\n**Curso:** Historia y Ciudadanía 4to Medio\n**Docente responsable:** Por asignar\n\n## Objetivos de la semana\n- Procesos históricos del siglo XX, ciudadanía activa y debate informado.\n- Promover el aprendizaje activo y colaborativo.\n- Evaluar avances a través de actividades formativas.\n\n## Actividades sugeridas\n1. Diagnóstico inicial para activar conocimientos previos.\n2. Desarrollo guiado con ejercicios de historia y ciudadanía.\n3. Trabajo colaborativo en equipos heterogéneos.\n4. Cierre reflexivo con salida escrita breve.\n\n## Recursos para la semana\n- Pizarra digital y material audiovisual.\n- Cuaderno del estudiante y fichas de trabajo.\n- Plataforma ACAChat para consultas asíncronas.\n','2025-11-03 00:28:22'),(12,6,'guia_aprendizaje_historia-y-ciudadania-4to-medio.txt','courses/6/guia_aprendizaje_historia-y-ciudadania-4to-medio.txt',636,'text/plain',8,'2025-11-03 00:28:22','Guía de aprendizaje - Historia y Ciudadanía 4to Medio\nInstitución: Liceo Gastronomía y Turismo\nGrado: 4to Medio\nDocente: Por asignar\n\nEsta guía acompaña la planificación semanal y se apoya en el chatbot del curso.\n\nInstrucciones para el estudiante:\n1. Revisa la planificación y marca los objetivos que dominas.\n2. Resuelve los ejercicios propuestos y valida tus respuestas con el chatbot.\n3. Anota dudas específicas para llevar a la clase presencial.\n4. Comparte un breve resumen de tu aprendizaje en el foro del curso.\n\nRecuerda que el chatbot usa este material como contexto, por lo que puedes referenciarlo en tus preguntas.','2025-11-03 00:28:22'),(13,7,'planificacion_matematicas-aplicadas-4to-medio.md','courses/7/planificacion_matematicas-aplicadas-4to-medio.md',824,'text/markdown',16,'2025-11-03 00:28:22','# Planificación semanal de Matemáticas Aplicadas\n\n**Institución:** Instituto Rafael Ariztía\n**Grado:** 4to Medio\n**Curso:** Matemáticas Aplicadas 4to Medio\n**Docente responsable:** Daniel Saavedra\n\n## Objetivos de la semana\n- Refuerzo de ejercicios tipo PAES y resolución de problemas contextualizados.\n- Promover el aprendizaje activo y colaborativo.\n- Evaluar avances a través de actividades formativas.\n\n## Actividades sugeridas\n1. Diagnóstico inicial para activar conocimientos previos.\n2. Desarrollo guiado con ejercicios de matemáticas aplicadas.\n3. Trabajo colaborativo en equipos heterogéneos.\n4. Cierre reflexivo con salida escrita breve.\n\n## Recursos para la semana\n- Pizarra digital y material audiovisual.\n- Cuaderno del estudiante y fichas de trabajo.\n- Plataforma ACAChat para consultas asíncronas.\n','2025-11-03 00:28:22'),(14,7,'guia_aprendizaje_matematicas-aplicadas-4to-medio.txt','courses/7/guia_aprendizaje_matematicas-aplicadas-4to-medio.txt',637,'text/plain',16,'2025-11-03 00:28:22','Guía de aprendizaje - Matemáticas Aplicadas 4to Medio\nInstitución: Instituto Rafael Ariztía\nGrado: 4to Medio\nDocente: Daniel Saavedra\n\nEsta guía acompaña la planificación semanal y se apoya en el chatbot del curso.\n\nInstrucciones para el estudiante:\n1. Revisa la planificación y marca los objetivos que dominas.\n2. Resuelve los ejercicios propuestos y valida tus respuestas con el chatbot.\n3. Anota dudas específicas para llevar a la clase presencial.\n4. Comparte un breve resumen de tu aprendizaje en el foro del curso.\n\nRecuerda que el chatbot usa este material como contexto, por lo que puedes referenciarlo en tus preguntas.','2025-11-03 00:28:22'),(15,8,'planificacion_lenguaje-y-comunicacion-4to-medio.md','courses/8/planificacion_lenguaje-y-comunicacion-4to-medio.md',845,'text/markdown',16,'2025-11-03 00:28:22','# Planificación semanal de Lenguaje y Comunicación\n\n**Institución:** Instituto Rafael Ariztía\n**Grado:** 4to Medio\n**Curso:** Lenguaje y Comunicación 4to Medio\n**Docente responsable:** Daniel Saavedra\n\n## Objetivos de la semana\n- Comprensión lectora avanzada, análisis de textos y preparación de ensayos argumentativos.\n- Promover el aprendizaje activo y colaborativo.\n- Evaluar avances a través de actividades formativas.\n\n## Actividades sugeridas\n1. Diagnóstico inicial para activar conocimientos previos.\n2. Desarrollo guiado con ejercicios de lenguaje y comunicación.\n3. Trabajo colaborativo en equipos heterogéneos.\n4. Cierre reflexivo con salida escrita breve.\n\n## Recursos para la semana\n- Pizarra digital y material audiovisual.\n- Cuaderno del estudiante y fichas de trabajo.\n- Plataforma ACAChat para consultas asíncronas.\n','2025-11-03 00:28:22'),(16,8,'guia_aprendizaje_lenguaje-y-comunicacion-4to-medio.txt','courses/8/guia_aprendizaje_lenguaje-y-comunicacion-4to-medio.txt',639,'text/plain',16,'2025-11-03 00:28:22','Guía de aprendizaje - Lenguaje y Comunicación 4to Medio\nInstitución: Instituto Rafael Ariztía\nGrado: 4to Medio\nDocente: Daniel Saavedra\n\nEsta guía acompaña la planificación semanal y se apoya en el chatbot del curso.\n\nInstrucciones para el estudiante:\n1. Revisa la planificación y marca los objetivos que dominas.\n2. Resuelve los ejercicios propuestos y valida tus respuestas con el chatbot.\n3. Anota dudas específicas para llevar a la clase presencial.\n4. Comparte un breve resumen de tu aprendizaje en el foro del curso.\n\nRecuerda que el chatbot usa este material como contexto, por lo que puedes referenciarlo en tus preguntas.','2025-11-03 00:28:22'),(17,9,'planificacion_historia-y-ciudadania-4to-medio.md','courses/9/planificacion_historia-y-ciudadania-4to-medio.md',816,'text/markdown',15,'2025-11-03 00:28:22','# Planificación semanal de Historia y Ciudadanía\n\n**Institución:** Instituto Rafael Ariztía\n**Grado:** 4to Medio\n**Curso:** Historia y Ciudadanía 4to Medio\n**Docente responsable:** Por asignar\n\n## Objetivos de la semana\n- Procesos históricos del siglo XX, ciudadanía activa y debate informado.\n- Promover el aprendizaje activo y colaborativo.\n- Evaluar avances a través de actividades formativas.\n\n## Actividades sugeridas\n1. Diagnóstico inicial para activar conocimientos previos.\n2. Desarrollo guiado con ejercicios de historia y ciudadanía.\n3. Trabajo colaborativo en equipos heterogéneos.\n4. Cierre reflexivo con salida escrita breve.\n\n## Recursos para la semana\n- Pizarra digital y material audiovisual.\n- Cuaderno del estudiante y fichas de trabajo.\n- Plataforma ACAChat para consultas asíncronas.\n','2025-11-03 00:28:22'),(18,9,'guia_aprendizaje_historia-y-ciudadania-4to-medio.txt','courses/9/guia_aprendizaje_historia-y-ciudadania-4to-medio.txt',633,'text/plain',15,'2025-11-03 00:28:22','Guía de aprendizaje - Historia y Ciudadanía 4to Medio\nInstitución: Instituto Rafael Ariztía\nGrado: 4to Medio\nDocente: Por asignar\n\nEsta guía acompaña la planificación semanal y se apoya en el chatbot del curso.\n\nInstrucciones para el estudiante:\n1. Revisa la planificación y marca los objetivos que dominas.\n2. Resuelve los ejercicios propuestos y valida tus respuestas con el chatbot.\n3. Anota dudas específicas para llevar a la clase presencial.\n4. Comparte un breve resumen de tu aprendizaje en el foro del curso.\n\nRecuerda que el chatbot usa este material como contexto, por lo que puedes referenciarlo en tus preguntas.','2025-11-03 00:28:22');
/*!40000 ALTER TABLE `course_files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `prompt` text COLLATE utf8mb4_unicode_ci,
  `institution_id` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `grade_id` int NOT NULL,
  `emoji` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `institution_id` (`institution_id`),
  KEY `ix_courses_grade_id` (`grade_id`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`institution_id`) REFERENCES `institutions` (`id`),
  CONSTRAINT `courses_ibfk_2` FOREIGN KEY (`grade_id`) REFERENCES `grades` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'Matemáticas Aplicadas 4to Medio','Eres el docente de Matemáticas Aplicadas 4to Medio en Colegio Inglés de Quillota. Refuerzo de ejercicios tipo PAES y resolución de problemas contextualizados. Mantén un tono cercano y coherente con el sello del establecimiento.',1,'2025-11-03 00:28:22','2025-11-03 00:28:22',1,12,'📘'),(2,'Lenguaje y Comunicación 4to Medio','Eres el docente de Lenguaje y Comunicación 4to Medio en Colegio Inglés de Quillota. Comprensión lectora avanzada, análisis de textos y preparación de ensayos argumentativos. Mantén un tono cercano y coherente con el sello del establecimiento.',1,'2025-11-03 00:28:22','2025-11-03 00:28:22',1,12,'📘'),(3,'Historia y Ciudadanía 4to Medio','Eres el docente de Historia y Ciudadanía 4to Medio en Colegio Inglés de Quillota. Procesos históricos del siglo XX, ciudadanía activa y debate informado. Mantén un tono cercano y coherente con el sello del establecimiento.',1,'2025-11-03 00:28:22','2025-11-03 00:28:22',1,12,'📘'),(4,'Matemáticas Aplicadas 4to Medio','Eres el docente de Matemáticas Aplicadas 4to Medio en Liceo Gastronomía y Turismo. Refuerzo de ejercicios tipo PAES y resolución de problemas contextualizados. Mantén un tono cercano y coherente con el sello del establecimiento.',2,'2025-11-03 00:28:22','2025-11-03 00:28:22',1,12,'📘'),(5,'Lenguaje y Comunicación 4to Medio','Eres el docente de Lenguaje y Comunicación 4to Medio en Liceo Gastronomía y Turismo. Comprensión lectora avanzada, análisis de textos y preparación de ensayos argumentativos. Mantén un tono cercano y coherente con el sello del establecimiento.',2,'2025-11-03 00:28:22','2025-11-03 00:28:22',1,12,'📘'),(6,'Historia y Ciudadanía 4to Medio','Eres el docente de Historia y Ciudadanía 4to Medio en Liceo Gastronomía y Turismo. Procesos históricos del siglo XX, ciudadanía activa y debate informado. Mantén un tono cercano y coherente con el sello del establecimiento.',2,'2025-11-03 00:28:22','2025-11-03 00:28:22',1,12,'📘'),(7,'Matemáticas Aplicadas 4to Medio','Eres el docente de Matemáticas Aplicadas 4to Medio en Instituto Rafael Ariztía. Refuerzo de ejercicios tipo PAES y resolución de problemas contextualizados. Mantén un tono cercano y coherente con el sello del establecimiento.',3,'2025-11-03 00:28:22','2025-11-03 00:28:22',1,12,'📘'),(8,'Lenguaje y Comunicación 4to Medio','Eres el docente de Lenguaje y Comunicación 4to Medio en Instituto Rafael Ariztía. Comprensión lectora avanzada, análisis de textos y preparación de ensayos argumentativos. Mantén un tono cercano y coherente con el sello del establecimiento.',3,'2025-11-03 00:28:22','2025-11-03 00:28:22',1,12,'📘'),(9,'Historia y Ciudadanía 4to Medio','Eres el docente de Historia y Ciudadanía 4to Medio en Instituto Rafael Ariztía. Procesos históricos del siglo XX, ciudadanía activa y debate informado. Mantén un tono cercano y coherente con el sello del establecimiento.',3,'2025-11-03 00:28:22','2025-11-03 00:28:22',1,12,'📘');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grades`
--

DROP TABLE IF EXISTS `grades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_grades_name` (`name`),
  UNIQUE KEY `ix_grades_order` (`order`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades`
--

LOCK TABLES `grades` WRITE;
/*!40000 ALTER TABLE `grades` DISABLE KEYS */;
INSERT INTO `grades` VALUES (1,'1ro Básico',1,'2025-11-03 00:28:17','2025-11-03 00:28:17'),(2,'2do Básico',2,'2025-11-03 00:28:17','2025-11-03 00:28:17'),(3,'3ro Básico',3,'2025-11-03 00:28:17','2025-11-03 00:28:17'),(4,'4to Básico',4,'2025-11-03 00:28:17','2025-11-03 00:28:17'),(5,'5to Básico',5,'2025-11-03 00:28:17','2025-11-03 00:28:17'),(6,'6to Básico',6,'2025-11-03 00:28:17','2025-11-03 00:28:17'),(7,'7mo Básico',7,'2025-11-03 00:28:17','2025-11-03 00:28:17'),(8,'8vo Básico',8,'2025-11-03 00:28:17','2025-11-03 00:28:17'),(9,'1ro Medio',9,'2025-11-03 00:28:17','2025-11-03 00:28:17'),(10,'2do Medio',10,'2025-11-03 00:28:17','2025-11-03 00:28:17'),(11,'3ro Medio',11,'2025-11-03 00:28:17','2025-11-03 00:28:17'),(12,'4to Medio',12,'2025-11-03 00:28:17','2025-11-03 00:28:17');
/*!40000 ALTER TABLE `grades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `institutions`
--

DROP TABLE IF EXISTS `institutions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `institutions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `direccion` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fundacion` date DEFAULT NULL,
  `paginaweb` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `logotipo` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `colorinstitucional` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `institutions`
--

LOCK TABLES `institutions` WRITE;
/*!40000 ALTER TABLE `institutions` DISABLE KEYS */;
INSERT INTO `institutions` VALUES (1,'Colegio Inglés de Quillota','José Miguel Carrera 550, Quillota','1933-05-16','https://colegioinglesquillota.cl/','institutions/logos/ingles.png','#43569c','2025-11-03 00:28:17','2025-11-03 00:28:17'),(2,'Liceo Gastronomía y Turismo','Diaguitas 1751, Quilpué','2003-03-03','https://liceogastronomiayturismo.webescuela.cl/','institutions/logos/lgt.png','#69b1ab','2025-11-03 00:28:19','2025-11-03 00:28:19'),(3,'Instituto Rafael Ariztía','O\"Higgins 500, Quillota','1914-03-08','https://www.ira.maristas.cl/','institutions/logos/ira.png','#111d5c','2025-11-03 00:28:21','2025-11-03 00:28:21');
/*!40000 ALTER TABLE `institutions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_courses`
--

DROP TABLE IF EXISTS `user_courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `course_id` int NOT NULL,
  `year` int NOT NULL,
  `role_in_course` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `enrolled_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_course_year` (`user_id`,`course_id`,`year`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `user_courses_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `user_courses_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_courses`
--

LOCK TABLES `user_courses` WRITE;
/*!40000 ALTER TABLE `user_courses` DISABLE KEYS */;
INSERT INTO `user_courses` VALUES (1,2,1,2025,'teacher','2025-11-03 00:28:22'),(2,3,1,2025,'student','2025-11-03 00:28:22'),(3,4,1,2025,'student','2025-11-03 00:28:22'),(4,5,1,2025,'student','2025-11-03 00:28:22'),(5,6,1,2025,'student','2025-11-03 00:28:22'),(6,7,1,2025,'student','2025-11-03 00:28:22'),(7,2,2,2025,'teacher','2025-11-03 00:28:22'),(8,3,2,2025,'student','2025-11-03 00:28:22'),(9,4,2,2025,'student','2025-11-03 00:28:22'),(10,5,2,2025,'student','2025-11-03 00:28:22'),(11,6,2,2025,'student','2025-11-03 00:28:22'),(12,7,2,2025,'student','2025-11-03 00:28:22'),(13,3,3,2025,'student','2025-11-03 00:28:22'),(14,4,3,2025,'student','2025-11-03 00:28:22'),(15,5,3,2025,'student','2025-11-03 00:28:22'),(16,6,3,2025,'student','2025-11-03 00:28:22'),(17,7,3,2025,'student','2025-11-03 00:28:22'),(18,9,4,2025,'teacher','2025-11-03 00:28:22'),(19,10,4,2025,'student','2025-11-03 00:28:22'),(20,11,4,2025,'student','2025-11-03 00:28:22'),(21,12,4,2025,'student','2025-11-03 00:28:22'),(22,13,4,2025,'student','2025-11-03 00:28:22'),(23,14,4,2025,'student','2025-11-03 00:28:22'),(24,9,5,2025,'teacher','2025-11-03 00:28:22'),(25,10,5,2025,'student','2025-11-03 00:28:22'),(26,11,5,2025,'student','2025-11-03 00:28:22'),(27,12,5,2025,'student','2025-11-03 00:28:22'),(28,13,5,2025,'student','2025-11-03 00:28:22'),(29,14,5,2025,'student','2025-11-03 00:28:22'),(30,10,6,2025,'student','2025-11-03 00:28:22'),(31,11,6,2025,'student','2025-11-03 00:28:22'),(32,12,6,2025,'student','2025-11-03 00:28:22'),(33,13,6,2025,'student','2025-11-03 00:28:22'),(34,14,6,2025,'student','2025-11-03 00:28:22'),(35,16,7,2025,'teacher','2025-11-03 00:28:22'),(36,17,7,2025,'student','2025-11-03 00:28:22'),(37,18,7,2025,'student','2025-11-03 00:28:22'),(38,19,7,2025,'student','2025-11-03 00:28:22'),(39,20,7,2025,'student','2025-11-03 00:28:22'),(40,21,7,2025,'student','2025-11-03 00:28:22'),(41,16,8,2025,'teacher','2025-11-03 00:28:22'),(42,17,8,2025,'student','2025-11-03 00:28:22'),(43,18,8,2025,'student','2025-11-03 00:28:22'),(44,19,8,2025,'student','2025-11-03 00:28:22'),(45,20,8,2025,'student','2025-11-03 00:28:22'),(46,21,8,2025,'student','2025-11-03 00:28:22'),(47,17,9,2025,'student','2025-11-03 00:28:22'),(48,18,9,2025,'student','2025-11-03 00:28:22'),(49,19,9,2025,'student','2025-11-03 00:28:22'),(50,20,9,2025,'student','2025-11-03 00:28:22'),(51,21,9,2025,'student','2025-11-03 00:28:22');
/*!40000 ALTER TABLE `user_courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rut` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `region` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `comuna` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `institution_id` int DEFAULT NULL,
  `grade_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_rut` (`rut`),
  UNIQUE KEY `ix_users_username` (`username`),
  KEY `ix_users_role` (`role`),
  KEY `ix_users_grade_id` (`grade_id`),
  KEY `ix_users_institution_id` (`institution_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`institution_id`) REFERENCES `institutions` (`id`),
  CONSTRAINT `users_ibfk_2` FOREIGN KEY (`grade_id`) REFERENCES `grades` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'22038002-5','Matias Diaz','matias.diaz.c01@mail.pucv.cl','Valparaíso','Quillota','$2b$12$S5vaikQ1dTNSX5PQ060fte3xA.knYhRixTxxZcjIub9c4God4NauC','2025-11-03 00:28:17','2025-11-03 00:28:17',1,'admin',1,NULL),(2,'11111111-1','Matias Diaz (Profesor)','matias.diaz@colegioinglesquillota.cl','Valparaíso','Quillota','$2b$12$gDZaVAxWWLHV5/Da7hDz0evUAZLc.8UVvYS9iB5iNU7Ytkh5zOrdS','2025-11-03 00:28:17','2025-11-03 00:28:17',1,'teacher',1,NULL),(3,'01.000.011-2','Alumno Falso 1 Quillota','alumno1@inglesquillota.cl','Valparaíso','Comuna Falsa','$2b$12$fY1pa//IOkXtnbSRqVvxBedFQP3WaiWvj7DCONDMGlLj5t/KTO8tC','2025-11-03 00:28:18','2025-11-03 00:28:18',1,'student',1,12),(4,'01.000.021-3','Alumno Falso 2 Quillota','alumno2@inglesquillota.cl','Valparaíso','Comuna Falsa','$2b$12$ngJeaYNFC7kBrwvabj6s1uzQkRamTF5NpNdwT1LUv/M5GF6Isutxq','2025-11-03 00:28:18','2025-11-03 00:28:18',1,'student',1,12),(5,'01.000.031-4','Alumno Falso 3 Quillota','alumno3@inglesquillota.cl','Valparaíso','Comuna Falsa','$2b$12$n905Oq6rkLOcA4qftULOke0d5NfQWCsxkPH/judUMPtOdlZF/V3nG','2025-11-03 00:28:18','2025-11-03 00:28:18',1,'student',1,12),(6,'01.000.041-5','Alumno Falso 4 Quillota','alumno4@inglesquillota.cl','Valparaíso','Comuna Falsa','$2b$12$sqq5kJCQXxHFyYVvxn7T7.pf1EhoYKzzZuXqSIYmhQcG1Sqshng0W','2025-11-03 00:28:18','2025-11-03 00:28:18',1,'student',1,12),(7,'01.000.051-6','Alumno Falso 5 Quillota','alumno5@inglesquillota.cl','Valparaíso','Comuna Falsa','$2b$12$QcnyD842gM3ZeykJHnYv0.M7m0r50kU/h8PcpfIoTsUHyc63pNfWq','2025-11-03 00:28:19','2025-11-03 00:28:19',1,'student',1,12),(8,'21523921-7','Giovanni Ahumada','giovanni.ahumada.t@mail.pucv.cl','Valparaíso','Quilpué','$2b$12$fhKwFj.X/dnLHIsFBJAS2.pV33mlSHu/PE5OoLYuCDjwBSB0XV4cG','2025-11-03 00:28:19','2025-11-03 00:28:19',1,'admin',2,NULL),(9,'22222222-2','Giovanni Ahumada (Profesor)','giovanni.ahumada@lgt.cl','Valparaíso','Quilpué','$2b$12$UkmbkP9urqJYYgXUHPyd8Otikv.8ttDAL6seH0xl29Spo99Hg8Hom','2025-11-03 00:28:19','2025-11-03 00:28:19',1,'teacher',2,NULL),(10,'02.000.012-3','Alumno Falso 1 Turismo','alumno1@turismo.cl','Valparaíso','Comuna Falsa','$2b$12$T4kqGno7Ykabh3dBg5q0F.Y8yjDLmcfmZLIyD.kGbqJPmtkj0jST2','2025-11-03 00:28:19','2025-11-03 00:28:19',1,'student',2,12),(11,'02.000.022-4','Alumno Falso 2 Turismo','alumno2@turismo.cl','Valparaíso','Comuna Falsa','$2b$12$/XV83qIk1S7Vxh1oifW94umqYaVsjFVNmG8f84E7KgWPOLxAujmR6','2025-11-03 00:28:20','2025-11-03 00:28:20',1,'student',2,12),(12,'02.000.032-5','Alumno Falso 3 Turismo','alumno3@turismo.cl','Valparaíso','Comuna Falsa','$2b$12$F6YTb2LB6t90JIEW1MMMwObcp1raOHZP/ls9cTS18FvlrT4UHWXRm','2025-11-03 00:28:20','2025-11-03 00:28:20',1,'student',2,12),(13,'02.000.042-6','Alumno Falso 4 Turismo','alumno4@turismo.cl','Valparaíso','Comuna Falsa','$2b$12$huqmyNNKoRvSrrTMXcdxT.ujdrUOBxHHezbm/Zj4Y9F/3mFGzxKkG','2025-11-03 00:28:20','2025-11-03 00:28:20',1,'student',2,12),(14,'02.000.052-7','Alumno Falso 5 Turismo','alumno5@turismo.cl','Valparaíso','Comuna Falsa','$2b$12$e9wHIRY6hCzSiNm0HMHCyOTE.N8ihw1Qy2CB83r5v2hxW28YW0Bq.','2025-11-03 00:28:21','2025-11-03 00:28:21',1,'student',2,12),(15,'21219402-6','Daniel Saavedra','daniel.saavedra.e@mail.pucv.cl','Valparaíso','Quillota','$2b$12$0.sqbV9LnzaeKiKBX1sN..e.C9hKhW5EM3/2ll1EKgLDtydjlrm/W','2025-11-03 00:28:21','2025-11-03 00:28:21',1,'admin',3,NULL),(16,'33333333-3','Daniel Saavedra (Profesor)','daniel.saavedra@ira.cl','Valparaíso','Quillota','$2b$12$YvsubFCOHeWPD0zcdNpBP.4NG0Z4UIAFqbfT4N690RCKDIPm06Fwq','2025-11-03 00:28:21','2025-11-03 00:28:21',1,'teacher',3,NULL),(17,'03.000.013-4','Alumno Falso 1 Ariztía','alumno1@maristas.cl','Valparaíso','Comuna Falsa','$2b$12$G91UbKI8yzjNSFeud9ge2uuHUB4cqu6z4t8QOAdF79urh2iCPzUrG','2025-11-03 00:28:21','2025-11-03 00:28:21',1,'student',3,12),(18,'03.000.023-5','Alumno Falso 2 Ariztía','alumno2@maristas.cl','Valparaíso','Comuna Falsa','$2b$12$U2ZgY/o/qMQfrQ5dCS9/fu7bT7jY8kFrNwdlO1Eeydfd.Rm7tHC5O','2025-11-03 00:28:22','2025-11-03 00:28:22',1,'student',3,12),(19,'03.000.033-6','Alumno Falso 3 Ariztía','alumno3@maristas.cl','Valparaíso','Comuna Falsa','$2b$12$UpyUeAN2pXKt1HkEJao7rebb.kBesIRz4zE4NMLU0mmmHnuDDLD3W','2025-11-03 00:28:22','2025-11-03 00:28:22',1,'student',3,12),(20,'03.000.043-7','Alumno Falso 4 Ariztía','alumno4@maristas.cl','Valparaíso','Comuna Falsa','$2b$12$9W2ihq532e/jFn.Ove8qOOLAyPuxSEPAFe3gdEV4PMQhCtjrdjgwu','2025-11-03 00:28:22','2025-11-03 00:28:22',1,'student',3,12),(21,'03.000.053-8','Alumno Falso 5 Ariztía','alumno5@maristas.cl','Valparaíso','Comuna Falsa','$2b$12$LR6IAKqvb8vdxwapMHG9f.pNIK4KTr8PBUXiHNPKjvcVFdGOUgXu.','2025-11-03 00:28:22','2025-11-03 00:28:22',1,'student',3,12);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 21:54:50
