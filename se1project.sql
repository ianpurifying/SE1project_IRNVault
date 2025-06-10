-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 10, 2025 at 07:54 AM
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
('0000000001', 'ADMIN', '$2b$12$hj9VecYWxkXUJ4anlXE4aeQm9mlKt4RBmzCYdk5XL59huQpSPveKq', 10000001265.83, 1, '2025-05-06 03:14:43'),
('2915648798', 'Rat', '$2b$12$FfNSO/5/Cw8hsJcjSeaAV.pSuL3MpHDRUJYlyM44xRCk5h.tHxD5u', 20000.00, 1, '2025-05-08 12:55:28'),
('4668993022', 'King Charles', '$2b$12$mKSkI12pYDopLQyBihYdy.ewgG1FLQ8eJ6hvwZ5iFFe5tOgwwndkq', 38734.17, 1, '2025-05-29 04:54:06'),
('5287548283', 'Ailen Carpio', '$2b$12$6TmVK6E5/MtJl1NNOElS0OCWJqaJmuJzHcSNqbi1wUI5ScW0wBVjW', 0.00, -1, '2025-05-30 03:26:33'),
('5498149298', 'Aiziel', '$2b$12$v3LTzlJ.9QbNKQZFcAUqcO/cETe4WkYTwVQHBJLsfri7Y.GDsqXb2', 0.00, 0, '2025-05-30 03:29:01'),
('5967648823', 'Grok', '$2b$12$gJ9QOoigOtM.856xgyTSz..KseRnC.Y3hoRVVL9rG6003f8bKVuz.', 0.00, -1, '2025-06-10 05:13:56');

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

--
-- Dumping data for table `account_declines`
--

INSERT INTO `account_declines` (`id`, `account_number`, `reason`, `declined_at`) VALUES
(2, '5287548283', 'No valid ID', '2025-05-30 03:29:25'),
(3, '5967648823', 'I hate you!', '2025-06-10 05:14:25');

-- --------------------------------------------------------

--
-- Table structure for table `loans`
--

CREATE TABLE `loans` (
  `id` int(11) NOT NULL,
  `application_id` int(11) NOT NULL,
  `account_number` varchar(10) NOT NULL,
  `principal_amount` decimal(15,2) NOT NULL,
  `interest_rate` decimal(5,2) NOT NULL,
  `term_months` int(11) NOT NULL,
  `monthly_payment` decimal(15,2) NOT NULL,
  `remaining_balance` decimal(15,2) NOT NULL,
  `next_payment_date` date NOT NULL,
  `status` enum('active','paid_off','defaulted') NOT NULL DEFAULT 'active',
  `disbursed_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `loans`
--

INSERT INTO `loans` (`id`, `application_id`, `account_number`, `principal_amount`, `interest_rate`, `term_months`, `monthly_payment`, `remaining_balance`, `next_payment_date`, `status`, `disbursed_at`) VALUES
(1, 1, '4668993022', 100000.00, 15.00, 12, 9025.83, 0.00, '2025-07-10', 'paid_off', '2025-06-10 05:47:04');

-- --------------------------------------------------------

--
-- Table structure for table `loan_applications`
--

CREATE TABLE `loan_applications` (
  `id` int(11) NOT NULL,
  `account_number` varchar(10) NOT NULL,
  `amount` decimal(15,2) NOT NULL,
  `purpose` varchar(255) NOT NULL,
  `monthly_income` decimal(15,2) NOT NULL,
  `employment_status` varchar(100) NOT NULL,
  `status` enum('pending','approved','rejected') NOT NULL DEFAULT 'pending',
  `interest_rate` decimal(5,2) DEFAULT NULL COMMENT 'Annual interest rate percentage',
  `term_months` int(11) DEFAULT NULL COMMENT 'Loan term in months',
  `monthly_payment` decimal(15,2) DEFAULT NULL,
  `admin_notes` text DEFAULT NULL,
  `applied_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `processed_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `loan_applications`
--

INSERT INTO `loan_applications` (`id`, `account_number`, `amount`, `purpose`, `monthly_income`, `employment_status`, `status`, `interest_rate`, `term_months`, `monthly_payment`, `admin_notes`, `applied_at`, `processed_at`) VALUES
(1, '4668993022', 100000.00, 'Investment', 20000.00, 'Full-time Employee', 'approved', 15.00, 12, 9025.83, NULL, '2025-06-10 05:44:15', '2025-06-10 05:47:04');

-- --------------------------------------------------------

--
-- Table structure for table `loan_payments`
--

CREATE TABLE `loan_payments` (
  `id` int(11) NOT NULL,
  `loan_id` int(11) NOT NULL,
  `account_number` varchar(10) NOT NULL,
  `payment_amount` decimal(15,2) NOT NULL,
  `principal_portion` decimal(15,2) NOT NULL,
  `interest_portion` decimal(15,2) NOT NULL,
  `remaining_balance` decimal(15,2) NOT NULL,
  `payment_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `payment_type` enum('regular','early','penalty') NOT NULL DEFAULT 'regular'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `loan_payments`
--

INSERT INTO `loan_payments` (`id`, `loan_id`, `account_number`, `payment_amount`, `principal_portion`, `interest_portion`, `remaining_balance`, `payment_date`, `payment_type`) VALUES
(1, 1, '4668993022', 100000.00, 98750.00, 1250.00, 1250.00, '2025-06-10 05:49:10', 'regular'),
(2, 1, '4668993022', 1250.00, 1234.38, 15.63, 15.63, '2025-06-10 05:50:09', 'regular'),
(3, 1, '4668993022', 15.63, 15.43, 0.20, 0.20, '2025-06-10 05:53:21', 'regular'),
(4, 1, '4668993022', 0.20, 0.20, 0.00, 0.00, '2025-06-10 05:53:36', 'regular');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `account_number` varchar(10) NOT NULL,
  `type` enum('deposit','withdrawal','transfer_in','transfer_out','loan_disbursement','loan_payment') NOT NULL,
  `amount` decimal(15,2) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `account_number`, `type`, `amount`, `timestamp`) VALUES
