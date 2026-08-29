import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database import db
import config
from dashboard import Dashboard

class LoginWindow:
    """Login Window for Hotel Management System"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        self.create_widgets()
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (300 // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """Create login form widgets"""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Hotel Management System",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Login to your account",
            font=("Arial", 10)
        )
        subtitle_label.pack(pady=5)
        
        # Username Label and Entry
        username_label = ttk.Label(main_frame, text="Username:", font=("Arial", 10))
        username_label.pack(anchor=W, pady=(20, 5))
        
        self.username_entry = ttk.Entry(main_frame, width=40)
        self.username_entry.pack(fill=X, ipady=8)
        self.username_entry.focus()
        
        # Password Label and Entry
        password_label = ttk.Label(main_frame, text="Password:", font=("Arial", 10))
        password_label.pack(anchor=W, pady=(15, 5))
        
        self.password_entry = ttk.Entry(main_frame, width=40, show="*")
        self.password_entry.pack(fill=X, ipady=8)
        
        # Login Button
        login_button = ttk.Button(
            main_frame,
            text="Login",
            command=self.login,
            bootstyle="success"
        )
        login_button.pack(fill=X, ipady=10, pady=20)
        
        # Bind Enter key
        self.root.bind("<Return>", lambda e: self.login())
    
    def login(self):
        """Handle login logic"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        # Connect to database
        if not db.connect():
            messagebox.showerror("Error", "Cannot connect to database")
            return
        
        # Check credentials
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        result = db.execute_query(query, (username, password))
        
        if result:
            # Login successful
            self.root.destroy()
            root = ttk.Window(themename=config.THEME)
            app = Dashboard(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)

def main():
    """Main entry point"""
    root = ttk.Window(themename=config.THEME)
    login_window = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()