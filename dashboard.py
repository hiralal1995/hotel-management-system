import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *
from database import db
import config
from customer import CustomerModule
from room import RoomModule
from booking import BookingModule
from billing import BillingModule
from employee import EmployeeModule
from reports import ReportsModule

class Dashboard:
    """Main Dashboard for Hotel Management System"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(config.APP_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        
        # Initialize modules
        self.customer_module = None
        self.room_module = None
        self.booking_module = None
        self.billing_module = None
        self.employee_module = None
        self.reports_module = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create dashboard widgets"""
        
        # Top Frame - Title and Welcome
        top_frame = ttk_bs.Frame(self.root, bootstyle="primary")
        top_frame.pack(fill=X, side=TOP)
        
        title_label = ttk_bs.Label(
            top_frame,
            text=config.APP_TITLE,
            font=("Arial", 20, "bold"),
            foreground="white"
        )
        title_label.pack(pady=15)
        
        # Left Sidebar - Navigation Menu
        left_frame = ttk_bs.Frame(self.root, width=200, bootstyle="secondary")
        left_frame.pack(fill=Y, side=LEFT)
        left_frame.pack_propagate(False)
        
        # Menu Title
        menu_title = ttk_bs.Label(
            left_frame,
            text="Menu",
            font=("Arial", 12, "bold")
        )
        menu_title.pack(pady=15)
        
        # Menu Buttons
        buttons_info = [
            ("Dashboard", self.show_dashboard),
            ("Customers", self.show_customers),
            ("Rooms", self.show_rooms),
            ("Bookings", self.show_bookings),
            ("Billing", self.show_billing),
            ("Employees", self.show_employees),
            ("Reports", self.show_reports),
            ("Logout", self.logout)
        ]
        
        for btn_text, btn_command in buttons_info:
            btn = ttk_bs.Button(
                left_frame,
                text=btn_text,
                command=btn_command,
                width=20,
                bootstyle="info"
            )
            btn.pack(pady=5, padx=10)
        
        # Right Frame - Content Area
        self.content_frame = ttk_bs.Frame(self.root, bootstyle="light")
        self.content_frame.pack(fill=BOTH, expand=True, side=LEFT)
        
        # Show welcome message
        self.show_dashboard()
    
    def clear_content(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show dashboard welcome screen"""
        self.clear_content()
        
        welcome_frame = ttk_bs.Frame(self.content_frame)
        welcome_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        welcome_label = ttk_bs.Label(
            welcome_frame,
            text="Welcome to Hotel Management System",
            font=("Arial", 24, "bold")
        )
        welcome_label.pack(pady=30)
        
        info_text = """
Select an option from the menu to get started:

• Customers: Manage customer information
• Rooms: View and manage hotel rooms
• Bookings: Create and manage room bookings
• Billing: Generate invoices and payments
• Employees: Manage employee information
• Reports: Generate various reports
        """
        
        info_label = ttk_bs.Label(
            welcome_frame,
            text=info_text,
            font=("Arial", 12),
            justify=LEFT
        )
        info_label.pack(pady=20, anchor=W)
    
    def show_customers(self):
        """Show customer management"""
        self.clear_content()
        self.customer_module = CustomerModule(self.content_frame)
    
    def show_rooms(self):
        """Show room management"""
        self.clear_content()
        self.room_module = RoomModule(self.content_frame)
    
    def show_bookings(self):
        """Show booking management"""
        self.clear_content()
        self.booking_module = BookingModule(self.content_frame)
    
    def show_billing(self):
        """Show billing management"""
        self.clear_content()
        self.billing_module = BillingModule(self.content_frame)
    
    def show_employees(self):
        """Show employee management"""
        self.clear_content()
        self.employee_module = EmployeeModule(self.content_frame)
    
    def show_reports(self):
        """Show reports"""
        self.clear_content()
        self.reports_module = ReportsModule(self.content_frame)
    
    def logout(self):
        """Logout and return to login"""
        db.disconnect()
        self.root.destroy()
        
        # Restart login
        from login import main
        main()