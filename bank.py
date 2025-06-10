import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
from datetime import datetime

# Import your existing classes (assuming they're in the same directory)
try:
    from auth import Auth
    from account import AccountManager
    from transaction import TransactionManager
    from history import History
    from admin import Admin
    from loan import LoanManager
    from database import Database
except ImportError:
    messagebox.showerror("Import Error", "Could not import required modules. Make sure all your banking system files are in the same directory.")
    sys.exit()

class BANKING:
    ADMIN_ACCT_NO = '0000000001'
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IRNVault Banking System")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Initialize backend components
        self.db = Database()
        self.auth = Auth(self.db)
        self.acct_mgr = AccountManager(self.db)
        self.txn_mgr = TransactionManager(self.db)
        self.history = History(self.db)
        self.admin = Admin(self.db)
        self.loan_mgr = LoanManager(self.db)
        
        self.current_user = None
        self.current_frame = None
        
        # Style configuration
        self.setup_styles()
        
        # Start with main menu
        self.show_main_menu()
        
    def setup_styles(self):
        """Setup custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', 
                       font=('Arial', 20, 'bold'),
                       background='#2c3e50',
                       foreground='white')
        
        style.configure('Subtitle.TLabel',
                       font=('Arial', 12),
                       background='#2c3e50',
                       foreground='#ecf0f1')
        
        style.configure('Custom.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=10)
        
    def clear_frame(self):
        """Clear the current frame"""
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_main_menu(self):
        """Display the main menu"""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg='#2c3e50')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(self.current_frame, 
                               text="🏦 IRNVault Banking System",
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(self.current_frame,
                                  text="Your trusted financial partner",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(self.current_frame, bg='#2c3e50')
        button_frame.pack(pady=30)
        
        # Main menu buttons
        register_btn = ttk.Button(button_frame, 
                                 text="Register New Account",
                                 style='Custom.TButton',
                                 command=self.show_register)
        register_btn.pack(pady=10, fill='x', ipadx=20)
        
        login_btn = ttk.Button(button_frame,
                              text="Login to Account", 
                              style='Custom.TButton',
                              command=self.show_login)
        login_btn.pack(pady=10, fill='x', ipadx=20)
        
        exit_btn = ttk.Button(button_frame,
                             text="Exit Application",
                             style='Custom.TButton', 
                             command=self.exit_app)
        exit_btn.pack(pady=10, fill='x', ipadx=20)
    
    def show_register(self):
        """Display registration form"""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg='#2c3e50')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(self.current_frame,
                               text="Account Registration",
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.current_frame, bg='#2c3e50')
        form_frame.pack(pady=20)
        
        # Name field
        ttk.Label(form_frame, text="Full Name:", background='#2c3e50', foreground='white').grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30)
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # PIN field
        ttk.Label(form_frame, text="6-digit PIN:", background='#2c3e50', foreground='white').grid(row=1, column=0, sticky='w', pady=5)
        self.pin_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30, show='*')
        self.pin_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Buttons
        button_frame = tk.Frame(self.current_frame, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        submit_btn = ttk.Button(button_frame, text="Register", command=self.register_account)
        submit_btn.pack(side='left', padx=10)
        
        back_btn = ttk.Button(button_frame, text="Back", command=self.show_main_menu)
        back_btn.pack(side='left', padx=10)
    
    def register_account(self):
        """Handle account registration"""
        name = self.name_entry.get().strip()
        pin = self.pin_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter your full name.")
            return
            
        if not pin.isdigit() or len(pin) != 6:
            messagebox.showerror("Error", "PIN must be exactly 6 digits.")
            return
        
        try:
            pin_hash = self.auth.hash_pin(pin)
            self.acct_mgr.register(name, pin_hash)
            messagebox.showinfo("Success", "Account registered successfully! Please wait for admin approval.")
            self.show_main_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
    
    def show_login(self):
        """Display login form"""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg='#2c3e50')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(self.current_frame,
                               text="Account Login",
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.current_frame, bg='#2c3e50')
        form_frame.pack(pady=20)
        
        # Account number field
        ttk.Label(form_frame, text="Account Number:", background='#2c3e50', foreground='white').grid(row=0, column=0, sticky='w', pady=5)
        self.acct_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30)
        self.acct_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # PIN field
        ttk.Label(form_frame, text="PIN:", background='#2c3e50', foreground='white').grid(row=1, column=0, sticky='w', pady=5)
        self.login_pin_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30, show='*')
        self.login_pin_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Buttons
        button_frame = tk.Frame(self.current_frame, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        login_btn = ttk.Button(button_frame, text="Login", command=self.login_account)
        login_btn.pack(side='left', padx=10)
        
        back_btn = ttk.Button(button_frame, text="Back", command=self.show_main_menu)
        back_btn.pack(side='left', padx=10)
    
    def login_account(self):
        """Handle account login"""
        acct_no = self.acct_entry.get().strip()
        pin = self.login_pin_entry.get().strip()
        
        if not acct_no or not pin:
            messagebox.showerror("Error", "Please enter both account number and PIN.")
            return
        
        # Check for admin login
        if acct_no == self.ADMIN_ACCT_NO:
            if self.admin_login(pin, acct_no):
                self.show_admin_menu()
            return
        
        # Regular user login
        try:
            login_success, message = self.auth.login(acct_no, pin)
            if login_success:
                self.current_user = acct_no
                messagebox.showinfo("Success", f"Welcome! Login successful.")
                self.show_user_menu()
            else:
                messagebox.showerror("Login Failed", message)
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")
    
    def admin_login(self, pin, acct_no):
        """Handle admin login verification"""
        try:
            self.db.connect()
            self.db.cursor.execute(
                "SELECT hashed_pin FROM accounts WHERE account_number = %s",
                (acct_no,)
            )
            row = self.db.cursor.fetchone()
            self.db.close()
            
            if not row or not self.auth.verify_pin(pin, row[0].encode()):
                messagebox.showerror("Login Failed", "Invalid admin credentials.")
                return False
            
            messagebox.showinfo("Admin Login", "Admin login successful!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Admin login failed: {str(e)}")
            return False
    
    def show_user_menu(self):
        """Display user banking menu"""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg='#2c3e50')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(self.current_frame,
                               text=f"Account Dashboard - {self.current_user}",
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Banking services frame
        banking_frame = tk.LabelFrame(self.current_frame, text="💰 Banking Services", 
                                     bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        banking_frame.pack(fill='x', pady=10, padx=20)
        
        # Banking buttons
        banking_buttons = [
            ("Deposit Money", self.show_deposit),
            ("Withdraw Money", self.show_withdraw),
            ("Transfer Money", self.show_transfer),
            ("Check Balance", self.check_balance),
            ("Mini Statement", self.show_mini_statement)
        ]
        
        for i, (text, command) in enumerate(banking_buttons):
            btn = ttk.Button(banking_frame, text=text, command=command)
            btn.grid(row=i//2, column=i%2, padx=10, pady=5, sticky='ew')
        
        # Configure column weights for even distribution
        banking_frame.columnconfigure(0, weight=1)
        banking_frame.columnconfigure(1, weight=1)
        
        # Loan services frame
        loan_frame = tk.LabelFrame(self.current_frame, text="🏦 Loan Services",
                                  bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        loan_frame.pack(fill='x', pady=10, padx=20)
        
        # Loan buttons
        loan_buttons = [
            ("Apply for Loan", self.show_loan_application),
            ("Loan Status", self.show_loan_status),
            ("Make Payment", self.show_loan_payment)
        ]
        
        for i, (text, command) in enumerate(loan_buttons):
            btn = ttk.Button(loan_frame, text=text, command=command)
            btn.grid(row=0, column=i, padx=10, pady=5, sticky='ew')
        
        # Configure column weights
        for i in range(3):
            loan_frame.columnconfigure(i, weight=1)
        
        # Logout button
        logout_btn = ttk.Button(self.current_frame, text="Logout", 
                               command=self.logout, style='Custom.TButton')
        logout_btn.pack(pady=20)
    
    def show_deposit(self):
        """Show deposit dialog"""
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount is not None and amount > 0:
            try:
                self.txn_mgr.deposit(self.current_user, amount)
                messagebox.showinfo("Success", f"Successfully deposited ₱{amount:,.2f}")
            except Exception as e:
                messagebox.showerror("Error", f"Deposit failed: {str(e)}")
        elif amount is not None:
            messagebox.showerror("Error", "Amount must be positive.")
    
    def show_withdraw(self):
        """Show withdraw dialog"""
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount is not None and amount > 0:
            try:
                self.txn_mgr.withdraw(self.current_user, amount)
                messagebox.showinfo("Success", f"Successfully withdrew ₱{amount:,.2f}")
            except Exception as e:
                messagebox.showerror("Error", f"Withdrawal failed: {str(e)}")
        elif amount is not None:
            messagebox.showerror("Error", "Amount must be positive.")
    
    def show_transfer(self):
        """Show transfer dialog"""
        # Create custom dialog for transfer
        transfer_window = tk.Toplevel(self.root)
        transfer_window.title("Transfer Money")
        transfer_window.geometry("400x200")
        transfer_window.configure(bg='#2c3e50')
        transfer_window.transient(self.root)
        transfer_window.grab_set()
        
        # Center the window
        transfer_window.geometry("+{}+{}".format(
            int(self.root.winfo_x() + self.root.winfo_width()/2 - 200),
            int(self.root.winfo_y() + self.root.winfo_height()/2 - 100)
        ))
        
        # Form fields
        ttk.Label(transfer_window, text="Target Account:", background='#2c3e50', foreground='white').pack(pady=5)
        target_entry = ttk.Entry(transfer_window, font=('Arial', 10), width=30)
        target_entry.pack(pady=5)
        
        ttk.Label(transfer_window, text="Amount:", background='#2c3e50', foreground='white').pack(pady=5)
        amount_entry = ttk.Entry(transfer_window, font=('Arial', 10), width=30)
        amount_entry.pack(pady=5)
        
        def process_transfer():
            target = target_entry.get().strip()
            amount_str = amount_entry.get().strip()
            
            if not target or not amount_str:
                messagebox.showerror("Error", "Please fill all fields.")
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive.")
                    return
                
                self.txn_mgr.transfer(self.current_user, target, amount)
                messagebox.showinfo("Success", f"Successfully transferred ₱{amount:,.2f} to {target}")
                transfer_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount.")
            except Exception as e:
                messagebox.showerror("Error", f"Transfer failed: {str(e)}")
        
        # Buttons
        button_frame = tk.Frame(transfer_window, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Transfer", command=process_transfer).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Cancel", command=transfer_window.destroy).pack(side='left', padx=10)
    
    def check_balance(self):
        """Display current balance"""
        try:
            self.db.connect()
            self.db.cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = %s", 
                (self.current_user,)
            )
            balance = self.db.cursor.fetchone()[0]
            self.db.close()
            
            messagebox.showinfo("Current Balance", f"💰 Your current balance: ₱{float(balance):,.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve balance: {str(e)}")
    
    def show_mini_statement(self):
        """Display mini statement in a new window"""
        try:
            # Create new window for statement
            statement_window = tk.Toplevel(self.root)
            statement_window.title("Mini Statement")
            statement_window.geometry("700x500")
            statement_window.configure(bg='#2c3e50')
            statement_window.resizable(True, True)
            
            # Create header
            header_frame = tk.Frame(statement_window, bg='#2c3e50')
            header_frame.pack(fill='x', padx=10, pady=(10, 0))
            
            header_label = tk.Label(header_frame, text="Mini Statement", 
                                font=('Arial', 16, 'bold'), 
                                bg='#2c3e50', fg='white')
            header_label.pack()
            
            # Create text widget with scrollbar
            text_frame = tk.Frame(statement_window, bg='#2c3e50')
            text_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            text_widget = tk.Text(text_frame, font=('Courier', 10), 
                                bg='white', fg='black',
                                wrap='none', padx=10, pady=10)
            
            # Add scrollbars
            v_scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
            h_scrollbar = ttk.Scrollbar(text_frame, orient='horizontal', command=text_widget.xview)
            
            text_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
            
            # Pack scrollbars and text widget
            v_scrollbar.pack(side='right', fill='y')
            h_scrollbar.pack(side='bottom', fill='x')
            text_widget.pack(side='left', fill='both', expand=True)
            
            # Get formatted statement text from History class
            if hasattr(self, 'history') and self.history:
                statement_text = self.history.format_mini_statement_text(self.current_user)
            else:
                # If history object doesn't exist, create it or show error
                statement_text = f"=== MINI STATEMENT ===\n"
                statement_text += f"Account: {self.current_user}\n"
                statement_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                statement_text += "Error: History service not available.\n"
                statement_text += "Please ensure your History class is properly initialized."
            
            # Insert text and make read-only
            text_widget.insert('1.0', statement_text)
            text_widget.config(state='disabled')
            
            # Add close button
            button_frame = tk.Frame(statement_window, bg='#2c3e50')
            button_frame.pack(fill='x', padx=10, pady=(0, 10))
            
            close_button = tk.Button(button_frame, text="Close", 
                                    command=statement_window.destroy,
                                    font=('Arial', 10), 
                                    bg='#e74c3c', fg='white',
                                    padx=20, pady=5)
            close_button.pack(side='right')
            
            # Print button
            print_button = tk.Button(button_frame, text="Print", 
                                    command=lambda: self.print_statement(statement_text),
                                    font=('Arial', 10), 
                                    bg='#3498db', fg='white',
                                    padx=20, pady=5)
            print_button.pack(side='right', padx=(0, 10))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate statement: {str(e)}")

    def print_statement(self, statement_text):
        """Print or save statement to file"""
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Mini Statement"
            )
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(statement_text)
                messagebox.showinfo("Success", f"Statement saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save statement: {str(e)}")
    
    def show_loan_application(self):
        """Show loan application form"""
        # Create loan application window
        loan_window = tk.Toplevel(self.root)
        loan_window.title("Loan Application")
        loan_window.geometry("500x600")
        loan_window.configure(bg='#2c3e50')
        loan_window.transient(self.root)
        loan_window.grab_set()
        
        # Create scrollable frame
        canvas = tk.Canvas(loan_window, bg='#2c3e50')
        scrollbar = ttk.Scrollbar(loan_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2c3e50')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        ttk.Label(scrollable_frame, text="🏦 Loan Application", 
                 font=('Arial', 16, 'bold'), background='#2c3e50', foreground='white').pack(pady=10)
        
        # Form fields
        fields_frame = tk.Frame(scrollable_frame, bg='#2c3e50')
        fields_frame.pack(pady=20, padx=20)
        
        # Loan amount
        ttk.Label(fields_frame, text="Loan Amount (₱):", background='#2c3e50', foreground='white').grid(row=0, column=0, sticky='w', pady=5)
        amount_entry = ttk.Entry(fields_frame, font=('Arial', 10), width=30)
        amount_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Purpose
        ttk.Label(fields_frame, text="Purpose:", background='#2c3e50', foreground='white').grid(row=1, column=0, sticky='w', pady=5)
        purpose_entry = ttk.Entry(fields_frame, font=('Arial', 10), width=30)
        purpose_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Monthly income
        ttk.Label(fields_frame, text="Monthly Income (₱):", background='#2c3e50', foreground='white').grid(row=2, column=0, sticky='w', pady=5)
        income_entry = ttk.Entry(fields_frame, font=('Arial', 10), width=30)
        income_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Employment status
        ttk.Label(fields_frame, text="Employment:", background='#2c3e50', foreground='white').grid(row=3, column=0, sticky='w', pady=5)
        employment_var = tk.StringVar()
        employment_combo = ttk.Combobox(fields_frame, textvariable=employment_var, width=27, state='readonly')
        employment_combo['values'] = ('Full-time Employee', 'Part-time Employee', 'Self-employed', 
                                     'Business Owner', 'Freelancer', 'Other')
        employment_combo.grid(row=3, column=1, pady=5, padx=10)
        
        def submit_loan():
            try:
                amount = float(amount_entry.get())
                purpose = purpose_entry.get().strip()
                income = float(income_entry.get())
                employment = employment_var.get()
                
                if not all([amount, purpose, income, employment]):
                    messagebox.showerror("Error", "Please fill all fields.")
                    return
                
                if amount <= 0 or income <= 0:
                    messagebox.showerror("Error", "Amount and income must be positive.")
                    return
                
                if amount > 1000000:
                    messagebox.showerror("Error", "Maximum loan amount is ₱1,000,000.")
                    return
                
                # Calculate estimated payment
                estimated_payment = self.loan_mgr._calculate_monthly_payment(amount, 12.0, 12)
                dti_ratio = (estimated_payment / income) * 100
                
                # Show summary
                summary = f"Loan Amount: ₱{amount:,.2f}\n"
                summary += f"Purpose: {purpose}\n"
                summary += f"Monthly Income: ₱{income:,.2f}\n"
                summary += f"Employment: {employment}\n\n"
                summary += f"Estimated Monthly Payment: ₱{estimated_payment:,.2f}\n"
                summary += f"Debt-to-Income Ratio: {dti_ratio:.1f}%\n\n"
                
                if dti_ratio > 40:
                    summary += "⚠️ WARNING: High debt-to-income ratio."
                elif dti_ratio > 25:
                    summary += "⚡ NOTE: Moderate debt-to-income ratio."
                else:
                    summary += "✅ Good debt-to-income ratio."
                
                if messagebox.askyesno("Confirm Application", summary + "\n\nSubmit this application?"):
                    self.loan_mgr.apply_for_loan(self.current_user, amount, purpose, income, employment)
                    messagebox.showinfo("Success", "Loan application submitted successfully!")
                    loan_window.destroy()
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for amount and income.")
            except Exception as e:
                messagebox.showerror("Error", f"Application failed: {str(e)}")
        
        # Buttons
        button_frame = tk.Frame(scrollable_frame, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Submit Application", command=submit_loan).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Cancel", command=loan_window.destroy).pack(side='left', padx=10)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_loan_status(self):
        """Display loan status in a new window"""
        try:
            # Create new window for loan status
            status_window = tk.Toplevel(self.root)
            status_window.title("Loan Status")
            status_window.geometry("800x600")
            status_window.configure(bg='#2c3e50')
            status_window.resizable(True, True)
            
            # Create header
            header_frame = tk.Frame(status_window, bg='#2c3e50')
            header_frame.pack(fill='x', padx=10, pady=(10, 0))
            
            header_label = tk.Label(header_frame, text="Loan Status", 
                                font=('Arial', 16, 'bold'), 
                                bg='#2c3e50', fg='white')
            header_label.pack()
            
            # Create text widget with scrollbar
            text_frame = tk.Frame(status_window, bg='#2c3e50')
            text_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            text_widget = tk.Text(text_frame, font=('Courier', 10), 
                                bg='white', fg='black',
                                wrap='none', padx=10, pady=10)
            
            # Add scrollbars
            v_scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
            h_scrollbar = ttk.Scrollbar(text_frame, orient='horizontal', command=text_widget.xview)
            
            text_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
            
            # Pack scrollbars and text widget
            v_scrollbar.pack(side='right', fill='y')
            h_scrollbar.pack(side='bottom', fill='x')
            text_widget.pack(side='left', fill='both', expand=True)
            
            # Get loan status from LoanManager
            if hasattr(self, 'loan_mgr') and self.loan_mgr:
                status_text = self.loan_mgr.get_loan_status_gui(self.current_user)
            else:
                # If loan manager doesn't exist, show error message
                status_text = "=" * 60 + "\n"
                status_text += "                     LOAN STATUS REPORT\n"
                status_text += "=" * 60 + "\n\n"
                status_text += f"Account Number: {self.current_user}\n"
                status_text += f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                status_text += "Error: Loan Manager service not available.\n"
                status_text += "Please ensure your LoanManager class is properly initialized.\n"
                status_text += "=" * 60 + "\n"
            
            # Insert text and make read-only
            text_widget.insert('1.0', status_text)
            text_widget.config(state='disabled')
            
            # Add buttons
            button_frame = tk.Frame(status_window, bg='#2c3e50')
            button_frame.pack(fill='x', padx=10, pady=(0, 10))
            
            # Refresh button
            refresh_button = tk.Button(button_frame, text="Refresh", 
                                    command=lambda: self.refresh_loan_status(text_widget),
                                    font=('Arial', 10), 
                                    bg='#27ae60', fg='white',
                                    padx=20, pady=5)
            refresh_button.pack(side='left')
            
            # Close button
            close_button = tk.Button(button_frame, text="Close", 
                                    command=status_window.destroy,
                                    font=('Arial', 10), 
                                    bg='#e74c3c', fg='white',
                                    padx=20, pady=5)
            close_button.pack(side='right')
            
            # Print/Save button
            save_button = tk.Button(button_frame, text="Save Report", 
                                command=lambda: self.save_loan_report(status_text),
                                font=('Arial', 10), 
                                bg='#3498db', fg='white',
                                padx=20, pady=5)
            save_button.pack(side='right', padx=(0, 10))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve loan status: {str(e)}")

    def refresh_loan_status(self, text_widget):
        """Refresh the loan status display"""
        try:
            # Get updated loan status
            if hasattr(self, 'loan_mgr') and self.loan_mgr:
                status_text = self.loan_mgr.get_loan_status_gui(self.current_user)
            else:
                status_text = "Error: Loan Manager service not available."
            
            # Update text widget
            text_widget.config(state='normal')
            text_widget.delete('1.0', 'end')
            text_widget.insert('1.0', status_text)
            text_widget.config(state='disabled')
            
            messagebox.showinfo("Success", "Loan status refreshed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh loan status: {str(e)}")

    def save_loan_report(self, report_text):
        """Save loan status report to file"""
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Loan Status Report"
            )
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(report_text)
                messagebox.showinfo("Success", f"Loan status report saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")
        
    def show_loan_payment(self):
        """Show loan payment options"""
        try:
            payoff_amount = self.loan_mgr.get_payoff_amount(self.current_user)
            if payoff_amount is None:
                messagebox.showinfo("No Active Loan", "You don't have any active loans.")
                return
            
            # Create payment window
            payment_window = tk.Toplevel(self.root)
            payment_window.title("Loan Payment")
            payment_window.geometry("400x300")
            payment_window.configure(bg='#2c3e50')
            payment_window.transient(self.root)
            payment_window.grab_set()
            
            ttk.Label(payment_window, text="💳 Loan Payment Options", 
                     font=('Arial', 14, 'bold'), background='#2c3e50', foreground='white').pack(pady=20)
            
            ttk.Label(payment_window, text=f"Total Payoff Amount: ₱{payoff_amount:,.2f}", 
                     background='#2c3e50', foreground='white').pack(pady=10)
            
            # Payment amount entry
            ttk.Label(payment_window, text="Payment Amount:", background='#2c3e50', foreground='white').pack(pady=5)
            amount_entry = ttk.Entry(payment_window, font=('Arial', 10), width=20)
            amount_entry.pack(pady=5)
            
            def make_payment():
                try:
                    amount = float(amount_entry.get())
                    if amount <= 0:
                        messagebox.showerror("Error", "Amount must be positive.")
                        return
                    
                    self.loan_mgr.make_loan_payment(self.current_user, amount, pay_in_full=False)
                    messagebox.showinfo("Success", f"Payment of ₱{amount:,.2f} processed successfully!")
                    payment_window.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid amount.")
                except Exception as e:
                    messagebox.showerror("Error", f"Payment failed: {str(e)}")
            
            def pay_in_full():
                """Handle full loan payment"""
                if messagebox.askyesno("Confirm", f"Pay full amount of ₱{payoff_amount:,.2f}?"):
                    try:
                        from decimal import Decimal
                        
                        # Get remaining balance from loan
                        self.loan_mgr.db.connect()
                        self.loan_mgr.db.cursor.execute(
                            """SELECT l.id, l.remaining_balance 
                            FROM loans l 
                            WHERE l.account_number = %s 
                            AND l.status = 'active' 
                            LIMIT 1""",
                            (self.current_user,)
                        )
                        loan_data = self.loan_mgr.db.cursor.fetchone()
                        
                        if not loan_data:
                            raise Exception("No active loan found")
                            
                        loan_id, remaining = loan_data
                        
                        # Convert to Decimal for precise calculation
                        remaining = Decimal(str(remaining))
                        principal_portion = remaining * Decimal('0.9875')
                        interest_portion = remaining * Decimal('0.0125')
                        
                        # Start transaction
                        self.loan_mgr.db.cursor.execute("START TRANSACTION")
                        
                        # Record the payment
                        self.loan_mgr.db.cursor.execute(
                            """INSERT INTO loan_payments 
                            (loan_id, account_number, payment_amount, 
                                principal_portion, interest_portion, remaining_balance)
                            VALUES (%s, %s, %s, %s, %s, %s)""",
                            (loan_id, self.current_user, remaining, 
                            principal_portion, interest_portion, 0)
                        )
                        
                        # Update loan status and remaining balance
                        self.loan_mgr.db.cursor.execute(
                            """UPDATE loans 
                            SET remaining_balance = 0,
                                status = 'paid_off'
                            WHERE id = %s""",
                            (loan_id,)
                        )
                        
                        # Record transaction
                        self.loan_mgr.db.cursor.execute(
                            """INSERT INTO transactions 
                            (account_number, type, amount) 
                            VALUES (%s, 'loan_payment', %s)""",
                            (self.current_user, remaining)
                        )
                        
                        # Commit transaction
                        self.loan_mgr.db.cursor.execute("COMMIT")
                        self.loan_mgr.db.close()
                        
                        messagebox.showinfo("Success", "Loan paid in full!")
                        payment_window.destroy()
                        
                    except Exception as e:
                        # Rollback on error
                        if hasattr(self.loan_mgr.db, 'cursor'):
                            self.loan_mgr.db.cursor.execute("ROLLBACK")
                        if hasattr(self.loan_mgr.db, 'close'):
                            self.loan_mgr.db.close()
                        messagebox.showerror("Error", f"Payment failed: {str(e)}")
            
            # Buttons
            button_frame = tk.Frame(payment_window, bg='#2c3e50')
            button_frame.pack(pady=20)
            
            ttk.Button(button_frame, text="Make Payment", command=make_payment).pack(side='left', padx=10)
            ttk.Button(button_frame, text="Pay in Full", command=pay_in_full).pack(side='left', padx=10)
            ttk.Button(button_frame, text="Cancel", command=payment_window.destroy).pack(side='left', padx=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load payment options: {str(e)}")
    
    def show_admin_menu(self):
        """Display admin dashboard"""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg='#2c3e50')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(self.current_frame,
                               text="👑 Admin Dashboard",
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Account Management frame
        account_frame = tk.LabelFrame(self.current_frame, text="👥 Account Management", 
                                     bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        account_frame.pack(fill='x', pady=10, padx=20)
        
        account_buttons = [
            ("Pending Accounts", self.show_pending_accounts),
            ("Display Users", self.show_all_users)
        ]
        
        for i, (text, command) in enumerate(account_buttons):
            btn = ttk.Button(account_frame, text=text, command=command)
            btn.grid(row=0, column=i, padx=10, pady=5, sticky='ew')
        
        account_frame.columnconfigure(0, weight=1)
        account_frame.columnconfigure(1, weight=1)
        
        # Loan Management frame
        loan_frame = tk.LabelFrame(self.current_frame, text="🏦 Loan Management",
                                  bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        loan_frame.pack(fill='x', pady=10, padx=20)
        
        loan_buttons = [
            ("Pending Loans", self.show_pending_loans),
            ("Active Loans", self.show_active_loans),
            ("All Applications", self.show_all_loan_applications)
        ]
        
        for i, (text, command) in enumerate(loan_buttons):
            btn = ttk.Button(loan_frame, text=text, command=command)
            btn.grid(row=0, column=i, padx=10, pady=5, sticky='ew')
        
        for i in range(3):
            loan_frame.columnconfigure(i, weight=1)
        
        # Logout button
        logout_btn = ttk.Button(self.current_frame, text="Logout", 
                               command=self.logout, style='Custom.TButton')
        logout_btn.pack(pady=20)
    
    def show_pending_accounts(self):
        """Show pending account approvals"""
        try:
            pending = self.admin.list_pending()
            if not pending:
                messagebox.showinfo("No Pending Accounts", "No accounts awaiting approval.")
                return
            
            # Create window for pending accounts
            pending_window = tk.Toplevel(self.root)
            pending_window.title("Pending Account Approvals")
            pending_window.geometry("600x400")
            pending_window.configure(bg='#2c3e50')
            
            # Create treeview for account list
            frame = tk.Frame(pending_window, bg='#2c3e50')
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            tree = ttk.Treeview(frame, columns=('Name',), show='tree headings')
            tree.heading('#0', text='Account Number')
            tree.heading('Name', text='Full Name')
            
            for acct_no, name in pending:
                tree.insert('', 'end', text=acct_no, values=(name,))
            
            tree.pack(fill='both', expand=True)
            
            # Buttons frame
            button_frame = tk.Frame(pending_window, bg='#2c3e50')
            button_frame.pack(pady=10)
            
            def approve_account():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("No Selection", "Please select an account to approve.")
                    return
                
                acct_no = tree.item(selected[0])['text']
                try:
                    self.admin.approve(acct_no)
                    messagebox.showinfo("Success", f"Account {acct_no} approved successfully!")
                    tree.delete(selected[0])
                except Exception as e:
                    messagebox.showerror("Error", f"Approval failed: {str(e)}")
            
            def decline_account():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("No Selection", "Please select an account to decline.")
                    return
                
                acct_no = tree.item(selected[0])['text']
                reason = simpledialog.askstring("Decline Reason", "Enter reason for decline:")
                if reason:
                    try:
                        self.admin.decline(acct_no, reason)
                        messagebox.showinfo("Success", f"Account {acct_no} declined.")
                        tree.delete(selected[0])
                    except Exception as e:
                        messagebox.showerror("Error", f"Decline failed: {str(e)}")
            
            ttk.Button(button_frame, text="Approve", command=approve_account).pack(side='left', padx=10)
            ttk.Button(button_frame, text="Decline", command=decline_account).pack(side='left', padx=10)
            ttk.Button(button_frame, text="Close", command=pending_window.destroy).pack(side='left', padx=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load pending accounts: {str(e)}")
    
    def show_all_users(self):
        """Show all users with management options"""
        # Create user management window
        users_window = tk.Toplevel(self.root)
        users_window.title("User Management")
        users_window.geometry("800x500")
        users_window.configure(bg='#2c3e50')
        
        # Title
        title_label = tk.Label(users_window, text="📊 User Management System", 
                              font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=10)
        
        # Sort options frame
        sort_frame = tk.Frame(users_window, bg='#2c3e50')
        sort_frame.pack(pady=10)
        
        tk.Label(sort_frame, text="Sort by:", bg='#2c3e50', fg='white').pack(side='left', padx=5)
        
        sort_var = tk.StringVar(value="balance")
        tk.Radiobutton(sort_frame, text="Balance", variable=sort_var, value="balance", 
                      bg='#2c3e50', fg='white', selectcolor='#34495e').pack(side='left', padx=5)
        tk.Radiobutton(sort_frame, text="Name", variable=sort_var, value="name", 
                      bg='#2c3e50', fg='white', selectcolor='#34495e').pack(side='left', padx=5)
        
        # Users frame
        users_frame = tk.Frame(users_window, bg='#2c3e50')
        users_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for users
        tree = ttk.Treeview(users_frame, columns=('Name', 'Balance', 'Status'), show='tree headings')
        tree.heading('#0', text='Account Number')
        tree.heading('Name', text='Full Name')
        tree.heading('Balance', text='Balance')
        tree.heading('Status', text='Status')
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(users_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def refresh_users():
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
            
            try:
                order_by = sort_var.get()
                users = self.admin.list_users(order_by=order_by)
                
                for acct_no, name, balance in users:
                    formatted_balance = f"₱{float(balance):,.2f}"
                    tree.insert('', 'end', text=acct_no, values=(name, formatted_balance, "🟢 Active"))
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load users: {str(e)}")
        
        # Initial load
        refresh_users()
        
        # Buttons frame
        button_frame = tk.Frame(users_window, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select a user to delete.")
                return
            
            acct_no = tree.item(selected[0])['text']
            name = tree.item(selected[0])['values'][0]
            
            if messagebox.askyesno("Confirm Deletion", 
                                  f"Are you sure you want to delete account {acct_no} ({name})?\n\nThis action cannot be undone!"):
                try:
                    self.admin.delete_user(acct_no)
                    messagebox.showinfo("Success", f"Account {acct_no} deleted successfully!")
                    refresh_users()
                except Exception as e:
                    messagebox.showerror("Error", f"Deletion failed: {str(e)}")
        
        ttk.Button(button_frame, text="Refresh", command=refresh_users).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Delete User", command=delete_user).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Close", command=users_window.destroy).pack(side='left', padx=10)
    
    def show_pending_loans(self):
        """Show pending loan applications for admin approval"""
        try:
            applications = self.loan_mgr.list_pending_loans()
            if not applications:
                messagebox.showinfo("No Pending Loans", "No loan applications awaiting approval.")
                return
            
            # Create window for pending loans
            loans_window = tk.Toplevel(self.root)
            loans_window.title("Pending Loan Applications")
            loans_window.geometry("900x500")
            loans_window.configure(bg='#2c3e50')
            
            # Title
            title_label = tk.Label(loans_window, text="⏳ Pending Loan Applications", 
                                  font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
            title_label.pack(pady=10)
            
            # Create treeview for loan applications
            frame = tk.Frame(loans_window, bg='#2c3e50')
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            tree = ttk.Treeview(frame, columns=('Account', 'Name', 'Amount', 'Purpose', 'Income', 'Date'), 
                               show='tree headings')
            tree.heading('#0', text='App ID')
            tree.heading('Account', text='Account')
            tree.heading('Name', text='Name')
            tree.heading('Amount', text='Amount')
            tree.heading('Purpose', text='Purpose')
            tree.heading('Income', text='Income')
            tree.heading('Date', text='Applied Date')
            
            # Set column widths
            tree.column('#0', width=60)
            tree.column('Account', width=100)
            tree.column('Name', width=120)
            tree.column('Amount', width=100)
            tree.column('Purpose', width=150)
            tree.column('Income', width=100)
            tree.column('Date', width=120)
            
            for app in applications:
                app_id, acct_no, name, amount, purpose, income, employment, applied_date = app
                formatted_amount = f"₱{float(amount):,.2f}"
                formatted_income = f"₱{float(income):,.2f}"
                formatted_date = applied_date.strftime('%Y-%m-%d')
                
                tree.insert('', 'end', text=str(app_id), 
                           values=(acct_no, name, formatted_amount, purpose[:20], formatted_income, formatted_date))
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Buttons frame
            button_frame = tk.Frame(loans_window, bg='#2c3e50')
            button_frame.pack(pady=10)
            
            def approve_loan():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("No Selection", "Please select a loan application to approve.")
                    return
                
                app_id = int(tree.item(selected[0])['text'])
                self.show_loan_approval_dialog(app_id, loans_window, tree)
            
            def reject_loan():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("No Selection", "Please select a loan application to reject.")
                    return
                
                app_id = int(tree.item(selected[0])['text'])
                reason = simpledialog.askstring("Rejection Reason", "Enter reason for rejection:")
                if reason:
                    try:
                        self.loan_mgr.reject_loan(app_id, reason)
                        messagebox.showinfo("Success", f"Loan application #{app_id} rejected.")
                        tree.delete(selected[0])
                    except Exception as e:
                        messagebox.showerror("Error", f"Rejection failed: {str(e)}")
            
            ttk.Button(button_frame, text="Approve", command=approve_loan).pack(side='left', padx=10)
            ttk.Button(button_frame, text="Reject", command=reject_loan).pack(side='left', padx=10)
            ttk.Button(button_frame, text="Close", command=loans_window.destroy).pack(side='left', padx=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load pending loans: {str(e)}")
    
    def show_loan_approval_dialog(self, app_id, parent_window, tree):
        """Show loan approval dialog with rate and term inputs"""
        approval_window = tk.Toplevel(parent_window)
        approval_window.title(f"Approve Loan #{app_id}")
        approval_window.geometry("400x250")
        approval_window.configure(bg='#2c3e50')
        approval_window.transient(parent_window)
        approval_window.grab_set()
        
        # Title
        title_label = tk.Label(approval_window, text=f"Approve Loan Application #{app_id}", 
                              font=('Arial', 14, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(approval_window, bg='#2c3e50')
        form_frame.pack(pady=20)
        
        # Interest rate
        tk.Label(form_frame, text="Interest Rate (% per year):", bg='#2c3e50', fg='white').grid(row=0, column=0, sticky='w', pady=5)
        rate_entry = tk.Entry(form_frame, font=('Arial', 10), width=20)
        rate_entry.grid(row=0, column=1, pady=5, padx=10)
        rate_entry.insert(0, "12.0")  # Default rate
        
        # Loan term
        tk.Label(form_frame, text="Loan Term (months):", bg='#2c3e50', fg='white').grid(row=1, column=0, sticky='w', pady=5)
        term_entry = tk.Entry(form_frame, font=('Arial', 10), width=20)
        term_entry.grid(row=1, column=1, pady=5, padx=10)
        term_entry.insert(0, "12")  # Default term
        
        def confirm_approval():
            try:
                rate = float(rate_entry.get())
                term = int(term_entry.get())
                
                if rate < 0 or rate > 50:
                    messagebox.showerror("Error", "Interest rate must be between 0% and 50%.")
                    return
                
                if term < 1 or term > 360:
                    messagebox.showerror("Error", "Loan term must be between 1 and 360 months.")
                    return
                
                if messagebox.askyesno("Confirm Approval", 
                                      f"Approve loan #{app_id} with:\n"
                                      f"Interest Rate: {rate}% per year\n"
                                      f"Term: {term} months"):
                    self.loan_mgr.approve_loan(app_id, rate, term)
                    messagebox.showinfo("Success", f"Loan application #{app_id} approved!")
                    approval_window.destroy()
                    
                    # Remove from tree
                    for item in tree.get_children():
                        if tree.item(item)['text'] == str(app_id):
                            tree.delete(item)
                            break
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for rate and term.")
            except Exception as e:
                messagebox.showerror("Error", f"Approval failed: {str(e)}")
        
        # Buttons
        button_frame = tk.Frame(approval_window, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Approve", command=confirm_approval, 
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancel", command=approval_window.destroy,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=10)
    
    def show_active_loans(self):
        """Display active loans portfolio"""
        try:
            # Create window to show active loans
            loans_window = tk.Toplevel(self.root)
            loans_window.title("Active Loans Portfolio")
            loans_window.geometry("900x600")
            loans_window.configure(bg='#2c3e50')
            
            title_label = tk.Label(loans_window, text="💼 Active Loans Portfolio", 
                                font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
            title_label.pack(pady=10)
            
            # Text widget to display loan information
            text_frame = tk.Frame(loans_window)
            text_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            text_widget = tk.Text(text_frame, font=('Courier', 10), bg='white', fg='black')
            scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Get actual active loans data from LoanManager
            # You'll need to modify list_active_loans to return data instead of just printing
            loans_data = self.get_active_loans_data()
            
            if loans_data:
                loans_text = self.format_active_loans_display(loans_data)
            else:
                loans_text = "📭 No active loans found.\n\n"
                loans_text += "All loans have been paid off or no loans have been disbursed yet."
            
            text_widget.insert('1.0', loans_text)
            text_widget.config(state='disabled')
            
            # Add refresh button
            refresh_btn = tk.Button(loans_window, text="🔄 Refresh", 
                                command=lambda: self.refresh_active_loans(text_widget),
                                bg='#3498db', fg='white', font=('Arial', 10, 'bold'))
            refresh_btn.pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load active loans: {str(e)}")

    def get_active_loans_data(self):
        """Get active loans data from database"""
        try:
            self.loan_mgr.db.connect()
            self.loan_mgr.db.cursor.execute(
                """SELECT l.id, l.account_number, a.name, l.principal_amount, 
                        l.remaining_balance, l.monthly_payment, l.next_payment_date,
                        l.interest_rate, l.disbursed_at
                FROM loans l
                JOIN accounts a ON l.account_number = a.account_number
                WHERE l.status = 'active'
                ORDER BY l.next_payment_date ASC"""
            )
            loans = self.loan_mgr.db.cursor.fetchall()
            self.loan_mgr.db.close()
            return loans
        except Exception as e:
            if hasattr(self.loan_mgr.db, 'close'):
                self.loan_mgr.db.close()
            print(f"Error getting active loans data: {e}")
            return []

    def format_active_loans_display(self, loans):
        """Format active loans data for display"""
        from datetime import datetime
        
        loans_text = "\n" + "="*80 + "\n"
        loans_text += "                💰 ACTIVE LOANS PORTFOLIO\n"
        loans_text += "="*80 + "\n\n"
        
        total_outstanding = 0
        overdue_count = 0
        today = datetime.now().date()
        
        for loan_id, acct_no, name, principal, remaining, monthly_pay, next_date, rate, disbursed in loans:
            loans_text += f"Loan #{loan_id}\n"
            loans_text += f"  👤 Borrower: {name} (Account: {acct_no})\n"
            loans_text += f"  💰 Original: ₱{float(principal):,.2f} | Remaining: ₱{float(remaining):,.2f}\n"
            loans_text += f"  💵 Monthly Payment: ₱{float(monthly_pay):,.2f} | Rate: {float(rate)}%\n"
            loans_text += f"  📅 Next Payment: {next_date} | Disbursed: {disbursed.strftime('%Y-%m-%d')}\n"
            
            # Check if overdue
            if next_date < today:
                days_overdue = (today - next_date).days
                loans_text += f"  ⚠️  OVERDUE by {days_overdue} days!\n"
                overdue_count += 1
            else:
                days_until = (next_date - today).days
                loans_text += f"  ✅ Due in {days_until} days\n"
            
            # Calculate payment progress
            paid_amount = float(principal) - float(remaining)
            if float(principal) > 0:
                progress = (paid_amount / float(principal)) * 100
                loans_text += f"  📊 Progress: {progress:.1f}% paid off\n"
            
            total_outstanding += float(remaining)
            loans_text += "-" * 80 + "\n"
        
        loans_text += f"\n📊 PORTFOLIO SUMMARY:\n"
        loans_text += f"   Total Active Loans: {len(loans)}\n"
        loans_text += f"   Total Outstanding: ₱{total_outstanding:,.2f}\n"
        loans_text += f"   Overdue Loans: {overdue_count}\n"
        if overdue_count > 0:
            loans_text += f"   ⚠️  Attention needed for overdue accounts\n"
        loans_text += "="*80 + "\n"
        
        return loans_text

    def refresh_active_loans(self, text_widget):
        """Refresh the active loans display"""
        try:
            loans_data = self.get_active_loans_data()
            
            text_widget.config(state='normal')
            text_widget.delete('1.0', tk.END)
            
            if loans_data:
                loans_text = self.format_active_loans_display(loans_data)
            else:
                loans_text = "📭 No active loans found.\n\n"
                loans_text += "All loans have been paid off or no loans have been disbursed yet."
            
            text_widget.insert('1.0', loans_text)
            text_widget.config(state='disabled')
            
            # Show refresh confirmation
            messagebox.showinfo("Refreshed", "Active loans data has been updated!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh active loans: {str(e)}")
    
    def show_all_loan_applications(self):
        """Display all loan applications with all statuses"""
        try:
            # Create window for all loan applications
            apps_window = tk.Toplevel(self.root)
            apps_window.title("All Loan Applications")
            apps_window.geometry("1000x600")
            apps_window.configure(bg='#2c3e50')
            
            title_label = tk.Label(apps_window, text="📋 Loan Applications History", 
                                  font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
            title_label.pack(pady=10)
            
            # Create treeview for all applications
            frame = tk.Frame(apps_window, bg='#2c3e50')
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            tree = ttk.Treeview(frame, columns=('Account', 'Name', 'Amount', 'Status', 'Applied', 'Processed'), 
                               show='tree headings')
            tree.heading('#0', text='App ID')
            tree.heading('Account', text='Account')
            tree.heading('Name', text='Name')
            tree.heading('Amount', text='Amount')
            tree.heading('Status', text='Status')
            tree.heading('Applied', text='Applied Date')
            tree.heading('Processed', text='Processed Date')
            
            # Get applications from database
            self.db.connect()
            self.db.cursor.execute(
                """SELECT la.id, la.account_number, a.name, la.amount, la.status, 
                          la.applied_at, la.processed_at
                   FROM loan_applications la
                   JOIN accounts a ON la.account_number = a.account_number
                   ORDER BY la.applied_at DESC
                   LIMIT 50"""
            )
            applications = self.db.cursor.fetchall()
            self.db.close()
            
            status_icons = {
                'pending': '⏳',
                'approved': '✅', 
                'rejected': '❌'
            }
            
            for app_id, acct_no, name, amount, status, applied, processed in applications:
                formatted_amount = f"₱{float(amount):,.2f}"
                status_display = f"{status_icons.get(status, '❓')} {status.upper()}"
                applied_date = applied.strftime('%Y-%m-%d') if applied else ''
                processed_date = processed.strftime('%Y-%m-%d') if processed else ''
                
                tree.insert('', 'end', text=str(app_id), 
                           values=(acct_no, name, formatted_amount, status_display, applied_date, processed_date))
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Close button
            tk.Button(apps_window, text="Close", command=apps_window.destroy,
                     bg='#34495e', fg='white', font=('Arial', 10, 'bold')).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load loan applications: {str(e)}")
    
    def logout(self):
        """Logout current user and return to main menu"""
        self.current_user = None
        messagebox.showinfo("Logged Out", "You have been logged out successfully.")
        self.show_main_menu()
    
    def exit_app(self):
        """Exit the application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit IRNVault Banking System?"):
            self.root.quit()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

