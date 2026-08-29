CREATE DATABASE IF NOT EXISTS hotel_management;

USE hotel_management;

-- ===================================
-- USERS
-- ===================================

CREATE TABLE users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(20)
);

INSERT INTO users(username,password,role)
VALUES
('admin','admin123','Admin');

-- ===================================
-- CUSTOMERS
-- ===================================

CREATE TABLE customers(
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100),
    gender VARCHAR(20),
    mobile VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    id_proof VARCHAR(50),
    id_number VARCHAR(100)
);

-- ===================================
-- ROOM TYPES
-- ===================================

CREATE TABLE room_types(
    type_id INT PRIMARY KEY AUTO_INCREMENT,
    room_type VARCHAR(50),
    price DECIMAL(10,2)
);

INSERT INTO room_types(room_type,price)
VALUES
('Standard',1500),
('Deluxe',2500),
('Super Deluxe',3500),
('Suite',6000);

-- ===================================
-- ROOMS
-- ===================================

CREATE TABLE rooms(
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    room_number VARCHAR(10),
    type_id INT,
    status VARCHAR(20),
    FOREIGN KEY(type_id) REFERENCES room_types(type_id)
);

-- Sample Rooms

INSERT INTO rooms(room_number,type_id,status)
VALUES
('101',1,'Available'),
('102',1,'Available'),
('103',1,'Available'),
('201',2,'Available'),
('202',2,'Available'),
('203',2,'Available'),
('301',3,'Available'),
('302',3,'Available'),
('401',4,'Available');

-- ===================================
-- BOOKINGS
-- ===================================

CREATE TABLE bookings(
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    room_id INT,
    check_in DATE,
    check_out DATE,
    adults INT,
    children INT,
    booking_date DATE,
    status VARCHAR(20),
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(room_id) REFERENCES rooms(room_id)
);

-- ===================================
-- PAYMENTS
-- ===================================

CREATE TABLE payments(
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT,
    amount DECIMAL(10,2),
    gst DECIMAL(10,2),
    total DECIMAL(10,2),
    payment_mode VARCHAR(20),
    payment_date DATE,
    FOREIGN KEY(booking_id) REFERENCES bookings(booking_id)
);

-- ===================================
-- EMPLOYEES
-- ===================================

CREATE TABLE employees(
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_name VARCHAR(100),
    designation VARCHAR(50),
    salary DECIMAL(10,2),
    mobile VARCHAR(20),
    address TEXT
);