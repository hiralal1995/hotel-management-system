import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *
from database import db
import config
from datetime import datetime

class BillingModule:
    """Billing and Payment Management Module"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()
        self.load_payments()
    
    def create_widgets(self):
        """Create billing management widgets"""
        
        # Title
        title_label = ttk_bs.Label(
            self.parent,
            text="Billing & Payments",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)
        
        # Button Frame
        button_frame = ttk_bs.Frame(self.parent)
        button_frame.pack(fill=X, padx=20, pady=10)
        
        add_btn = ttk_bs.Button(
            button_frame,
            text="Create Invoice",
            command=self.create_invoice,
            bootstyle="success"
        )
        add_btn.pack(side=LEFT, padx=5)
        
        view_btn = ttk_bs.Button(
            button_frame,
            text="View Invoice",
            command=self.view_invoice,
            bootstyle="info"
        )
        view_btn.pack(side=LEFT, padx=5)
        
        refresh_btn = ttk_bs.Button(
            button_frame,
            text="Refresh",
            command=self.load_payments,
            bootstyle="warning"
        )
        refresh_btn.pack(side=LEFT, padx=5)
        
        # Treeview Frame
        tree_frame = ttk_bs.Frame(self.parent)
        tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Booking", "Amount", "GST", "Total", "Mode", "Date"),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("ID", anchor=CENTER, width=50)
        self.tree.column("Booking", anchor=CENTER, width=80)
        self.tree.column("Amount", anchor=CENTER, width=100)
        self.tree.column("GST", anchor=CENTER, width=80)
        self.tree.column("Total", anchor=CENTER, width=100)
        self.tree.column("Mode", anchor=CENTER, width=100)
        self.tree.column("Date", anchor=CENTER, width=100)
        
        # Define headings
        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Booking", text="Booking ID", anchor=CENTER)
        self.tree.heading("Amount", text="Amount (₹)", anchor=CENTER)
        self.tree.heading("GST", text="GST (₹)", anchor=CENTER)
        self.tree.heading("Total", text="Total (₹)", anchor=CENTER)
        self.tree.heading("Mode", text="Payment Mode", anchor=CENTER)
        self.tree.heading("Date", text="Date", anchor=CENTER)
        
        self.tree.pack(fill=BOTH, expand=True)
    
    def load_payments(self):
        """Load payments from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch payments
        query = """
        SELECT payment_id, booking_id, amount, gst, total, payment_mode, payment_date
        FROM payments
        ORDER BY payment_date DESC
        """
        payments = db.execute_query(query)
        
        if payments:
            for payment in payments:
                self.tree.insert("", END, values=(
                    payment['payment_id'],
                    payment['booking_id'],
                    f"₹{payment['amount']}",
                    f"₹{payment['gst']}",
                    f"₹{payment['total']}",
                    payment['payment_mode'],
                    payment['payment_date']
                ))
    
    def create_invoice(self):
        """Create new invoice"""
        dialog = InvoiceDialog(self.parent, "Create Invoice")
        if dialog.result:
            booking_id, amount, gst, total, payment_mode = dialog.result
            query = """
            INSERT INTO payments (booking_id, amount, gst, total, payment_mode, payment_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            payment_date = datetime.now().date()
            if db.execute_update(query, (booking_id, amount, gst, total, payment_mode, payment_date)):
                messagebox.showinfo("Success", "Invoice created successfully")
                self.load_payments()
            else:
                messagebox.showerror("Error", "Failed to create invoice")
    
    def view_invoice(self):
        """View invoice details"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a payment")
            return
        
        values = self.tree.item(selection[0])['values']
        payment_id = values[0]
        
        # Fetch payment details
        query = "SELECT * FROM payments WHERE payment_id = %s"
        result = db.execute_query(query, (payment_id,))
        
        if result:
            payment = result[0]
            details = f"""
Payment ID: {payment['payment_id']}
Booking ID: {payment['booking_id']}
Amount: ₹{payment['amount']}
GST (18%): ₹{payment['gst']}
Total: ₹{payment['total']}
Payment Mode: {payment['payment_mode']}
Date: {payment['payment_date']}
            """
            messagebox.showinfo("Invoice Details", details)


