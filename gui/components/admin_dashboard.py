# banking-app/gui/components/admin_dashboard.py
import customtkinter as ctk
from typing import Dict, Callable, Any
import tkinter.messagebox as messagebox
import datetime

class AdminDashboard:
    def __init__(self, parent, callbacks: Dict[str, Callable], admin_data: Dict[str, Any], admin_service):
        self.parent = parent
        self.callbacks = callbacks
        self.admin_data = admin_data
        self.admin_service = admin_service
        self.setup_ui()
    
    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.create_header()
        self.create_main_content()
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_frame)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        left_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        ctk.CTkLabel(left_frame, text=f"👨‍💼 Admin Panel - Welcome, {self.admin_data['name']}", 
                    font=ctk.CTkFont(size=20, weight="bold"), text_color=("#dc3545", "#e74c3c")).pack(anchor="w")
        ctk.CTkLabel(left_frame, text="System Administrator", font=ctk.CTkFont(size=14), 
                    text_color=("gray60", "gray40")).pack(anchor="w", pady=(5, 0))
        
        right_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        ctk.CTkButton(right_frame, text="🚪 Logout", font=ctk.CTkFont(size=12), height=30, width=80,
                     fg_color=("#6c757d", "#495057"), hover_color=("#5a6268", "#343a40"), 
                     command=self.callbacks['logout']).pack(anchor="e")
    
    def create_main_content(self):
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        self.tabview = ctk.CTkTabview(content_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add the new tab here
        for tab in ["⏳ Pending Accounts", "👥 All Users", "💰 Loan Management", "📊 User Transactions"]:
            self.tabview.add(tab)
        
        self.setup_pending_accounts_tab()
        self.setup_all_users_tab()
        self.setup_loan_management_tab()
        self.setup_user_transactions_tab()
        
        self.refresh_pending_accounts()
        self.refresh_all_users()
        self.refresh_loan_data()
        self.refresh_user_transactions()
    
    def create_tab_header(self, tab, title, refresh_func):
        header_frame = ctk.CTkFrame(tab)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkLabel(header_frame, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=15, pady=10)
        ctk.CTkButton(header_frame, text="🔄 Refresh", font=ctk.CTkFont(size=12), height=30, width=80, 
                     command=refresh_func).pack(side="right", padx=15, pady=10)
    
    def setup_pending_accounts_tab(self):
        tab = self.tabview.tab("⏳ Pending Accounts")
        self.create_tab_header(tab, "📋 Accounts Awaiting Approval", self.refresh_pending_accounts)
        self.pending_frame = ctk.CTkScrollableFrame(tab)
        self.pending_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
    
    def setup_all_users_tab(self):
        """Setup All Users tab with sub-tabs for Accounts and Declined/Suspended Accounts"""
        tab = self.tabview.tab("👥 All Users")
        
        # Create header for the main tab
        self.create_tab_header(tab, "👥 All System Users", self.refresh_all_users_data)
        
        # Create sub-tabview for Accounts and Declined Accounts
        self.users_subtabview = ctk.CTkTabview(tab)
        self.users_subtabview.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Add sub-tabs
        self.users_subtabview.add("📋 Accounts")
        self.users_subtabview.add("🚫 Declined/Suspended Accounts")
        
        # Setup Accounts sub-tab
        accounts_tab = self.users_subtabview.tab("📋 Accounts")
        self.users_frame = ctk.CTkScrollableFrame(accounts_tab)
        self.users_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Setup Declined/Suspended Accounts sub-tab
        declined_tab = self.users_subtabview.tab("🚫 Declined/Suspended Accounts")
        self.declined_frame = ctk.CTkScrollableFrame(declined_tab)
        self.declined_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def refresh_all_users_data(self):
        """Refresh both accounts and declined accounts data"""
        self.refresh_all_users()
        self.refresh_declined_accounts()

    def refresh_declined_accounts(self):
        """Refresh declined/suspended accounts display"""
        try:
            for widget in self.declined_frame.winfo_children():
                widget.destroy()
            
            declined_accounts = self.admin_service.get_declined_accounts()
            
            if not declined_accounts:
                ctk.CTkLabel(self.declined_frame, text="✅ No declined or suspended accounts.", 
                            font=ctk.CTkFont(size=14), text_color=("gray60", "gray40")).pack(pady=50)
                return
            
            # Header
            header_frame = ctk.CTkFrame(self.declined_frame)
            header_frame.pack(fill="x", padx=10, pady=(10, 5))
            
            header_text = f"{'Account Number':<15} {'Decline Reason':<30} {'Declined Date':<20} {'Actions'}"
            ctk.CTkLabel(header_frame, text=header_text, 
                        font=ctk.CTkFont(size=12, weight="bold", family="Courier"), 
                        text_color=("#495057", "#6c757d")).pack(pady=10, padx=15, anchor="w")
            
            for account in declined_accounts:
                account_frame = ctk.CTkFrame(self.declined_frame)
                account_frame.pack(fill="x", padx=10, pady=2)
                
                # Left side: Account info
                info_frame = ctk.CTkFrame(account_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=8)
                
                # Format date for display
                decline_date = account['declined_at'].strftime("%Y-%m-%d %H:%M") if account['declined_at'] else "Unknown"
                
                # Truncate long reasons for display
                display_reason = account['reason'][:25] + "..." if len(account['reason']) > 25 else account['reason']
                
                info_text = f"{account['account_number']:<15} {display_reason:<30} {decline_date:<20}"
                
                ctk.CTkLabel(info_frame, text=info_text,
                            font=ctk.CTkFont(size=11, family="Courier"),
                            text_color=("#dc3545", "#e74c3c")).pack(anchor="w")
                
                # Show full reason as tooltip/secondary line if truncated
                if len(account['reason']) > 25:
                    ctk.CTkLabel(info_frame, text=f"Full reason: {account['reason']}",
                                font=ctk.CTkFont(size=9),
                                text_color=("gray60", "gray40")).pack(anchor="w", padx=(20, 0))
                
                # Right side: Action buttons
                action_frame = ctk.CTkFrame(account_frame, fg_color="transparent")
                action_frame.pack(side="right", padx=15, pady=5)
                
                # Reactivate button
                ctk.CTkButton(action_frame, text="🔄 Reactivate", 
                            font=ctk.CTkFont(size=10, weight="bold"),
                            height=25, width=90,
                            fg_color=("#28a745", "#20c997"),
                            hover_color=("#218838", "#1dd1a1"),
                            command=lambda acc=account['account_number']: self.reactivate_account(acc)).pack(side="left", padx=(0, 5))
                
                # Delete Permanently button
                ctk.CTkButton(action_frame, text="🗑️ Delete",
                            font=ctk.CTkFont(size=10, weight="bold"),
                            height=25, width=70,
                            fg_color=("#dc3545", "#e74c3c"),
                            hover_color=("#c82333", "#c0392b"),
                            command=lambda acc=account['account_number']: self.delete_declined_account(acc)).pack(side="left")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing declined accounts: {str(e)}")

    def reactivate_account(self, account_number):
        """Reactivate a declined account"""
        if messagebox.askyesno("Confirm Reactivation", 
                            f"Are you sure you want to reactivate account {account_number}?\n\n"
                            "This will:\n"
                            "• Move the account back to active accounts\n"
                            "• Set approval status to approved\n"
                            "• Remove from declined accounts list\n\n"
                            "Note: User will need to reset their PIN."):
            try:
                if self.admin_service.reactivate_declined_account(account_number):
                    messagebox.showinfo("Success", f"Account {account_number} reactivated successfully!")
                    self.refresh_all_users_data()
                else:
                    messagebox.showerror("Error", "Failed to reactivate account. Account may not exist in declined list.")
            except Exception as e:
                messagebox.showerror("Error", f"Error reactivating account: {str(e)}")

    def delete_declined_account(self, account_number):
        """Permanently delete a declined account"""
        if messagebox.askyesno("Confirm Permanent Deletion", 
                            f"⚠️ Are you sure you want to PERMANENTLY DELETE account {account_number}?\n\n"
                            "This will:\n"
                            "• Completely remove the account from declined list\n"
                            "• This action CANNOT be undone\n\n"
                            "The account number can be reused for new registrations."):
            try:
                if self.admin_service.delete_declined_account_permanently(account_number):
                    messagebox.showinfo("Success", f"Account {account_number} deleted permanently!")
                    self.refresh_declined_accounts()
                else:
                    messagebox.showerror("Error", "Failed to delete account. Account may not exist.")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting account: {str(e)}")
    
    def refresh_pending_accounts(self):
        try:
            for widget in self.pending_frame.winfo_children():
                widget.destroy()
            
            pending_accounts = self.admin_service.get_pending_accounts()
            
            if not pending_accounts:
                ctk.CTkLabel(self.pending_frame, text="✅ No pending accounts at this time.", 
                            font=ctk.CTkFont(size=14), text_color=("gray60", "gray40")).pack(pady=50)
                return
            
            for account in pending_accounts:
                account_frame = ctk.CTkFrame(self.pending_frame)
                account_frame.pack(fill="x", padx=10, pady=5)
                
                info_frame = ctk.CTkFrame(account_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
                
                for text, size, color, pady in [
                    (f"👤 {account['name']}", 14, None, 0),
                    (f"Account: {account['account_number']}", 12, None, 0),
                    (f"Created: {account['created_at']}", 11, ("gray60", "gray40"), 0)
                ]:
                    label = ctk.CTkLabel(info_frame, text=text, font=ctk.CTkFont(size=size, weight="bold" if size==14 else "normal"))
                    if color: label.configure(text_color=color)
                    label.pack(anchor="w", pady=(pady, 0))
                
                button_frame = ctk.CTkFrame(account_frame, fg_color="transparent")
                button_frame.pack(side="right", padx=15, pady=10)
                
                for text, color, hover_color, func, side_pady in [
                    ("✅ Approve", ("#28a745", "#20c997"), ("#218838", "#1dd1a1"), 
                     lambda acc=account['account_number']: self.approve_account(acc), (0, 5)),
                    ("❌ Reject", ("#dc3545", "#e74c3c"), ("#c82333", "#c0392b"), 
                     lambda acc=account['account_number']: self.reject_account_with_reason(acc), (0, 0))
                ]:
                    ctk.CTkButton(button_frame, text=text, font=ctk.CTkFont(size=11, weight="bold"), 
                                 height=30, width=80, fg_color=color, hover_color=hover_color, 
                                 command=func).pack(side="top", pady=side_pady)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing pending accounts: {str(e)}")

    def refresh_all_users(self):
        try:
            for widget in self.users_frame.winfo_children():
                widget.destroy()
            
            all_users = self.admin_service.get_all_users()
            
            if not all_users:
                ctk.CTkLabel(self.users_frame, text="No users found in the system.", 
                            font=ctk.CTkFont(size=14), text_color=("gray60", "gray40")).pack(pady=50)
                return
            
            # Enhanced header with action column
            header_frame = ctk.CTkFrame(self.users_frame)
            header_frame.pack(fill="x", padx=10, pady=(10, 5))
            
            header_text = f"{'Account':<12} {'Name':<18} {'Balance':<12} {'Status':<10} {'Actions'}"
            ctk.CTkLabel(header_frame, text=header_text, 
                        font=ctk.CTkFont(size=12, weight="bold", family="Courier"), 
                        text_color=("#495057", "#6c757d")).pack(pady=10, padx=15, anchor="w")
            
            for user in all_users:
                user_frame = ctk.CTkFrame(self.users_frame)
                user_frame.pack(fill="x", padx=10, pady=2)
                
                # Left side: User info
                info_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=8)
                
                status = "✅ Active" if user['is_approved'] else "⏸️ Suspended"
                status_color = ("#28a745", "#20c997") if user['is_approved'] else ("#ffc107", "#f39c12")
                
                # Truncate long names for display
                display_name = user['name'][:15] + "..." if len(user['name']) > 15 else user['name']
                info_text = f"{user['account_number']:<12} {display_name:<18} ₱{user['balance']:<11.2f} {status}"
                
                ctk.CTkLabel(info_frame, text=info_text,
                            font=ctk.CTkFont(size=11, family="Courier"),
                            text_color=status_color).pack(anchor="w")
                
                # Right side: Action buttons
                action_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
                action_frame.pack(side="right", padx=15, pady=5)
                
                # Edit button
                ctk.CTkButton(action_frame, text="✏️ Edit", 
                            font=ctk.CTkFont(size=10, weight="bold"),
                            height=25, width=60,
                            fg_color=("#17a2b8", "#1abc9c"),
                            hover_color=("#138496", "#16a085"),
                            command=lambda u=user: self.edit_user(u)).pack(side="left", padx=(0, 5))
                
                # Toggle Status button
                toggle_text = "⏸️ Suspend" if user['is_approved'] else "✅ Activate"
                toggle_color = ("#ffc107", "#f39c12") if user['is_approved'] else ("#28a745", "#20c997")
                toggle_hover = ("#e0a800", "#e67e22") if user['is_approved'] else ("#218838", "#1dd1a1")
                
                ctk.CTkButton(action_frame, text=toggle_text,
                            font=ctk.CTkFont(size=10, weight="bold"),
                            height=25, width=70,
                            fg_color=toggle_color,
                            hover_color=toggle_hover,
                            command=lambda acc=user['account_number']: self.toggle_user_status(acc)).pack(side="left", padx=(0, 5))
                
                # Delete button
                ctk.CTkButton(action_frame, text="🗑️ Delete",
                            font=ctk.CTkFont(size=10, weight="bold"),
                            height=25, width=70,
                            fg_color=("#dc3545", "#e74c3c"),
                            hover_color=("#c82333", "#c0392b"),
                            command=lambda acc=user['account_number'], name=user['name']: self.delete_user(acc, name)).pack(side="left")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing users: {str(e)}")

    def edit_user(self, user):
        """Open edit dialog for user"""
        # Create edit dialog window
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(f"Edit User - {user['name']}")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")
        
        # Dialog content
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(main_frame, text=f"Edit User Account", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 20))
        
        # Account number (read-only)
        ctk.CTkLabel(main_frame, text=f"Account: {user['account_number']}",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=("gray60", "gray40")).pack(pady=(0, 10))
        
        # Name field
        ctk.CTkLabel(main_frame, text="Name:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20)
        name_entry = ctk.CTkEntry(main_frame, height=35, font=ctk.CTkFont(size=12))
        name_entry.pack(fill="x", padx=20, pady=(5, 15))
        name_entry.insert(0, user['name'])
        
        # Balance field
        ctk.CTkLabel(main_frame, text="Balance:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20)
        balance_entry = ctk.CTkEntry(main_frame, height=35, font=ctk.CTkFont(size=12))
        balance_entry.pack(fill="x", padx=20, pady=(5, 25))
        balance_entry.insert(0, str(user['balance']))
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=10)
        
        def save_changes():
            try:
                new_name = name_entry.get().strip()
                new_balance = float(balance_entry.get().strip())
                
                if not new_name:
                    messagebox.showerror("Error", "Name cannot be empty!")
                    return
                
                if new_balance < 0:
                    messagebox.showerror("Error", "Balance cannot be negative!")
                    return
                
                # Check if anything changed
                if new_name == user['name'] and new_balance == user['balance']:
                    messagebox.showinfo("Info", "No changes to save.")
                    dialog.destroy()
                    return
                
                if self.admin_service.update_user_details(user['account_number'], new_name, new_balance):
                    messagebox.showinfo("Success", f"User {new_name} updated successfully!")
                    dialog.destroy()
                    self.refresh_all_users()
                else:
                    messagebox.showerror("Error", "Failed to update user details.")
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid balance amount!")
            except Exception as e:
                messagebox.showerror("Error", f"Error updating user: {str(e)}")
        
        ctk.CTkButton(button_frame, text="💾 Save Changes",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    height=35, width=120,
                    fg_color=("#28a745", "#20c997"),
                    hover_color=("#218838", "#1dd1a1"),
                    command=save_changes).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(button_frame, text="❌ Cancel",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    height=35, width=120,
                    fg_color=("#6c757d", "#495057"),
                    hover_color=("#5a6268", "#343a40"),
                    command=dialog.destroy).pack(side="left")

    def toggle_user_status(self, account_number):
        """Toggle user active/suspended status"""
        try:
            if self.admin_service.toggle_user_status(account_number):
                messagebox.showinfo("Success", "User status updated successfully!")
                self.refresh_all_users()
            else:
                messagebox.showerror("Error", "Failed to update user status.")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating status: {str(e)}")

    def delete_user(self, account_number, name):
        """Delete user with confirmation"""
        # Double confirmation for safety
        if messagebox.askyesno("Confirm Deletion", 
                            f"⚠️ Are you sure you want to delete user '{name}' (Account: {account_number})?\n\n"
                            "This will permanently delete:\n"
                            "• User account and profile\n"
                            "• All transaction history\n"
                            "• All loan records\n"
                            "• All related data\n\n"
                            "This action CANNOT be undone!"):
            
            # Second confirmation
            if messagebox.askyesno("FINAL CONFIRMATION", 
                                f"🚨 FINAL WARNING 🚨\n\n"
                                f"You are about to PERMANENTLY DELETE:\n"
                                f"User: {name}\n"
                                f"Account: {account_number}\n\n"
                                f"Type 'DELETE' in the next dialog to confirm."):
                
                # Require typing DELETE to confirm
                confirmation = ctk.CTkInputDialog(
                    text="Type 'DELETE' to confirm permanent deletion:",
                    title="Type DELETE to Confirm"
                ).get_input()
                
                if confirmation == "DELETE":
                    try:
                        if self.admin_service.delete_user_account(account_number):
                            messagebox.showinfo("Success", f"User {name} deleted successfully!")
                            self.refresh_all_users()
                        else:
                            messagebox.showerror("Error", "Failed to delete user account.")
                    except Exception as e:
                        messagebox.showerror("Error", f"Error deleting user: {str(e)}")
                else:
                    messagebox.showinfo("Cancelled", "Deletion cancelled - incorrect confirmation.")
            else:
                messagebox.showinfo("Cancelled", "User deletion cancelled.")
    
    def approve_account(self, account_number):
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
        dialog = ctk.CTkInputDialog(text=f"Enter reason for rejecting account {account_number}:", title="Reject Account")
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

    def setup_loan_management_tab(self):
        tab = self.tabview.tab("💰 Loan Management")
        
        self.loan_tabview = ctk.CTkTabview(tab)
        self.loan_tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        for subtab in ["⏳ Pending Loans", "✅ Active Loans", "📋 Application History"]:
            self.loan_tabview.add(subtab)
        
        self.setup_pending_loans_tab()
        self.setup_active_loans_tab()
        self.setup_loan_history_tab()

    def setup_pending_loans_tab(self):
        tab = self.loan_tabview.tab("⏳ Pending Loans")
        self.create_tab_header(tab, "💰 Loan Applications Awaiting Approval", self.refresh_pending_loans)
        self.pending_loans_frame = ctk.CTkScrollableFrame(tab)
        self.pending_loans_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    def setup_active_loans_tab(self):
        tab = self.loan_tabview.tab("✅ Active Loans")
        self.create_tab_header(tab, "🏦 Currently Active Loans", self.refresh_active_loans)
        self.active_loans_frame = ctk.CTkScrollableFrame(tab)
        self.active_loans_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    def setup_loan_history_tab(self):
        tab = self.loan_tabview.tab("📋 Application History")
        self.create_tab_header(tab, "📊 Complete Loan Application History", self.refresh_loan_history)
        self.loan_history_frame = ctk.CTkScrollableFrame(tab)
        self.loan_history_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    def refresh_loan_data(self):
        self.refresh_pending_loans()
        self.refresh_active_loans()
        self.refresh_loan_history()

    def refresh_pending_loans(self):
        try:
            for widget in self.pending_loans_frame.winfo_children():
                widget.destroy()
            
            pending_loans = self.get_pending_loans()
            
            if not pending_loans:
                ctk.CTkLabel(self.pending_loans_frame, text="✅ No pending loan applications at this time.", 
                            font=ctk.CTkFont(size=14), text_color=("gray60", "gray40")).pack(pady=50)
                return
            
            for loan in pending_loans:
                loan_frame = ctk.CTkFrame(self.pending_loans_frame)
                loan_frame.pack(fill="x", padx=10, pady=8)
                
                info_frame = ctk.CTkFrame(loan_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)
                
                for text, size, color, pady in [
                    (f"👤 {loan['applicant_name']} (Account: {loan['account_number']})", 14, None, 0),
                    (f"💰 Amount: ₱{loan['amount']:,.2f}", 13, ("#007bff", "#0066cc"), 3),
                    (f"📋 Purpose: {loan['purpose']}", 12, None, 0),
                    (f"💼 Monthly Income: ₱{loan['monthly_income']:,.2f} | Status: {loan['employment_status']}", 11, ("gray60", "gray40"), 0),
                    (f"📅 Applied: {loan['applied_at']}", 11, ("gray60", "gray40"), 0)
                ]:
                    label = ctk.CTkLabel(info_frame, text=text, font=ctk.CTkFont(size=size, weight="bold" if size>=13 else "normal"))
                    if color: label.configure(text_color=color)
                    label.pack(anchor="w", pady=(pady, 0))
                
                button_frame = ctk.CTkFrame(loan_frame, fg_color="transparent")
                button_frame.pack(side="right", padx=15, pady=15)
                
                for text, color, hover_color, func, pady in [
                    ("✅ Approve", ("#28a745", "#20c997"), ("#218838", "#1dd1a1"), 
                     lambda loan_id=loan['id'], loan_data=loan: self.show_approve_loan_dialog(loan_id, loan_data), (0, 8)),
                    ("❌ Decline", ("#dc3545", "#e74c3c"), ("#c82333", "#c0392b"), 
                     lambda loan_id=loan['id']: self.decline_loan_application(loan_id), (0, 0))
                ]:
                    ctk.CTkButton(button_frame, text=text, font=ctk.CTkFont(size=11, weight="bold"), 
                                 height=35, width=90, fg_color=color, hover_color=hover_color, 
                                 command=func).pack(side="top", pady=pady)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing pending loans: {str(e)}")

    def refresh_active_loans(self):
        try:
            for widget in self.active_loans_frame.winfo_children():
                widget.destroy()
            
            active_loans = self.get_active_loans()
            
            if not active_loans:
                ctk.CTkLabel(self.active_loans_frame, text="📋 No active loans at this time.", 
                            font=ctk.CTkFont(size=14), text_color=("gray60", "gray40")).pack(pady=50)
                return
            
            header_frame = ctk.CTkFrame(self.active_loans_frame)
            header_frame.pack(fill="x", padx=10, pady=(10, 5))
            
            header_text = f"{'Borrower':<20} {'Amount':<12} {'Balance':<12} {'Rate':<6} {'Payment':<10} {'Next Due':<12}"
            ctk.CTkLabel(header_frame, text=header_text, font=ctk.CTkFont(size=11, weight="bold", family="Courier"), 
                        text_color=("#495057", "#6c757d")).pack(pady=8)
            
            for loan in active_loans:
                loan_frame = ctk.CTkFrame(self.active_loans_frame)
                loan_frame.pack(fill="x", padx=10, pady=3)
                
                progress = ((loan['principal_amount'] - loan['remaining_balance']) / loan['principal_amount']) * 100
                
                loan_text = (f"{loan['borrower_name']:<20} "
                            f"₱{loan['principal_amount']:<11,.0f} "
                            f"₱{loan['remaining_balance']:<11,.2f} "
                            f"{loan['interest_rate']:<5.1f}% "
                            f"₱{loan['monthly_payment']:<9,.0f} "
                            f"{loan['next_payment_date']}")
                
                ctk.CTkLabel(loan_frame, text=loan_text, font=ctk.CTkFont(size=10, family="Courier")).pack(pady=8, padx=15, anchor="w")
                
                progress_bar = ctk.CTkProgressBar(loan_frame, width=200, height=8)
                progress_bar.set(progress / 100)
                progress_bar.pack(pady=(0, 8), padx=15, anchor="w")
                
                ctk.CTkLabel(loan_frame, text=f"Paid: {progress:.1f}%", font=ctk.CTkFont(size=9), 
                            text_color=("gray60", "gray40")).pack(pady=(0, 8), padx=15, anchor="w")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing active loans: {str(e)}")

    def refresh_loan_history(self):
        try:
            for widget in self.loan_history_frame.winfo_children():
                widget.destroy()
            
            loan_history = self.get_loan_application_history()
            
            if not loan_history:
                ctk.CTkLabel(self.loan_history_frame, text="📋 No loan application history found.", 
                            font=ctk.CTkFont(size=14), text_color=("gray60", "gray40")).pack(pady=50)
                return
            
            header_frame = ctk.CTkFrame(self.loan_history_frame)
            header_frame.pack(fill="x", padx=10, pady=(10, 5))
            
            ctk.CTkLabel(header_frame, text="Complete Loan Application History (Most Recent First)", 
                        font=ctk.CTkFont(size=13, weight="bold"), text_color=("#495057", "#6c757d")).pack(pady=10)
            
            for app in loan_history:
                app_frame = ctk.CTkFrame(self.loan_history_frame)
                app_frame.pack(fill="x", padx=10, pady=5)
                
                status_data = {
                    'approved': (("#28a745", "#20c997"), "✅"),
                    'rejected': (("#dc3545", "#e74c3c"), "❌"),
                    'pending': (("#ffc107", "#f39c12"), "⏳")
                }
                status_color, status_icon = status_data.get(app['status'], status_data['pending'])
                
                info_frame = ctk.CTkFrame(app_frame, fg_color="transparent")
                info_frame.pack(fill="both", expand=True, padx=15, pady=12)
                
                row1_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
                row1_frame.pack(fill="x", anchor="w")
                
                ctk.CTkLabel(row1_frame, text=f"{status_icon} {app['applicant_name']} - ₱{app['amount']:,.2f} - {app['status'].upper()}", 
                            font=ctk.CTkFont(size=13, weight="bold"), text_color=status_color).pack(side="left")
                
                ctk.CTkLabel(row1_frame, text=f"Applied: {app['applied_at']}", font=ctk.CTkFont(size=11), 
                            text_color=("gray60", "gray40")).pack(side="right")
                
                ctk.CTkLabel(info_frame, text=f"Account: {app['account_number']} | Purpose: {app['purpose']} | Income: ₱{app['monthly_income']:,.2f}", 
                            font=ctk.CTkFont(size=11), text_color=("gray70", "gray50")).pack(anchor="w", pady=(3, 0))
                
                if app['status'] == 'approved' and app['processed_at']:
                    ctk.CTkLabel(info_frame, text=f"Approved: {app['processed_at']} | Rate: {app['interest_rate']}% | Term: {app['term_months']} months | Payment: ₱{app['monthly_payment']:,.2f}", 
                                font=ctk.CTkFont(size=10), text_color=("#28a745", "#20c997")).pack(anchor="w", pady=(2, 0))
                
                if app['admin_notes']:
                    ctk.CTkLabel(info_frame, text=f"Notes: {app['admin_notes']}", font=ctk.CTkFont(size=10), 
                                text_color=("gray60", "gray40")).pack(anchor="w", pady=(2, 0))
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing loan history: {str(e)}")

    def get_pending_loans(self):
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
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Approve Loan Application")
        dialog.geometry("400x500")
        dialog.transient(self.parent)
        dialog.grab_set()
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 200
        y = (dialog.winfo_screenheight() // 2) - 250
        dialog.geometry(f"400x500+{x}+{y}")
        
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="Approve Loan Application", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 20))
        ctk.CTkLabel(main_frame, text=f"Applicant: {loan_data['applicant_name']}\nAmount: ₱{loan_data['amount']:,.2f}\nPurpose: {loan_data['purpose']}", font=ctk.CTkFont(size=12), justify="left").pack(pady=(0, 20))
        
        ctk.CTkLabel(main_frame, text="Interest Rate (% annually):", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=20)
        rate_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., 15.0")
        rate_entry.pack(fill="x", padx=20, pady=(5, 15))
        rate_entry.insert(0, "15.0")
        
        ctk.CTkLabel(main_frame, text="Loan Term (months):", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=20)
        term_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., 12")
        term_entry.pack(fill="x", padx=20, pady=(5, 15))
        term_entry.insert(0, "12")
        
        ctk.CTkLabel(main_frame, text="Admin Notes (optional):", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=20)
        notes_entry = ctk.CTkTextbox(main_frame, height=80)
        notes_entry.pack(fill="x", padx=20, pady=(5, 20))
        
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
        
        ctk.CTkButton(button_frame, text="Cancel", font=ctk.CTkFont(size=12), height=35, width=100, fg_color=("gray60", "gray40"), command=dialog.destroy).pack(side="left", padx=(0, 10))
        ctk.CTkButton(button_frame, text="Approve Loan", font=ctk.CTkFont(size=12, weight="bold"), height=35, width=120, fg_color=("#28a745", "#20c997"), hover_color=("#218838", "#1dd1a1"), command=approve_loan).pack(side="right")

    def approve_loan_application(self, loan_id, interest_rate, term_months, admin_notes):
        try:
            self.admin_service.db.begin_transaction()
            loan_data = self.admin_service.db.fetch_one("SELECT amount, account_number FROM loan_applications WHERE id = %s", (loan_id,))
            if not loan_data:
                raise Exception("Loan application not found")
            
            principal = float(loan_data['amount'])
            monthly_rate = interest_rate / 100 / 12
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**term_months) / ((1 + monthly_rate)**term_months - 1) if monthly_rate > 0 else principal / term_months
            
            self.admin_service.db.execute_query("UPDATE loan_applications SET status = 'approved', interest_rate = %s, term_months = %s, monthly_payment = %s, admin_notes = %s, processed_at = NOW() WHERE id = %s", (interest_rate, term_months, monthly_payment, admin_notes, loan_id))
            
            import datetime
            next_payment_date = datetime.date.today() + datetime.timedelta(days=30)
            self.admin_service.db.execute_query("INSERT INTO loans (application_id, account_number, principal_amount, interest_rate, term_months, monthly_payment, remaining_balance, next_payment_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (loan_id, loan_data['account_number'], principal, interest_rate, term_months, monthly_payment, principal, next_payment_date))
            
            self.admin_service.db.execute_query("UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (principal, loan_data['account_number']))
            self.admin_service.db.execute_query("INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'loan_disbursement', %s)", (loan_data['account_number'], principal))
            
            self.admin_service.db.commit_transaction()
            return True
        except Exception as e:
            self.admin_service.db.rollback_transaction()
            print(f"Error approving loan: {str(e)}")
            return False

    def decline_loan_application(self, loan_id):
        reason = ctk.CTkInputDialog(text="Enter reason for declining loan application:", title="Decline Loan Application").get_input()
        if reason:
            try:
                if self.admin_service.db.execute_query("UPDATE loan_applications SET status = 'rejected', admin_notes = %s, processed_at = NOW() WHERE id = %s", (reason, loan_id)):
                    messagebox.showinfo("Success", "Loan application declined.")
                    self.refresh_loan_data()
                else:
                    messagebox.showerror("Error", "Failed to decline loan application.")
            except Exception as e:
                messagebox.showerror("Error", f"Error declining loan: {str(e)}")

    def setup_user_transactions_tab(self):
        """Setup the user transactions tab"""
        tab = self.tabview.tab("📊 User Transactions")
        self.create_tab_header(tab, "📊 User Transaction Histories", self.refresh_user_transactions)
        
        # Create main container with two sections
        main_container = ctk.CTkFrame(tab)
        main_container.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Left section - User list
        left_frame = ctk.CTkFrame(main_container)
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        ctk.CTkLabel(left_frame, text="👥 Select User", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        self.users_list_frame = ctk.CTkScrollableFrame(left_frame)
        self.users_list_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Right section - Transaction details
        right_frame = ctk.CTkFrame(main_container)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        self.transaction_details_frame = ctk.CTkFrame(right_frame)
        self.transaction_details_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initialize with empty state
        self.show_empty_transaction_state()

    def refresh_user_transactions(self):
        try:
            for widget in self.users_list_frame.winfo_children():
                widget.destroy()
            
            all_users = self.admin_service.get_all_users()
            approved_users = [user for user in all_users if user['is_approved']]
            
            if not approved_users:
                ctk.CTkLabel(self.users_list_frame, text="No approved users found.", 
                            font=ctk.CTkFont(size=12), text_color=("gray60", "gray40")).pack(pady=20)
                return
            
            for user in approved_users:
                user_frame = ctk.CTkFrame(self.users_list_frame)
                user_frame.pack(fill="x", padx=5, pady=3)
                
                tx_summary = self.admin_service.get_user_transaction_summary(user['account_number'])
                
                user_button = ctk.CTkButton(
                    user_frame,
                    text=f"👤 {user['name']}\nAccount: {user['account_number']}\nTransactions: {tx_summary['total']}",
                    font=ctk.CTkFont(size=11),
                    height=60,
                    fg_color=("gray70", "gray30"),
                    hover_color=("#007bff", "#0066cc"),
                    command=lambda acc=user['account_number'], name=user['name']: self.show_user_transactions(acc, name)
                )
                user_button.pack(fill="x", padx=10, pady=8)
                
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Error refreshing user transactions: {str(e)}")

    def show_empty_transaction_state(self):
        for widget in self.transaction_details_frame.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(
            self.transaction_details_frame,
            text="📊 Select a user to view transaction history",
            font=ctk.CTkFont(size=14),
            text_color=("gray60", "gray40")
        ).pack(expand=True)

    def show_user_transactions(self, account_number: str, user_name: str):
        try:
            # Clear the transaction details frame
            for widget in self.transaction_details_frame.winfo_children():
                widget.destroy()
            
            # Header
            header_frame = ctk.CTkFrame(self.transaction_details_frame)
            header_frame.pack(fill="x", padx=10, pady=(10, 5))
            
            ctk.CTkLabel(
                header_frame,
                text=f"📊 Transaction History - {user_name}",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(side="left", padx=15, pady=10)
            
            ctk.CTkLabel(
                header_frame,
                text=f"Account: {account_number}",
                font=ctk.CTkFont(size=12),
                text_color=("gray60", "gray40")
            ).pack(side="left", padx=(0, 15), pady=10)
            
            # Period tabs
            period_tabview = ctk.CTkTabview(self.transaction_details_frame)
            period_tabview.pack(fill="both", expand=True, padx=10, pady=(5, 10))
            
            periods = [
                ("📅 Today", "today"),
                ("📆 This Month", "month"), 
                ("📋 This Year", "year"),
                ("📜 All Time", "all")
            ]
            
            for tab_name, period_key in periods:
                period_tabview.add(tab_name)
                self.setup_transaction_period_tab(period_tabview.tab(tab_name), account_number, period_key)
            
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Error loading transaction history: {str(e)}")

    def setup_transaction_period_tab(self, tab, account_number: str, period: str):
        try:
            transactions = self.admin_service.get_user_transactions_by_period(account_number, period)
            
            if not transactions:
                ctk.CTkLabel(
                    tab,
                    text=f"No transactions found for this period.",
                    font=ctk.CTkFont(size=12),
                    text_color=("gray60", "gray40")
                ).pack(expand=True)
                return
            
            # Scrollable frame for transactions
            scroll_frame = ctk.CTkScrollableFrame(tab)
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            header_frame = ctk.CTkFrame(scroll_frame)
            header_frame.pack(fill="x", padx=5, pady=(5, 10))
            
            header_text = f"{'Type':<20} {'Amount':<15} {'Date & Time':<20}"
            ctk.CTkLabel(
                header_frame,
                text=header_text,
                font=ctk.CTkFont(size=11, weight="bold", family="Courier"),
                text_color=("#495057", "#6c757d")
            ).pack(pady=8)
            
            # Transaction list
            for tx in transactions:
                tx_frame = ctk.CTkFrame(scroll_frame)
                tx_frame.pack(fill="x", padx=5, pady=2)
                
                formatted_time = tx['timestamp'].strftime("%Y-%m-%d %H:%M")
                
                type_colors = {
                    'deposit': ("#28a745", "#20c997"),
                    'withdrawal': ("#dc3545", "#e74c3c"),
                    'transfer_in': ("#007bff", "#0066cc"),
                    'transfer_out': ("#fd7e14", "#f39c12"),
                    'loan_disbursement': ("#17a2b8", "#17a2b8"),
                    'loan_payment': ("#6f42c1", "#6f42c1")
                }
                
                color = type_colors.get(tx['type'], ("gray60", "gray40"))
                
                tx_text = f"{tx['type_display']:<20} {tx['formatted_amount']:<15} {formatted_time}"
                
                ctk.CTkLabel(
                    tx_frame,
                    text=tx_text,
                    font=ctk.CTkFont(size=10, family="Courier"),
                    text_color=color
                ).pack(pady=6, padx=10, anchor="w")
            
            # Summary at bottom
            total_amount = sum(tx['amount'] for tx in transactions if tx['type'] in ['deposit', 'transfer_in', 'loan_disbursement'])
            total_out = sum(tx['amount'] for tx in transactions if tx['type'] in ['withdrawal', 'transfer_out', 'loan_payment'])
            
            summary_frame = ctk.CTkFrame(scroll_frame)
            summary_frame.pack(fill="x", padx=5, pady=(10, 5))
            
            summary_text = f"Total In: ₱{total_amount:,.2f} | Total Out: ₱{total_out:,.2f} | Net: ₱{total_amount - total_out:,.2f}"
            ctk.CTkLabel(
                summary_frame,
                text=summary_text,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=("#495057", "#6c757d")
            ).pack(pady=8)
            
        except Exception as e:
            ctk.CTkLabel(
                tab,
                text=f"Error loading transactions: {str(e)}",
                font=ctk.CTkFont(size=12),
                text_color=("#dc3545", "#e74c3c")
            ).pack(expand=True)

    def destroy(self):
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()