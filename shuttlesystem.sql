-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 29, 2026 at 02:10 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `shuttlesystem`
--

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `bookingID` int(11) NOT NULL,
  `passengerID` int(11) NOT NULL,
  `routeID` int(11) NOT NULL,
  `tripID` int(11) NOT NULL,
  `seatNumber` int(11) NOT NULL,
  `bookingStatus` enum('Confirmed','Cancelled') NOT NULL,
  `date` date NOT NULL,
  `tripStatus` enum('On-time','Delayed') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bus`
--

CREATE TABLE `bus` (
  `busID` int(11) NOT NULL,
  `plateNumber` varchar(20) NOT NULL,
  `capacity` int(11) NOT NULL,
  `busStatus` enum('Active','Inactive') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `busassignment`
--

CREATE TABLE `busassignment` (
  `assignmentID` int(11) NOT NULL,
  `routeID` int(11) NOT NULL,
  `busID` int(11) NOT NULL,
  `driverID` int(11) NOT NULL,
  `coordinatorID` int(11) NOT NULL,
  `tripDate` date NOT NULL,
  `estimateArrivalTime` time NOT NULL,
  `tripStatus` enum('On-time','Delayed') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `incident`
--

CREATE TABLE `incident` (
  `incidentID` int(11) NOT NULL,
  `routeID` int(11) NOT NULL,
  `busID` int(11) NOT NULL,
  `reporterID` int(11) NOT NULL,
  `description` text NOT NULL,
  `status` enum('New','In progress','Resolved') NOT NULL,
  `classification` varchar(50) NOT NULL,
  `timestamp` datetime NOT NULL,
  `updateByAdminID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `notificationID` int(11) NOT NULL,
  `messageContent` text NOT NULL,
  `targetAudience` enum('passenger','driver','TC','admin') NOT NULL,
  `channel` enum('email','SMS') NOT NULL,
  `timestamp` datetime NOT NULL,
  `confirmationStatus` enum('sent','failed') NOT NULL,
  `date` date NOT NULL,
  `tripStatus` enum('On-time','Delayed') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `report`
--

