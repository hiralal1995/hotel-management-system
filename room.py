import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *
from database import db
import config

class RoomModule:
    """Room Management Module"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()
        self.load_rooms()
    
    def create_widgets(self):
        """Create room management widgets"""
        
        # Title
        title_label = ttk_bs.Label(
            self.parent,
            text="Room Management",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)
        
        # Button Frame
        button_frame = ttk_bs.Frame(self.parent)
        button_frame.pack(fill=X, padx=20, pady=10)
        
        add_btn = ttk_bs.Button(
            button_frame,
            text="Add Room",
            command=self.add_room,
            bootstyle="success"
        )
        add_btn.pack(side=LEFT, padx=5)
        
        edit_btn = ttk_bs.Button(
            button_frame,
            text="Edit Room",
            command=self.edit_room,
            bootstyle="warning"
        )
        edit_btn.pack(side=LEFT, padx=5)
        
        delete_btn = ttk_bs.Button(
            button_frame,
            text="Delete Room",
            command=self.delete_room,
            bootstyle="danger"
        )
        delete_btn.pack(side=LEFT, padx=5)
        
        refresh_btn = ttk_bs.Button(
            button_frame,
            text="Refresh",
            command=self.load_rooms,
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
            columns=("ID", "Room Number", "Type", "Price", "Status"),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("ID", anchor=CENTER, width=60)
        self.tree.column("Room Number", anchor=CENTER, width=120)
        self.tree.column("Type", anchor=W, width=150)
        self.tree.column("Price", anchor=CENTER, width=100)
        self.tree.column("Status", anchor=CENTER, width=120)
        
        # Define headings
        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Room Number", text="Room Number", anchor=CENTER)
        self.tree.heading("Type", text="Room Type", anchor=W)
        self.tree.heading("Price", text="Price (₹)", anchor=CENTER)
        self.tree.heading("Status", text="Status", anchor=CENTER)
        
        self.tree.pack(fill=BOTH, expand=True)
    
    def load_rooms(self):
        """Load rooms from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch rooms with type information
        query = """
        SELECT r.room_id, r.room_number, rt.room_type, rt.price, r.status
        FROM rooms r
        JOIN room_types rt ON r.type_id = rt.type_id
        ORDER BY r.room_number
        """
        rooms = db.execute_query(query)
        
        if rooms:
            for room in rooms:
                self.tree.insert("", END, values=(
                    room['room_id'],
                    room['room_number'],
                    room['room_type'],
                    f"₹{room['price']}",
                    room['status']
                ))
    
    def add_room(self):
        """Add new room"""
        dialog = RoomDialog(self.parent, "Add Room")
        if dialog.result:
            room_number, type_id, status = dialog.result
            query = "INSERT INTO rooms (room_number, type_id, status) VALUES (%s, %s, %s)"
            if db.execute_update(query, (room_number, type_id, status)):
                messagebox.showinfo("Success", "Room added successfully")
                self.load_rooms()
            else:
                messagebox.showerror("Error", "Failed to add room")
    
    def edit_room(self):
        """Edit selected room"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a room")
            return
        
        values = self.tree.item(selection[0])['values']
        dialog = RoomDialog(self.parent, "Edit Room", values)
        
        if dialog.result:
            room_number, type_id, status = dialog.result
            query = "UPDATE rooms SET room_number=%s, type_id=%s, status=%s WHERE room_id=%s"
            if db.execute_update(query, (room_number, type_id, status, values[0])):
                messagebox.showinfo("Success", "Room updated successfully")
                self.load_rooms()
            else:
                messagebox.showerror("Error", "Failed to update room")
    
    def delete_room(self):
        """Delete selected room"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a room")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this room?"):
            values = self.tree.item(selection[0])['values']
            query = "DELETE FROM rooms WHERE room_id = %s"
            if db.execute_update(query, (values[0],)):
                messagebox.showinfo("Success", "Room deleted successfully")
                self.load_rooms()
            else:
                messagebox.showerror("Error", "Failed to delete room")


class RoomDialog:
    """Dialog for adding/editing rooms"""
    
    def __init__(self, parent, title, data=None):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x350")
        self.dialog.resizable(False, False)
        
        # Center dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets(data)
    
    def create_widgets(self, data=None):
        """Create dialog widgets"""
        
        main_frame = ttk_bs.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Room Number
        ttk_bs.Label(main_frame, text="Room Number:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.room_number_entry = ttk_bs.Entry(main_frame, width=40)
        self.room_number_entry.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Room Type
        ttk_bs.Label(main_frame, text="Room Type:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.type_var = tk.StringVar()
        
        # Fetch room types from database
        query = "SELECT type_id, room_type FROM room_types"
        types = db.execute_query(query)
        
        type_values = [f"{t['room_type']} (₹{t['price']})" for t in types] if types else []
        self.type_ids = [t['type_id'] for t in types] if types else []
        
        type_combo = ttk_bs.Combobox(main_frame, textvariable=self.type_var, values=type_values, state="readonly", width=37)
        type_combo.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Status
        ttk_bs.Label(main_frame, text="Status:", font=("Arial", 10)).pack(anchor=W, pady=(10, 0))
        self.status_var = tk.StringVar(value="Available")
        status_combo = ttk_bs.Combobox(main_frame, textvariable=self.status_var, 
                                      values=["Available", "Occupied", "Maintenance"], 
                                      state="readonly", width=37)
        status_combo.pack(fill=X, ipady=8, pady=(0, 10))
        
        # Fill existing data
        if data:
            self.room_number_entry.insert(0, data[1])
            # Find and select room type
            for i, type_id in enumerate(self.type_ids):
                if data[2] in type_values[i]:
                    self.type_var.set(type_values[i])
                    break
            self.status_var.set(data[4])
        
        # Buttons
        button_frame = ttk_bs.Frame(main_frame)
        button_frame.pack(fill=X, pady=20)
        
        save_btn = ttk_bs.Button(button_frame, text="Save", command=self.save, bootstyle="success")
        save_btn.pack(side=LEFT, padx=5)
        
        cancel_btn = ttk_bs.Button(button_frame, text="Cancel", command=self.dialog.destroy, bootstyle="danger")
        cancel_btn.pack(side=LEFT, padx=5)
    
    def save(self):
        """Save room data"""
        room_number = self.room_number_entry.get().strip()
        type_index = -1
        
        # Find selected type index
        type_values = self.type_var.get()
        
        if not all([room_number, type_values]):
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        # Get type combo values
        query = "SELECT type_id, room_type FROM room_types"
        types = db.execute_query(query)
        type_values_list = [f"{t['room_type']} (₹{t['price']})" for t in types]
        
        type_index = type_values_list.index(type_values)
        type_id = types[type_index]['type_id']
        status = self.status_var.get()
        
        self.result = (room_number, type_id, status)
        self.dialog.destroy()