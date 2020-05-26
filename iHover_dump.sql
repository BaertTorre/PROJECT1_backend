-- MySQL dump 10.17  Distrib 10.3.22-MariaDB, for debian-linux-gnueabihf (armv8l)
--
-- Host: localhost    Database: iHover
-- ------------------------------------------------------
-- Server version	10.3.22-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `GPS data`
--

DROP TABLE IF EXISTS `GPS data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GPS data` (
  `id GPS data` int(11) NOT NULL AUTO_INCREMENT,
  `coordinaat lengte` float NOT NULL,
  `coordinaat breedte` float NOT NULL,
  `time_id time` int(11) NOT NULL,
  PRIMARY KEY (`id GPS data`,`time_id time`),
  UNIQUE KEY `id GPS data_UNIQUE` (`id GPS data`),
  KEY `fk_GPS data_time1_idx` (`time_id time`),
  CONSTRAINT `fk_GPS data_time1` FOREIGN KEY (`time_id time`) REFERENCES `time` (`id time`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GPS data`
--

LOCK TABLES `GPS data` WRITE;
/*!40000 ALTER TABLE `GPS data` DISABLE KEYS */;
INSERT INTO `GPS data` VALUES (1,69,170,1),(2,57,351,2),(3,179,313,3),(4,22,143,4),(5,133,73,5),(6,83,57,6),(7,271,43,7),(8,327,86,8),(9,137,190,9),(10,212,300,10);
/*!40000 ALTER TABLE `GPS data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LDR data`
--

DROP TABLE IF EXISTS `LDR data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LDR data` (
  `id LDR data` int(11) NOT NULL AUTO_INCREMENT,
  `LDR data` int(11) NOT NULL,
  `LED aan uit` tinyint(4) NOT NULL,
  `time_id time` int(11) NOT NULL,
  PRIMARY KEY (`id LDR data`,`time_id time`),
  KEY `fk_LDR data_time1_idx` (`time_id time`),
  CONSTRAINT `fk_LDR data_time1` FOREIGN KEY (`time_id time`) REFERENCES `time` (`id time`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LDR data`
--

LOCK TABLES `LDR data` WRITE;
/*!40000 ALTER TABLE `LDR data` DISABLE KEYS */;
INSERT INTO `LDR data` VALUES (1,992,0,1),(2,710,1,2),(3,144,1,3),(4,711,1,4),(5,205,1,5),(6,82,1,6),(7,906,1,7),(8,880,0,8),(9,937,0,9),(10,267,0,10);
/*!40000 ALTER TABLE `LDR data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `error codes`
--

DROP TABLE IF EXISTS `error codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `error codes` (
  `id error code` int(11) NOT NULL,
  `explanation error code` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id error code`),
  UNIQUE KEY `id codes_UNIQUE` (`id error code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `error codes`
--

LOCK TABLES `error codes` WRITE;
/*!40000 ALTER TABLE `error codes` DISABLE KEYS */;
INSERT INTO `error codes` VALUES (200,'eu, odio. Phasellus at augue id ante dictum cursus. Nunc'),(204,'sem molestie sodales.'),(208,'non, hendrerit id, ante. Nunc'),(212,'Ut'),(216,'adipiscing fringilla, porttitor vulputate, posuere vulputate, lacus.'),(220,'mi enim, condimentum eget, volutpat ornare, facilisis eget, ipsum. Donec'),(224,'eu, odio. Phasellus at augue id'),(228,'ut, pharetra sed, hendrerit a, arcu. Sed et'),(232,'euismod urna. Nullam lobortis quam'),(236,'non nisi.');
/*!40000 ALTER TABLE `error codes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `max speed`
--

DROP TABLE IF EXISTS `max speed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `max speed` (
  `id max speed` int(11) NOT NULL,
  `max speed` int(11) NOT NULL,
  PRIMARY KEY (`id max speed`),
  UNIQUE KEY `id max speed_UNIQUE` (`id max speed`),
  UNIQUE KEY `max speed_UNIQUE` (`max speed`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `max speed`
--

LOCK TABLES `max speed` WRITE;
/*!40000 ALTER TABLE `max speed` DISABLE KEYS */;
INSERT INTO `max speed` VALUES (1,1),(2,11),(3,21),(4,31),(5,41),(6,51),(7,61),(8,71),(9,81),(10,91);
/*!40000 ALTER TABLE `max speed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `settings` (
  `id settings` int(11) NOT NULL AUTO_INCREMENT,
  `explanation settings thema` varchar(100) DEFAULT NULL,
  `auto lamp aan uit` tinyint(4) NOT NULL,
  `avoidance systems aan uit` tinyint(4) NOT NULL,
  `max speed_id max speed` int(11) NOT NULL,
  PRIMARY KEY (`id settings`,`max speed_id max speed`),
  UNIQUE KEY `id settings_UNIQUE` (`id settings`),
  KEY `fk_settings_max speed1_idx` (`max speed_id max speed`),
  CONSTRAINT `fk_settings_max speed1` FOREIGN KEY (`max speed_id max speed`) REFERENCES `max speed` (`id max speed`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` VALUES (1,'ut, pharetra sed, hendrerit a, arcu. Sed',1,1,1),(2,'est, vitae sodales nisi magna',1,1,2),(3,'Integer vulputate, risus a ultricies adipiscing, enim mi tempor lorem,',0,0,3),(4,'lectus convallis',0,1,4),(5,'sem eget massa. Suspendisse eleifend.',1,0,5),(6,'libero lacus, varius et, euismod',1,1,6),(7,'Donec vitae erat vel pede blandit congue. In',1,0,7),(8,'dapibus quam quis diam. Pellentesque habitant morbi',1,0,8),(9,'eget tincidunt dui augue eu tellus. Phasellus elit pede, malesuada',0,1,9),(10,'bibendum sed, est. Nunc',1,1,10);
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `time`
--

DROP TABLE IF EXISTS `time`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `time` (
  `id time` int(11) NOT NULL AUTO_INCREMENT,
  `time stamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `error codes_id error code` int(11) NOT NULL,
  PRIMARY KEY (`id time`,`error codes_id error code`),
  KEY `fk_time_error codes1_idx` (`error codes_id error code`),
  CONSTRAINT `fk_time_error codes1` FOREIGN KEY (`error codes_id error code`) REFERENCES `error codes` (`id error code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `time`
--

LOCK TABLES `time` WRITE;
/*!40000 ALTER TABLE `time` DISABLE KEYS */;
INSERT INTO `time` VALUES (1,'2020-05-23 01:59:47',200),(2,'2020-05-23 01:59:47',204),(3,'2020-05-23 01:59:47',208),(4,'2020-05-23 01:59:47',212),(5,'2020-05-23 01:59:47',216),(6,'2020-05-23 01:59:47',220),(7,'2020-05-23 01:59:47',224),(8,'2020-05-23 01:59:47',228),(9,'2020-05-23 01:59:47',232),(10,'2020-05-23 01:59:47',236);
/*!40000 ALTER TABLE `time` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ultrasonic data`
--

DROP TABLE IF EXISTS `ultrasonic data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ultrasonic data` (
  `id ultrasonic data` int(11) NOT NULL AUTO_INCREMENT,
  `ultrasonic data` int(11) NOT NULL,
  `ultrasonic positie rechts midden links` int(11) NOT NULL,
  `time_id time` int(11) NOT NULL,
  PRIMARY KEY (`id ultrasonic data`,`time_id time`),
  KEY `fk_ultrasonic data_time1_idx` (`time_id time`),
  CONSTRAINT `fk_ultrasonic data_time1` FOREIGN KEY (`time_id time`) REFERENCES `time` (`id time`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ultrasonic data`
--

LOCK TABLES `ultrasonic data` WRITE;
/*!40000 ALTER TABLE `ultrasonic data` DISABLE KEYS */;
INSERT INTO `ultrasonic data` VALUES (1,308,3,1),(2,925,2,2),(3,1333,2,3),(4,1577,2,4),(5,1939,1,5),(6,217,1,6),(7,871,2,7),(8,892,2,8),(9,9,1,9),(10,1387,1,10);
/*!40000 ALTER TABLE `ultrasonic data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-23  4:34:40
