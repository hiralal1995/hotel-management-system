import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *
from database import db
import config

class EmployeeModule:
    """Employee Management Module"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()
        self.load_employees()
    
    def create_widgets(self):
        """Create employee management widgets"""
        
        # Title
        title_label = ttk_bs.Label(
            self.parent,
            text="Employee Management",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)
        
        # Button Frame
        button_frame = ttk_bs.Frame(self.parent)
        button_frame.pack(fill=X, padx=20, pady=10)
        
        add_btn = ttk_bs.Button(
            button_frame,
            text="Add Employee",
            command=self.add_employee,
            bootstyle="success"
        )
        add_btn.pack(side=LEFT, padx=5)
        
        edit_btn = ttk_bs.Button(
            button_frame,
            text="Edit Employee",
            command=self.edit_employee,
            bootstyle="warning"
        )
        edit_btn.pack(side=LEFT, padx=5)
        
        delete_btn = ttk_bs.Button(
            button_frame,
            text="Delete Employee",
            command=self.delete_employee,
            bootstyle="danger"
        )
        delete_btn.pack(side=LEFT, padx=5)
        
        refresh_btn = ttk_bs.Button(
            button_frame,
            text="Refresh",
            command=self.load_employees,
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
            columns=("ID", "Name", "Designation", "Salary", "Mobile", "Address"),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("ID", anchor=CENTER, width=50)
        self.tree.column("Name", anchor=W, width=150)
        self.tree.column("Designation", anchor=W, width=150)
        self.tree.column("Salary", anchor=CENTER, width=100)
        self.tree.column("Mobile", anchor=CENTER, width=120)
        self.tree.column("Address", anchor=W, width=200)
        
        # Define headings
        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Name", text="Employee Name", anchor=W)
        self.tree.heading("Designation", text="Designation", anchor=W)
        self.tree.heading("Salary", text="Salary (₹)", anchor=CENTER)
        self.tree.heading("Mobile", text="Mobile", anchor=CENTER)
        self.tree.heading("Address", text="Address", anchor=W)
        
        self.tree.pack(fill=BOTH, expand=True)
    
    def load_employees(self):
        """Load employees from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch employees
        query = "SELECT * FROM employees ORDER BY employee_id"
        employees = db.execute_query(query)
        
        if employees:
            for emp in employees:
                self.tree.insert("", END, values=(
                    emp['employee_id'],
                    emp['employee_name'],
                    emp['designation'],
                    f"₹{emp['salary']}",
                    emp['mobile'],
                    emp['address']
                ))
    
    def add_employee(self):
        """Add new employee"""
        dialog = EmployeeDialog(self.parent, "Add Employee")
        if dialog.result:
            name, designation, salary, mobile, address = dialog.result
            query = """
            INSERT INTO employees (employee_name, designation, salary, mobile, address)
            VALUES (%s, %s, %s, %s, %s)
            """
            if db.execute_update(query, (name, designation, salary, mobile, address)):
                messagebox.showinfo("Success", "Employee added successfully")
                self.load_employees()
            else:
                messagebox.showerror("Error", "Failed to add employee")
    
    def edit_employee(self):
        """Edit selected employee"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an employee")
            return
        
        values = self.tree.item(selection[0])['values']
        dialog = EmployeeDialog(self.parent, "Edit Employee", values)
        
        if dialog.result:
            name, designation, salary, mobile, address = dialog.result
            query = """
            UPDATE employees 
            SET employee_name=%s, designation=%s, salary=%s, mobile=%s, address=%s
            WHERE employee_id=%s
            """
            if db.execute_update(query, (name, designation, salary, mobile, address, values[0])):
                messagebox.showinfo("Success", "Employee updated successfully")
                self.load_employees()
            else:
                messagebox.showerror("Error", "Failed to update employee")
    
    def delete_employee(self):
        """Delete selected employee"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an employee")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
            values = self.tree.item(selection[0])['values']
            query = "DELETE FROM employees WHERE employee_id = %s"
            if db.execute_update(query, (values[0],)):
                messagebox.showinfo("Success", "Employee deleted successfully")
                self.load_employees()
            else:
                messagebox.showerror("Error", "Failed to delete employee")


class EmployeeDialog:
    """Dialog for adding/editing employees"""
    
    def __init__(self, parent, title, data=None):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x400")
        self.dialog.resizable(False, False)
        
        # Center dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets(data)
    
    def create_widgets(self, data=None):
        """Create dialog widgets"""
        
        main_frame = ttk_bs.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Employee Name
        ttk_bs.Label(main_frame, text="Name:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.name_entry = ttk_bs.Entry(main_frame, width=40)
        self.name_entry.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Designation
        ttk_bs.Label(main_frame, text="Designation:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.designation_entry = ttk_bs.Entry(main_frame, width=40)
        self.designation_entry.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Salary
        ttk_bs.Label(main_frame, text="Salary (₹):", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.salary_entry = ttk_bs.Entry(main_frame, width=40)
        self.salary_entry.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Mobile
        ttk_bs.Label(main_frame, text="Mobile:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.mobile_entry = ttk_bs.Entry(main_frame, width=40)
        self.mobile_entry.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Address
        ttk_bs.Label(main_frame, text="Address:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.address_text = tk.Text(main_frame, height=3, width=40)
        self.address_text.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Fill existing data
        if data:
            self.name_entry.insert(0, data[1])
            self.designation_entry.insert(0, data[2])
            # Remove ₹ and any spaces from salary for display
            salary_str = str(data[3]).replace("₹", "").strip()
            self.salary_entry.insert(0, salary_str)
            self.mobile_entry.insert(0, data[4])
            self.address_text.insert("1.0", data[5])
        
        # Buttons
        button_frame = ttk_bs.Frame(main_frame)
        button_frame.pack(fill=X, pady=20)
        
        save_btn = ttk_bs.Button(button_frame, text="Save", command=self.save, bootstyle="success")
        save_btn.pack(side=LEFT, padx=5)
        
        cancel_btn = ttk_bs.Button(button_frame, text="Cancel", command=self.dialog.destroy, bootstyle="danger")
        cancel_btn.pack(side=LEFT, padx=5)
    
    def save(self):
        """Save employee data"""
        name = self.name_entry.get().strip()
        designation = self.designation_entry.get().strip()
        salary = self.salary_entry.get().strip()
        mobile = self.mobile_entry.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        
        if not all([name, designation, salary, mobile, address]):
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        try:
            salary = float(salary)
        except ValueError:
            messagebox.showerror("Error", "Salary must be a valid number")
            return
        
        self.result = (name, designation, salary, mobile, address)
        self.dialog.destroy()