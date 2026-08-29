import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *
from database import db
import config
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime, timedelta
import os

class ReportsModule:
    """Reports Generation Module"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()
    
    def create_widgets(self):
        """Create reports management widgets"""
        
        # Title
        title_label = ttk_bs.Label(
            self.parent,
            text="Reports & Analytics",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)
        
        # Button Frame
        button_frame = ttk_bs.Frame(self.parent)
        button_frame.pack(fill=X, padx=20, pady=20)
        
        # Report buttons
        ttk_bs.Button(
            button_frame,
            text="Occupancy Report",
            command=self.occupancy_report,
            bootstyle="success",
            width=20
        ).pack(side=LEFT, padx=10, pady=5)
        
        ttk_bs.Button(
            button_frame,
            text="Revenue Report",
            command=self.revenue_report,
            bootstyle="info",
            width=20
        ).pack(side=LEFT, padx=10, pady=5)
        
        ttk_bs.Button(
            button_frame,
            text="Customer Report",
            command=self.customer_report,
            bootstyle="warning",
            width=20
        ).pack(side=LEFT, padx=10, pady=5)
        
        ttk_bs.Button(
            button_frame,
            text="Booking Report",
            command=self.booking_report,
            bootstyle="primary",
            width=20
        ).pack(side=LEFT, padx=10, pady=5)
        
        # Analytics section
        analytics_label = ttk_bs.Label(
            self.parent,
            text="Quick Statistics",
            font=("Arial", 14, "bold")
        )
        analytics_label.pack(pady=20)
        
        # Statistics Frame
        stats_frame = ttk_bs.Frame(self.parent)
        stats_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Create statistics cards
        self.create_stat_card(stats_frame, "Total Rooms", self.get_total_rooms, 0)
        self.create_stat_card(stats_frame, "Available Rooms", self.get_available_rooms, 1)
        self.create_stat_card(stats_frame, "Occupied Rooms", self.get_occupied_rooms, 2)
        self.create_stat_card(stats_frame, "Total Customers", self.get_total_customers, 3)
        self.create_stat_card(stats_frame, "Total Bookings", self.get_total_bookings, 4)
        self.create_stat_card(stats_frame, "Today's Revenue", self.get_todays_revenue, 5)
    
    def create_stat_card(self, parent, title, value_func, column):
        """Create a statistics card"""
        card = ttk_bs.Frame(parent, bootstyle="light", relief="solid", borderwidth=1)
        card.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        
        ttk_bs.Label(
            card,
            text=title,
            font=("Arial", 11, "bold")
        ).pack(pady=10)
        
        value = value_func()
        ttk_bs.Label(
            card,
            text=str(value),
            font=("Arial", 20, "bold"),
            foreground="darkblue"
        ).pack(pady=10)
    
    # Statistics functions
    def get_total_rooms(self):
        query = "SELECT COUNT(*) as total FROM rooms"
        result = db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_available_rooms(self):
        query = "SELECT COUNT(*) as total FROM rooms WHERE status = 'Available'"
        result = db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_occupied_rooms(self):
        query = "SELECT COUNT(*) as total FROM rooms WHERE status = 'Occupied'"
        result = db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_total_customers(self):
        query = "SELECT COUNT(*) as total FROM customers"
        result = db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_total_bookings(self):
        query = "SELECT COUNT(*) as total FROM bookings"
        result = db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_todays_revenue(self):
        query = """
        SELECT COALESCE(SUM(total), 0) as revenue 
        FROM payments 
        WHERE DATE(payment_date) = CURDATE()
        """
        result = db.execute_query(query)
        return f"₹{result[0]['revenue']:.2f}" if result else "₹0.00"
    
    # Report generation functions
    def occupancy_report(self):
        """Generate occupancy report"""
        try:
            filename = f"reports/Occupancy_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            os.makedirs('reports', exist_ok=True)
            
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            
            # Title
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1f77b4'),
                spaceAfter=30,
                alignment=1
            )
            elements.append(Paragraph("Occupancy Report", title_style))
            elements.append(Paragraph(f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", styles['Normal']))
            elements.append(Spacer(1, 0.5))
            
            # Data
            query = """
            SELECT r.room_number, rt.room_type, r.status
            FROM rooms r
            JOIN room_types rt ON r.type_id = rt.type_id
            ORDER BY r.room_number
            """
            rooms = db.execute_query(query)
            
            data = [["Room Number", "Room Type", "Status"]]
            if rooms:
                for room in rooms:
                    data.append([
                        str(room['room_number']),
                        room['room_type'],
                        room['status']
                    ])
            
            # Table
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            
            doc.build(elements)
            messagebox.showinfo("Success", f"Report generated: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def revenue_report(self):
        """Generate revenue report"""
        try:
            filename = f"reports/Revenue_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            os.makedirs('reports', exist_ok=True)
            
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            
            # Title
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1f77b4'),
                spaceAfter=30,
                alignment=1
            )
            elements.append(Paragraph("Revenue Report", title_style))
            elements.append(Paragraph(f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", styles['Normal']))
            elements.append(Spacer(1, 0.5))
            
            # Data
            query = """
            SELECT p.payment_id, p.booking_id, p.amount, p.gst, p.total, p.payment_mode, p.payment_date
            FROM payments p
            ORDER BY p.payment_date DESC
            """
            payments = db.execute_query(query)
            
            data = [["Payment ID", "Booking ID", "Amount", "GST", "Total", "Mode", "Date"]]
            total_revenue = 0
            if payments:
                for payment in payments:
                    data.append([
                        str(payment['payment_id']),
                        str(payment['booking_id']),
                        f"₹{payment['amount']}",
                        f"₹{payment['gst']}",
                        f"₹{payment['total']}",
                        payment['payment_mode'],
                        str(payment['payment_date'])
                    ])
                    total_revenue += payment['total']
            
            # Table
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            elements.append(Spacer(1, 0.5))
            elements.append(Paragraph(f"Total Revenue: ₹{total_revenue:.2f}", styles['Heading3']))
            
            doc.build(elements)
            messagebox.showinfo("Success", f"Report generated: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def customer_report(self):
        """Generate customer report"""
        try:
            filename = f"reports/Customer_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            os.makedirs('reports', exist_ok=True)
            
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            
            # Title
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1f77b4'),
                spaceAfter=30,
                alignment=1
            )
            elements.append(Paragraph("Customer Report", title_style))
            elements.append(Paragraph(f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", styles['Normal']))
            elements.append(Spacer(1, 0.5))
            
            # Data
            query = "SELECT * FROM customers ORDER BY customer_id"
            customers = db.execute_query(query)
            
            data = [["ID", "Name", "Gender", "Mobile", "Email", "ID Proof"]]
            if customers:
                for customer in customers:
                    data.append([
                        str(customer['customer_id']),
                        customer['customer_name'],
                        customer['gender'],
                        customer['mobile'],
                        customer['email'],
                        customer['id_proof']
                    ])
            
            # Table
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            
            doc.build(elements)
            messagebox.showinfo("Success", f"Report generated: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def booking_report(self):
        """Generate booking report"""
        try:
            filename = f"reports/Booking_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            os.makedirs('reports', exist_ok=True)
            
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            
            # Title
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1f77b4'),
                spaceAfter=30,
                alignment=1
            )
            elements.append(Paragraph("Booking Report", title_style))
            elements.append(Paragraph(f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", styles['Normal']))
            elements.append(Spacer(1, 0.5))
            
            # Data
            query = """
            SELECT b.booking_id, c.customer_name, r.room_number, b.check_in, b.check_out, b.status
            FROM bookings b
            JOIN customers c ON b.customer_id = c.customer_id
            JOIN rooms r ON b.room_id = r.room_id
            ORDER BY b.booking_id DESC
            """
            bookings = db.execute_query(query)
            
            data = [["Booking ID", "Customer", "Room", "Check-In", "Check-Out", "Status"]]
            if bookings:
                for booking in bookings:
                    data.append([
                        str(booking['booking_id']),
                        booking['customer_name'],
                        booking['room_number'],
                        str(booking['check_in']),
                        str(booking['check_out']),
                        booking['status']
                    ])
            
            # Table
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            
            doc.build(elements)
            messagebox.showinfo("Success", f"Report generated: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")