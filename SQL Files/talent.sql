-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Apr 01, 2022 at 01:11 PM
-- Server version: 5.7.34
-- PHP Version: 7.4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `talent`
--
CREATE DATABASE IF NOT EXISTS `talent` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `talent`;

-- --------------------------------------------------------

--
-- Table structure for table `talent`
--

DROP TABLE IF EXISTS `talent`;
CREATE TABLE IF NOT EXISTS `talent` (
  `talentID` int(255) NOT NULL AUTO_INCREMENT,
  `name` varchar(300) NOT NULL,
  `contactNumber` int(8) NOT NULL,
  `contactEmail` varchar(300) NOT NULL,
  PRIMARY KEY (`talentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
