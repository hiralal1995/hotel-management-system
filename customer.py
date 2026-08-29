import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *
from database import db
import config

class CustomerModule:
    """Customer Management Module"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()
        self.load_customers()
    
    def create_widgets(self):
        """Create customer management widgets"""
        
        # Title
        title_label = ttk_bs.Label(
            self.parent,
            text="Customer Management",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)
        
        # Button Frame
        button_frame = ttk_bs.Frame(self.parent)
        button_frame.pack(fill=X, padx=20, pady=10)
        
        add_btn = ttk_bs.Button(
            button_frame,
            text="Add Customer",
            command=self.add_customer,
            bootstyle="success"
        )
        add_btn.pack(side=LEFT, padx=5)
        
        edit_btn = ttk_bs.Button(
            button_frame,
            text="Edit Customer",
            command=self.edit_customer,
            bootstyle="warning"
        )
        edit_btn.pack(side=LEFT, padx=5)
        
        delete_btn = ttk_bs.Button(
            button_frame,
            text="Delete Customer",
            command=self.delete_customer,
            bootstyle="danger"
        )
        delete_btn.pack(side=LEFT, padx=5)
        
        refresh_btn = ttk_bs.Button(
            button_frame,
            text="Refresh",
            command=self.load_customers,
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
            columns=("ID", "Name", "Gender", "Mobile", "Email", "Address", "ID Proof", "ID Number"),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("ID", anchor=CENTER, width=40)
        self.tree.column("Name", anchor=W, width=120)
        self.tree.column("Gender", anchor=CENTER, width=70)
        self.tree.column("Mobile", anchor=CENTER, width=100)
        self.tree.column("Email", anchor=W, width=150)
        self.tree.column("Address", anchor=W, width=150)
        self.tree.column("ID Proof", anchor=CENTER, width=80)
        self.tree.column("ID Number", anchor=CENTER, width=100)
        
        # Define headings
        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Name", text="Name", anchor=W)
        self.tree.heading("Gender", text="Gender", anchor=CENTER)
        self.tree.heading("Mobile", text="Mobile", anchor=CENTER)
        self.tree.heading("Email", text="Email", anchor=W)
        self.tree.heading("Address", text="Address", anchor=W)
        self.tree.heading("ID Proof", text="ID Proof", anchor=CENTER)
        self.tree.heading("ID Number", text="ID Number", anchor=CENTER)
        
        self.tree.pack(fill=BOTH, expand=True)
    
    def load_customers(self):
        """Load customers from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch customers
        query = "SELECT * FROM customers"
        customers = db.execute_query(query)
        
        if customers:
            for customer in customers:
                self.tree.insert("", END, values=(
                    customer['customer_id'],
                    customer['customer_name'],
                    customer['gender'],
                    customer['mobile'],
                    customer['email'],
                    customer['address'],
                    customer['id_proof'],
                    customer['id_number']
                ))
    
    def add_customer(self):
        """Add new customer"""
        dialog = CustomerDialog(self.parent, "Add Customer")
        if dialog.result:
            query = """
            INSERT INTO customers (customer_name, gender, mobile, email, address, id_proof, id_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            if db.execute_update(query, dialog.result):
                messagebox.showinfo("Success", "Customer added successfully")
                self.load_customers()
            else:
                messagebox.showerror("Error", "Failed to add customer")
    
    def edit_customer(self):
        """Edit selected customer"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a customer")
            return
        
        values = self.tree.item(selection[0])['values']
        dialog = CustomerDialog(self.parent, "Edit Customer", values)
        
        if dialog.result:
            query = """
            UPDATE customers 
            SET customer_name=%s, gender=%s, mobile=%s, email=%s, address=%s, id_proof=%s, id_number=%s
            WHERE customer_id=%s
            """
            params = dialog.result + (values[0],)
            if db.execute_update(query, params):
                messagebox.showinfo("Success", "Customer updated successfully")
                self.load_customers()
            else:
                messagebox.showerror("Error", "Failed to update customer")
    
    def delete_customer(self):
        """Delete selected customer"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a customer")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?"):
            values = self.tree.item(selection[0])['values']
            query = "DELETE FROM customers WHERE customer_id = %s"
            if db.execute_update(query, (values[0],)):
                messagebox.showinfo("Success", "Customer deleted successfully")
                self.load_customers()
            else:
                messagebox.showerror("Error", "Failed to delete customer")


class CustomerDialog:
    """Dialog for adding/editing customers"""
    
    def __init__(self, parent, title, data=None):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)
        
        # Center dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets(data)
    
    def create_widgets(self, data=None):
        """Create dialog widgets"""
        
        main_frame = ttk_bs.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Customer Name
        ttk_bs.Label(main_frame, text="Name:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.name_entry = ttk_bs.Entry(main_frame, width=40)
        self.name_entry.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Gender
        ttk_bs.Label(main_frame, text="Gender:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.gender_var = tk.StringVar(value=data[2] if data else "")
        gender_combo = ttk_bs.Combobox(main_frame, textvariable=self.gender_var, values=["Male", "Female", "Other"], state="readonly", width=37)
        gender_combo.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Mobile
        ttk_bs.Label(main_frame, text="Mobile:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.mobile_entry = ttk_bs.Entry(main_frame, width=40)
        self.mobile_entry.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Email
        ttk_bs.Label(main_frame, text="Email:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.email_entry = ttk_bs.Entry(main_frame, width=40)
        self.email_entry.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Address
        ttk_bs.Label(main_frame, text="Address:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.address_text = tk.Text(main_frame, height=4, width=40)
        self.address_text.pack(fill=X, ipady=8, pady=(0, 10))
        
        # ID Proof
        ttk_bs.Label(main_frame, text="ID Proof:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.id_proof_entry = ttk_bs.Entry(main_frame, width=40)
        self.id_proof_entry.pack(fill=X, ipady=8, pady=(0, 10))
        
        # ID Number
        ttk_bs.Label(main_frame, text="ID Number:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.id_number_entry = ttk_bs.Entry(main_frame, width=40)
        self.id_number_entry.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Fill existing data
        if data:
            self.name_entry.insert(0, data[1])
            self.mobile_entry.insert(0, data[3])
            self.email_entry.insert(0, data[4])
            self.address_text.insert("1.0", data[5])
            self.id_proof_entry.insert(0, data[6])
            self.id_number_entry.insert(0, data[7])
        
        # Buttons
        button_frame = ttk_bs.Frame(main_frame)
        button_frame.pack(fill=X, pady=20)
        
        save_btn = ttk_bs.Button(button_frame, text="Save", command=self.save, bootstyle="success")
        save_btn.pack(side=LEFT, padx=5)
        
        cancel_btn = ttk_bs.Button(button_frame, text="Cancel", command=self.dialog.destroy, bootstyle="danger")
        cancel_btn.pack(side=LEFT, padx=5)
    
    def save(self):
        """Save customer data"""
        name = self.name_entry.get().strip()
        gender = self.gender_var.get()
        mobile = self.mobile_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        id_proof = self.id_proof_entry.get().strip()
        id_number = self.id_number_entry.get().strip()
        
        if not all([name, gender, mobile, email, address, id_proof, id_number]):
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        self.result = (name, gender, mobile, email, address, id_proof, id_number)
        self.dialog.destroy()