--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `account_number` varchar(10) NOT NULL COMMENT '10-digit unique account number',
  `name` varchar(100) NOT NULL,
  `hashed_pin` varchar(60) NOT NULL COMMENT 'bcrypt hash',
  `balance` decimal(15,2) NOT NULL DEFAULT 0.00,
  `is_approved` tinyint(1) NOT NULL DEFAULT 0 COMMENT '-1=rejected, 0=pending, 1=approved',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `loans`
--
ALTER TABLE `loans`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `loan_applications`
--
ALTER TABLE `loan_applications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `loan_payments`
--
ALTER TABLE `loan_payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=130;

--
-- Constraints for dumped tables
--

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
