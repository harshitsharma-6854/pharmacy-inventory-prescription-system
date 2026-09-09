import os
import sqlite3
from pathlib import Path
import mysql.connector
from mysql.connector import Error as MySQLError
from config import Config

class DatabaseManager:
    _instance = None
    _is_mysql = False
    _connection_error = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        """Attempts to connect to MySQL 8.x; gracefully falls back to SQLite if offline."""
        try:
            conn = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                port=Config.MYSQL_PORT,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DATABASE,
                connect_timeout=3
            )
            if conn.is_connected():
                self._is_mysql = True
                conn.close()
                print(f"[*] Connected successfully to MySQL 8.x on {Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}")
                return
        except Exception as e:
            self._connection_error = str(e)
            self._is_mysql = False
            print(f"[!] MySQL not reachable ({e}). Initializing zero-config Fallback Demo Database.")
            self._init_sqlite_fallback()

    def _init_sqlite_fallback(self):
        """Initializes an identical schema and sample dataset in SQLite for seamless demo."""
        db_path = Config.FALLBACK_DB_PATH
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Schema definition compatible with SQLite
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS PHARMACY (
            Pharmacy_ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Rating REAL DEFAULT 5.0,
            City TEXT NOT NULL,
            State TEXT NOT NULL,
            Street TEXT NOT NULL,
            Contact_No TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS PHARMACY_CONTACT (
            Pharmacy_ID INTEGER NOT NULL,
            Contact_No TEXT NOT NULL,
            PRIMARY KEY (Pharmacy_ID, Contact_No),
            FOREIGN KEY (Pharmacy_ID) REFERENCES PHARMACY(Pharmacy_ID) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS PATIENT (
            Patient_ID INTEGER PRIMARY KEY,
            DOB TEXT NOT NULL,
            Sex TEXT NOT NULL,
            City TEXT NOT NULL,
            State TEXT NOT NULL,
            Street TEXT NOT NULL,
            First_Name TEXT NOT NULL,
            Last_Name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS PATIENT_CONTACT (
            Patient_ID INTEGER NOT NULL,
            Contact_No TEXT NOT NULL,
            PRIMARY KEY (Patient_ID, Contact_No),
            FOREIGN KEY (Patient_ID) REFERENCES PATIENT(Patient_ID) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS HOSPITAL (
            Hospital_ID INTEGER PRIMARY KEY,
            Pharmacy_ID INTEGER NOT NULL,
            City TEXT NOT NULL,
            State TEXT NOT NULL,
            Street TEXT NOT NULL,
            Name TEXT NOT NULL,
            Contact TEXT NOT NULL,
            FOREIGN KEY (Pharmacy_ID) REFERENCES PHARMACY(Pharmacy_ID)
        );

        CREATE TABLE IF NOT EXISTS DOCTOR (
            Doctor_ID INTEGER PRIMARY KEY,
            Hospital_ID INTEGER NOT NULL,
            Experience INTEGER DEFAULT 0,
            Contact_No TEXT NOT NULL,
            First_Name TEXT NOT NULL,
            Last_Name TEXT NOT NULL,
            Qualification TEXT NOT NULL,
            FOREIGN KEY (Hospital_ID) REFERENCES HOSPITAL(Hospital_ID)
        );

        CREATE TABLE IF NOT EXISTS PRESCRIPTION (
            Prescription_ID INTEGER PRIMARY KEY,
            Doctor_ID INTEGER NOT NULL,
            Patient_ID INTEGER NOT NULL,
            Date TEXT NOT NULL,
            FOREIGN KEY (Doctor_ID) REFERENCES DOCTOR(Doctor_ID),
            FOREIGN KEY (Patient_ID) REFERENCES PATIENT(Patient_ID)
        );

        CREATE TABLE IF NOT EXISTS MEDICINE (
            Medicine_ID INTEGER PRIMARY KEY,
            Manu_Date TEXT NOT NULL,
            Exp_Date TEXT NOT NULL,
            Name TEXT NOT NULL,
            Price REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS PRESCRIPTION_ITEM (
            Item_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Prescription_ID INTEGER NOT NULL,
            Medicine_ID INTEGER NOT NULL,
            Dosage TEXT NOT NULL,
            Frequency TEXT NOT NULL,
            Duration TEXT NOT NULL,
            FOREIGN KEY (Prescription_ID) REFERENCES PRESCRIPTION(Prescription_ID) ON DELETE CASCADE,
            FOREIGN KEY (Medicine_ID) REFERENCES MEDICINE(Medicine_ID)
        );

        CREATE TABLE IF NOT EXISTS BILL (
            Bill_ID INTEGER PRIMARY KEY,
            Pharmacy_ID INTEGER NOT NULL,
            Amount REAL NOT NULL,
            Patient_ID INTEGER NOT NULL,
            FOREIGN KEY (Pharmacy_ID) REFERENCES PHARMACY(Pharmacy_ID),
            FOREIGN KEY (Patient_ID) REFERENCES PATIENT(Patient_ID)
        );

        CREATE TABLE IF NOT EXISTS PHARMACIST (
            Pharmacist_ID INTEGER PRIMARY KEY,
            Pharmacy_ID INTEGER NOT NULL,
            Shift TEXT NOT NULL,
            Name TEXT NOT NULL,
            FOREIGN KEY (Pharmacy_ID) REFERENCES PHARMACY(Pharmacy_ID)
        );

        CREATE TABLE IF NOT EXISTS MANUFACTURER (
            Manufacturer_ID INTEGER PRIMARY KEY,
            Brand_Name TEXT NOT NULL,
            City TEXT NOT NULL,
            State TEXT NOT NULL,
            Street TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS SUPPLIER (
            Supplier_ID INTEGER PRIMARY KEY,
            Contact TEXT NOT NULL,
            City TEXT NOT NULL,
            State TEXT NOT NULL,
            Street TEXT NOT NULL,
            Name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS SUPPLIER_MANUFACTURER (
            Supplier_ID INTEGER NOT NULL,
            Manufacturer_ID INTEGER NOT NULL,
            PRIMARY KEY (Supplier_ID, Manufacturer_ID),
            FOREIGN KEY (Supplier_ID) REFERENCES SUPPLIER(Supplier_ID) ON DELETE CASCADE,
            FOREIGN KEY (Manufacturer_ID) REFERENCES MANUFACTURER(Manufacturer_ID) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS WHOLESALE_SUPPLIER (
            GST_No TEXT PRIMARY KEY,
            City TEXT NOT NULL,
            State TEXT NOT NULL,
            Street TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS SUPPLIER_WHOLESALE (
            Supplier_ID INTEGER NOT NULL,
            GST_No TEXT NOT NULL,
            PRIMARY KEY (Supplier_ID, GST_No),
            FOREIGN KEY (Supplier_ID) REFERENCES SUPPLIER(Supplier_ID) ON DELETE CASCADE,
            FOREIGN KEY (GST_No) REFERENCES WHOLESALE_SUPPLIER(GST_No) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS SUPPLIER_PHARMACY (
            Supplier_ID INTEGER NOT NULL,
            Pharmacy_ID INTEGER NOT NULL,
            PRIMARY KEY (Supplier_ID, Pharmacy_ID),
            FOREIGN KEY (Supplier_ID) REFERENCES SUPPLIER(Supplier_ID) ON DELETE CASCADE,
            FOREIGN KEY (Pharmacy_ID) REFERENCES PHARMACY(Pharmacy_ID) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS `ORDER` (
            Order_ID INTEGER PRIMARY KEY,
            Supplier_ID INTEGER NOT NULL,
            Pharmacy_ID INTEGER NOT NULL,
            Date TEXT NOT NULL,
            Arrival_Date TEXT,
            Payment_Status TEXT NOT NULL,
            Order_Status TEXT NOT NULL,
            Quantity_Ordered INTEGER NOT NULL,
            FOREIGN KEY (Supplier_ID) REFERENCES SUPPLIER(Supplier_ID),
            FOREIGN KEY (Pharmacy_ID) REFERENCES PHARMACY(Pharmacy_ID)
        );

        CREATE TABLE IF NOT EXISTS INVENTORY (
            Inventory_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Pharmacy_ID INTEGER NOT NULL,
            Medicine_ID INTEGER NOT NULL,
            Quantity INTEGER NOT NULL DEFAULT 0,
            Reorder_Level INTEGER NOT NULL DEFAULT 15,
            Last_Updated TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (Pharmacy_ID, Medicine_ID),
            FOREIGN KEY (Pharmacy_ID) REFERENCES PHARMACY(Pharmacy_ID) ON DELETE CASCADE,
            FOREIGN KEY (Medicine_ID) REFERENCES MEDICINE(Medicine_ID) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS STOCK_LOG (
            Log_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Pharmacy_ID INTEGER NOT NULL,
            Medicine_ID INTEGER NOT NULL,
            Quantity_Change INTEGER NOT NULL,
            Change_Type TEXT NOT NULL,
            Change_Date TEXT DEFAULT CURRENT_TIMESTAMP,
            Reference_ID TEXT,
            FOREIGN KEY (Pharmacy_ID) REFERENCES PHARMACY(Pharmacy_ID) ON DELETE CASCADE,
            FOREIGN KEY (Medicine_ID) REFERENCES MEDICINE(Medicine_ID) ON DELETE CASCADE
        );
        """)
        
        # Check if sample data is populated
        cursor.execute("SELECT COUNT(*) FROM PHARMACY")
        if cursor.fetchone()[0] == 0:
            self._seed_sqlite(cursor)
            conn.commit()
            print("[*] Fallback SQLite database seeded with authentic DA1 sample dataset.")
            
        conn.close()

    def _seed_sqlite(self, cursor):
        """Loads default records into SQLite fallback matching 02_sample_data.sql."""
        pharmacies = [
            (101, 'Apollo HealthCity Pharmacy', 4.8, 'Mumbai', 'Maharashtra', 'Ground Floor, Bandra Reclamation, Hill Road', '+91 22 2640 5555'),
            (102, 'MedPlus Community Care', 4.6, 'Bengaluru', 'Karnataka', '82 100-Ft Road, 4th Block, Koramangala', '+91 80 4120 7788'),
            (103, 'Fortis MedStore Express', 4.9, 'New Delhi', 'Delhi', 'Gate No 2, Sector B, Vasant Kunj Marg', '+91 11 4277 6200')
        ]
        cursor.executemany("INSERT INTO PHARMACY VALUES (?,?,?,?,?,?,?)", pharmacies)

        pharm_contacts = [
            (101, '+91 22 2640 5555'), (101, '+91 22 2640 5599'),
            (102, '+91 80 4120 7788'), (102, '+91 98450 11223'),
            (103, '+91 11 4277 6200'), (103, '+91 11 4277 6299')
        ]
        cursor.executemany("INSERT INTO PHARMACY_CONTACT VALUES (?,?)", pharm_contacts)

        hospitals = [
            (201, 101, 'Mumbai', 'Maharashtra', 'A-791 Bandra West, Near Lilavati Road', 'Lilavati Hospital & Research Centre', '+91 22 2675 1000'),
            (202, 102, 'Bengaluru', 'Karnataka', '98 HAL Old Airport Road, Kodihalli', 'Manipal Hospital Bengaluru', '+91 80 2502 4444'),
            (203, 103, 'New Delhi', 'Delhi', 'Sri Aurobindo Marg, Ansari Nagar East', 'AIIMS Apex Trauma & Medical Center', '+91 11 2658 8500')
        ]
        cursor.executemany("INSERT INTO HOSPITAL VALUES (?,?,?,?,?,?,?)", hospitals)

        doctors = [
            (301, 201, 14, '+91 98201 44552', 'Rajesh', 'Kulkarni', 'MBBS, MD (General Medicine)'),
            (302, 201, 18, '+91 98205 11984', 'Sunita', 'Deshmukh', 'MBBS, MS (General Surgery)'),
            (303, 202, 11, '+91 97410 88231', 'Anand', 'Narayanaswamy', 'MBBS, MD, DM (Cardiology)'),
            (304, 202, 8,  '+91 98451 77210', 'Pooja', 'Rao', 'MBBS, DCH, MD (Pediatrics)'),
            (305, 202, 15, '+91 96112 33490', 'Venkatesh', 'Bhat', 'MBBS, MS (Orthopedics)'),
            (306, 203, 20, '+91 98110 55671', 'Arvind', 'Aggarwal', 'MBBS, MD, DM (Neurology)'),
            (307, 203, 9,  '+91 98188 44321', 'Meenakshi', 'Sundaram', 'MBBS, MD (Pulmonology)'),
            (308, 203, 12, '+91 99102 99012', 'Kabir', 'Malhotra', 'MBBS, MD (Endocrinology)')
        ]
        cursor.executemany("INSERT INTO DOCTOR VALUES (?,?,?,?,?,?,?)", doctors)

        patients = [
            (401, '1982-04-14', 'M', 'Mumbai', 'Maharashtra', 'Flat 402, Sea View Apts, Worli Seaface', 'Rahul', 'Sharma'),
            (402, '1990-09-22', 'F', 'Mumbai', 'Maharashtra', '12 Gokul Dham, Andheri East', 'Priya', 'Patel'),
            (403, '1975-11-05', 'M', 'Bengaluru', 'Karnataka', '204 Silver Oak Enclave, Indiranagar', 'Suresh', 'Menon'),
            (404, '1988-03-19', 'F', 'Bengaluru', 'Karnataka', '45 Green Glen Layout, Bellandur', 'Deepika', 'Iyer'),
            (405, '1964-07-30', 'M', 'Bengaluru', 'Karnataka', '108 Brigade Gateway, Malleshwaram', 'Ramesh', 'Gowda'),
            (406, '1995-12-11', 'F', 'New Delhi', 'Delhi', 'C-14 Hauz Khas Enclave, South Delhi', 'Ananya', 'Verma'),
            (407, '1970-01-25', 'M', 'New Delhi', 'Delhi', 'B-4/88 Safdarjung Enclave', 'Vikram', 'Singh'),
            (408, '1985-08-16', 'F', 'New Delhi', 'Delhi', 'Plot 12 Sector 14, Rohini', 'Sneha', 'Gupta'),
            (409, '1958-05-02', 'M', 'Mumbai', 'Maharashtra', '71 Parsi Colony, Dadar East', 'Homi', 'Wadia'),
            (410, '2001-10-28', 'F', 'Bengaluru', 'Karnataka', '5th Cross, HSR Layout Sector 2', 'Kavya', 'Reddy')
        ]
        cursor.executemany("INSERT INTO PATIENT VALUES (?,?,?,?,?,?,?,?)", patients)

        pat_contacts = [
            (401, '+91 98200 12345'), (401, '+91 22 2493 0011'),
            (402, '+91 98211 23456'), (403, '+91 98450 34567'),
            (403, '+91 98450 99887'), (404, '+91 99000 45678'),
            (405, '+91 98440 56789'), (406, '+91 98100 67890'),
            (407, '+91 98111 78901'), (408, '+91 98180 89012'),
            (409, '+91 98202 90123'), (410, '+91 99800 01234')
        ]
        cursor.executemany("INSERT INTO PATIENT_CONTACT VALUES (?,?)", pat_contacts)

        medicines = [
            (501, '2024-01-15', '2026-12-31', 'Dolo 650 (Paracetamol 650mg)', 32.50),
            (502, '2023-11-10', '2025-10-31', 'Augmentin 625 Duo (Amoxicillin & Clavulanate)', 205.00),
            (503, '2024-02-01', '2027-01-31', 'Glycomet GP 1 (Metformin 500mg + Glimepiride 1mg)', 118.50),
            (504, '2023-08-20', '2026-07-31', 'Atorva 20 (Atorvastatin 20mg)', 185.00),
            (505, '2024-03-05', '2026-02-28', 'Azithral 500 (Azithromycin 500mg)', 124.00),
            (506, '2024-04-10', '2027-03-31', 'Pantocid 40 (Pantoprazole 40mg)', 142.00),
            (507, '2023-09-15', '2025-08-31', 'Cetzine 10 (Cetirizine 10mg)', 48.00),
            (508, '2024-01-10', '2026-06-30', 'Ascoril D Plus Cough Syrup 100ml', 115.00),
            (509, '2023-12-01', '2025-11-30', 'Lantus Solostar Insulin Pen (100 IU/ml)', 890.00),
            (510, '2024-02-25', '2027-01-15', 'Telma 40 (Telmisartan 40mg)', 155.00),
            (511, '2023-05-10', '2025-04-30', 'Montair LC (Montelukast + Levocetirizine)', 178.00),
            (512, '2022-01-10', '2024-06-30', 'Combiflam Tablet (Ibuprofen + Paracetamol)', 45.00)
        ]
        cursor.executemany("INSERT INTO MEDICINE VALUES (?,?,?,?,?)", medicines)

        pharmacists = [
            (601, 101, 'Morning', 'Manoj Kumar Tiwari'),
            (602, 101, 'Evening', 'Shilpa Nair'),
            (603, 102, 'Morning', 'Girish Channappa'),
            (604, 102, 'Night',   'Karthik Somayaji'),
            (605, 103, 'Morning', 'Harish Chander Sharma'),
            (606, 103, 'Evening', 'Pratibha Chauhan')
        ]
        cursor.executemany("INSERT INTO PHARMACIST VALUES (?,?,?,?)", pharmacists)

        manufacturers = [
            (701, 'Sun Pharmaceutical Industries Ltd', 'Mumbai', 'Maharashtra', 'Sun House, Goregaon East'),
            (702, 'Cipla Limited', 'Mumbai', 'Maharashtra', 'Cipla House, Lower Parel'),
            (703, 'Dr. Reddy Laboratories', 'Hyderabad', 'Telangana', 'Banjara Hills'),
            (704, 'Lupin Pharmaceuticals', 'Mumbai', 'Maharashtra', 'Santacruz East'),
            (705, 'Torrent Pharmaceuticals Ltd', 'Ahmedabad', 'Gujarat', 'Navrangpura')
        ]
        cursor.executemany("INSERT INTO MANUFACTURER VALUES (?,?,?,?,?)", manufacturers)

        suppliers = [
            (801, '+91 22 2850 4433', 'Mumbai', 'Maharashtra', 'Sakinaka, Andheri', 'Apex Pharma Distributors LLP'),
            (802, '+91 80 2226 9911', 'Bengaluru', 'Karnataka', 'Chickpet Commercial Complex', 'Karnataka Medico Supplies'),
            (803, '+91 11 2386 1120', 'New Delhi', 'Delhi', 'Bhagirath Palace, Chandni Chowk', 'Capital Healthcare Logistics'),
            (804, '+91 40 2465 7788', 'Hyderabad', 'Telangana', 'Gowliguda Chaman, Koti', 'Deccan Drug Distributors'),
            (805, '+91 79 2658 3344', 'Ahmedabad', 'Gujarat', 'Relief Road', 'Western Gujarat Pharma Trade')
        ]
        cursor.executemany("INSERT INTO SUPPLIER VALUES (?,?,?,?,?,?)", suppliers)

        supp_mfg = [
            (801, 701), (801, 702), (801, 704),
            (802, 701), (802, 703), (802, 705),
            (803, 702), (803, 703),
            (804, 703), (804, 704),
            (805, 701), (805, 705)
        ]
        cursor.executemany("INSERT INTO SUPPLIER_MANUFACTURER VALUES (?,?)", supp_mfg)

        ws = [
            ('27AAACH1234F1Z5', 'Mumbai', 'Maharashtra', 'APMC Market Yard, Vashi'),
            ('29AABCK5678P1ZQ', 'Bengaluru', 'Karnataka', 'Peenya Industrial Area 3rd Phase'),
            ('07AABCW9012M1Z8', 'New Delhi', 'Delhi', 'Okhla Industrial Area Phase II'),
            ('36AABCS3456L1Z2', 'Hyderabad', 'Telangana', 'Autonagar Industrial Corridor, LB Nagar'),
            ('24AABCT7890N1Z9', 'Ahmedabad', 'Gujarat', 'Vatva GIDC Phase IV')
        ]
        cursor.executemany("INSERT INTO WHOLESALE_SUPPLIER VALUES (?,?,?,?)", ws)

        supp_ws = [
            (801, '27AAACH1234F1Z5'), (802, '29AABCK5678P1ZQ'),
            (803, '07AABCW9012M1Z8'), (804, '36AABCS3456L1Z2'),
            (805, '24AABCT7890N1Z9'), (801, '29AABCK5678P1ZQ')
        ]
        cursor.executemany("INSERT INTO SUPPLIER_WHOLESALE VALUES (?,?)", supp_ws)

        supp_pharm = [
            (801, 101), (801, 102), (802, 102), (803, 103),
            (804, 101), (804, 102), (805, 101), (805, 103)
        ]
        cursor.executemany("INSERT INTO SUPPLIER_PHARMACY VALUES (?,?)", supp_pharm)

        orders = [
            (901, 801, 101, '2026-08-01', '2026-08-04', 'Paid', 'Delivered', 250),
            (902, 801, 101, '2026-08-10', '2026-08-14', 'Paid', 'Delivered', 180),
            (903, 802, 102, '2026-08-12', '2026-08-16', 'Paid', 'Delivered', 300),
            (904, 803, 103, '2026-08-15', '2026-08-19', 'Paid', 'Delivered', 150),
            (905, 804, 101, '2026-08-20', '2026-08-24', 'Partial', 'Delivered', 120),
            (906, 802, 102, '2026-08-25', '2026-08-29', 'Paid', 'Delivered', 220),
            (907, 803, 103, '2026-08-28', '2026-09-02', 'Paid', 'Delivered', 190),
            (908, 801, 101, '2026-08-30', '2026-09-05', 'Pending', 'Processing', 140),
            (909, 805, 103, '2026-09-01', '2026-09-06', 'Pending', 'Shipped', 200),
            (910, 802, 102, '2026-09-02', None, 'Pending', 'Pending', 100),
            (911, 804, 102, '2026-08-05', None, 'Refunded', 'Cancelled', 80),
            (912, 805, 101, '2026-09-03', '2026-09-08', 'Pending', 'Processing', 160)
        ]
        cursor.executemany("INSERT INTO `ORDER` VALUES (?,?,?,?,?,?,?,?)", orders)

        prescriptions = [
            (1001, 301, 401, '2026-08-10'),
            (1002, 301, 402, '2026-08-12'),
            (1003, 303, 403, '2026-08-14'),
            (1004, 304, 404, '2026-08-18'),
            (1005, 305, 405, '2026-08-20'),
            (1006, 306, 406, '2026-08-22'),
            (1007, 307, 407, '2026-08-25'),
            (1008, 308, 408, '2026-08-28'),
            (1009, 301, 409, '2026-08-30'),
            (1010, 303, 410, '2026-09-01'),
            (1011, 302, 401, '2026-09-02'),
            (1012, 306, 407, '2026-09-03')
        ]
        cursor.executemany("INSERT INTO PRESCRIPTION VALUES (?,?,?,?)", prescriptions)

        items = [
            (1, 1001, 501, '650mg', 'Thrice Daily (TDS)', '5 Days'),
            (2, 1001, 506, '40mg', 'Once Daily Before Breakfast (OD)', '10 Days'),
            (3, 1002, 502, '625mg', 'Twice Daily After Food (BD)', '7 Days'),
            (4, 1002, 507, '10mg', 'Once Daily at Bedtime (HS)', '5 Days'),
            (5, 1003, 503, '500mg', 'Twice Daily with Meals (BD)', '30 Days'),
            (6, 1003, 504, '20mg', 'Once Daily at Night (OD)', '30 Days'),
            (7, 1003, 510, '40mg', 'Once Daily Morning (OD)', '30 Days'),
            (8, 1004, 501, '250mg', 'SOS As Needed', '3 Days'),
            (9, 1004, 508, '5ml', 'Thrice Daily (TDS)', '5 Days'),
            (10, 1005, 501, '650mg', 'Twice Daily (BD)', '5 Days'),
            (11, 1005, 506, '40mg', 'Once Daily (OD)', '7 Days'),
            (12, 1006, 507, '10mg', 'Once Daily (OD)', '10 Days'),
            (13, 1006, 511, '10mg', 'Once Daily at Night (HS)', '14 Days'),
            (14, 1007, 505, '500mg', 'Once Daily for 3 Days (OD)', '3 Days'),
            (15, 1007, 508, '10ml', 'Thrice Daily (TDS)', '7 Days'),
            (16, 1008, 503, '500mg', 'Twice Daily (BD)', '30 Days'),
            (17, 1008, 509, '18 IU', 'Once Daily Subcutaneous (OD)', '30 Days'),
            (18, 1009, 504, '20mg', 'Once Daily (OD)', '30 Days'),
            (19, 1009, 510, '40mg', 'Once Daily Morning (OD)', '30 Days'),
            (20, 1010, 502, '625mg', 'Twice Daily (BD)', '5 Days'),
            (21, 1010, 506, '40mg', 'Once Daily (OD)', '7 Days'),
            (22, 1011, 501, '650mg', 'Twice Daily (BD)', '3 Days'),
            (23, 1011, 506, '40mg', 'Once Daily (OD)', '5 Days'),
            (24, 1012, 504, '20mg', 'Once Daily (OD)', '30 Days'),
            (25, 1012, 507, '10mg', 'Once Daily (OD)', '7 Days'),
            (26, 1002, 501, '650mg', 'SOS (As Needed)', '3 Days')
        ]
        cursor.executemany("INSERT INTO PRESCRIPTION_ITEM VALUES (?,?,?,?,?,?)", items)

        bills = [
            (1101, 101, 174.50, 401),
            (1102, 101, 285.50, 402),
            (1103, 102, 458.50, 403),
            (1104, 102, 147.50, 404),
            (1105, 102, 174.50, 405),
            (1106, 103, 226.00, 406),
            (1107, 103, 239.00, 407),
            (1108, 103, 1008.50, 408),
            (1109, 101, 340.00, 409),
            (1110, 102, 347.00, 410),
            (1111, 101, 174.50, 401),
            (1112, 103, 233.00, 407)
        ]
        cursor.executemany("INSERT INTO BILL VALUES (?,?,?,?)", bills)

        inventory = [
            (None, 101, 501, 140, 25, '2026-08-30 10:00:00'),
            (None, 101, 502, 42, 15, '2026-08-30 10:00:00'),
            (None, 101, 503, 85, 20, '2026-08-30 10:00:00'),
            (None, 101, 504, 12, 15, '2026-08-30 10:00:00'), # LOW STOCK
            (None, 101, 505, 30, 10, '2026-08-30 10:00:00'),
            (None, 101, 506, 65, 20, '2026-08-30 10:00:00'),
            (None, 101, 507, 9, 15, '2026-08-30 10:00:00'),  # LOW STOCK
            (None, 101, 508, 0, 10, '2026-08-30 10:00:00'),  # OUT OF STOCK
            (None, 101, 509, 18, 5, '2026-08-30 10:00:00'),
            (None, 101, 510, 50, 15, '2026-08-30 10:00:00'),
            (None, 101, 511, 28, 12, '2026-08-30 10:00:00'),
            (None, 101, 512, 15, 10, '2026-08-30 10:00:00'),
            (None, 102, 501, 185, 30, '2026-08-30 10:00:00'),
            (None, 102, 502, 8, 15, '2026-08-30 10:00:00'),  # LOW STOCK
            (None, 102, 503, 90, 20, '2026-08-30 10:00:00'),
            (None, 102, 504, 60, 15, '2026-08-30 10:00:00'),
            (None, 102, 505, 45, 10, '2026-08-30 10:00:00'),
            (None, 102, 506, 70, 20, '2026-08-30 10:00:00'),
            (None, 102, 507, 80, 15, '2026-08-30 10:00:00'),
            (None, 102, 508, 35, 12, '2026-08-30 10:00:00'),
            (None, 102, 509, 4, 5, '2026-08-30 10:00:00'),   # LOW STOCK
            (None, 102, 510, 48, 15, '2026-08-30 10:00:00'),
            (None, 103, 501, 210, 30, '2026-08-30 10:00:00'),
            (None, 103, 502, 55, 15, '2026-08-30 10:00:00'),
            (None, 103, 503, 110, 25, '2026-08-30 10:00:00'),
            (None, 103, 504, 45, 15, '2026-08-30 10:00:00'),
            (None, 103, 505, 5, 15, '2026-08-30 10:00:00'),  # LOW STOCK
            (None, 103, 506, 92, 20, '2026-08-30 10:00:00'),
            (None, 103, 507, 65, 15, '2026-08-30 10:00:00'),
            (None, 103, 508, 40, 15, '2026-08-30 10:00:00'),
            (None, 103, 509, 12, 5, '2026-08-30 10:00:00'),
            (None, 103, 510, 75, 20, '2026-08-30 10:00:00')
        ]
        cursor.executemany("INSERT INTO INVENTORY VALUES (?,?,?,?,?,?)", inventory)

        logs = [
            (None, 101, 501, 200, 'RESTOCK', '2026-08-04 10:30:00', 'ORD-901'),
            (None, 101, 501, -30, 'DISPENSE', '2026-08-10 11:15:00', 'BILL-1101'),
            (None, 101, 501, -30, 'DISPENSE', '2026-08-12 14:20:00', 'BILL-1102'),
            (None, 101, 504, 30, 'RESTOCK', '2026-08-14 09:00:00', 'ORD-902'),
            (None, 101, 504, -18, 'DISPENSE', '2026-08-15 16:45:00', 'BILL-1109'),
            (None, 102, 501, 250, 'RESTOCK', '2026-08-16 11:00:00', 'ORD-903'),
            (None, 102, 503, 120, 'RESTOCK', '2026-08-16 11:05:00', 'ORD-903'),
            (None, 102, 503, -30, 'DISPENSE', '2026-08-18 12:10:00', 'BILL-1103'),
            (None, 103, 505, 50, 'RESTOCK', '2026-08-19 15:30:00', 'ORD-904'),
            (None, 103, 505, -45, 'DISPENSE', '2026-08-25 17:00:00', 'BILL-1107'),
            (None, 101, 508, -15, 'DAMAGE', '2026-08-28 10:00:00', 'AUDIT-LOG-1'),
            (None, 103, 509, 20, 'RESTOCK', '2026-09-02 09:45:00', 'ORD-907')
        ]
        cursor.executemany("INSERT INTO STOCK_LOG VALUES (?,?,?,?,?,?,?)", logs)

    def get_connection(self):
        """Returns active database connection (MySQL or SQLite)."""
        if self._is_mysql:
            return mysql.connector.connect(
                host=Config.MYSQL_HOST,
                port=Config.MYSQL_PORT,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DATABASE
            )
        else:
            conn = sqlite3.connect(Config.FALLBACK_DB_PATH)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON;")
            return conn

    def get_status(self):
        """Returns connection health and metadata for UI badge."""
        return {
            "is_mysql": self._is_mysql,
            "engine": "MySQL 8.x Enterprise" if self._is_mysql else "Zero-Config Fallback Demo Engine (SQLite)",
            "database": Config.MYSQL_DATABASE if self._is_mysql else str(Config.FALLBACK_DB_PATH.name),
            "host": f"{Config.MYSQL_HOST}:{Config.MYSQL_PORT}" if self._is_mysql else "Embedded Local Memory/File",
            "active": True
        }

    def execute_query(self, sql, params=None, fetchall=True, fetchone=False):
        """Executes parameterized SELECT query."""
        conn = self.get_connection()
        try:
            if self._is_mysql:
                cursor = conn.cursor(dictionary=True)
                # In MySQL, replace ? with %s if needed
                mysql_sql = sql.replace('?', '%s')
                cursor.execute(mysql_sql, params or ())
                if fetchone:
                    return cursor.fetchone()
                return cursor.fetchall()
            else:
                cursor = conn.cursor()
                # In SQLite, replace %s with ? if needed
                sqlite_sql = sql.replace('%s', '?')
                cursor.execute(sqlite_sql, params or ())
                if fetchone:
                    row = cursor.fetchone()
                    return dict(row) if row else None
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
        finally:
            conn.close()

    def execute_mutation(self, sql, params=None):
        """Executes INSERT/UPDATE/DELETE statement."""
        conn = self.get_connection()
        try:
            if self._is_mysql:
                cursor = conn.cursor()
                mysql_sql = sql.replace('?', '%s')
                cursor.execute(mysql_sql, params or ())
                conn.commit()
                return cursor.lastrowid or cursor.rowcount
            else:
                cursor = conn.cursor()
                sqlite_sql = sql.replace('%s', '?')
                cursor.execute(sqlite_sql, params or ())
                conn.commit()
                return cursor.lastrowid or cursor.rowcount
        finally:
            conn.close()

    def call_procedure(self, proc_name, args):
        """Executes stored procedure with native MySQL support or emulated PL/SQL logic."""
        if self._is_mysql:
            conn = self.get_connection()
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.callproc(proc_name, args)
                conn.commit()
                return {"success": True, "message": f"Procedure `{proc_name}` executed successfully in MySQL 8.x"}
            except MySQLError as err:
                return {"success": False, "error": str(err.msg if hasattr(err, 'msg') else err)}
            finally:
                conn.close()
        else:
            # Emulated procedure execution in Python for the fallback mode
            return self._emulate_procedure(proc_name, args)

    def _emulate_procedure(self, proc_name, args):
        """Emulates MySQL stored procedures for fallback demo mode."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if proc_name == 'add_patient':
                # args: p_id, p_fname, p_lname, p_dob, p_sex, p_street, p_city, p_state, p_contact
                p_id, p_fname, p_lname, p_dob, p_sex, p_street, p_city, p_state, p_contact = args
                cursor.execute("SELECT COUNT(*) FROM PATIENT WHERE Patient_ID = ?", (p_id,))
                if cursor.fetchone()[0] > 0:
                    raise Exception("Patient with this ID already exists.")
                if p_sex not in ('M', 'F', 'O'):
                    raise Exception("Invalid sex code. Must be M, F, or O.")
                cursor.execute(
                    "INSERT INTO PATIENT VALUES (?,?,?,?,?,?,?,?)",
                    (p_id, p_dob, p_sex, p_city, p_state, p_street, p_fname, p_lname)
                )
                if p_contact:
                    cursor.execute("INSERT INTO PATIENT_CONTACT VALUES (?,?)", (p_id, p_contact))
                conn.commit()
                return {"success": True, "message": f"Patient {p_fname} {p_lname} added successfully via add_patient()"}

            elif proc_name == 'add_medicine':
                # args: p_id, p_name, p_manu, p_exp, p_price, p_pharmacy_id, p_stock, p_reorder
                p_id, p_name, p_manu, p_exp, p_price, p_pharm_id, p_stock, p_reorder = args
                if float(p_price) <= 0:
                    raise Exception("Medicine price must be strictly greater than zero.")
                if p_exp <= p_manu:
                    raise Exception("Expiration date must be strictly after manufacturing date.")
                cursor.execute("SELECT COUNT(*) FROM MEDICINE WHERE Medicine_ID = ?", (p_id,))
                if cursor.fetchone()[0] > 0:
                    raise Exception("Medicine with this ID already exists.")
                cursor.execute("INSERT INTO MEDICINE VALUES (?,?,?,?,?)", (p_id, p_manu, p_exp, p_name, p_price))
                if p_pharm_id:
                    cursor.execute(
                        "INSERT INTO INVENTORY (Pharmacy_ID, Medicine_ID, Quantity, Reorder_Level) VALUES (?,?,?,?)",
                        (p_pharm_id, p_id, p_stock or 0, p_reorder or 15)
                    )
                    if p_stock and int(p_stock) > 0:
                        cursor.execute(
                            "INSERT INTO STOCK_LOG (Pharmacy_ID, Medicine_ID, Quantity_Change, Change_Type, Reference_ID) VALUES (?,?,?,?,?)",
                            (p_pharm_id, p_id, p_stock, 'RESTOCK', 'INITIAL-SETUP')
                        )
                conn.commit()
                return {"success": True, "message": f"Medicine `{p_name}` added and stock initialized via add_medicine()"}

            elif proc_name == 'restock_medicine':
                # args: p_pharmacy_id, p_medicine_id, p_quantity, p_reference_id
                p_pharm_id, p_med_id, p_qty, p_ref = args
                if int(p_qty) <= 0:
                    raise Exception("Restock quantity must be positive.")
                # Update inventory
                cursor.execute(
                    "UPDATE INVENTORY SET Quantity = Quantity + ?, Last_Updated = CURRENT_TIMESTAMP WHERE Pharmacy_ID = ? AND Medicine_ID = ?",
                    (p_qty, p_pharm_id, p_med_id)
                )
                if cursor.rowcount == 0:
                    cursor.execute(
                        "INSERT INTO INVENTORY (Pharmacy_ID, Medicine_ID, Quantity, Reorder_Level) VALUES (?,?,?,15)",
                        (p_pharm_id, p_med_id, p_qty)
                    )
                # Log to stock_log
                cursor.execute(
                    "INSERT INTO STOCK_LOG (Pharmacy_ID, Medicine_ID, Quantity_Change, Change_Type, Reference_ID) VALUES (?,?,?,?,?)",
                    (p_pharm_id, p_med_id, p_qty, 'RESTOCK', p_ref or 'MANUAL-RESTOCK')
                )
                conn.commit()
                return {"success": True, "message": f"Restocked +{p_qty} units and generated audit entry in STOCK_LOG."}

            elif proc_name == 'create_prescription':
                # args: p_id, p_doc_id, p_pat_id, p_date
                p_id, p_doc_id, p_pat_id, p_date = args
                cursor.execute("SELECT COUNT(*) FROM DOCTOR WHERE Doctor_ID = ?", (p_doc_id,))
                if cursor.fetchone()[0] == 0:
                    raise Exception("Prescribing Doctor does not exist in registry.")
                cursor.execute("SELECT COUNT(*) FROM PATIENT WHERE Patient_ID = ?", (p_pat_id,))
                if cursor.fetchone()[0] == 0:
                    raise Exception("Patient does not exist in registry.")
                cursor.execute("INSERT INTO PRESCRIPTION VALUES (?,?,?,?)", (p_id, p_doc_id, p_pat_id, p_date))
                conn.commit()
                return {"success": True, "message": f"Prescription #{p_id} registered successfully."}

            elif proc_name == 'generate_bill':
                # args: p_bill_id, p_pharmacy_id, p_patient_id, p_prescription_id
                p_bill_id, p_pharm_id, p_pat_id, p_presc_id = args
                cursor.execute("SELECT SUM(M.Price) FROM PRESCRIPTION_ITEM PI JOIN MEDICINE M ON PI.Medicine_ID = M.Medicine_ID WHERE PI.Prescription_ID = ?", (p_presc_id,))
                total = cursor.fetchone()[0] or 50.00
                cursor.execute("INSERT INTO BILL VALUES (?,?,?,?)", (p_bill_id, p_pharm_id, total, p_pat_id))
                # Decrement stock and log
                cursor.execute("SELECT Medicine_ID FROM PRESCRIPTION_ITEM WHERE Prescription_ID = ?", (p_presc_id,))
                items = cursor.fetchall()
                for item in items:
                    med_id = item[0]
                    cursor.execute("UPDATE INVENTORY SET Quantity = MAX(0, Quantity - 1) WHERE Pharmacy_ID = ? AND Medicine_ID = ?", (p_pharm_id, med_id))
                    cursor.execute("INSERT INTO STOCK_LOG (Pharmacy_ID, Medicine_ID, Quantity_Change, Change_Type, Reference_ID) VALUES (?,?,?,?,?)",
                                   (p_pharm_id, med_id, -1, 'DISPENSE', f"BILL-{p_bill_id}"))
                conn.commit()
                return {"success": True, "message": f"Bill #{p_bill_id} generated for ₹{float(total):,.2f}."}

            elif proc_name == 'place_order':
                # args: p_order_id, p_supplier_id, p_pharmacy_id, p_qty, p_date, p_arrival, p_pay, p_status
                p_ord_id, p_supp_id, p_pharm_id, p_qty, p_date, p_arrival, p_pay, p_status = args
                cursor.execute("INSERT INTO `ORDER` VALUES (?,?,?,?,?,?,?,?)", (p_ord_id, p_supp_id, p_pharm_id, p_date, p_arrival, p_pay, p_status, p_qty))
                conn.commit()
                return {"success": True, "message": f"Purchase Order #{p_ord_id} placed successfully."}

            else:
                return {"success": False, "error": f"Unknown procedure {proc_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            conn.close()

db = DatabaseManager()
