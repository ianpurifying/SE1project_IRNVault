from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
from database import Database

class LoanManager:
    def __init__(self, db: Database):
        self.db = db
        self.ADMIN_ACCT_NO = '0000000001'
        
    def apply_for_loan(self, account_number: str, amount: float, purpose: str, 
                      monthly_income: float, employment_status: str):
        """Submit a loan application"""
        try:
            # Validate inputs
            if amount <= 0:
                print("Error: Loan amount must be positive.")
                return
            
            if monthly_income <= 0:
                print("Error: Monthly income must be positive.")
                return
                
            # Check if user has any pending applications
            self.db.connect()
            self.db.cursor.execute(
                "SELECT COUNT(*) FROM loan_applications WHERE account_number = %s AND status = 'pending'",
                (account_number,)
            )
            pending_count = self.db.cursor.fetchone()[0]
            
            if pending_count > 0:
                print("Error: You already have a pending loan application. Please wait for admin approval.")
                self.db.close()
                return
            
            # Check if user has any active loans
            self.db.cursor.execute(
                "SELECT COUNT(*) FROM loans WHERE account_number = %s AND status = 'active'",
                (account_number,)
            )
            active_loans = self.db.cursor.fetchone()[0]
            
            if active_loans > 0:
                print("Error: You already have an active loan. Pay off your current loan before applying for a new one.")
                self.db.close()
                return
            
            # Submit application
            self.db.cursor.execute(
                """INSERT INTO loan_applications 
                   (account_number, amount, purpose, monthly_income, employment_status) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (account_number, amount, purpose, monthly_income, employment_status)
            )
            self.db.commit()
            print(f"✅ Loan application submitted successfully!")
            print(f"   Amount: ₱{amount:,.2f}")
            print(f"   Purpose: {purpose}")
            print(f"   Status: Pending admin approval")
            
        except Exception as e:
            self.db.rollback()
            print(f"Error submitting loan application: {e}")
        finally:
            self.db.close()
    
    def get_loan_status_gui(self, account_number: str):
        """Get loan status formatted for GUI display"""
        try:
            self.db.connect()
            
            # Check for loan applications
            self.db.cursor.execute(
                """SELECT id, amount, purpose, status, applied_at, admin_notes, 
                        interest_rate, term_months, monthly_payment
                FROM loan_applications 
                WHERE account_number = %s 
                ORDER BY applied_at DESC LIMIT 5""",
                (account_number,)
            )
            applications = self.db.cursor.fetchall()
            
            # Check for active loans
            self.db.cursor.execute(
                """SELECT l.id, l.principal_amount, l.remaining_balance, l.monthly_payment, 
                        l.next_payment_date, l.interest_rate, l.term_months, l.status,
                        l.disbursed_at
                FROM loans l 
                WHERE l.account_number = %s AND l.status IN ('active', 'paid_off')
                ORDER BY l.disbursed_at DESC""",
                (account_number,)
            )
            active_loans = self.db.cursor.fetchall()
            
            # Check for recent loan payments
            self.db.cursor.execute(
                """SELECT lp.payment_amount, lp.principal_portion, lp.interest_portion,
                        lp.remaining_balance, lp.payment_date, lp.payment_type
                FROM loan_payments lp
                JOIN loans l ON lp.loan_id = l.id
                WHERE l.account_number = %s
                ORDER BY lp.payment_date DESC LIMIT 5""",
                (account_number,)
            )
            recent_payments = self.db.cursor.fetchall()
            
            self.db.close()
            
            # Format the information for GUI display
            status_text = "=" * 60 + "\n"
            status_text += "                     LOAN STATUS REPORT\n"
            status_text += "=" * 60 + "\n\n"
            
            status_text += f"Account Number: {account_number}\n"
            status_text += f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # Display loan applications
            if applications:
                status_text += "📝 LOAN APPLICATIONS:\n"
                status_text += "-" * 60 + "\n"
                for app_id, amount, purpose, status, applied_at, notes, rate, term, monthly_pay in applications:
                    status_icons = {"pending": "⏳", "approved": "✅", "rejected": "❌"}
                    status_text += f"Application #{app_id}\n"
                    status_text += f"  Amount: ${float(amount):,.2f}\n"
                    status_text += f"  Purpose: {purpose}\n"
                    status_text += f"  Status: {status_icons.get(status, '❓')} {status.upper()}\n"
                    status_text += f"  Applied: {applied_at.strftime('%Y-%m-%d %H:%M')}\n"
                    
                    if status == 'approved' and rate and term and monthly_pay:
                        status_text += f"  Interest Rate: {float(rate)}% per year\n"
                        status_text += f"  Term: {term} months\n"
                        status_text += f"  Monthly Payment: ${float(monthly_pay):,.2f}\n"
                    
                    if notes:
                        status_text += f"  Admin Notes: {notes}\n"
                    status_text += "\n"
            else:
                status_text += "📝 LOAN APPLICATIONS: None found\n\n"
            
            # Display active/paid loans
            if active_loans:
                status_text += "💰 LOAN DETAILS:\n"
                status_text += "-" * 60 + "\n"
                
                for loan_id, principal, remaining, monthly_pay, next_date, rate, term, loan_status, disbursed in active_loans:
                    status_icons = {"active": "🟢", "paid_off": "✅", "defaulted": "❌"}
                    status_text += f"Loan #{loan_id} - {status_icons.get(loan_status, '❓')} {loan_status.upper()}\n"
                    status_text += f"  Original Amount: ${float(principal):,.2f}\n"
                    status_text += f"  Remaining Balance: ${float(remaining):,.2f}\n"
                    status_text += f"  Monthly Payment: ${float(monthly_pay):,.2f}\n"
                    status_text += f"  Interest Rate: {float(rate)}% per year\n"
                    status_text += f"  Term: {term} months\n"
                    status_text += f"  Disbursed: {disbursed.strftime('%Y-%m-%d')}\n"
                    
                    if loan_status == 'active':
                        status_text += f"  Next Payment Due: {next_date}\n"
                        
                        # Calculate progress
                        paid_amount = float(principal) - float(remaining)
                        if float(principal) > 0:
                            progress = (paid_amount / float(principal)) * 100
                            status_text += f"  Progress: {progress:.1f}% paid off\n"
                        
                        # Check if overdue
                        today = datetime.now().date()
                        if next_date < today:
                            days_overdue = (today - next_date).days
                            status_text += f"  ⚠️  OVERDUE by {days_overdue} days!\n"
                        else:
                            days_until = (next_date - today).days
                            status_text += f"  ✅ Due in {days_until} days\n"
                    
                    status_text += "\n"
            else:
                status_text += "💰 ACTIVE LOANS: None found\n\n"
            
            # Display recent payments
            if recent_payments:
                status_text += "💳 RECENT LOAN PAYMENTS:\n"
                status_text += "-" * 60 + "\n"
                status_text += f"{'Date':<12} {'Amount':<12} {'Principal':<12} {'Interest':<12} {'Balance':<12}\n"
                status_text += "-" * 60 + "\n"
                
                for payment_amt, principal_portion, interest_portion, remaining_bal, payment_date, payment_type in recent_payments:
                    date_str = payment_date.strftime('%Y-%m-%d')
                    status_text += f"{date_str:<12} ${float(payment_amt):>9,.2f} ${float(principal_portion):>9,.2f} ${float(interest_portion):>9,.2f} ${float(remaining_bal):>9,.2f}\n"
            else:
                status_text += "💳 RECENT PAYMENTS: None found\n\n"
            
            status_text += "\n" + "=" * 60 + "\n"
            status_text += "For loan applications or payments, contact your bank.\n"
            status_text += "=" * 60 + "\n"
            
            return status_text
            
        except Exception as e:
            self.db.close()
            return f"Error retrieving loan status: {str(e)}\n\nAccount: {account_number}"

    def make_loan_payment(self, account_number: str, payment_amount: float = None, pay_in_full: bool = False):
        """Make a payment towards an active loan or pay it off completely"""
        self.db.connect()
        try:
            # Get active loan details
            self.db.cursor.execute(
                """SELECT id, remaining_balance, interest_rate, monthly_payment, next_payment_date, principal_amount
                   FROM loans WHERE account_number = %s AND status = 'active'""",
                (account_number,)
            )
            loan_data = self.db.cursor.fetchone()
            
            if not loan_data:
                print("❌ No active loan found.")
                return
            
            loan_id, remaining_balance, interest_rate, monthly_payment, next_payment_date, principal_amount = loan_data
            
            # Check user's account balance first
            self.db.cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = %s FOR UPDATE",
                (account_number,)
            )
            user_balance = self.db.cursor.fetchone()[0]
            
            if pay_in_full:
                # Calculate total payoff amount (remaining balance + any accrued interest)
                monthly_interest_rate = Decimal(str(float(interest_rate))) / Decimal('12') / Decimal('100')
                remaining_decimal = Decimal(str(float(remaining_balance)))
                
                # For simplicity, we'll use the remaining balance as the payoff amount
                payoff_amount = float(remaining_decimal)
                
                print(f"\n💰 LOAN PAYOFF CALCULATION:")
                print(f"   Current Remaining Balance: ₱{float(remaining_balance):,.2f}")
                print(f"   Total Payoff Amount: ₱{payoff_amount:,.2f}")
                
                if payoff_amount > float(user_balance):
                    print(f"❌ Insufficient funds for full payoff.")
                    print(f"   Required: ₱{payoff_amount:,.2f}")
                    print(f"   Available: ₱{float(user_balance):,.2f}")
                    return
                
                # Confirm payoff
                confirm = input(f"\n🎯 Pay off loan completely for ₱{payoff_amount:,.2f}? (y/N): ").lower()
                if confirm != 'y':
                    print("Payoff canceled.")
                    return
                
                payment_amount = payoff_amount
                
                # Deduct from user's account
                new_user_balance = float(user_balance) - payment_amount
                self.db.cursor.execute(
                    "UPDATE accounts SET balance = %s WHERE account_number = %s",
                    (new_user_balance, account_number)
                )
                
                # Credit to admin account
                self.db.cursor.execute(
                    "SELECT balance FROM accounts WHERE account_number = %s FOR UPDATE",
                    (self.ADMIN_ACCT_NO,)
                )
                admin_balance = self.db.cursor.fetchone()[0]
                new_admin_balance = float(admin_balance) + payment_amount
                self.db.cursor.execute(
                    "UPDATE accounts SET balance = %s WHERE account_number = %s",
                    (new_admin_balance, self.ADMIN_ACCT_NO)
                )
                
                # Mark loan as paid off
                self.db.cursor.execute(
                    "UPDATE loans SET remaining_balance = 0.00, status = 'paid_off' WHERE id = %s",
                    (loan_id,)
                )
                
                # Record the payment (all principal since we're paying off)
                principal_portion = payment_amount
                interest_portion = 0.00
                
                self.db.cursor.execute(
                    """INSERT INTO loan_payments 
                       (loan_id, account_number, payment_amount, principal_portion, 
                        interest_portion, remaining_balance, payment_type) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (loan_id, account_number, payment_amount, principal_portion, 
                     interest_portion, 0.00, 'early')
                )
                
                # Log transaction
                self.db.cursor.execute(
                    "INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'loan_payment', %s)",
                    (account_number, payment_amount)
                )
                
                self.db.commit()
                
                print("\n🎉 CONGRATULATIONS! Your loan has been paid off completely!")
                print("="*60)
                print(f"✅ Final Payment: ₱{payment_amount:,.2f}")
                print(f"💰 Your New Balance: ₱{new_user_balance:,.2f}")
                print(f"🏆 Loan Status: PAID OFF")
                print("="*60)
                print("Thank you for choosing IRNVault for your loan needs! 🏦")
                
            else:
                # Regular payment flow
                if payment_amount is None:
                    print("❌ Payment amount is required for regular payments.")
                    return
                    
                # Validate payment amount
                if payment_amount <= 0:
                    print("❌ Payment amount must be positive.")
                    return
                
                if payment_amount > float(remaining_balance):
                    print(f"❌ Payment amount (₱{payment_amount:,.2f}) exceeds remaining balance (₱{float(remaining_balance):,.2f}).")
                    print("💡 Tip: Use the 'Pay in Full' option to pay off the loan completely.")
                    return
                
                if payment_amount > float(user_balance):
                    print(f"❌ Insufficient funds. Your balance: ₱{float(user_balance):,.2f}")
                    return
                
                # Calculate interest and principal portions
                monthly_interest_rate = float(interest_rate) / 12 / 100
                interest_portion = float(remaining_balance) * monthly_interest_rate
                principal_portion = payment_amount - interest_portion
                
                if principal_portion <= 0:
                    principal_portion = payment_amount * 0.1  # At least 10% goes to principal
                    interest_portion = payment_amount - principal_portion
                
                new_remaining_balance = float(remaining_balance) - principal_portion
                
                # Deduct from user's account
                new_user_balance = float(user_balance) - payment_amount
                self.db.cursor.execute(
                    "UPDATE accounts SET balance = %s WHERE account_number = %s",
                    (new_user_balance, account_number)
                )
                
                # Credit to admin account
                self.db.cursor.execute(
                    "SELECT balance FROM accounts WHERE account_number = %s FOR UPDATE",
                    (self.ADMIN_ACCT_NO,)
                )
                admin_balance = self.db.cursor.fetchone()[0]
                new_admin_balance = float(admin_balance) + payment_amount
                self.db.cursor.execute(
                    "UPDATE accounts SET balance = %s WHERE account_number = %s",
                    (new_admin_balance, self.ADMIN_ACCT_NO)
                )
                
                # Update loan balance
                if new_remaining_balance <= 0.01:  # Loan is paid off
                    new_remaining_balance = 0
                    self.db.cursor.execute(
                        "UPDATE loans SET remaining_balance = 0, status = 'paid_off' WHERE id = %s",
                        (loan_id,)
                    )
                    print("🎉 Congratulations! Your loan has been paid off completely!")
                else:
                    # Calculate next payment date (30 days from now)
                    next_date = (datetime.now() + timedelta(days=30)).date()
                    self.db.cursor.execute(
                        "UPDATE loans SET remaining_balance = %s, next_payment_date = %s WHERE id = %s",
                        (new_remaining_balance, next_date, loan_id)
                    )
                
                # Record the payment
                self.db.cursor.execute(
                    """INSERT INTO loan_payments 
                       (loan_id, account_number, payment_amount, principal_portion, 
                        interest_portion, remaining_balance) 
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (loan_id, account_number, payment_amount, principal_portion, 
                     interest_portion, new_remaining_balance)
                )
                
                # Log transaction
                self.db.cursor.execute(
                    "INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'loan_payment', %s)",
                    (account_number, payment_amount)
                )
                
                self.db.commit()
                
                print("✅ Payment processed successfully!")
                print(f"   Payment Amount: ₱{payment_amount:,.2f}")
                print(f"   Principal Portion: ₱{principal_portion:,.2f}")
                print(f"   Interest Portion: ₱{interest_portion:,.2f}")
                print(f"   Remaining Balance: ₱{new_remaining_balance:,.2f}")
                print(f"   Your New Balance: ₱{new_user_balance:,.2f}")
            
        except Exception as e:
            self.db.rollback()
            print(f"Error processing loan payment: {e}")
        finally:
            self.db.close()
    
    def get_payoff_amount(self, account_number: str):
        """Calculate the exact payoff amount for a loan"""
        self.db.connect()
        try:
            self.db.cursor.execute(
                """SELECT remaining_balance, interest_rate FROM loans 
                   WHERE account_number = %s AND status = 'active'""",
                (account_number,)
            )
            loan_data = self.db.cursor.fetchone()
            
            if not loan_data:
                return None
            
            remaining_balance, interest_rate = loan_data
            
            # For simplicity, payoff amount is the remaining balance
            payoff_amount = float(remaining_balance)
            
            return payoff_amount
            
        except Exception as e:
            print(f"Error calculating payoff amount: {e}")
            return None
        finally:
            self.db.close()
    
    # Admin functions
    def list_pending_loans(self):
        """List all pending loan applications for admin review"""
        self.db.connect()
        try:
            self.db.cursor.execute(
                """SELECT la.id, la.account_number, a.name, la.amount, la.purpose, 
                          la.monthly_income, la.employment_status, la.applied_at
                   FROM loan_applications la
                   JOIN accounts a ON la.account_number = a.account_number
                   WHERE la.status = 'pending'
                   ORDER BY la.applied_at ASC"""
            )
            applications = self.db.cursor.fetchall()
            
            if not applications:
                print("📭 No pending loan applications.")
                return []
            
            print("\n" + "="*80)
            print("              📋 PENDING LOAN APPLICATIONS")
            print("="*80)
            
            for app_id, acct_no, name, amount, purpose, income, employment, applied in applications:
                print(f"Application #{app_id}")
                print(f"  👤 Applicant: {name} (Account: {acct_no})")
                print(f"  💰 Requested Amount: ₱{float(amount):,.2f}")
                print(f"  📝 Purpose: {purpose}")
                print(f"  💼 Employment: {employment}")
                print(f"  💵 Monthly Income: ₱{float(income):,.2f}")
                print(f"  📅 Applied: {applied.strftime('%Y-%m-%d %H:%M')}")
                
                # Calculate debt-to-income ratio
                estimated_payment = self._calculate_monthly_payment(float(amount), 12.0, 12)
                dti_ratio = (estimated_payment / float(income)) * 100
                print(f"  📊 Est. Payment: ₱{estimated_payment:,.2f} (DTI: {dti_ratio:.1f}%)")
                
                # Risk assessment
                if dti_ratio > 40:
                    print(f"  ⚠️  HIGH RISK - DTI ratio exceeds 40%")
                elif dti_ratio > 25:
                    print(f"  ⚡ MEDIUM RISK - DTI ratio above 25%")
                else:
                    print(f"  ✅ LOW RISK - Good DTI ratio")
                
                print("-" * 80)
            
            return applications
            
        except Exception as e:
            print(f"Error listing pending loans: {e}")
            return []
        finally:
            self.db.close()
    
    def _calculate_monthly_payment(self, principal: float, annual_rate: float, term_months: int) -> float:
        """Calculate monthly payment using loan amortization formula"""
        if annual_rate == 0:
            return principal / term_months
        
        monthly_rate = annual_rate / 12 / 100
        payment = principal * (monthly_rate * (1 + monthly_rate) ** term_months) / \
                 ((1 + monthly_rate) ** term_months - 1)
        return round(payment, 2)
    
    def approve_loan(self, application_id: int, interest_rate: float, term_months: int):
        """Approve a loan application and disburse funds"""
        self.db.connect()
        try:
            # Get application details
            self.db.cursor.execute(
                """SELECT account_number, amount, status 
                   FROM loan_applications WHERE id = %s""",
                (application_id,)
            )
            app_data = self.db.cursor.fetchone()
            
            if not app_data:
                print("❌ Application not found.")
                return
            
            account_number, amount, status = app_data
            
            if status != 'pending':
                print(f"❌ Application is already {status}.")
                return
            
            # Validate inputs
            if interest_rate < 0 or interest_rate > 50:
                print("❌ Interest rate must be between 0% and 50%.")
                return
            
            if term_months < 1 or term_months > 360:
                print("❌ Term must be between 1 and 360 months.")
                return
            
            # Check admin account balance
            self.db.cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = %s FOR UPDATE",
                (self.ADMIN_ACCT_NO,)
            )
            admin_balance = self.db.cursor.fetchone()[0]
            
            if float(amount) > float(admin_balance):
                print(f"❌ Insufficient funds in admin account.")
                print(f"   Required: ₱{float(amount):,.2f}")
                print(f"   Available: ₱{float(admin_balance):,.2f}")
                return
            
            # Calculate monthly payment
            monthly_payment = self._calculate_monthly_payment(float(amount), interest_rate, term_months)
            
            # Deduct from admin account
            new_admin_balance = float(admin_balance) - float(amount)
            self.db.cursor.execute(
                "UPDATE accounts SET balance = %s WHERE account_number = %s",
                (new_admin_balance, self.ADMIN_ACCT_NO)
            )
            
            # Credit to borrower's account
            self.db.cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = %s FOR UPDATE",
                (account_number,)
            )
            borrower_balance = self.db.cursor.fetchone()[0]
            new_borrower_balance = float(borrower_balance) + float(amount)
            self.db.cursor.execute(
                "UPDATE accounts SET balance = %s WHERE account_number = %s",
                (new_borrower_balance, account_number)
            )
            
            # Update application status
            self.db.cursor.execute(
                """UPDATE loan_applications 
                   SET status = 'approved', interest_rate = %s, term_months = %s, 
                       monthly_payment = %s, processed_at = NOW()
                   WHERE id = %s""",
                (interest_rate, term_months, monthly_payment, application_id)
            )
            
            # Create active loan record
            next_payment_date = (datetime.now() + timedelta(days=30)).date()
            self.db.cursor.execute(
                """INSERT INTO loans 
                   (application_id, account_number, principal_amount, interest_rate, 
                    term_months, monthly_payment, remaining_balance, next_payment_date)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (application_id, account_number, amount, interest_rate, 
                 term_months, monthly_payment, amount, next_payment_date)
            )
            
            # Log transaction
            self.db.cursor.execute(
                "INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'loan_disbursement', %s)",
                (account_number, amount)
            )
            
            self.db.commit()
            
            print("✅ Loan approved and disbursed successfully!")
            print(f"   Amount: ₱{float(amount):,.2f}")
            print(f"   Interest Rate: {interest_rate}% per year")
            print(f"   Term: {term_months} months")
            print(f"   Monthly Payment: ₱{monthly_payment:,.2f}")
            print(f"   Next Payment Due: {next_payment_date}")
            
        except Exception as e:
            self.db.rollback()
            print(f"Error approving loan: {e}")
        finally:
            self.db.close()
    
    def reject_loan(self, application_id: int, reason: str):
        """Reject a loan application"""
        self.db.connect()
        try:
            # Check if application exists and is pending
            self.db.cursor.execute(
                "SELECT status FROM loan_applications WHERE id = %s",
                (application_id,)
            )
            result = self.db.cursor.fetchone()
            
            if not result:
                print("❌ Application not found.")
                return
            
            if result[0] != 'pending':
                print(f"❌ Application is already {result[0]}.")
                return
            
            # Update application status
            self.db.cursor.execute(
                """UPDATE loan_applications 
                   SET status = 'rejected', admin_notes = %s, processed_at = NOW()
                   WHERE id = %s""",
                (reason, application_id)
            )
            
            self.db.commit()
            print(f"❌ Loan application #{application_id} rejected.")
            print(f"   Reason: {reason}")
            
        except Exception as e:
            self.db.rollback()
            print(f"Error rejecting loan: {e}")
        finally:
            self.db.close()
    
    def list_active_loans(self):
        """List all active loans for admin monitoring"""
        self.db.connect()
        try:
            self.db.cursor.execute(
                """SELECT l.id, l.account_number, a.name, l.principal_amount, 
                          l.remaining_balance, l.monthly_payment, l.next_payment_date,
                          l.interest_rate, l.disbursed_at
                   FROM loans l
                   JOIN accounts a ON l.account_number = a.account_number
                   WHERE l.status = 'active'
                   ORDER BY l.next_payment_date ASC"""
            )
            loans = self.db.cursor.fetchall()
            
            if not loans:
                print("📭 No active loans.")
                return
            
            print("\n" + "="*80)
            print("                💰 ACTIVE LOANS PORTFOLIO")
            print("="*80)
            
            total_outstanding = 0
            overdue_count = 0
            today = datetime.now().date()
            
            for loan_id, acct_no, name, principal, remaining, monthly_pay, next_date, rate, disbursed in loans:
                print(f"Loan #{loan_id}")
                print(f"  👤 Borrower: {name} (Account: {acct_no})")
                print(f"  💰 Original: ₱{float(principal):,.2f} | Remaining: ₱{float(remaining):,.2f}")
                print(f"  💵 Monthly Payment: ₱{float(monthly_pay):,.2f} | Rate: {float(rate)}%")
                print(f"  📅 Next Payment: {next_date} | Disbursed: {disbursed.strftime('%Y-%m-%d')}")
                
                # Check if overdue
                if next_date < today:
                    days_overdue = (today - next_date).days
                    print(f"  ⚠️  OVERDUE by {days_overdue} days!")
                    overdue_count += 1
                else:
                    days_until = (next_date - today).days
                    print(f"  ✅ Due in {days_until} days")
                
                total_outstanding += float(remaining)
                print("-" * 80)
            
            print(f"📊 PORTFOLIO SUMMARY:")
            print(f"   Total Active Loans: {len(loans)}")
            print(f"   Total Outstanding: ₱{total_outstanding:,.2f}")
            print(f"   Overdue Loans: {overdue_count}")
            print("="*80)
            
        except Exception as e:
            print(f"Error listing active loans: {e}")
        finally:
            self.db.close()