CREATE TABLE `report` (
  `reportID` int(11) NOT NULL,
  `routeID` int(11) NOT NULL,
  `incidentType` varchar(5000) NOT NULL,
  `dateRangeStart` date NOT NULL,
  `dateRangeEnd` date NOT NULL,
  `generatedTimestamp` datetime NOT NULL,
  `reportData` text NOT NULL,
  `tripStatus` enum('On-time','Delayed') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `route`
--

CREATE TABLE `route` (
  `routeID` int(11) NOT NULL,
  `routeName` varchar(100) NOT NULL,
  `startPoint` varchar(100) NOT NULL,
  `endPoint` varchar(100) NOT NULL,
  `status` enum('Active','Inactive') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `shuttlelocation`
--

CREATE TABLE `shuttlelocation` (
  `locationID` int(11) NOT NULL,
  `busID` int(11) NOT NULL,
  `routeID` int(11) NOT NULL,
  `timestamp` datetime NOT NULL,
  `latitude` decimal(9,5) NOT NULL,
  `longitude` decimal(9,5) NOT NULL,
  `estimateArrivalTime` time NOT NULL,
  `tripStatus` enum('On-time','Delayed') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `timetable`
--

CREATE TABLE `timetable` (
  `timetableID` int(11) NOT NULL,
  `routeID` int(11) NOT NULL,
  `departureTime` time NOT NULL,
  `arrivalTime` time NOT NULL,
  `day` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `trip`
--

CREATE TABLE `trip` (
  `tripID` int(11) NOT NULL,
  `routeID` int(11) NOT NULL,
  `timetableID` int(11) NOT NULL,
  `busID` int(11) NOT NULL,
  `driverID` int(11) NOT NULL,
  `coordinatorID` int(11) NOT NULL,
  `tripDate` date NOT NULL,
  `tripStatus` enum('Scheduled','Ongoing','Completed') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userID` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` enum('Passenger','Driver','TC','Admin') NOT NULL,
  `password` varchar(255) NOT NULL,
  `accountStatus` enum('Active','Inactive') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`bookingID`),
  ADD KEY `passengerID` (`passengerID`),
  ADD KEY `routeID` (`routeID`),
  ADD KEY `tripID` (`tripID`);

--
-- Indexes for table `bus`
--
ALTER TABLE `bus`
  ADD PRIMARY KEY (`busID`);

--
-- Indexes for table `busassignment`
--
ALTER TABLE `busassignment`
  ADD PRIMARY KEY (`assignmentID`),
  ADD KEY `routeID` (`routeID`),
  ADD KEY `busID` (`busID`),
  ADD KEY `driverID` (`driverID`),
  ADD KEY `coordinatorID` (`coordinatorID`);

--
-- Indexes for table `incident`
--
ALTER TABLE `incident`
  ADD PRIMARY KEY (`incidentID`),
  ADD KEY `routeID` (`routeID`),
  ADD KEY `busID` (`busID`),
  ADD KEY `reporterID` (`reporterID`),
  ADD KEY `updateByAdminID` (`updateByAdminID`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`notificationID`);

--
-- Indexes for table `report`
--
ALTER TABLE `report`
  ADD PRIMARY KEY (`reportID`),
  ADD KEY `routeID` (`routeID`);

--
-- Indexes for table `route`
--
ALTER TABLE `route`
  ADD PRIMARY KEY (`routeID`);

--
-- Indexes for table `shuttlelocation`
--
ALTER TABLE `shuttlelocation`
  ADD PRIMARY KEY (`locationID`),
  ADD KEY `busID` (`busID`),
  ADD KEY `routeID` (`routeID`);

--
-- Indexes for table `timetable`
--
ALTER TABLE `timetable`
  ADD PRIMARY KEY (`timetableID`),
  ADD KEY `routeID` (`routeID`);

--
-- Indexes for table `trip`
--
ALTER TABLE `trip`
  ADD PRIMARY KEY (`tripID`),
  ADD KEY `routeID` (`routeID`),
  ADD KEY `timetableID` (`timetableID`),
  ADD KEY `busID` (`busID`),
  ADD KEY `driverID` (`driverID`),
  ADD KEY `coordinatorID` (`coordinatorID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`passengerID`) REFERENCES `user` (`userID`),
  ADD CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`routeID`) REFERENCES `route` (`routeID`),
  ADD CONSTRAINT `booking_ibfk_3` FOREIGN KEY (`tripID`) REFERENCES `trip` (`tripID`);

--
-- Constraints for table `busassignment`
--
ALTER TABLE `busassignment`
  ADD CONSTRAINT `busassignment_ibfk_1` FOREIGN KEY (`routeID`) REFERENCES `route` (`routeID`),
  ADD CONSTRAINT `busassignment_ibfk_2` FOREIGN KEY (`busID`) REFERENCES `bus` (`busID`),
  ADD CONSTRAINT `busassignment_ibfk_3` FOREIGN KEY (`driverID`) REFERENCES `user` (`userID`),
  ADD CONSTRAINT `busassignment_ibfk_4` FOREIGN KEY (`coordinatorID`) REFERENCES `user` (`userID`);

--
-- Constraints for table `incident`
--
ALTER TABLE `incident`
  ADD CONSTRAINT `incident_ibfk_1` FOREIGN KEY (`routeID`) REFERENCES `route` (`routeID`),
  ADD CONSTRAINT `incident_ibfk_2` FOREIGN KEY (`busID`) REFERENCES `bus` (`busID`),
  ADD CONSTRAINT `incident_ibfk_3` FOREIGN KEY (`reporterID`) REFERENCES `user` (`userID`),
  ADD CONSTRAINT `incident_ibfk_4` FOREIGN KEY (`updateByAdminID`) REFERENCES `user` (`userID`);

--
-- Constraints for table `report`
--
ALTER TABLE `report`
  ADD CONSTRAINT `report_ibfk_1` FOREIGN KEY (`routeID`) REFERENCES `route` (`routeID`);

--
-- Constraints for table `shuttlelocation`
--
ALTER TABLE `shuttlelocation`
  ADD CONSTRAINT `shuttlelocation_ibfk_1` FOREIGN KEY (`busID`) REFERENCES `bus` (`busID`),
  ADD CONSTRAINT `shuttlelocation_ibfk_2` FOREIGN KEY (`routeID`) REFERENCES `route` (`routeID`);

--
-- Constraints for table `timetable`
--
ALTER TABLE `timetable`
  ADD CONSTRAINT `timetable_ibfk_1` FOREIGN KEY (`routeID`) REFERENCES `route` (`routeID`);

--
-- Constraints for table `trip`
--
ALTER TABLE `trip`
  ADD CONSTRAINT `trip_ibfk_1` FOREIGN KEY (`routeID`) REFERENCES `route` (`routeID`),
  ADD CONSTRAINT `trip_ibfk_2` FOREIGN KEY (`timetableID`) REFERENCES `timetable` (`timetableID`),
  ADD CONSTRAINT `trip_ibfk_3` FOREIGN KEY (`busID`) REFERENCES `bus` (`busID`),
  ADD CONSTRAINT `trip_ibfk_4` FOREIGN KEY (`driverID`) REFERENCES `user` (`userID`),
  ADD CONSTRAINT `trip_ibfk_5` FOREIGN KEY (`coordinatorID`) REFERENCES `user` (`userID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
