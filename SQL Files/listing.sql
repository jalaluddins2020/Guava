-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Mar 31, 2022 at 09:00 AM
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
-- Database: `listing`
--
CREATE DATABASE IF NOT EXISTS `listing` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `listing`;

-- --------------------------------------------------------

--
-- Table structure for table `listing`
--

DROP TABLE IF EXISTS `listing`;
CREATE TABLE `listing` (
  `listingID` int(11) NOT NULL,
  `customerID` int(11) NOT NULL,
  `talentID` int(11) DEFAULT NULL,
  `name` varchar(300) NOT NULL,
  `details` varchar(300) NOT NULL,
  `status` varchar(300) NOT NULL,
  `price` float(6,2) NOT NULL,
  `paymentStatus` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `listing`
--

INSERT INTO `listing` (`listingID`, `customerID`, `talentID`, `name`, `details`, `status`, `price`, `paymentStatus`) VALUES
(1, 1, 2, 'Wedding Photoshoot', 'Require a wedding photographer!', 'Accepted', 100.00, 'unpaid'),
(2, 2, NULL, 'Professional Photographer', 'Looking for a professional photographer that can help my company take some quality photos!', 'available', 300.00, 'unpaid'),
(3, 1, NULL, 'Picnic Photographer', 'Have an upcoming picnic even this weekend with my family. Looking for a photographer that is willing to tag along and document it!', 'available', 50.00, 'unpaid');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `listing`
--
ALTER TABLE `listing`
  ADD PRIMARY KEY (`listingID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `listing`
--
ALTER TABLE `listing`
  MODIFY `listingID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
