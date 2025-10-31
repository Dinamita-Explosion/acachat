-- MySQL dump 10.13  Distrib 9.5.0, for macos26.0 (arm64)
--
-- Host: localhost    Database: acachat_db
-- ------------------------------------------------------
-- Server version	9.4.0

-- Contraseña de giovanni: Admin1234

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
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `filename` varchar(255) NOT NULL,
  `filepath` varchar(500) NOT NULL,
  `filesize` int NOT NULL,
  `mimetype` varchar(100) NOT NULL,
  `uploaded_by` int NOT NULL,
  `uploaded_at` datetime NOT NULL,
  `parsed_content` text,
  `parsed_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  KEY `uploaded_by` (`uploaded_by`),
  CONSTRAINT `course_files_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `course_files_ibfk_2` FOREIGN KEY (`uploaded_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_files`
--

LOCK TABLES `course_files` WRITE;
/*!40000 ALTER TABLE `course_files` DISABLE KEYS */;
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
  `nombre` varchar(200) NOT NULL,
  `prompt` text,
  `institution_id` int NOT NULL,
  `grade_id` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `emoji` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `institution_id` (`institution_id`),
  KEY `ix_courses_grade_id` (`grade_id`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`institution_id`) REFERENCES `institutions` (`id`),
  CONSTRAINT `courses_ibfk_2` FOREIGN KEY (`grade_id`) REFERENCES `grades` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'Matemáticas 4° Medio','Curso de matemáticas avanzadas para cuarto año medio. Incluye cálculo, álgebra avanzada y estadística.',1,12,'2025-10-29 02:47:58','2025-10-29 02:47:58',1,'📘'),(2,'Historia y Ciencias Sociales 3° Medio','Historia de Chile y América Latina en el contexto mundial. Análisis de procesos históricos contemporáneos.',1,11,'2025-10-29 02:47:58','2025-10-29 02:47:58',1,'📘'),(3,'Física 4° Medio','Física avanzada con énfasis en mecánica cuántica y termodinámica.',1,12,'2025-10-29 02:47:58','2025-10-29 02:47:58',1,'📘'),(4,'Lenguaje y Comunicación ','Contesta amablemente a todo',2,12,'2025-10-29 14:21:09','2025-10-29 14:21:09',1,'📘');
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
  `name` varchar(50) NOT NULL,
  `order` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_grades_order` (`order`),
  UNIQUE KEY `ix_grades_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades`
--

LOCK TABLES `grades` WRITE;
/*!40000 ALTER TABLE `grades` DISABLE KEYS */;
INSERT INTO `grades` VALUES (1,'1ro Básico',1,'2025-10-29 02:47:56','2025-10-29 02:47:56'),(2,'2do Básico',2,'2025-10-29 02:47:56','2025-10-29 02:47:56'),(3,'3ro Básico',3,'2025-10-29 02:47:56','2025-10-29 02:47:56'),(4,'4to Básico',4,'2025-10-29 02:47:56','2025-10-29 02:47:56'),(5,'5to Básico',5,'2025-10-29 02:47:56','2025-10-29 02:47:56'),(6,'6to Básico',6,'2025-10-29 02:47:56','2025-10-29 02:47:56'),(7,'7mo Básico',7,'2025-10-29 02:47:56','2025-10-29 02:47:56'),(8,'8vo Básico',8,'2025-10-29 02:47:56','2025-10-29 02:47:56'),(9,'1ro Medio',9,'2025-10-29 02:47:56','2025-10-29 02:47:56'),(10,'2do Medio',10,'2025-10-29 02:47:56','2025-10-29 02:47:56'),(11,'3ro Medio',11,'2025-10-29 02:47:56','2025-10-29 02:47:56'),(12,'4to Medio',12,'2025-10-29 02:47:56','2025-10-29 02:47:56');
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
  `nombre` varchar(200) NOT NULL,
  `direccion` varchar(300) DEFAULT NULL,
  `fundacion` date DEFAULT NULL,
  `paginaweb` varchar(200) DEFAULT NULL,
  `logotipo` varchar(500) DEFAULT NULL,
  `colorinstitucional` varchar(7) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `institutions`
--

LOCK TABLES `institutions` WRITE;
/*!40000 ALTER TABLE `institutions` DISABLE KEYS */;
INSERT INTO `institutions` VALUES (1,'Instituto Nacional','Arturo Prat 33, Santiago, Región Metropolitana','1813-08-10','https://www.institutonacional.cl',NULL,'#003DA5','2025-10-29 02:47:57','2025-10-29 02:47:57'),(2,'Liceo Gastronomia y Turismo','Diaguitas','2002-03-03','https://lgt.cl','institutions/logos/d1369c7343a942f5b4a5edbd72523695.png','#0042aa','2025-10-29 03:24:31','2025-10-29 14:54:29');
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
  `role_in_course` varchar(20) NOT NULL,
  `enrolled_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_course_year` (`user_id`,`course_id`,`year`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `user_courses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_courses_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_courses`
--

LOCK TABLES `user_courses` WRITE;
/*!40000 ALTER TABLE `user_courses` DISABLE KEYS */;
INSERT INTO `user_courses` VALUES (1,2,1,2025,'teacher','2025-10-29 02:47:58'),(2,3,2,2025,'teacher','2025-10-29 02:47:58'),(3,4,1,2025,'student','2025-10-29 02:47:58'),(4,4,2,2025,'student','2025-10-29 02:47:58'),(5,5,1,2025,'student','2025-10-29 02:47:58'),(6,5,2,2025,'student','2025-10-29 02:47:58'),(7,6,1,2025,'student','2025-10-29 02:47:58'),(8,6,2,2025,'student','2025-10-29 02:47:58'),(9,1,4,2025,'teacher','2025-10-29 14:21:30');
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
  `rut` varchar(12) NOT NULL,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `region` varchar(100) NOT NULL,
  `comuna` varchar(100) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `role` varchar(20) NOT NULL,
  `institution_id` int DEFAULT NULL,
  `grade_id` int DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_rut` (`rut`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`),
  KEY `ix_users_institution_id` (`institution_id`),
  KEY `ix_users_role` (`role`),
  KEY `ix_users_grade_id` (`grade_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`institution_id`) REFERENCES `institutions` (`id`),
  CONSTRAINT `users_ibfk_2` FOREIGN KEY (`grade_id`) REFERENCES `grades` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'11111111-1','Giovanni Ahumada','giovanni.ahumada.t@gmail.com','Metropolitana','Santiago','$2b$12$gY8lj4cReoUff2Y/XnPhAuyXEGMwFOyzwch7/Z98X8OOTN7xAQVDu','admin',2,NULL,'2025-10-29 02:47:57','2025-10-29 03:33:25',1),(2,'12345678-5','Profesor Matemáticas','profesor.matematicas@institutonacional.cl','Metropolitana','Santiago','$2b$12$tx8atJsWcHjju0UEbcXejuJrrq5DVDzzP9PuIDmrqt.A53AiJJ79G','teacher',1,12,'2025-10-29 02:47:57','2025-10-29 02:47:57',1),(3,'23456789-6','Profesora Historia','profesora.historia@institutonacional.cl','Metropolitana','Santiago','$2b$12$5jFLsvjxhaIoLycxEHY/p.C7vICLqBn60a28f3Bjq.CDR4PVEqKUS','teacher',1,11,'2025-10-29 02:47:57','2025-10-29 02:47:57',1),(4,'20111222-3','Juan Pérez','juan.perez@estudiante.cl','Metropolitana','Santiago','$2b$12$ilhTXonXEOEltg/8gbhLEO09JRma6qwwooaEF/1kWt6/v9ZUYevQe','student',1,12,'2025-10-29 02:47:57','2025-10-29 02:47:57',1),(5,'20222333-4','María González','maria.gonzalez@estudiante.cl','Metropolitana','Providencia','$2b$12$1Yeztq72X8izopcBti81OOWlqD.PlqlMsrQ9dgjv5AJadQcGrZUt6','student',1,12,'2025-10-29 02:47:58','2025-10-29 02:47:58',1),(6,'20333444-5','Pedro Silva','pedro.silva@estudiante.cl','Metropolitana','Las Condes','$2b$12$Sp2kzFAu1rrnrccAcx4VkevpX/uRI6x1fXIsYIxp4MtBd6uRRsHpS','student',1,11,'2025-10-29 02:47:58','2025-10-29 02:47:58',1),(8,'8.032.822-2','Giovanni peo','giovanni.ahumada.t@mail.pucv.cl','V','valparaiso','$2b$12$1bzR2VoGQyDwmgEFFxlooOU3.FKEZ2BYeEPF8hEt1OE2BjR4a2C9G','student',2,12,'2025-10-29 14:35:57','2025-10-29 14:35:57',1);
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

-- Dump completed on 2025-10-30 19:42:19
