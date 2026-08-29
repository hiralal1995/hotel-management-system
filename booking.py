import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *
from database import db
import config
from datetime import datetime, timedelta

class BookingModule:
    """Booking Management Module"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()
        self.load_bookings()
    
    def create_widgets(self):
        """Create booking management widgets"""
        
        # Title
        title_label = ttk_bs.Label(
            self.parent,
            text="Booking Management",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)
        
        # Button Frame
        button_frame = ttk_bs.Frame(self.parent)
        button_frame.pack(fill=X, padx=20, pady=10)
        
        add_btn = ttk_bs.Button(
            button_frame,
            text="New Booking",
            command=self.add_booking,
            bootstyle="success"
        )
        add_btn.pack(side=LEFT, padx=5)
        
        edit_btn = ttk_bs.Button(
            button_frame,
            text="Edit Booking",
            command=self.edit_booking,
            bootstyle="warning"
        )
        edit_btn.pack(side=LEFT, padx=5)
        
        delete_btn = ttk_bs.Button(
            button_frame,
            text="Cancel Booking",
            command=self.delete_booking,
            bootstyle="danger"
        )
        delete_btn.pack(side=LEFT, padx=5)
        
        refresh_btn = ttk_bs.Button(
            button_frame,
            text="Refresh",
            command=self.load_bookings,
            bootstyle="info"
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
            columns=("ID", "Customer", "Room", "Check-In", "Check-Out", "Adults", "Children", "Status"),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("ID", anchor=CENTER, width=50)
        self.tree.column("Customer", anchor=W, width=120)
        self.tree.column("Room", anchor=CENTER, width=70)
        self.tree.column("Check-In", anchor=CENTER, width=100)
        self.tree.column("Check-Out", anchor=CENTER, width=100)
        self.tree.column("Adults", anchor=CENTER, width=60)
        self.tree.column("Children", anchor=CENTER, width=70)
        self.tree.column("Status", anchor=CENTER, width=100)
        
        # Define headings
        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Customer", text="Customer Name", anchor=W)
        self.tree.heading("Room", text="Room No.", anchor=CENTER)
        self.tree.heading("Check-In", text="Check-In", anchor=CENTER)
        self.tree.heading("Check-Out", text="Check-Out", anchor=CENTER)
        self.tree.heading("Adults", text="Adults", anchor=CENTER)
        self.tree.heading("Children", text="Children", anchor=CENTER)
        self.tree.heading("Status", text="Status", anchor=CENTER)
        
        self.tree.pack(fill=BOTH, expand=True)
    
    def load_bookings(self):
        """Load bookings from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch bookings with customer and room information
        query = """
        SELECT b.booking_id, c.customer_name, r.room_number, b.check_in, b.check_out, b.adults, b.children, b.status
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        JOIN rooms r ON b.room_id = r.room_id
        ORDER BY b.check_in DESC
        """
        bookings = db.execute_query(query)
        
        if bookings:
            for booking in bookings:
                self.tree.insert("", END, values=(
                    booking['booking_id'],
                    booking['customer_name'],
                    booking['room_number'],
                    booking['check_in'],
                    booking['check_out'],
                    booking['adults'],
                    booking['children'],
                    booking['status']
                ))
    
    def add_booking(self):
        """Add new booking"""
        dialog = BookingDialog(self.parent, "New Booking")
        if dialog.result:
            customer_id, room_id, check_in, check_out, adults, children = dialog.result
            query = """
            INSERT INTO bookings (customer_id, room_id, check_in, check_out, adults, children, booking_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            booking_date = datetime.now().date()
            if db.execute_update(query, (customer_id, room_id, check_in, check_out, adults, children, booking_date, "Confirmed")):
                # Update room status
                db.execute_update("UPDATE rooms SET status = %s WHERE room_id = %s", ("Occupied", room_id))
                messagebox.showinfo("Success", "Booking created successfully")
                self.load_bookings()
            else:
                messagebox.showerror("Error", "Failed to create booking")
    
    def edit_booking(self):
        """Edit selected booking"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a booking")
            return
        
        values = self.tree.item(selection[0])['values']
        dialog = BookingDialog(self.parent, "Edit Booking", values)
        
        if dialog.result:
            customer_id, room_id, check_in, check_out, adults, children = dialog.result
            query = """
            UPDATE bookings 
            SET customer_id=%s, room_id=%s, check_in=%s, check_out=%s, adults=%s, children=%s
            WHERE booking_id=%s
            """
            if db.execute_update(query, (customer_id, room_id, check_in, check_out, adults, children, values[0])):
                messagebox.showinfo("Success", "Booking updated successfully")
                self.load_bookings()
            else:
                messagebox.showerror("Error", "Failed to update booking")
    
    def delete_booking(self):
        """Cancel selected booking"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a booking")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to cancel this booking?"):
            values = self.tree.item(selection[0])['values']
            query = "UPDATE bookings SET status = %s WHERE booking_id = %s"
            if db.execute_update(query, ("Cancelled", values[0])):
                messagebox.showinfo("Success", "Booking cancelled successfully")
                self.load_bookings()
            else:
                messagebox.showerror("Error", "Failed to cancel booking")


class BookingDialog:
    """Dialog for adding/editing bookings"""
    
    def __init__(self, parent, title, data=None):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("450x550")
        self.dialog.resizable(False, False)
        
        # Center dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets(data)
    
    def create_widgets(self, data=None):
        """Create dialog widgets"""
        
        main_frame = ttk_bs.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Customer
        ttk_bs.Label(main_frame, text="Customer:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.customer_var = tk.StringVar()
        
        # Fetch customers from database
        query = "SELECT customer_id, customer_name FROM customers"
        customers = db.execute_query(query)
        
        customer_values = [c['customer_name'] for c in customers] if customers else []
        self.customer_ids = [c['customer_id'] for c in customers] if customers else []
        
        customer_combo = ttk_bs.Combobox(main_frame, textvariable=self.customer_var, values=customer_values, state="readonly", width=40)
        customer_combo.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Room
        ttk_bs.Label(main_frame, text="Room:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.room_var = tk.StringVar()
        
        # Fetch available rooms
        query = "SELECT room_id, room_number FROM rooms WHERE status = %s"
        rooms = db.execute_query(query, ("Available",))
        
        room_values = [r['room_number'] for r in rooms] if rooms else []
        self.room_ids = [r['room_id'] for r in rooms] if rooms else []
        
        room_combo = ttk_bs.Combobox(main_frame, textvariable=self.room_var, values=room_values, state="readonly", width=40)
        room_combo.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Check-In Date
        ttk_bs.Label(main_frame, text="Check-In Date (YYYY-MM-DD):", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.checkin_entry = ttk_bs.Entry(main_frame, width=40)
        self.checkin_entry.pack(fill=X, ipady=8, pady=(0, 10))
        self.checkin_entry.insert(0, datetime.now().date())
        
        # Check-Out Date
        ttk_bs.Label(main_frame, text="Check-Out Date (YYYY-MM-DD):", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.checkout_entry = ttk_bs.Entry(main_frame, width=40)
        self.checkout_entry.pack(fill=X, ipady=8, pady=(0, 10))
        self.checkout_entry.insert(0, (datetime.now() + timedelta(days=1)).date())
        
        # Adults
        ttk_bs.Label(main_frame, text="Number of Adults:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.adults_entry = ttk_bs.Entry(main_frame, width=40)
        self.adults_entry.pack(fill=X, ipady=8, pady=(0, 10))
        self.adults_entry.insert(0, "1")
        
        # Children
        ttk_bs.Label(main_frame, text="Number of Children:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.children_entry = ttk_bs.Entry(main_frame, width=40)
        self.children_entry.pack(fill=X, ipady=8, pady=(0, 10))
        self.children_entry.insert(0, "0")
        
        # Fill existing data
        if data:
            # Find and select customer
            for i, cust_id in enumerate(self.customer_ids):
                query = "SELECT customer_name FROM customers WHERE customer_id = %s"
                result = db.execute_query(query, (cust_id,))
                if result and result[0]['customer_name'] == data[1]:
                    self.customer_var.set(customer_values[i])
                    break
            
            # Find and select room
            for i, room_id in enumerate(self.room_ids):
                query = "SELECT room_number FROM rooms WHERE room_id = %s"
                result = db.execute_query(query, (room_id,))
                if result and result[0]['room_number'] == data[2]:
                    self.room_var.set(room_values[i])
                    break
            
            self.checkin_entry.delete(0, tk.END)
            self.checkin_entry.insert(0, data[3])
            self.checkout_entry.delete(0, tk.END)
            self.checkout_entry.insert(0, data[4])
            self.adults_entry.delete(0, tk.END)
            self.adults_entry.insert(0, data[5])
            self.children_entry.delete(0, tk.END)
            self.children_entry.insert(0, data[6])
        
        # Buttons
        button_frame = ttk_bs.Frame(main_frame)
        button_frame.pack(fill=X, pady=20)
        
        save_btn = ttk_bs.Button(button_frame, text="Save", command=self.save, bootstyle="success")
        save_btn.pack(side=LEFT, padx=5)
        
        cancel_btn = ttk_bs.Button(button_frame, text="Cancel", command=self.dialog.destroy, bootstyle="danger")
        cancel_btn.pack(side=LEFT, padx=5)
    
    def save(self):
        """Save booking data"""
        customer_str = self.customer_var.get()
        room_str = self.room_var.get()
        check_in = self.checkin_entry.get().strip()
        check_out = self.checkout_entry.get().strip()
        adults = self.adults_entry.get().strip()
        children = self.children_entry.get().strip()
        
        if not all([customer_str, room_str, check_in, check_out, adults, children]):
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        try:
            adults = int(adults)
            children = int(children)
        except ValueError:
            messagebox.showerror("Error", "Adults and Children must be numbers")
            return
        
        # Get customer_id and room_id
        customer_index = self.customer_var.get()
        room_index = self.room_var.get()
        
        query = "SELECT customer_id FROM customers WHERE customer_name = %s"
        result = db.execute_query(query, (customer_index,))
        customer_id = result[0]['customer_id'] if result else None
        
        query = "SELECT room_id FROM rooms WHERE room_number = %s"
        result = db.execute_query(query, (room_index,))
        room_id = result[0]['room_id'] if result else None
        
        if not customer_id or not room_id:
            messagebox.showerror("Error", "Invalid customer or room selection")
            return
        
        self.result = (customer_id, room_id, check_in, check_out, adults, children)
        self.dialog.destroy()