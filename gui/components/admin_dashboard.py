# banking-app/gui/components/admin_dashboard.py
"""
Admin Dashboard Component
Administrative interface for managing users and accounts
"""

import customtkinter as ctk
from typing import Dict, Callable, Any
import tkinter.messagebox as messagebox

class AdminDashboard:
    def __init__(self, parent, callbacks: Dict[str, Callable], admin_data: Dict[str, Any], admin_service):
        self.parent = parent
        self.callbacks = callbacks
        self.admin_data = admin_data
        self.admin_service = admin_service
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the admin dashboard UI"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create dashboard layout
        self.create_header()
        self.create_main_content()
    
    def create_header(self):
        """Create the admin dashboard header"""
        header_frame = ctk.CTkFrame(self.main_frame)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        # Left side - admin info
        left_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        welcome_label = ctk.CTkLabel(
            left_frame,
            text=f"👨‍💼 Admin Panel - Welcome, {self.admin_data['name']}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#dc3545", "#e74c3c")
        )
        welcome_label.pack(anchor="w")
        
        admin_label = ctk.CTkLabel(
            left_frame,
            text="System Administrator",
            font=ctk.CTkFont(size=14),
            text_color=("gray60", "gray40")
        )
        admin_label.pack(anchor="w", pady=(5, 0))
        
        # Right side - logout
        right_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        logout_btn = ctk.CTkButton(
            right_frame,
            text="🚪 Logout",
            font=ctk.CTkFont(size=12),
            height=30,
            width=80,
            fg_color=("#6c757d", "#495057"),
            hover_color=("#5a6268", "#343a40"),
            command=self.callbacks['logout']
        )
        logout_btn.pack(anchor="e")
    
    def create_main_content(self):
        """Create the main admin dashboard content"""
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        # Create tabview for different admin sections
        self.tabview = ctk.CTkTabview(content_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("⏳ Pending Accounts")
        self.tabview.add("👥 All Users")
        self.tabview.add("💰 Loan Management")  # NEW TAB
        self.tabview.add("⚙️ Admin Actions")
        
        # Setup tab content
        self.setup_pending_accounts_tab()
        self.setup_all_users_tab()
        self.setup_loan_management_tab()  # NEW TAB SETUP
        self.setup_admin_actions_tab()
        
        # Load initial data
        self.refresh_pending_accounts()
        self.refresh_all_users()
        self.refresh_loan_data()  # NEW DATA REFRESH
    
    def setup_pending_accounts_tab(self):
        """Setup the pending accounts tab"""
        tab = self.tabview.tab("⏳ Pending Accounts")
        
        # Header with refresh button
        header_frame = ctk.CTkFrame(tab)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📋 Accounts Awaiting Approval",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=15, pady=10)
        
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            font=ctk.CTkFont(size=12),
            height=30,
            width=80,
            command=self.refresh_pending_accounts
        )
        refresh_btn.pack(side="right", padx=15, pady=10)
        
        # Scrollable frame for pending accounts
        self.pending_frame = ctk.CTkScrollableFrame(tab)
        self.pending_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
    
    def setup_all_users_tab(self):
        """Setup the all users tab"""
        tab = self.tabview.tab("👥 All Users")
        
        # Header with refresh button
        header_frame = ctk.CTkFrame(tab)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="👥 All System Users",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=15, pady=10)
        
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            font=ctk.CTkFont(size=12),
            height=30,
            width=80,
            command=self.refresh_all_users
        )
        refresh_btn.pack(side="right", padx=15, pady=10)
        
        # Scrollable frame for all users
        self.users_frame = ctk.CTkScrollableFrame(tab)
        self.users_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
    
    def setup_admin_actions_tab(self):
        """Setup the admin actions tab"""
        tab = self.tabview.tab("⚙️ Admin Actions")
        
        # Manual account actions
        actions_frame = ctk.CTkFrame(tab)
        actions_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            actions_frame,
            text="🛠️ Manual Account Management",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(15, 20))
        
        # Approve account section
        approve_frame = ctk.CTkFrame(actions_frame)
        approve_frame.pack(fill="x", padx=15, pady=10)
        
        approve_title = ctk.CTkLabel(
            approve_frame,
            text="✅ Approve Account",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#28a745", "#20c997")
        )
        approve_title.pack(pady=(10, 5))
        
        self.approve_entry = ctk.CTkEntry(
            approve_frame,
            placeholder_text="Enter account number to approve",
            font=ctk.CTkFont(size=12),
            height=35,
            width=250
        )
        self.approve_entry.pack(pady=5)
        
        approve_btn = ctk.CTkButton(
            approve_frame,
            text="Approve Account",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            width=150,
            fg_color=("#28a745", "#20c997"),
            hover_color=("#218838", "#1dd1a1"),
            command=self.manual_approve_account
        )
        approve_btn.pack(pady=(5, 15))
        
        # Reject account section
        reject_frame = ctk.CTkFrame(actions_frame)
        reject_frame.pack(fill="x", padx=15, pady=10)
        
        reject_title = ctk.CTkLabel(
            reject_frame,
            text="❌ Reject Account",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#dc3545", "#e74c3c")
        )
        reject_title.pack(pady=(10, 5))
        
        self.reject_entry = ctk.CTkEntry(
            reject_frame,
            placeholder_text="Enter account number to reject",
            font=ctk.CTkFont(size=12),
            height=35,
            width=250
        )
        self.reject_entry.pack(pady=5)
        
        self.reason_entry = ctk.CTkEntry(
            reject_frame,
            placeholder_text="Enter reason for rejection",
            font=ctk.CTkFont(size=12),
            height=35,
            width=250
        )
        self.reason_entry.pack(pady=5)
        
        reject_btn = ctk.CTkButton(
            reject_frame,
            text="Reject Account",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            width=150,
            fg_color=("#dc3545", "#e74c3c"),
            hover_color=("#c82333", "#c0392b"),
            command=self.manual_reject_account
        )
        reject_btn.pack(pady=(5, 15))
    
    def refresh_pending_accounts(self):
        """Refresh and display pending accounts"""
        try:
            # Clear existing content
            for widget in self.pending_frame.winfo_children():
                widget.destroy()
            
            # Get pending accounts
            pending_accounts = self.admin_service.get_pending_accounts()
            
            if not pending_accounts:
                no_pending_label = ctk.CTkLabel(
                    self.pending_frame,
                    text="✅ No pending accounts at this time.",
                    font=ctk.CTkFont(size=14),
                    text_color=("gray60", "gray40")
                )
                no_pending_label.pack(pady=50)
                return
            
            # Display pending accounts
            for account in pending_accounts:
                account_frame = ctk.CTkFrame(self.pending_frame)
                account_frame.pack(fill="x", padx=10, pady=5)
                
                # Account info
                info_frame = ctk.CTkFrame(account_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
                
                name_label = ctk.CTkLabel(
                    info_frame,
                    text=f"👤 {account['name']}",
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                name_label.pack(anchor="w")
                
                account_label = ctk.CTkLabel(
                    info_frame,
                    text=f"Account: {account['account_number']}",
                    font=ctk.CTkFont(size=12)
                )
                account_label.pack(anchor="w")
                
                date_label = ctk.CTkLabel(
                    info_frame,
                    text=f"Created: {account['created_at']}",
                    font=ctk.CTkFont(size=11),
                    text_color=("gray60", "gray40")
                )
                date_label.pack(anchor="w")
                
                # Action buttons
                button_frame = ctk.CTkFrame(account_frame, fg_color="transparent")
                button_frame.pack(side="right", padx=15, pady=10)
                
                approve_btn = ctk.CTkButton(
                    button_frame,
                    text="✅ Approve",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    height=30,
                    width=80,
                    fg_color=("#28a745", "#20c997"),
                    hover_color=("#218838", "#1dd1a1"),
                    command=lambda acc_num=account['account_number']: self.approve_account(acc_num)
                )
                approve_btn.pack(side="top", pady=(0, 5))
                
                reject_btn = ctk.CTkButton(
                    button_frame,
                    text="❌ Reject",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    height=30,
                    width=80,
                    fg_color=("#dc3545", "#e74c3c"),
                    hover_color=("#c82333", "#c0392b"),
                    command=lambda acc_num=account['account_number']: self.reject_account_with_reason(acc_num)
                )
                reject_btn.pack(side="top")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing pending accounts: {str(e)}")
    
    def refresh_all_users(self):
        """Refresh and display all users"""
        try:
            # Clear existing content
            for widget in self.users_frame.winfo_children():
                widget.destroy()
            
            # Get all users
            all_users = self.admin_service.get_all_users()
            
            if not all_users:
                no_users_label = ctk.CTkLabel(
                    self.users_frame,
                    text="No users found in the system.",
                    font=ctk.CTkFont(size=14),
                    text_color=("gray60", "gray40")
                )
                no_users_label.pack(pady=50)
                return
            
            # Create header
            header_frame = ctk.CTkFrame(self.users_frame)
            header_frame.pack(fill="x", padx=10, pady=(10, 5))
            
            header_label = ctk.CTkLabel(
                header_frame,
                text=f"{'Account Number':<15} {'Name':<20} {'Balance':<12} {'Status':<10}",
                font=ctk.CTkFont(size=12, weight="bold", family="Courier"),
                text_color=("#495057", "#6c757d")
            )
            header_label.pack(pady=10)
            
            # Display all users
            for user in all_users:
                user_frame = ctk.CTkFrame(self.users_frame)
                user_frame.pack(fill="x", padx=10, pady=2)
                
                status = "✅ Approved" if user['is_approved'] else "⏳ Pending"
                status_color = ("#28a745", "#20c997") if user['is_approved'] else ("#ffc107", "#f39c12")
                
                # User info display
                info_text = f"{user['account_number']:<15} {user['name']:<20} ₱{user['balance']:<11.2f} {status}"
                
                user_label = ctk.CTkLabel(
                    user_frame,
                    text=info_text,
                    font=ctk.CTkFont(size=11, family="Courier"),
                    text_color=status_color
                )
                user_label.pack(pady=8, padx=15, anchor="w")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing users: {str(e)}")
    
    def approve_account(self, account_number):
        """Approve a specific account"""
        try:
            if self.admin_service.approve_account(account_number):
                messagebox.showinfo("Success", f"Account {account_number} approved successfully!")
                self.refresh_pending_accounts()
                self.refresh_all_users()
            else:
                messagebox.showerror("Error", "Account not found or already approved.")
        except Exception as e:
            messagebox.showerror("Error", f"Error approving account: {str(e)}")
    
    def reject_account_with_reason(self, account_number):
        """Reject account with reason dialog"""
        # Create dialog for rejection reason
        dialog = ctk.CTkInputDialog(
            text=f"Enter reason for rejecting account {account_number}:",
            title="Reject Account"
        )
        reason = dialog.get_input()
        
        if reason:
            try:
                if self.admin_service.reject_account(account_number, reason):
                    messagebox.showinfo("Success", f"Account {account_number} rejected successfully!")
                    self.refresh_pending_accounts()
                    self.refresh_all_users()
                else:
                    messagebox.showerror("Error", "Account not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Error rejecting account: {str(e)}")
    
    def manual_approve_account(self):
        """Manually approve account from entry field"""
        account_number = self.approve_entry.get().strip()
        
        if not account_number:
            messagebox.showerror("Error", "Please enter an account number.")
            return
        
        try:
            if self.admin_service.approve_account(account_number):
                messagebox.showinfo("Success", f"Account {account_number} approved successfully!")
                self.approve_entry.delete(0, 'end')
                self.refresh_pending_accounts()
                self.refresh_all_users()
            else:
                messagebox.showerror("Error", "Account not found or already approved.")
        except Exception as e:
            messagebox.showerror("Error", f"Error approving account: {str(e)}")
    
    def manual_reject_account(self):
        """Manually reject account from entry fields"""
        account_number = self.reject_entry.get().strip()
        reason = self.reason_entry.get().strip()
        
        if not account_number:
            messagebox.showerror("Error", "Please enter an account number.")
            return
        
        if not reason:
            messagebox.showerror("Error", "Please enter a reason for rejection.")
            return
        
        try:
            if self.admin_service.reject_account(account_number, reason):
                messagebox.showinfo("Success", f"Account {account_number} rejected successfully!")
                self.reject_entry.delete(0, 'end')
                self.reason_entry.delete(0, 'end')
                self.refresh_pending_accounts()
                self.refresh_all_users()
            else:
                messagebox.showerror("Error", "Account not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error rejecting account: {str(e)}")


    def setup_loan_management_tab(self):
        """Setup the loan management tab"""
        tab = self.tabview.tab("💰 Loan Management")
        
        # Create sub-tabview for loan sections
        self.loan_tabview = ctk.CTkTabview(tab)
        self.loan_tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add loan sub-tabs
        self.loan_tabview.add("⏳ Pending Loans")
        self.loan_tabview.add("✅ Active Loans")
        self.loan_tabview.add("📋 Application History")
        
        # Setup loan sub-tabs
        self.setup_pending_loans_tab()
        self.setup_active_loans_tab()
        self.setup_loan_history_tab()

    def setup_pending_loans_tab(self):
        """Setup the pending loans tab"""
        tab = self.loan_tabview.tab("⏳ Pending Loans")
        
        # Header with refresh button
        header_frame = ctk.CTkFrame(tab)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="💰 Loan Applications Awaiting Approval",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=15, pady=10)
        
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            font=ctk.CTkFont(size=12),
            height=30,
            width=80,
            command=self.refresh_pending_loans
        )
        refresh_btn.pack(side="right", padx=15, pady=10)
        
        # Scrollable frame for pending loans
        self.pending_loans_frame = ctk.CTkScrollableFrame(tab)
        self.pending_loans_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    def setup_active_loans_tab(self):
        """Setup the active loans tab"""
        tab = self.loan_tabview.tab("✅ Active Loans")
        
        # Header with refresh button
        header_frame = ctk.CTkFrame(tab)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🏦 Currently Active Loans",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=15, pady=10)
        
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            font=ctk.CTkFont(size=12),
            height=30,
            width=80,
            command=self.refresh_active_loans
        )
        refresh_btn.pack(side="right", padx=15, pady=10)
        
        # Scrollable frame for active loans
        self.active_loans_frame = ctk.CTkScrollableFrame(tab)
        self.active_loans_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    def setup_loan_history_tab(self):
        """Setup the loan application history tab"""
        tab = self.loan_tabview.tab("📋 Application History")
        
        # Header with refresh button
        header_frame = ctk.CTkFrame(tab)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Complete Loan Application History",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=15, pady=10)
        
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            font=ctk.CTkFont(size=12),
            height=30,
            width=80,
            command=self.refresh_loan_history
        )
        refresh_btn.pack(side="right", padx=15, pady=10)
        
        # Scrollable frame for loan history
        self.loan_history_frame = ctk.CTkScrollableFrame(tab)
        self.loan_history_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    def refresh_loan_data(self):
        """Refresh all loan-related data"""
        self.refresh_pending_loans()
        self.refresh_active_loans()
        self.refresh_loan_history()

    def refresh_pending_loans(self):
        """Refresh and display pending loan applications"""
        try:
            # Clear existing content
            for widget in self.pending_loans_frame.winfo_children():
                widget.destroy()
            
            # Get pending loans from database
            pending_loans = self.get_pending_loans()
            
            if not pending_loans:
                no_pending_label = ctk.CTkLabel(
                    self.pending_loans_frame,
                    text="✅ No pending loan applications at this time.",
                    font=ctk.CTkFont(size=14),
                    text_color=("gray60", "gray40")
                )
                no_pending_label.pack(pady=50)
                return
            
            # Display pending loans
            for loan in pending_loans:
                loan_frame = ctk.CTkFrame(self.pending_loans_frame)
                loan_frame.pack(fill="x", padx=10, pady=8)
                
                # Left side - loan info
                info_frame = ctk.CTkFrame(loan_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)
                
                # Applicant name and account
                name_label = ctk.CTkLabel(
                    info_frame,
                    text=f"👤 {loan['applicant_name']} (Account: {loan['account_number']})",
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                name_label.pack(anchor="w")
                
                # Loan amount and purpose
                amount_label = ctk.CTkLabel(
                    info_frame,
                    text=f"💰 Amount: ₱{loan['amount']:,.2f}",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=("#007bff", "#0066cc")
                )
                amount_label.pack(anchor="w", pady=(3, 0))
                
                purpose_label = ctk.CTkLabel(
                    info_frame,
                    text=f"📋 Purpose: {loan['purpose']}",
                    font=ctk.CTkFont(size=12)
                )
                purpose_label.pack(anchor="w")
                
                # Income and employment
                income_label = ctk.CTkLabel(
                    info_frame,
                    text=f"💼 Monthly Income: ₱{loan['monthly_income']:,.2f} | Status: {loan['employment_status']}",
                    font=ctk.CTkFont(size=11),
                    text_color=("gray60", "gray40")
                )
                income_label.pack(anchor="w")
                
                # Application date
                date_label = ctk.CTkLabel(
                    info_frame,
                    text=f"📅 Applied: {loan['applied_at']}",
                    font=ctk.CTkFont(size=11),
                    text_color=("gray60", "gray40")
                )
                date_label.pack(anchor="w")
                
                # Right side - action buttons
                button_frame = ctk.CTkFrame(loan_frame, fg_color="transparent")
                button_frame.pack(side="right", padx=15, pady=15)
                
                approve_btn = ctk.CTkButton(
                    button_frame,
                    text="✅ Approve",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    height=35,
                    width=90,
                    fg_color=("#28a745", "#20c997"),
                    hover_color=("#218838", "#1dd1a1"),
                    command=lambda loan_id=loan['id']: self.show_approve_loan_dialog(loan_id, loan)
                )
                approve_btn.pack(side="top", pady=(0, 8))
                
                decline_btn = ctk.CTkButton(
                    button_frame,
                    text="❌ Decline",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    height=35,
                    width=90,
                    fg_color=("#dc3545", "#e74c3c"),
                    hover_color=("#c82333", "#c0392b"),
                    command=lambda loan_id=loan['id']: self.decline_loan_application(loan_id)
                )
                decline_btn.pack(side="top")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing pending loans: {str(e)}")

    def refresh_active_loans(self):
        """Refresh and display active loans"""
        try:
            # Clear existing content
            for widget in self.active_loans_frame.winfo_children():
                widget.destroy()
            
            # Get active loans from database
            active_loans = self.get_active_loans()
            
            if not active_loans:
                no_active_label = ctk.CTkLabel(
                    self.active_loans_frame,
                    text="📋 No active loans at this time.",
                    font=ctk.CTkFont(size=14),
                    text_color=("gray60", "gray40")
                )
                no_active_label.pack(pady=50)
                return
            
            # Create header for active loans
            header_frame = ctk.CTkFrame(self.active_loans_frame)
            header_frame.pack(fill="x", padx=10, pady=(10, 5))
            
            header_text = f"{'Borrower':<20} {'Amount':<12} {'Balance':<12} {'Rate':<6} {'Payment':<10} {'Next Due':<12}"
            header_label = ctk.CTkLabel(
                header_frame,
                text=header_text,
                font=ctk.CTkFont(size=11, weight="bold", family="Courier"),
                text_color=("#495057", "#6c757d")
            )
            header_label.pack(pady=8)
            
            # Display active loans
            for loan in active_loans:
                loan_frame = ctk.CTkFrame(self.active_loans_frame)
                loan_frame.pack(fill="x", padx=10, pady=3)
                
                # Format loan display
                progress = ((loan['principal_amount'] - loan['remaining_balance']) / loan['principal_amount']) * 100
                
                # Loan info display
                loan_text = (f"{loan['borrower_name']:<20} "
                            f"₱{loan['principal_amount']:<11,.0f} "
                            f"₱{loan['remaining_balance']:<11,.2f} "
                            f"{loan['interest_rate']:<5.1f}% "
                            f"₱{loan['monthly_payment']:<9,.0f} "
                            f"{loan['next_payment_date']}")
                
                loan_label = ctk.CTkLabel(
                    loan_frame,
                    text=loan_text,
                    font=ctk.CTkFont(size=10, family="Courier")
                )
                loan_label.pack(pady=8, padx=15, anchor="w")
                
                # Progress bar for loan completion
                progress_bar = ctk.CTkProgressBar(loan_frame, width=200, height=8)
                progress_bar.set(progress / 100)
                progress_bar.pack(pady=(0, 8), padx=15, anchor="w")
                
                # Progress percentage
                progress_label = ctk.CTkLabel(
                    loan_frame,
                    text=f"Paid: {progress:.1f}%",
                    font=ctk.CTkFont(size=9),
                    text_color=("gray60", "gray40")
                )
                progress_label.pack(pady=(0, 8), padx=15, anchor="w")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing active loans: {str(e)}")

    def refresh_loan_history(self):
        """Refresh and display loan application history"""
        try:
            # Clear existing content
            for widget in self.loan_history_frame.winfo_children():
                widget.destroy()
            
            # Get loan history from database
            loan_history = self.get_loan_application_history()
            
            if not loan_history:
                no_history_label = ctk.CTkLabel(
                    self.loan_history_frame,
                    text="📋 No loan application history found.",
                    font=ctk.CTkFont(size=14),
                    text_color=("gray60", "gray40")
                )
                no_history_label.pack(pady=50)
                return
            
            # Create header
            header_frame = ctk.CTkFrame(self.loan_history_frame)
            header_frame.pack(fill="x", padx=10, pady=(10, 5))
            
            header_label = ctk.CTkLabel(
                header_frame,
                text="Complete Loan Application History (Most Recent First)",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=("#495057", "#6c757d")
            )
            header_label.pack(pady=10)
            
            # Display loan history
            for app in loan_history:
                app_frame = ctk.CTkFrame(self.loan_history_frame)
                app_frame.pack(fill="x", padx=10, pady=5)
                
                # Status color coding
                if app['status'] == 'approved':
                    status_color = ("#28a745", "#20c997")
                    status_icon = "✅"
                elif app['status'] == 'rejected':
                    status_color = ("#dc3545", "#e74c3c")
                    status_icon = "❌"
                else:
                    status_color = ("#ffc107", "#f39c12")
                    status_icon = "⏳"
                
                # Main info
                info_frame = ctk.CTkFrame(app_frame, fg_color="transparent")
                info_frame.pack(fill="both", expand=True, padx=15, pady=12)
                
                # First row - name, amount, status
                row1_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
                row1_frame.pack(fill="x", anchor="w")
                
                main_info = ctk.CTkLabel(
                    row1_frame,
                    text=f"{status_icon} {app['applicant_name']} - ₱{app['amount']:,.2f} - {app['status'].upper()}",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=status_color
                )
                main_info.pack(side="left")
                
                date_label = ctk.CTkLabel(
                    row1_frame,
                    text=f"Applied: {app['applied_at']}",
                    font=ctk.CTkFont(size=11),
                    text_color=("gray60", "gray40")
                )
                date_label.pack(side="right")
                
                # Second row - details
                details_label = ctk.CTkLabel(
                    info_frame,
                    text=f"Account: {app['account_number']} | Purpose: {app['purpose']} | Income: ₱{app['monthly_income']:,.2f}",
                    font=ctk.CTkFont(size=11),
                    text_color=("gray70", "gray50")
                )
                details_label.pack(anchor="w", pady=(3, 0))
                
                # Show additional info for approved loans
                if app['status'] == 'approved' and app['processed_at']:
                    approved_info = ctk.CTkLabel(
                        info_frame,
                        text=f"Approved: {app['processed_at']} | Rate: {app['interest_rate']}% | Term: {app['term_months']} months | Payment: ₱{app['monthly_payment']:,.2f}",
                        font=ctk.CTkFont(size=10),
                        text_color=("#28a745", "#20c997")
                    )
                    approved_info.pack(anchor="w", pady=(2, 0))
                
                # Show admin notes if any
                if app['admin_notes']:
                    notes_label = ctk.CTkLabel(
                        info_frame,
                        text=f"Notes: {app['admin_notes']}",
                        font=ctk.CTkFont(size=10),
                        text_color=("gray60", "gray40")
                    )
                    notes_label.pack(anchor="w", pady=(2, 0))
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing loan history: {str(e)}")

    def get_pending_loans(self):
        """Get pending loan applications from database"""
        query = """
            SELECT la.id, la.account_number, la.amount, la.purpose, la.monthly_income, 
                la.employment_status, la.applied_at, a.name as applicant_name
            FROM loan_applications la
            JOIN accounts a ON la.account_number = a.account_number
            WHERE la.status = 'pending'
            ORDER BY la.applied_at ASC
        """
        return self.admin_service.db.fetch_all(query)

    def get_active_loans(self):
        """Get active loans from database"""
        query = """
            SELECT l.id, l.account_number, l.principal_amount, l.interest_rate, 
                l.term_months, l.monthly_payment, l.remaining_balance, 
                l.next_payment_date, l.disbursed_at, a.name as borrower_name
            FROM loans l
            JOIN accounts a ON l.account_number = a.account_number
            WHERE l.status = 'active'
            ORDER BY l.next_payment_date ASC
        """
        return self.admin_service.db.fetch_all(query)

    def get_loan_application_history(self):
        """Get complete loan application history"""
        query = """
            SELECT la.id, la.account_number, la.amount, la.purpose, la.monthly_income,
                la.employment_status, la.status, la.interest_rate, la.term_months,
                la.monthly_payment, la.admin_notes, la.applied_at, la.processed_at,
                a.name as applicant_name
            FROM loan_applications la
            JOIN accounts a ON la.account_number = a.account_number
            ORDER BY la.applied_at DESC
        """
        return self.admin_service.db.fetch_all(query)

    def show_approve_loan_dialog(self, loan_id, loan_data):
        """Show dialog for approving loan with terms"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Approve Loan Application")
        dialog.geometry("400x500")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"400x500+{x}+{y}")
        
        # Dialog content
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Approve Loan Application",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Loan info
        info_text = f"Applicant: {loan_data['applicant_name']}\nAmount: ₱{loan_data['amount']:,.2f}\nPurpose: {loan_data['purpose']}"
        info_label = ctk.CTkLabel(
            main_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info_label.pack(pady=(0, 20))
        
        # Interest rate
        rate_label = ctk.CTkLabel(main_frame, text="Interest Rate (% annually):", font=ctk.CTkFont(size=12))
        rate_label.pack(anchor="w", padx=20)
        
        rate_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., 15.0")
        rate_entry.pack(fill="x", padx=20, pady=(5, 15))
        rate_entry.insert(0, "15.0")  # Default rate
        
        # Term in months
        term_label = ctk.CTkLabel(main_frame, text="Loan Term (months):", font=ctk.CTkFont(size=12))
        term_label.pack(anchor="w", padx=20)
        
        term_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., 12")
        term_entry.pack(fill="x", padx=20, pady=(5, 15))
        term_entry.insert(0, "12")  # Default term
        
        # Admin notes
        notes_label = ctk.CTkLabel(main_frame, text="Admin Notes (optional):", font=ctk.CTkFont(size=12))
        notes_label.pack(anchor="w", padx=20)
        
        notes_entry = ctk.CTkTextbox(main_frame, height=80)
        notes_entry.pack(fill="x", padx=20, pady=(5, 20))
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        def approve_loan():
            try:
                interest_rate = float(rate_entry.get())
                term_months = int(term_entry.get())
                admin_notes = notes_entry.get("1.0", "end-1c").strip()
                
                if self.approve_loan_application(loan_id, interest_rate, term_months, admin_notes):
                    dialog.destroy()
                    self.refresh_loan_data()
                    messagebox.showinfo("Success", "Loan approved successfully!")
                else:
                    messagebox.showerror("Error", "Failed to approve loan.")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values.")
            except Exception as e:
                messagebox.showerror("Error", f"Error approving loan: {str(e)}")
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=ctk.CTkFont(size=12),
            height=35,
            width=100,
            fg_color=("gray60", "gray40"),
            command=dialog.destroy
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        approve_btn = ctk.CTkButton(
            button_frame,
            text="Approve Loan",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            width=120,
            fg_color=("#28a745", "#20c997"),
            hover_color=("#218838", "#1dd1a1"),
            command=approve_loan
        )
        approve_btn.pack(side="right")

    def approve_loan_application(self, loan_id, interest_rate, term_months, admin_notes):
        """Approve a loan application and create the loan"""
        try:
            self.admin_service.db.begin_transaction()
            
            # Calculate monthly payment (simple interest calculation)
            # Get loan amount
            query = "SELECT amount, account_number FROM loan_applications WHERE id = %s"
            loan_data = self.admin_service.db.fetch_one(query, (loan_id,))
            
            if not loan_data:
                raise Exception("Loan application not found")
            
            principal = float(loan_data['amount'])
            monthly_rate = interest_rate / 100 / 12
            
            # Calculate monthly payment using amortization formula
            if monthly_rate > 0:
                monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**term_months) / ((1 + monthly_rate)**term_months - 1)
            else:
                monthly_payment = principal / term_months
            
            # Update loan application
            update_query = """
                UPDATE loan_applications 
                SET status = 'approved', interest_rate = %s, term_months = %s, 
                    monthly_payment = %s, admin_notes = %s, processed_at = NOW()
                WHERE id = %s
            """
            self.admin_service.db.execute_query(update_query, 
                (interest_rate, term_months, monthly_payment, admin_notes, loan_id))
            
            # Create loan record
            import datetime
            next_payment_date = datetime.date.today() + datetime.timedelta(days=30)
            
            loan_query = """
                INSERT INTO loans (application_id, account_number, principal_amount, interest_rate,
                                term_months, monthly_payment, remaining_balance, next_payment_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.admin_service.db.execute_query(loan_query,
                (loan_id, loan_data['account_number'], principal, interest_rate,
                term_months, monthly_payment, principal, next_payment_date))
            
            # Add loan disbursement to account balance
            balance_query = """
                UPDATE accounts SET balance = balance + %s WHERE account_number = %s
            """
            self.admin_service.db.execute_query(balance_query, (principal, loan_data['account_number']))
            
            # Record transaction
            transaction_query = """
                INSERT INTO transactions (account_number, type, amount)
                VALUES (%s, 'loan_disbursement', %s)
            """
            self.admin_service.db.execute_query(transaction_query, (loan_data['account_number'], principal))
            
            self.admin_service.db.commit_transaction()
            return True
            
        except Exception as e:
            self.admin_service.db.rollback_transaction()
            print(f"Error approving loan: {str(e)}")
            return False

    def decline_loan_application(self, loan_id):
        """Decline a loan application with reason"""
        dialog = ctk.CTkInputDialog(
            text="Enter reason for declining loan application:",
            title="Decline Loan Application"
        )
        reason = dialog.get_input()
        
        if reason:
            try:
                query = """
                    UPDATE loan_applications 
                    SET status = 'rejected', admin_notes = %s, processed_at = NOW()
                    WHERE id = %s
                """
                if self.admin_service.db.execute_query(query, (reason, loan_id)):
                    messagebox.showinfo("Success", "Loan application declined.")
                    self.refresh_loan_data()
                else:
                    messagebox.showerror("Error", "Failed to decline loan application.")
            except Exception as e:
                messagebox.showerror("Error", f"Error declining loan: {str(e)}")
    
    def destroy(self):
        """Clean up the dashboard"""
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()