(13, '4668993022', 'deposit', 50000.00, '2025-05-29 04:56:17'),
(14, '4668993022', 'withdrawal', 10000.00, '2025-05-29 05:07:28'),
(17, '4668993022', 'transfer_out', 5000.00, '2025-05-29 05:19:31'),
(18, '2915648798', 'transfer_in', 5000.00, '2025-05-29 05:19:31'),
(19, '2915648798', 'withdrawal', 1000.00, '2025-05-29 05:21:43'),
(20, '2915648798', 'deposit', 1000.00, '2025-05-29 05:22:00'),
(21, '2915648798', 'transfer_out', 5000.00, '2025-05-29 05:22:15'),
(22, '4668993022', 'transfer_in', 5000.00, '2025-05-29 05:22:15'),
(26, '4668993022', 'transfer_in', 5000.00, '2025-05-30 03:31:51'),
(27, '4668993022', 'loan_disbursement', 100000.00, '2025-06-10 05:47:04'),
(28, '4668993022', 'loan_payment', 100000.00, '2025-06-10 05:49:10'),
(29, '4668993022', 'loan_payment', 1250.00, '2025-06-10 05:50:09'),
(30, '4668993022', 'loan_payment', 15.63, '2025-06-10 05:53:21'),
(31, '4668993022', 'loan_payment', 0.20, '2025-06-10 05:53:36');

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
-- Indexes for table `loans`
--
ALTER TABLE `loans`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_active_loans` (`account_number`,`status`),
  ADD KEY `idx_payment_date` (`next_payment_date`),
  ADD KEY `fk_loan_application` (`application_id`);

--
-- Indexes for table `loan_applications`
--
ALTER TABLE `loan_applications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_loan_account` (`account_number`),
  ADD KEY `idx_loan_status` (`status`);

--
-- Indexes for table `loan_payments`
--
ALTER TABLE `loan_payments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_loan_payments` (`loan_id`),
  ADD KEY `idx_payment_account` (`account_number`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `loans`
--
ALTER TABLE `loans`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `loan_applications`
--
ALTER TABLE `loan_applications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `loan_payments`
--
ALTER TABLE `loan_payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `account_declines`
--
ALTER TABLE `account_declines`
  ADD CONSTRAINT `fk_decline_account` FOREIGN KEY (`account_number`) REFERENCES `accounts` (`account_number`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `loans`
--
ALTER TABLE `loans`
  ADD CONSTRAINT `fk_loan_application` FOREIGN KEY (`application_id`) REFERENCES `loan_applications` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_loan_borrower` FOREIGN KEY (`account_number`) REFERENCES `accounts` (`account_number`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `loan_applications`
--
ALTER TABLE `loan_applications`
  ADD CONSTRAINT `fk_loan_account` FOREIGN KEY (`account_number`) REFERENCES `accounts` (`account_number`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `loan_payments`
--
ALTER TABLE `loan_payments`
  ADD CONSTRAINT `fk_payment_account` FOREIGN KEY (`account_number`) REFERENCES `accounts` (`account_number`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_payment_loan` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `fk_txn_account` FOREIGN KEY (`account_number`) REFERENCES `accounts` (`account_number`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
