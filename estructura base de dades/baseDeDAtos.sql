-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.2.0 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para proyecto
CREATE DATABASE IF NOT EXISTS `proyecto` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `proyecto`;

-- Volcando estructura para tabla proyecto.grupo
CREATE TABLE IF NOT EXISTS `grupo` (
  `grupo_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` text,
  `horario` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`grupo_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla proyecto.grupo: ~3 rows (aproximadamente)
INSERT INTO `grupo` (`grupo_id`, `nombre`, `descripcion`, `horario`) VALUES
	(1, 'Aula02', 'Aula de programación', '09:00 - 17:00'),
	(2, 'Aula03', 'Aula de bases de datos', '10:00 - 18:00'),
	(3, 'Aula05', 'Aula de sistemas', '08:30 - 16:30');

-- Volcando estructura para tabla proyecto.permiso
CREATE TABLE IF NOT EXISTS `permiso` (
  `permiso_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) DEFAULT NULL,
  `descripcion` text,
  PRIMARY KEY (`permiso_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla proyecto.permiso: ~2 rows (aproximadamente)
INSERT INTO `permiso` (`permiso_id`, `nombre`, `descripcion`) VALUES
	(1, 'Pasar lista', 'Permiso para poder pasar lista de los alumnos'),
	(2, 'Asistencia', 'Permiso para modificar la asistencia de un alumno');

-- Volcando estructura para tabla proyecto.persona
CREATE TABLE IF NOT EXISTS `persona` (
  `persona_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) DEFAULT NULL,
  `apellido` varchar(30) DEFAULT NULL,
  `dni` varchar(20) DEFAULT NULL,
  `grupo_id` int DEFAULT NULL,
  `rol_id` int DEFAULT NULL,
  `aula` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`persona_id`),
  KEY `fk_grupo` (`grupo_id`),
  KEY `fk_rol` (`rol_id`),
  CONSTRAINT `fk_grupo` FOREIGN KEY (`grupo_id`) REFERENCES `grupo` (`grupo_id`),
  CONSTRAINT `fk_rol` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`rol_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla proyecto.persona: ~3 rows (aproximadamente)
INSERT INTO `persona` (`persona_id`, `nombre`, `apellido`, `dni`, `grupo_id`, `rol_id`, `aula`) VALUES
	(1, 'Juan', 'Perez', '12345678', 1, 1, 'Aula 1'),
	(2, 'Ana', 'Lopez', '87654321', 2, 2, 'Aula 2'),
	(3, 'Carlos', 'Garcia', '13579246', 3, 3, 'Aula 3');

-- Volcando estructura para tabla proyecto.registrotarjeta
CREATE TABLE IF NOT EXISTS `registrotarjeta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tarjeta_id` int DEFAULT NULL,
  `fecha_lectura` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `tipo_lectura` enum('Entrada','Salida') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tarjeta_id` (`tarjeta_id`),
  CONSTRAINT `registrotarjeta_ibfk_1` FOREIGN KEY (`tarjeta_id`) REFERENCES `tarjeta` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla proyecto.registrotarjeta: ~4 rows (aproximadamente)
INSERT INTO `registrotarjeta` (`id`, `tarjeta_id`, `fecha_lectura`, `tipo_lectura`) VALUES
	(1, 1, '2024-11-14 15:19:11', 'Entrada'),
	(2, 1, '2024-11-14 15:19:11', 'Salida'),
	(3, 2, '2024-11-14 15:19:11', 'Entrada'),
	(4, 3, '2024-11-14 15:19:11', 'Entrada');

-- Volcando estructura para tabla proyecto.rol
CREATE TABLE IF NOT EXISTS `rol` (
  `rol_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) DEFAULT NULL,
  `descripcion` text,
  `permiso_id` int DEFAULT NULL,
  PRIMARY KEY (`rol_id`),
  KEY `fk_permiso` (`permiso_id`),
  CONSTRAINT `fk_permiso` FOREIGN KEY (`permiso_id`) REFERENCES `permiso` (`permiso_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla proyecto.rol: ~3 rows (aproximadamente)
INSERT INTO `rol` (`rol_id`, `nombre`, `descripcion`, `permiso_id`) VALUES
	(1, 'Alumno', 'Rol para alumnos, sin permisos administrativos', NULL),
	(2, 'Profesor', 'Rol para profesores, con permisos limitados', 1),
	(3, 'Administrador', 'Rol con permisos completos para gestionar', 2);

-- Volcando estructura para tabla proyecto.tarjeta
CREATE TABLE IF NOT EXISTS `tarjeta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codigo` varchar(100) NOT NULL,
  `persona_id` int DEFAULT NULL,
  `fecha_asignacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('Activa','Inactiva') DEFAULT 'Activa',
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`),
  KEY `persona_id` (`persona_id`),
  CONSTRAINT `tarjeta_ibfk_1` FOREIGN KEY (`persona_id`) REFERENCES `persona` (`persona_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla proyecto.tarjeta: ~3 rows (aproximadamente)
INSERT INTO `tarjeta` (`id`, `codigo`, `persona_id`, `fecha_asignacion`, `estado`) VALUES
	(1, 'TARJ001', 1, '2024-11-14 15:19:11', 'Activa'),
	(2, 'TARJ002', 2, '2024-11-14 15:19:11', 'Inactiva'),
	(3, 'TARJ003', 3, '2024-11-14 15:19:11', 'Activa');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
