import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import datetime

from database import db


class Dashboard:

    def __init__(self, user):

        self.user = user

        self.window = ttk.Window(
            themename="flatly"
        )

        self.window.title(
            "Hotel Management Dashboard"
        )

        self.window.geometry(
            "1200x700"
        )

        self.window.state("zoomed")


        # =========================
        # Sidebar
        # =========================

        self.sidebar = ttk.Frame(
            self.window,
            bootstyle="primary",
            width=220
        )

        self.sidebar.pack(
            side=LEFT,
            fill=Y
        )


        ttk.Label(
            self.sidebar,
            text="HOTEL SYSTEM",
            font=(
                "Arial",
                18,
                "bold"
            ),
            bootstyle="inverse-primary"
        ).pack(
            pady=30
        )


        menu_buttons = [

            ("Dashboard", self.home),

            ("Customers", self.open_customer),

            ("Rooms", self.open_rooms),

            ("Bookings", self.open_booking),

            ("Billing", self.open_billing),

            ("Employees", self.open_employee),

            ("Reports", self.open_reports)

        ]


        for text, command in menu_buttons:

            ttk.Button(

                self.sidebar,

                text=text,

                width=20,

                bootstyle="light",

                command=command

            ).pack(
                pady=8,
                padx=10
            )


        ttk.Button(

            self.sidebar,

            text="Logout",

            width=20,

            bootstyle="danger",

            command=self.logout

        ).pack(

            side=BOTTOM,

            pady=20

        )


        # =========================
        # Main Area
        # =========================


        self.main_frame = ttk.Frame(
            self.window
        )

        self.main_frame.pack(
            expand=True,
            fill=BOTH,
            padx=20,
            pady=20
        )


        self.home()


        self.window.mainloop()



    # =========================
    # Dashboard Home
    # =========================


    def home(self):

        for widget in self.main_frame.winfo_children():

            widget.destroy()



        ttk.Label(

            self.main_frame,

            text=f"Welcome, {self.user['username']}",

            font=(
                "Arial",
                24,
                "bold"
            )

        ).pack(
            anchor=W
        )


        self.time_label = ttk.Label(

            self.main_frame,

            font=(
                "Arial",
                14
            )

        )

        self.time_label.pack(
            anchor=W,
            pady=10
        )


        self.update_time()



        # Cards

        cards_frame = ttk.Frame(

            self.main_frame

        )

        cards_frame.pack(

            pady=30

        )


        rooms = self.get_total_rooms()

        available = self.get_available_rooms()

        customers = self.get_customers()

        bookings = self.get_bookings()



        self.create_card(

            cards_frame,

            "Total Rooms",

            rooms,

            0

        )


        self.create_card(

            cards_frame,

            "Available Rooms",

            available,

            1

        )


        self.create_card(

            cards_frame,

            "Customers",

            customers,

            2

        )


        self.create_card(

            cards_frame,

            "Bookings",

            bookings,

            3

        )



    # =========================
    # Dashboard Cards
    # =========================


    def create_card(
            self,
            parent,
            title,
            value,
            column):


        frame = ttk.Frame(

            parent,

            bootstyle="info",

            width=220,

            height=130

        )

        frame.grid(

            row=0,

            column=column,

            padx=15

        )


        ttk.Label(

            frame,

            text=title,

            font=(

                "Arial",

                14,

                "bold"

            )

        ).pack(

            pady=15

        )


        ttk.Label(

            frame,

            text=str(value),

            font=(

                "Arial",

                25,

                "bold"

            )

        ).pack()



    # =========================
    # Database Statistics
    # =========================


    def get_total_rooms(self):

        db.execute(

            "SELECT COUNT(*) AS total FROM rooms"

        )

        return db.fetchone()["total"]



    def get_available_rooms(self):

        db.execute(

            """
            SELECT COUNT(*) AS total
            FROM rooms
            WHERE status='Available'
            """

        )

        return db.fetchone()["total"]



    def get_customers(self):

        db.execute(

            "SELECT COUNT(*) AS total FROM customers"

        )

        return db.fetchone()["total"]



    def get_bookings(self):

        db.execute(

            "SELECT COUNT(*) AS total FROM bookings"

        )

        return db.fetchone()["total"]



    # =========================
    # Clock
    # =========================


    def update_time(self):

        now = datetime.now().strftime(

            "%d-%m-%Y   %I:%M:%S %p"

        )

        self.time_label.config(

            text=now

        )

        self.time_label.after(

            1000,

            self.update_time

        )



    # =========================
    # Module Connectors
    # =========================


    def open_customer(self):

        from customer import Customer

        Customer()


    def open_rooms(self):

        from room import Room

        Room()


    def open_booking(self):

        from booking import Booking

        Booking()


    def open_billing(self):

        messagebox.showinfo(
            "Billing",
            "Billing module will be connected soon"
        )


    def open_employee(self):

        messagebox.showinfo(
            "Employees",
            "Employee module will be connected soon"
        )


    def open_reports(self):

        messagebox.showinfo(
            "Reports",
            "Reports module will be connected soon"
        )



    def logout(self):

        self.window.destroy()

        from login import Login

        Login()