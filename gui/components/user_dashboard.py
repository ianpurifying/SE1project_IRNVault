# banking-app/gui/components/user_dashboard.py
"""
User Dashboard Component
Main interface for authenticated users
"""

import customtkinter as ctk
from typing import Dict, Callable, Any
import tkinter.messagebox as messagebox
from datetime import datetime

class UserDashboard:
    def __init__(self, parent, callbacks: Dict[str, Callable], user_data: Dict[str, Any], services: Dict):
        self.parent = parent
        self.callbacks = callbacks
        self.user_data = user_data
        self.services = services
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user dashboard UI"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create dashboard layout
        self.create_header()
        self.create_main_content()
    
    def create_header(self):
        """Create the dashboard header"""
        header_frame = ctk.CTkFrame(self.main_frame)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        # Left side - user info
        left_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        welcome_label = ctk.CTkLabel(
            left_frame,
            text=f"👤 Welcome, {self.user_data['name']}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#1f538d", "#4dabf7")
        )
        welcome_label.pack(anchor="w")
        
        account_label = ctk.CTkLabel(
            left_frame,
            text=f"Account: {self.user_data['account_number']}",
            font=ctk.CTkFont(size=14),
            text_color=("gray60", "gray40")
        )
        account_label.pack(anchor="w", pady=(5, 0))
        
        # Right side - balance and logout
        right_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        # Balance container with refresh button
        balance_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        balance_frame.pack(anchor="e")
        
        # Refresh button (left side of balance)
        refresh_btn = ctk.CTkButton(
            balance_frame,
            text="🔄",
            font=ctk.CTkFont(size=14),
            height=25,
            width=30,
            fg_color=("#17a2b8", "#20c997"),
            hover_color=("#138496", "#17a085"),
            command=self.refresh_balance  # Uses your existing function
        )
        refresh_btn.pack(side="left", padx=(0, 5))
        
        # Balance label
        self.balance_label = ctk.CTkLabel(
            balance_frame,
            text=f"💰 Balance: ₱{self.user_data['balance']:.2f}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#28a745", "#20c997")
        )
        self.balance_label.pack(side="left")
        
        logout_btn = ctk.CTkButton(
            right_frame,
            text="🚪 Logout",
            font=ctk.CTkFont(size=12),
            height=30,
            width=80,
            fg_color=("#dc3545", "#e74c3c"),
            hover_color=("#c82333", "#c0392b"),
            command=self.callbacks['logout']
        )
        logout_btn.pack(anchor="e", pady=(10, 0))
    
    def create_main_content(self):
        """Create the main dashboard content"""
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        # Create tabview for different sections
        self.tabview = ctk.CTkTabview(content_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("💳 Transactions")
        self.tabview.add("📊 Statements")
        self.tabview.add("ℹ️ Account Info")
        self.tabview.add("💰 Loans")
        
        # Setup tab content
        self.setup_transactions_tab()
        self.setup_statements_tab()
        self.setup_account_info_tab()
        self.setup_loans_tab()
    
    def setup_transactions_tab(self):
        """Setup the transactions tab"""
        tab = self.tabview.tab("💳 Transactions")
        
        # Transaction buttons container
        button_frame = ctk.CTkFrame(tab)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        # Deposit section
        deposit_frame = ctk.CTkFrame(button_frame)
        deposit_frame.pack(fill="x", padx=10, pady=10)
        
        deposit_title = ctk.CTkLabel(
            deposit_frame,
            text="💵 Deposit Money",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        deposit_title.pack(pady=(15, 10))
        
        self.deposit_entry = ctk.CTkEntry(
            deposit_frame,
            placeholder_text="Enter amount to deposit",
            font=ctk.CTkFont(size=14),
            height=35,
            width=200
        )
        self.deposit_entry.pack(pady=5)
        
        deposit_btn = ctk.CTkButton(
            deposit_frame,
            text="Deposit",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=35,
            width=120,
            fg_color=("#28a745", "#20c997"),
            hover_color=("#218838", "#1dd1a1"),
            command=self.handle_deposit
        )
        deposit_btn.pack(pady=(5, 15))
        
        # Withdraw section
        withdraw_frame = ctk.CTkFrame(button_frame)
        withdraw_frame.pack(fill="x", padx=10, pady=10)
        
        withdraw_title = ctk.CTkLabel(
            withdraw_frame,
            text="💸 Withdraw Money",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        withdraw_title.pack(pady=(15, 10))
        
        self.withdraw_entry = ctk.CTkEntry(
            withdraw_frame,
            placeholder_text="Enter amount to withdraw",
            font=ctk.CTkFont(size=14),
            height=35,
            width=200
        )
        self.withdraw_entry.pack(pady=5)
        
        withdraw_btn = ctk.CTkButton(
            withdraw_frame,
            text="Withdraw",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=35,
            width=120,
            fg_color=("#ffc107", "#f39c12"),
            hover_color=("#e0a800", "#e67e22"),
            command=self.handle_withdraw
        )
        withdraw_btn.pack(pady=(5, 15))
        
        # Transfer section
        transfer_frame = ctk.CTkFrame(button_frame)
        transfer_frame.pack(fill="x", padx=10, pady=10)
        
        transfer_title = ctk.CTkLabel(
            transfer_frame,
            text="🔄 Transfer Money",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        transfer_title.pack(pady=(15, 10))
        
        self.recipient_entry = ctk.CTkEntry(
            transfer_frame,
            placeholder_text="Recipient account number",
            font=ctk.CTkFont(size=14),
            height=35,
            width=200
        )
        self.recipient_entry.pack(pady=5)
        
        self.transfer_entry = ctk.CTkEntry(
            transfer_frame,
            placeholder_text="Enter amount to transfer",
            font=ctk.CTkFont(size=14),
            height=35,
            width=200
        )
        self.transfer_entry.pack(pady=5)
        
        transfer_btn = ctk.CTkButton(
            transfer_frame,
            text="Transfer",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=35,
            width=120,
            fg_color=("#17a2b8", "#3498db"),
            hover_color=("#138496", "#2980b9"),
            command=self.handle_transfer
        )
        transfer_btn.pack(pady=(5, 15))
    
    def setup_statements_tab(self):
        """Setup the statements tab"""
        tab = self.tabview.tab("📊 Statements")
        
        # Statement options
        options_frame = ctk.CTkFrame(tab)
        options_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            options_frame,
            text="📈 Transaction History",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(15, 20))
        
        # Statement buttons
        btn_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        daily_btn = ctk.CTkButton(
            btn_frame,
            text="📅 Today's Transactions",
            font=ctk.CTkFont(size=14),
            height=40,
            width=180,
            command=lambda: self.show_statement('daily')
        )
        daily_btn.pack(side="left", padx=5)
        
        monthly_btn = ctk.CTkButton(
            btn_frame,
            text="📆 This Month",
            font=ctk.CTkFont(size=14),
            height=40,
            width=140,
            command=lambda: self.show_statement('monthly')
        )
        monthly_btn.pack(side="left", padx=5)
        
        yearly_btn = ctk.CTkButton(
            btn_frame,
            text="📊 This Year",
            font=ctk.CTkFont(size=14),
            height=40,
            width=120,
            command=lambda: self.show_statement('yearly')
        )
        yearly_btn.pack(side="left", padx=5)
        
        all_btn = ctk.CTkButton(
            btn_frame,
            text="📋 All Transactions",
            font=ctk.CTkFont(size=14),
            height=40,
            width=150,
            command=lambda: self.show_statement('all')
        )
        all_btn.pack(side="left", padx=5)
        
        # Statement display area
        self.statement_frame = ctk.CTkScrollableFrame(tab)
        self.statement_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
    
    def setup_account_info_tab(self):
        """Setup the account info tab"""
        tab = self.tabview.tab("ℹ️ Account Info")
        
        info_frame = ctk.CTkFrame(tab)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            info_frame,
            text="🏦 Account Information",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Account details
        details_frame = ctk.CTkFrame(info_frame)
        details_frame.pack(fill="x", padx=20, pady=10)
        
        # Account holder name
        name_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        name_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            name_frame,
            text="Account Holder:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            name_frame,
            text=self.user_data['name'],
            font=ctk.CTkFont(size=14)
        ).pack(side="right")
        
        # Account number
        acc_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        acc_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            acc_frame,
            text="Account Number:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            acc_frame,
            text=self.user_data['account_number'],
            font=ctk.CTkFont(size=14)
        ).pack(side="right")
        
        # Current balance
        balance_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        balance_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            balance_frame,
            text="Current Balance:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        self.info_balance_label = ctk.CTkLabel(
            balance_frame,
            text=f"₱{self.user_data['balance']:.2f}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#28a745", "#20c997")
        )
        self.info_balance_label.pack(side="right")
        
        # Refresh balance button
        refresh_btn = ctk.CTkButton(
            info_frame,
            text="🔄 Refresh Balance",
            font=ctk.CTkFont(size=14),
            height=35,
            width=150,
            command=self.refresh_balance
        )
        refresh_btn.pack(pady=20)
    
    def handle_deposit(self):
        """Handle deposit transaction"""
        try:
            amount_str = self.deposit_entry.get().strip()
            if not amount_str:
                messagebox.showerror("Input Error", "Please enter an amount to deposit.")
                return
            
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Input Error", "Amount must be positive.")
                return
            
            self.services['transaction_service'].deposit(self.user_data['account_number'], amount)
            self.user_data['balance'] += amount
            self.update_balance_display()
            
            messagebox.showinfo("Success", f"Successfully deposited ₱{amount:.2f}")
            self.deposit_entry.delete(0, 'end')
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
        except Exception as e:
            messagebox.showerror("Transaction Error", f"Deposit failed: {str(e)}")
    
    def handle_withdraw(self):
        """Handle withdraw transaction"""
        try:
            amount_str = self.withdraw_entry.get().strip()
            if not amount_str:
                messagebox.showerror("Input Error", "Please enter an amount to withdraw.")
                return
            
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Input Error", "Amount must be positive.")
                return
            
            if amount > self.user_data['balance']:
                messagebox.showerror("Insufficient Funds", "You don't have enough balance.")
                return
            
            self.services['transaction_service'].withdraw(self.user_data['account_number'], amount)
            self.user_data['balance'] -= amount
            self.update_balance_display()
            
            messagebox.showinfo("Success", f"Successfully withdrew ₱{amount:.2f}")
            self.withdraw_entry.delete(0, 'end')
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
        except Exception as e:
            messagebox.showerror("Transaction Error", f"Withdrawal failed: {str(e)}")
    
    def handle_transfer(self):
        """Handle transfer transaction"""
        try:
            recipient = self.recipient_entry.get().strip()
            amount_str = self.transfer_entry.get().strip()
            
            if not recipient:
                messagebox.showerror("Input Error", "Please enter recipient account number.")
                return
            
            if not amount_str:
                messagebox.showerror("Input Error", "Please enter an amount to transfer.")
                return
            
            if len(recipient) != 10 or not recipient.isdigit():
                messagebox.showerror("Input Error", "Recipient account number must be 10 digits.")
                return
            
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Input Error", "Amount must be positive.")
                return
            
            if amount > self.user_data['balance']:
                messagebox.showerror("Insufficient Funds", "You don't have enough balance.")
                return
            
            # Check if recipient exists
            if not self.services['user_service'].get_user_by_account(recipient):
                messagebox.showerror("Transfer Error", "Recipient account not found.")
                return
            
            self.services['transaction_service'].transfer(
                self.user_data['account_number'], 
                recipient, 
                amount
            )
            self.user_data['balance'] -= amount
            self.update_balance_display()
            
            messagebox.showinfo("Success", f"Successfully transferred ₱{amount:.2f} to {recipient}")
            self.recipient_entry.delete(0, 'end')
            self.transfer_entry.delete(0, 'end')
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
        except Exception as e:
            messagebox.showerror("Transaction Error", f"Transfer failed: {str(e)}")
    
    def show_statement(self, period):
        """Show transaction statement for specified period"""
        try:
            # Clear previous statement
            for widget in self.statement_frame.winfo_children():
                widget.destroy()
            
            # Get transactions based on period
            if period == 'daily':
                transactions = self.services['statement_service'].get_daily_statement(
                    self.user_data['account_number']
                )
                title = "Today's Transactions"
            elif period == 'monthly':
                transactions = self.services['statement_service'].get_monthly_statement(
                    self.user_data['account_number']
                )
                title = "This Month's Transactions"
            elif period == 'yearly':
                transactions = self.services['statement_service'].get_yearly_statement(
                    self.user_data['account_number']
                )
                title = "This Year's Transactions"
            else:  # all
                transactions = self.services['statement_service'].get_all_transactions(
                    self.user_data['account_number']
                )
                title = "All Transactions"
            
            # Display title
            title_label = ctk.CTkLabel(
                self.statement_frame,
                text=title,
                font=ctk.CTkFont(size=16, weight="bold")
            )
            title_label.pack(pady=(10, 20))
            
            if not transactions:
                no_data_label = ctk.CTkLabel(
                    self.statement_frame,
                    text="No transactions found for this period.",
                    font=ctk.CTkFont(size=14),
                    text_color=("gray60", "gray40")
                )
                no_data_label.pack(pady=20)
                return
            
            # Display transactions
            for i, txn in enumerate(transactions):
                txn_frame = ctk.CTkFrame(self.statement_frame)
                txn_frame.pack(fill="x", padx=10, pady=5)
                
                # Transaction type and amount
                left_frame = ctk.CTkFrame(txn_frame, fg_color="transparent")
                left_frame.pack(side="left", fill="y", padx=10, pady=10)
                
                type_label = ctk.CTkLabel(
                    left_frame,
                    text=txn['type'].title(),
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                type_label.pack(anchor="w")
                
                # Check if transaction type should be green (positive) or red (negative)
                if txn['type'] in ['deposit', 'transfer_in', 'loan_disbursement']:
                    amount_color = ("#28a745", "#20c997")  # Green colors
                    amount_prefix = "+"
                else:
                    amount_color = ("#dc3545", "#e74c3c")  # Red colors  
                    amount_prefix = "-"
                
                amount_label = ctk.CTkLabel(
                    left_frame,
                    text=f"{amount_prefix}₱{txn['amount']:.2f}",
                    font=ctk.CTkFont(size=12),
                    text_color=amount_color
                )
                amount_label.pack(anchor="w")
                
                # Date
                date_label = ctk.CTkLabel(
                    txn_frame,
                    text=txn['timestamp'],
                    font=ctk.CTkFont(size=11),
                    text_color=("gray60", "gray40")
                )
                date_label.pack(side="right", padx=10, pady=10)
                
        except Exception as e:
            messagebox.showerror("Statement Error", f"Error retrieving statement: {str(e)}")
    
    def refresh_balance(self):
        """Refresh balance from database"""
        try:
            user = self.services['user_service'].get_user_by_account(self.user_data['account_number'])
            if user:
                self.user_data['balance'] = user['balance']
                self.update_balance_display()
                messagebox.showinfo("Success", "Balance refreshed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh balance: {str(e)}")
    
    def update_balance_display(self):
        """Update balance display in UI"""
        self.balance_label.configure(text=f"💰 Balance: ₱{self.user_data['balance']:.2f}")
        self.info_balance_label.configure(text=f"₱{self.user_data['balance']:.2f}")

    def setup_loans_tab(self):
        """Setup the loans tab"""
        tab = self.tabview.tab("💰 Loans")
        
        # Main container with scrollable frame
        main_container = ctk.CTkScrollableFrame(tab)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Loans action buttons
        actions_frame = ctk.CTkFrame(main_container)
        actions_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            actions_frame,
            text="💰 Loan Services",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(15, 20))
        
        # Action buttons container
        buttons_container = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_container.pack(pady=(0, 15))
        
        apply_btn = ctk.CTkButton(
            buttons_container,
            text="📝 Apply for Loan",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=150,
            fg_color=("#28a745", "#20c997"),
            hover_color=("#218838", "#1dd1a1"),
            command=self.show_loan_application
        )
        apply_btn.pack(side="left", padx=5)
        
        status_btn = ctk.CTkButton(
            buttons_container,
            text="📊 Loan Status",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=140,
            fg_color=("#17a2b8", "#3498db"),
            hover_color=("#138496", "#2980b9"),
            command=self.show_loan_status
        )
        status_btn.pack(side="left", padx=5)
        
        payment_btn = ctk.CTkButton(
            buttons_container,
            text="💳 Make Payment",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=140,
            fg_color=("#ffc107", "#f39c12"),
            hover_color=("#e0a800", "#e67e22"),
            command=self.show_loan_payment
        )
        payment_btn.pack(side="left", padx=5)
        
        # Content display area
        self.loans_content_frame = ctk.CTkFrame(main_container)
        self.loans_content_frame.pack(fill="both", expand=True)
        
        # Initially show loan status
        self.show_loan_status()

    def show_loan_application(self):
        """Display loan application form"""
        # Clear content
        for widget in self.loans_content_frame.winfo_children():
            widget.destroy()
        
        # Application form
        form_frame = ctk.CTkFrame(self.loans_content_frame)
        form_frame.pack(fill="x", padx=20, pady=20)
        
        title = ctk.CTkLabel(
            form_frame,
            text="📝 Loan Application Form",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(20, 30))
        
        # Loan Amount
        amount_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        amount_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            amount_frame,
            text="Loan Amount (₱):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        self.loan_amount_entry = ctk.CTkEntry(
            amount_frame,
            placeholder_text="Enter loan amount",
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.loan_amount_entry.pack(fill="x", pady=(5, 0))
        
        # Purpose
        purpose_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        purpose_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            purpose_frame,
            text="Loan Purpose:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        self.loan_purpose_var = ctk.StringVar(value="investment")
        purpose_options = ["investment", "education", "home_improvement", "business", "personal", "other"]
        
        self.loan_purpose_menu = ctk.CTkOptionMenu(
            purpose_frame,
            variable=self.loan_purpose_var,
            values=purpose_options,
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.loan_purpose_menu.pack(fill="x", pady=(5, 0))
        
        # Monthly Income
        income_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        income_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            income_frame,
            text="Monthly Income (₱):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        self.monthly_income_entry = ctk.CTkEntry(
            income_frame,
            placeholder_text="Enter monthly income",
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.monthly_income_entry.pack(fill="x", pady=(5, 0))
        
        # Employment Type
        employment_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        employment_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            employment_frame,
            text="Employment Type:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        self.employment_var = ctk.StringVar(value="full-time")
        employment_options = ["full-time", "part-time", "freelance", "self-employed", "unemployed"]
        
        self.employment_menu = ctk.CTkOptionMenu(
            employment_frame,
            variable=self.employment_var,
            values=employment_options,
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.employment_menu.pack(fill="x", pady=(5, 0))
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(20, 30))
        
        submit_btn = ctk.CTkButton(
            button_frame,
            text="Submit Application",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=150,
            fg_color=("#28a745", "#20c997"),
            hover_color=("#218838", "#1dd1a1"),
            command=self.submit_loan_application
        )
        submit_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=ctk.CTkFont(size=14),
            height=40,
            width=100,
            fg_color=("#6c757d", "#495057"),
            hover_color=("#5a6268", "#343a40"),
            command=self.show_loan_status
        )
        cancel_btn.pack(side="left")

    def submit_loan_application(self):
        """Submit loan application"""
        try:
            # Validate inputs
            amount_str = self.loan_amount_entry.get().strip()
            income_str = self.monthly_income_entry.get().strip()
            
            if not amount_str:
                messagebox.showerror("Input Error", "Please enter loan amount.")
                return
            
            if not income_str:
                messagebox.showerror("Input Error", "Please enter monthly income.")
                return
            
            amount = float(amount_str)
            income = float(income_str)
            
            if amount <= 0:
                messagebox.showerror("Input Error", "Loan amount must be positive.")
                return
            
            if income <= 0:
                messagebox.showerror("Input Error", "Monthly income must be positive.")
                return
            
            # Submit application
            application_id = self.services['loan_service'].apply_for_loan(
                self.user_data['account_number'],
                amount,
                self.loan_purpose_var.get(),
                income,
                self.employment_var.get()
            )
            
            messagebox.showinfo(
                "Success", 
                f"Loan application submitted successfully!\nApplication ID: {application_id}\n\nYour application is now under review."
            )
            
            # Clear form and show status
            self.show_loan_status()
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
        except Exception as e:
            messagebox.showerror("Application Error", f"Failed to submit application: {str(e)}")

    def show_loan_status(self):
        """Display loan status and history"""
        # Clear content
        for widget in self.loans_content_frame.winfo_children():
            widget.destroy()
        
        try:
            # Get loan applications and active loans
            applications = self.services['loan_service'].get_loan_applications(self.user_data['account_number'])
            active_loans = self.services['loan_service'].get_active_loans(self.user_data['account_number'])
            
            # Status container
            status_frame = ctk.CTkFrame(self.loans_content_frame)
            status_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            title = ctk.CTkLabel(
                status_frame,
                text="📊 Loan Status & History",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            title.pack(pady=(20, 30))
            
            # Active Loans Section
            if active_loans:
                active_title = ctk.CTkLabel(
                    status_frame,
                    text="🔥 Active Loans",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=("#28a745", "#20c997")
                )
                active_title.pack(anchor="w", padx=20, pady=(0, 10))
                
                for loan in active_loans:
                    loan_frame = ctk.CTkFrame(status_frame)
                    loan_frame.pack(fill="x", padx=20, pady=5)
                    
                    # Loan details
                    details_frame = ctk.CTkFrame(loan_frame, fg_color="transparent")
                    details_frame.pack(fill="x", padx=15, pady=10)
                    
                    # Left side - loan info
                    left_info = ctk.CTkFrame(details_frame, fg_color="transparent")
                    left_info.pack(side="left", fill="y")
                    
                    ctk.CTkLabel(
                        left_info,
                        text=f"Purpose: {loan['purpose']}",
                        font=ctk.CTkFont(size=12, weight="bold")
                    ).pack(anchor="w")
                    
                    ctk.CTkLabel(
                        left_info,
                        text=f"Principal: ₱{loan['principal_amount']:.2f}",
                        font=ctk.CTkFont(size=11)
                    ).pack(anchor="w")
                    
                    ctk.CTkLabel(
                        left_info,
                        text=f"Monthly Payment: ₱{loan['monthly_payment']:.2f}",
                        font=ctk.CTkFont(size=11)
                    ).pack(anchor="w")
                    
                    # Right side - balance info
                    right_info = ctk.CTkFrame(details_frame, fg_color="transparent")
                    right_info.pack(side="right", fill="y")
                    
                    ctk.CTkLabel(
                        right_info,
                        text=f"Remaining: ₱{loan['remaining_balance']:.2f}",
                        font=ctk.CTkFont(size=12, weight="bold"),
                        text_color=("#dc3545", "#e74c3c")
                    ).pack(anchor="e")
                    
                    ctk.CTkLabel(
                        right_info,
                        text=f"Next Payment: {loan['next_payment_date']}",
                        font=ctk.CTkFont(size=11)
                    ).pack(anchor="e")
                    
                    ctk.CTkLabel(
                        right_info,
                        text=f"Interest Rate: {loan['interest_rate']:.2f}%",
                        font=ctk.CTkFont(size=11)
                    ).pack(anchor="e")
            
            # Applications Section
            if applications:
                apps_title = ctk.CTkLabel(
                    status_frame,
                    text="📋 Application History",
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                apps_title.pack(anchor="w", padx=20, pady=(20, 10))
                
                for app in applications:
                    app_frame = ctk.CTkFrame(status_frame)
                    app_frame.pack(fill="x", padx=20, pady=5)
                    
                    app_details = ctk.CTkFrame(app_frame, fg_color="transparent")
                    app_details.pack(fill="x", padx=15, pady=10)
                    
                    # Left side
                    left_app = ctk.CTkFrame(app_details, fg_color="transparent")
                    left_app.pack(side="left", fill="y")
                    
                    ctk.CTkLabel(
                        left_app,
                        text=f"Amount: ₱{app['amount']:.2f} - {app['purpose']}",
                        font=ctk.CTkFont(size=12, weight="bold")
                    ).pack(anchor="w")
                    
                    ctk.CTkLabel(
                        left_app,
                        text=f"Applied: {app['applied_at'].strftime('%Y-%m-%d')}",
                        font=ctk.CTkFont(size=11)
                    ).pack(anchor="w")
                    
                    # Right side - status
                    status_color = {
                        'pending': ("#ffc107", "#f39c12"),
                        'approved': ("#28a745", "#20c997"),
                        'rejected': ("#dc3545", "#e74c3c")
                    }
                    
                    ctk.CTkLabel(
                        app_details,
                        text=app['status'].upper(),
                        font=ctk.CTkFont(size=12, weight="bold"),
                        text_color=status_color.get(app['status'], ("gray60", "gray40"))
                    ).pack(side="right", padx=15, pady=15)
            
            if not applications and not active_loans:
                no_data_label = ctk.CTkLabel(
                    status_frame,
                    text="No loan applications or active loans found.\nClick 'Apply for Loan' to get started!",
                    font=ctk.CTkFont(size=14),
                    text_color=("gray60", "gray40")
                )
                no_data_label.pack(pady=50)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load loan status: {str(e)}")

    def show_loan_payment(self):
        """Display loan payment interface"""
        # Clear content
        for widget in self.loans_content_frame.winfo_children():
            widget.destroy()
        
        try:
            # Get active loans
            active_loans = self.services['loan_service'].get_active_loans(self.user_data['account_number'])
            
            if not active_loans:
                # No active loans
                no_loans_frame = ctk.CTkFrame(self.loans_content_frame)
                no_loans_frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                ctk.CTkLabel(
                    no_loans_frame,
                    text="💳 No Active Loans",
                    font=ctk.CTkFont(size=16, weight="bold")
                ).pack(pady=(50, 20))
                
                ctk.CTkLabel(
                    no_loans_frame,
                    text="You don't have any active loans to make payments on.",
                    font=ctk.CTkFont(size=14),
                    text_color=("gray60", "gray40")
                ).pack(pady=20)
                
                return
            
            # Payment form
            payment_frame = ctk.CTkFrame(self.loans_content_frame)
            payment_frame.pack(fill="x", padx=20, pady=20)
            
            title = ctk.CTkLabel(
                payment_frame,
                text="💳 Make Loan Payment",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            title.pack(pady=(20, 30))
            
            # Loan selection
            loan_frame = ctk.CTkFrame(payment_frame, fg_color="transparent")
            loan_frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(
                loan_frame,
                text="Select Loan:",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(anchor="w")
            
            # Create loan options with readable format
            loan_options = []
            self.loan_mapping = {}
            
            for loan in active_loans:
                option_text = f"{loan['purpose']} - Balance: ₱{loan['remaining_balance']:.2f}"
                loan_options.append(option_text)
                self.loan_mapping[option_text] = loan
            
            self.selected_loan_var = ctk.StringVar(value=loan_options[0])
            self.loan_select_menu = ctk.CTkOptionMenu(
                loan_frame,
                variable=self.selected_loan_var,
                values=loan_options,
                font=ctk.CTkFont(size=14),
                height=35,
                command=self.update_payment_info
            )
            self.loan_select_menu.pack(fill="x", pady=(5, 0))
            
            # Payment info display
            self.payment_info_frame = ctk.CTkFrame(payment_frame)
            self.payment_info_frame.pack(fill="x", padx=20, pady=15)
            
            # Payment amount options
            amount_frame = ctk.CTkFrame(payment_frame, fg_color="transparent")
            amount_frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(
                amount_frame,
                text="Payment Options:",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(anchor="w", pady=(0, 10))
            
            # Payment type selection
            self.payment_type_var = ctk.StringVar(value="monthly")
            
            monthly_radio = ctk.CTkRadioButton(
                amount_frame,
                text="Monthly Payment",
                variable=self.payment_type_var,
                value="monthly",
                font=ctk.CTkFont(size=12),
                command=self.update_payment_amount
            )
            monthly_radio.pack(anchor="w", pady=2)
            
            partial_radio = ctk.CTkRadioButton(
                amount_frame,
                text="Partial Payment (Custom Amount)",
                variable=self.payment_type_var,
                value="partial",
                font=ctk.CTkFont(size=12),
                command=self.update_payment_amount
            )
            partial_radio.pack(anchor="w", pady=2)
            
            full_radio = ctk.CTkRadioButton(
                amount_frame,
                text="Pay in Full",
                variable=self.payment_type_var,
                value="full",
                font=ctk.CTkFont(size=12),
                command=self.update_payment_amount
            )
            full_radio.pack(anchor="w", pady=2)
            
            # Payment amount entry
            self.payment_amount_frame = ctk.CTkFrame(payment_frame, fg_color="transparent")
            self.payment_amount_frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(
                self.payment_amount_frame,
                text="Payment Amount (₱):",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(anchor="w")
            
            self.payment_amount_entry = ctk.CTkEntry(
                self.payment_amount_frame,
                placeholder_text="Payment amount",
                font=ctk.CTkFont(size=14),
                height=35
            )
            
            self.payment_amount_entry.pack(fill="x", pady=(5, 0))

            # Buttons
            button_frame = ctk.CTkFrame(payment_frame, fg_color="transparent")
            button_frame.pack(fill="x", padx=20, pady=(20, 30))
            
            process_btn = ctk.CTkButton(
                button_frame,
                text="Process Payment",
                font=ctk.CTkFont(size=14, weight="bold"),
                height=40,
                width=150,
                fg_color=("#28a745", "#20c997"),
                hover_color=("#218838", "#1dd1a1"),
                command=self.process_loan_payment
            )
            process_btn.pack(side="left", padx=(0, 10))
            
            cancel_btn = ctk.CTkButton(
                button_frame,
                text="Cancel",
                font=ctk.CTkFont(size=14),
                height=40,
                width=100,
                fg_color=("#6c757d", "#495057"),
                hover_color=("#5a6268", "#343a40"),
                command=self.show_loan_status
            )
            cancel_btn.pack(side="left")
            
            # Initialize payment info
            self.update_payment_info()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load payment interface: {str(e)}")

    def update_payment_info(self, *args):
        """Update payment information display"""
        try:
            # Clear existing info
            for widget in self.payment_info_frame.winfo_children():
                widget.destroy()
            
            # Get selected loan
            selected_option = self.selected_loan_var.get()
            loan = self.loan_mapping[selected_option]
            
            # Display loan information
            info_title = ctk.CTkLabel(
                self.payment_info_frame,
                text="📋 Loan Information",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            info_title.pack(pady=(15, 10))
            
            # Create info grid
            info_grid = ctk.CTkFrame(self.payment_info_frame, fg_color="transparent")
            info_grid.pack(fill="x", padx=15, pady=(0, 15))
            
            # Left column
            left_col = ctk.CTkFrame(info_grid, fg_color="transparent")
            left_col.pack(side="left", fill="both", expand=True)
            
            ctk.CTkLabel(
                left_col,
                text=f"Purpose: {loan['purpose']}",
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w", pady=2)
            
            ctk.CTkLabel(
                left_col,
                text=f"Principal Amount: ₱{loan['principal_amount']:.2f}",
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w", pady=2)
            
            ctk.CTkLabel(
                left_col,
                text=f"Interest Rate: {loan['interest_rate']:.2f}%",
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w", pady=2)
            
            # Right column
            right_col = ctk.CTkFrame(info_grid, fg_color="transparent")
            right_col.pack(side="right", fill="both", expand=True)
            
            ctk.CTkLabel(
                right_col,
                text=f"Remaining Balance: ₱{loan['remaining_balance']:.2f}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=("#dc3545", "#e74c3c")
            ).pack(anchor="e", pady=2)
            
            ctk.CTkLabel(
                right_col,
                text=f"Monthly Payment: ₱{loan['monthly_payment']:.2f}",
                font=ctk.CTkFont(size=12)
            ).pack(anchor="e", pady=2)
            
            ctk.CTkLabel(
                right_col,
                text=f"Next Due: {loan['next_payment_date']}",
                font=ctk.CTkFont(size=12)
            ).pack(anchor="e", pady=2)
            
            # Update payment amount based on current selection
            self.update_payment_amount()
            
        except Exception as e:
            print(f"Error updating payment info: {str(e)}")

    def update_payment_amount(self):
        """Update payment amount based on selection"""
        try:
            selected_option = self.selected_loan_var.get()
            loan = self.loan_mapping[selected_option]
            payment_type = self.payment_type_var.get()
            
            if payment_type == "monthly":
                # Set to monthly payment amount
                self.payment_amount_entry.delete(0, 'end')
                self.payment_amount_entry.insert(0, f"{loan['monthly_payment']:.2f}")
                self.payment_amount_entry.configure(state="disabled")
                
            elif payment_type == "full":
                # Set to remaining balance
                self.payment_amount_entry.delete(0, 'end')
                self.payment_amount_entry.insert(0, f"{loan['remaining_balance']:.2f}")
                self.payment_amount_entry.configure(state="disabled")
                
            else:  # partial
                # Enable custom entry
                self.payment_amount_entry.configure(state="normal")
                self.payment_amount_entry.delete(0, 'end')
                
        except Exception as e:
            print(f"Error updating payment amount: {str(e)}")

    def process_loan_payment(self):
        """Process the loan payment"""
        try:
            # Get selected loan
            selected_option = self.selected_loan_var.get()
            loan = self.loan_mapping[selected_option]
            
            # Validate payment amount
            amount_str = self.payment_amount_entry.get().strip()
            if not amount_str:
                messagebox.showerror("Input Error", "Please enter payment amount.")
                return
            
            try:
                payment_amount = float(amount_str)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid payment amount.")
                return
            
            if payment_amount <= 0:
                messagebox.showerror("Input Error", "Payment amount must be positive.")
                return
            
            if payment_amount > loan['remaining_balance']:
                messagebox.showerror("Input Error", "Payment amount cannot exceed remaining balance.")
                return
            
            # Determine payment type for recording
            payment_type = self.payment_type_var.get()
            if payment_type == "monthly":
                record_type = "regular"
            elif payment_type == "full":
                record_type = "full_payment"
            else:
                record_type = "partial"
            
            # Confirm payment
            confirm_msg = f"Confirm payment of ₱{payment_amount:.2f} for {loan['purpose']} loan?"
            if not messagebox.askyesno("Confirm Payment", confirm_msg):
                return
            
            # Check account balance (assuming you have a method to get account balance)
            # You might want to add this check based on your account service
            
            # Process payment
            success = self.services['loan_service'].make_loan_payment(
                loan['id'],
                self.user_data['account_number'],
                payment_amount,
                record_type
            )
            
            if success:
                # Show success message
                remaining_after = loan['remaining_balance'] - payment_amount
                if remaining_after <= 0:
                    success_msg = f"Payment of ₱{payment_amount:.2f} processed successfully!\n\nCongratulations! Your loan has been paid in full! 🎉"
                else:
                    success_msg = f"Payment of ₱{payment_amount:.2f} processed successfully!\n\nRemaining balance: ₱{remaining_after:.2f}"
                
                messagebox.showinfo("Payment Successful", success_msg)
                
                # Refresh the loan status view
                self.show_loan_status()
                
            else:
                messagebox.showerror("Payment Error", "Failed to process payment. Please try again.")
                
        except Exception as e:
            messagebox.showerror("Payment Error", f"Payment processing failed: {str(e)}")

    def get_loan_payment_history_display(self):
        """Display loan payment history (optional method)"""
        try:
            # Get payment history
            payment_history = self.services['loan_service'].get_loan_payment_history(
                self.user_data['account_number']
            )
            
            if not payment_history:
                return "No payment history found."
            
            # Format payment history for display
            history_text = "Recent Payments:\n\n"
            for payment in payment_history[:5]:  # Show last 5 payments
                history_text += f"Date: {payment['payment_date']}\n"
                history_text += f"Amount: ₱{payment['payment_amount']:.2f}\n"
                history_text += f"Principal: ₱{payment['principal_portion']:.2f}\n"
                history_text += f"Interest: ₱{payment['interest_portion']:.2f}\n"
                history_text += f"Balance After: ₱{payment['remaining_balance']:.2f}\n"
                history_text += "-" * 40 + "\n"
            
            return history_text
            
        except Exception as e:
            return f"Error loading payment history: {str(e)}"

    def destroy(self):
        """Clean up the window"""
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()