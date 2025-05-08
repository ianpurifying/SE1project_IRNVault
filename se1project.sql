-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 08, 2025 at 02:59 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `se1project`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `account_number` varchar(10) NOT NULL COMMENT '10-digit unique account number',
  `name` varchar(100) NOT NULL,
  `hashed_pin` varchar(60) NOT NULL COMMENT 'bcrypt hash',
  `balance` decimal(15,2) NOT NULL DEFAULT 0.00,
  `is_approved` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0=pending,1=approved',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`account_number`, `name`, `hashed_pin`, `balance`, `is_approved`, `created_at`) VALUES
('0000000001', 'ADMIN', '$2b$12$hj9VecYWxkXUJ4anlXE4aeQm9mlKt4RBmzCYdk5XL59huQpSPveKq', 0.00, 1, '2025-05-06 03:14:43'),
('1940112756', 'Shit', '$2b$12$TFb3ovh0hfKb6971k3M.3umT2HycpABndMPHjVEMVBZQL0M7EGC8m', 50000.00, 1, '2025-05-06 03:25:17'),
('2915648798', 'Rat', '$2b$12$FfNSO/5/Cw8hsJcjSeaAV.pSuL3MpHDRUJYlyM44xRCk5h.tHxD5u', 15000.00, 1, '2025-05-08 12:55:28'),
('9348634104', 'Ass', '$2b$12$Q7RPvteGOHVFQ24WEW7uz.ql3HeNJPBkgT2PfYxkl2a1Adk32SIRi', 100.00, 1, '2025-05-06 03:44:45');

-- --------------------------------------------------------

--
-- Table structure for table `account_declines`
--

CREATE TABLE `account_declines` (
  `id` int(11) NOT NULL,
  `account_number` varchar(10) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `declined_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `account_number` varchar(10) NOT NULL,
  `type` enum('deposit','withdrawal','transfer') NOT NULL,
  `amount` decimal(15,2) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `account_number`, `type`, `amount`, `timestamp`) VALUES
(5, '1940112756', 'deposit', 100100.00, '2025-05-06 03:44:23'),
(6, '1940112756', '', 100.00, '2025-05-06 03:45:51'),
(7, '9348634104', '', 100.00, '2025-05-06 03:45:51'),
(8, '1940112756', 'withdrawal', 50000.00, '2025-05-06 03:46:19'),
(9, '1940112756', 'deposit', 20000.00, '2025-05-08 12:57:50'),
(10, '1940112756', 'withdrawal', 5000.00, '2025-05-08 12:58:01'),
(11, '1940112756', '', 15000.00, '2025-05-08 12:58:19'),
(12, '2915648798', '', 15000.00, '2025-05-08 12:58:19');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`account_number`),
  ADD KEY `idx_is_approved` (`is_approved`);

--
-- Indexes for table `account_declines`
--
ALTER TABLE `account_declines`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_decline_acct` (`account_number`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_txn_acct` (`account_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account_declines`
--
ALTER TABLE `account_declines`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `account_declines`
--
ALTER TABLE `account_declines`
  ADD CONSTRAINT `fk_decline_account` FOREIGN KEY (`account_number`) REFERENCES `accounts` (`account_number`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `fk_txn_account` FOREIGN KEY (`account_number`) REFERENCES `accounts` (`account_number`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