class InvoiceDialog:
    """Dialog for creating invoices"""
    
    def __init__(self, parent, title):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("450x450")
        self.dialog.resizable(False, False)
        
        # Center dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create dialog widgets"""
        
        main_frame = ttk_bs.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Booking ID
        ttk_bs.Label(main_frame, text="Select Booking:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.booking_var = tk.StringVar()
        
        # Fetch confirmed bookings
        query = "SELECT booking_id FROM bookings WHERE status = %s"
        bookings = db.execute_query(query, ("Confirmed",))
        
        booking_values = [str(b['booking_id']) for b in bookings] if bookings else []
        
        booking_combo = ttk_bs.Combobox(main_frame, textvariable=self.booking_var, values=booking_values, state="readonly", width=40)
        booking_combo.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Amount
        ttk_bs.Label(main_frame, text="Amount (₹):", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.amount_entry = ttk_bs.Entry(main_frame, width=40)
        self.amount_entry.pack(fill=X, ipady=8, pady=(0, 10))
        self.amount_entry.bind("<KeyRelease>", self.calculate_total)
        
        # GST (18%)
        ttk_bs.Label(main_frame, text="GST (18%):", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.gst_entry = ttk_bs.Entry(main_frame, width=40, state="readonly")
        self.gst_entry.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Total
        ttk_bs.Label(main_frame, text="Total (₹):", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.total_entry = ttk_bs.Entry(main_frame, width=40, state="readonly")
        self.total_entry.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Payment Mode
        ttk_bs.Label(main_frame, text="Payment Mode:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.mode_var = tk.StringVar(value="Cash")
        mode_combo = ttk_bs.Combobox(main_frame, textvariable=self.mode_var, 
                                    values=config.PAYMENT_MODES, state="readonly", width=40)
        mode_combo.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Buttons
        button_frame = ttk_bs.Frame(main_frame)
        button_frame.pack(fill=X, pady=20)
        
        save_btn = ttk_bs.Button(button_frame, text="Create Invoice", command=self.save, bootstyle="success")
        save_btn.pack(side=LEFT, padx=5)
        
        cancel_btn = ttk_bs.Button(button_frame, text="Cancel", command=self.dialog.destroy, bootstyle="danger")
        cancel_btn.pack(side=LEFT, padx=5)
    
    def calculate_total(self, event=None):
        """Calculate GST and total"""
        try:
            amount = float(self.amount_entry.get() or 0)
            gst = amount * config.DEFAULT_GST_RATE
            total = amount + gst
            
            # Update GST and Total fields
            self.gst_entry.config(state="normal")
            self.gst_entry.delete(0, tk.END)
            self.gst_entry.insert(0, f"{gst:.2f}")
            self.gst_entry.config(state="readonly")
            
            self.total_entry.config(state="normal")
            self.total_entry.delete(0, tk.END)
            self.total_entry.insert(0, f"{total:.2f}")
            self.total_entry.config(state="readonly")
        except ValueError:
            pass
    
    def save(self):
        """Save invoice data"""
        booking_id = self.booking_var.get().strip()
        amount_str = self.amount_entry.get().strip()
        gst_str = self.gst_entry.get().strip()
        total_str = self.total_entry.get().strip()
        payment_mode = self.mode_var.get()
        
        if not all([booking_id, amount_str, payment_mode]):
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        try:
            booking_id = int(booking_id)
            amount = float(amount_str)
            gst = float(gst_str)
            total = float(total_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount values")
            return
        
        self.result = (booking_id, amount, gst, total, payment_mode)
        self.dialog.destroy()