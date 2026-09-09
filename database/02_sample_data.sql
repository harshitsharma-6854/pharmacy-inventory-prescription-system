-- ============================================================================
-- PHARMACY INVENTORY AND PRESCRIPTION TRACKING SYSTEM
-- DA2 College Database Project - Comprehensive Sample Data
-- Indian Context: Authentic Names, Cities, Hospitals & Medical Formulations
-- ============================================================================

USE pharmacy_system_new;

-- ----------------------------------------------------------------------------
-- 1. PHARMACIES (3 Major Dispensing Branches)
-- ----------------------------------------------------------------------------
INSERT INTO `PHARMACY` (`Pharmacy_ID`, `Name`, `Rating`, `City`, `State`, `Street`, `Contact_No`) VALUES
(101, 'Apollo HealthCity Pharmacy', 4.8, 'Mumbai', 'Maharashtra', 'Ground Floor, Bandra Reclamation, Hill Road', '+91 22 2640 5555'),
(102, 'MedPlus Community Care', 4.6, 'Bengaluru', 'Karnataka', '82 100-Ft Road, 4th Block, Koramangala', '+91 80 4120 7788'),
(103, 'Fortis MedStore Express', 4.9, 'New Delhi', 'Delhi', 'Gate No 2, Sector B, Vasant Kunj Marg', '+91 11 4277 6200');

-- ----------------------------------------------------------------------------
-- 2. PHARMACY CONTACTS (Multi-valued attribute resolution)
-- ----------------------------------------------------------------------------
INSERT INTO `PHARMACY_CONTACT` (`Pharmacy_ID`, `Contact_No`) VALUES
(101, '+91 22 2640 5555'),
(101, '+91 22 2640 5599'), -- 24x7 Emergency Desk
(102, '+91 80 4120 7788'),
(102, '+91 98450 11223'), -- Night Duty Mobile
(103, '+91 11 4277 6200'),
(103, '+91 11 4277 6299'); -- Senior Pharmacist Line

-- ----------------------------------------------------------------------------
-- 3. HOSPITALS (3 Leading Partner Hospitals)
-- ----------------------------------------------------------------------------
INSERT INTO `HOSPITAL` (`Hospital_ID`, `Pharmacy_ID`, `City`, `State`, `Street`, `Name`, `Contact`) VALUES
(201, 101, 'Mumbai', 'Maharashtra', 'A-791 Bandra West, Near Lilavati Road', 'Lilavati Hospital & Research Centre', '+91 22 2675 1000'),
(202, 102, 'Bengaluru', 'Karnataka', '98 HAL Old Airport Road, Kodihalli', 'Manipal Hospital Bengaluru', '+91 80 2502 4444'),
(203, 103, 'New Delhi', 'Delhi', 'Sri Aurobindo Marg, Ansari Nagar East', 'AIIMS Apex Trauma & Medical Center', '+91 11 2658 8500');

-- ----------------------------------------------------------------------------
-- 4. DOCTORS (8 Qualified Specialists)
-- ----------------------------------------------------------------------------
INSERT INTO `DOCTOR` (`Doctor_ID`, `Hospital_ID`, `Experience`, `Contact_No`, `First_Name`, `Last_Name`, `Qualification`) VALUES
(301, 201, 14, '+91 98201 44552', 'Rajesh', 'Kulkarni', 'MBBS, MD (General Medicine)'),
(302, 201, 18, '+91 98205 11984', 'Sunita', 'Deshmukh', 'MBBS, MS (General Surgery)'),
(303, 202, 11, '+91 97410 88231', 'Anand', 'Narayanaswamy', 'MBBS, MD, DM (Cardiology)'),
(304, 202, 8,  '+91 98451 77210', 'Pooja', 'Rao', 'MBBS, DCH, MD (Pediatrics)'),
(305, 202, 15, '+91 96112 33490', 'Venkatesh', 'Bhat', 'MBBS, MS (Orthopedics)'),
(306, 203, 20, '+91 98110 55671', 'Arvind', 'Aggarwal', 'MBBS, MD, DM (Neurology)'),
(307, 203, 9,  '+91 98188 44321', 'Meenakshi', 'Sundaram', 'MBBS, MD (Pulmonology)'),
(308, 203, 12, '+91 99102 99012', 'Kabir', 'Malhotra', 'MBBS, MD (Endocrinology)');

-- ----------------------------------------------------------------------------
-- 5. PATIENTS (10 Diverse Patients)
-- ----------------------------------------------------------------------------
INSERT INTO `PATIENT` (`Patient_ID`, `DOB`, `Sex`, `City`, `State`, `Street`, `First_Name`, `Last_Name`) VALUES
(401, '1982-04-14', 'M', 'Mumbai', 'Maharashtra', 'Flat 402, Sea View Apts, Worli Seaface', 'Rahul', 'Sharma'),
(402, '1990-09-22', 'F', 'Mumbai', 'Maharashtra', '12 Gokul Dham, Andheri East', 'Priya', 'Patel'),
(403, '1975-11-05', 'M', 'Bengaluru', 'Karnataka', '204 Silver Oak Enclave, Indiranagar', 'Suresh', 'Menon'),
(404, '1988-03-19', 'F', 'Bengaluru', 'Karnataka', '45 Green Glen Layout, Bellandur', 'Deepika', 'Iyer'),
(405, '1964-07-30', 'M', 'Bengaluru', 'Karnataka', '108 Brigade Gateway, Malleshwaram', 'Ramesh', 'Gowda'),
(406, '1995-12-11', 'F', 'New Delhi', 'Delhi', 'C-14 Hauz Khas Enclave, South Delhi', 'Ananya', 'Verma'),
(407, '1970-01-25', 'M', 'New Delhi', 'Delhi', 'B-4/88 Safdarjung Enclave', 'Vikram', 'Singh'),
(408, '1985-08-16', 'F', 'New Delhi', 'Delhi', 'Plot 12 Sector 14, Rohini', 'Sneha', 'Gupta'),
(409, '1958-05-02', 'M', 'Mumbai', 'Maharashtra', '71 Parsi Colony, Dadar East', 'Homi', 'Wadia'),
(410, '2001-10-28', 'F', 'Bengaluru', 'Karnataka', '5th Cross, HSR Layout Sector 2', 'Kavya', 'Reddy');

-- ----------------------------------------------------------------------------
-- 6. PATIENT CONTACTS (Multi-valued attribute resolution)
-- ----------------------------------------------------------------------------
INSERT INTO `PATIENT_CONTACT` (`Patient_ID`, `Contact_No`) VALUES
(401, '+91 98200 12345'),
(401, '+91 22 2493 0011'), -- Landline
(402, '+91 98211 23456'),
(403, '+91 98450 34567'),
(403, '+91 98450 99887'), -- Spouse Alternate
(404, '+91 99000 45678'),
(405, '+91 98440 56789'),
(406, '+91 98100 67890'),
(407, '+91 98111 78901'),
(408, '+91 98180 89012'),
(409, '+91 98202 90123'),
(410, '+91 99800 01234');

-- ----------------------------------------------------------------------------
-- 7. MEDICINES (12 Essential Formulations with Realistic Prices & Dates)
-- ----------------------------------------------------------------------------
INSERT INTO `MEDICINE` (`Medicine_ID`, `Manu_Date`, `Exp_Date`, `Name`, `Price`) VALUES
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
(512, '2022-01-10', '2024-06-30', 'Combiflam Tablet (Ibuprofen + Paracetamol)', 45.00); -- Intentionally expired for query demo

-- ----------------------------------------------------------------------------
-- 8. PHARMACISTS (6 Certified Pharmacists across Shifts)
-- ----------------------------------------------------------------------------
INSERT INTO `PHARMACIST` (`Pharmacist_ID`, `Pharmacy_ID`, `Shift`, `Name`) VALUES
(601, 101, 'Morning', 'Manoj Kumar Tiwari'),
(602, 101, 'Evening', 'Shilpa Nair'),
(603, 102, 'Morning', 'Girish Channappa'),
(604, 102, 'Night',   'Karthik Somayaji'),
(605, 103, 'Morning', 'Harish Chander Sharma'),
(606, 103, 'Evening', 'Pratibha Chauhan');

-- ----------------------------------------------------------------------------
-- 9. MANUFACTURERS (5 Top Indian Pharma Giants)
-- ----------------------------------------------------------------------------
INSERT INTO `MANUFACTURER` (`Manufacturer_ID`, `Brand_Name`, `City`, `State`, `Street`) VALUES
(701, 'Sun Pharmaceutical Industries Ltd', 'Mumbai', 'Maharashtra', 'Sun House, CTS No. 201 B/1, Western Express Hwy, Goregaon East'),
(702, 'Cipla Limited', 'Mumbai', 'Maharashtra', 'Cipla House, Peninsula Business Park, Ganpatrao Kadam Marg, Lower Parel'),
(703, 'Dr. Reddy Laboratories', 'Hyderabad', 'Telangana', '8-2-337 Road No 3, Banjara Hills'),
(704, 'Lupin Pharmaceuticals', 'Mumbai', 'Maharashtra', 'Kalpataru Inspire, 3rd Floor, Off Western Express Hwy, Santacruz East'),
(705, 'Torrent Pharmaceuticals Ltd', 'Ahmedabad', 'Gujarat', 'Torrent House, Off Ashram Road, Navrangpura');

-- ----------------------------------------------------------------------------
-- 10. SUPPLIERS (5 Certified Pharmaceutical Distributors)
-- ----------------------------------------------------------------------------
INSERT INTO `SUPPLIER` (`Supplier_ID`, `Contact`, `City`, `State`, `Street`, `Name`) VALUES
(801, '+91 22 2850 4433', 'Mumbai', 'Maharashtra', 'Gala 14, New Sonal Industrial Estate, Sakinaka, Andheri', 'Apex Pharma Distributors LLP'),
(802, '+91 80 2226 9911', 'Bengaluru', 'Karnataka', '42 OTC Road, Chickpet Commercial Complex', 'Karnataka Medico Supplies'),
(803, '+91 11 2386 1120', 'New Delhi', 'Delhi', 'Shop 108 Bhagirath Palace, Chandni Chowk', 'Capital Healthcare Logistics'),
(804, '+91 40 2465 7788', 'Hyderabad', 'Telangana', '15-4-282 Gowliguda Chaman, Koti', 'Deccan Drug Distributors'),
(805, '+91 79 2658 3344', 'Ahmedabad', 'Gujarat', 'B-12 Relief Commercial Hub, Relief Road', 'Western Gujarat Pharma Trade');

-- ----------------------------------------------------------------------------
-- 11. JUNCTION: SUPPLIER_MANUFACTURER (M:N Distribution Rights)
-- ----------------------------------------------------------------------------
INSERT INTO `SUPPLIER_MANUFACTURER` (`Supplier_ID`, `Manufacturer_ID`) VALUES
(801, 701), -- Apex distributes Sun Pharma
(801, 702), -- Apex distributes Cipla
(801, 704), -- Apex distributes Lupin
(802, 701), -- Karnataka Medico distributes Sun Pharma
(802, 703), -- Karnataka Medico distributes Dr. Reddy's
(802, 705), -- Karnataka Medico distributes Torrent
(803, 702), -- Capital Healthcare distributes Cipla
(803, 703), -- Capital Healthcare distributes Dr. Reddy's
(804, 703), -- Deccan distributes Dr. Reddy's
(804, 704), -- Deccan distributes Lupin
(805, 701), -- Western Gujarat distributes Sun Pharma
(805, 705); -- Western Gujarat distributes Torrent

-- ----------------------------------------------------------------------------
-- 12. WHOLESALE SUPPLIERS (GST-Registered Entities)
-- ----------------------------------------------------------------------------
INSERT INTO `WHOLESALE_SUPPLIER` (`GST_No`, `City`, `State`, `Street`) VALUES
('27AAACH1234F1Z5', 'Mumbai', 'Maharashtra', 'Building C, APMC Market Yard, Vashi, Navi Mumbai'),
('29AABCK5678P1ZQ', 'Bengaluru', 'Karnataka', 'Warehouse 18, Peenya Industrial Area 3rd Phase'),
('07AABCW9012M1Z8', 'New Delhi', 'Delhi', 'Godown 4, Okhla Industrial Area Phase II'),
('36AABCS3456L1Z2', 'Hyderabad', 'Telangana', 'Shed 9, Autonagar Industrial Corridor, LB Nagar'),
('24AABCT7890N1Z9', 'Ahmedabad', 'Gujarat', 'Plot 55, Vatva GIDC Phase IV');

-- ----------------------------------------------------------------------------
-- 13. JUNCTION: SUPPLIER_WHOLESALE (M:N Business Associations)
-- ----------------------------------------------------------------------------
INSERT INTO `SUPPLIER_WHOLESALE` (`Supplier_ID`, `GST_No`) VALUES
(801, '27AAACH1234F1Z5'),
(802, '29AABCK5678P1ZQ'),
(803, '07AABCW9012M1Z8'),
(804, '36AABCS3456L1Z2'),
(805, '24AABCT7890N1Z9'),
(801, '29AABCK5678P1ZQ'); -- Inter-state wholesale supply

-- ----------------------------------------------------------------------------
-- 14. JUNCTION: SUPPLIER_PHARMACY (M:N Authorized Procurement Channels)
-- ----------------------------------------------------------------------------
INSERT INTO `SUPPLIER_PHARMACY` (`Supplier_ID`, `Pharmacy_ID`) VALUES
(801, 101),
(801, 102),
(802, 102),
(803, 103),
(804, 101),
(804, 102),
(805, 101),
(805, 103);

-- ----------------------------------------------------------------------------
-- 15. ORDERS (12 Procurement Transactions Across Statuses)
-- ----------------------------------------------------------------------------
INSERT INTO `ORDER` (`Order_ID`, `Supplier_ID`, `Pharmacy_ID`, `Date`, `Arrival_Date`, `Payment_Status`, `Order_Status`, `Quantity_Ordered`) VALUES
(901, 801, 101, '2026-08-01', '2026-08-04', 'Paid',     'Delivered',   250),
(902, 801, 101, '2026-08-10', '2026-08-14', 'Paid',     'Delivered',   180),
(903, 802, 102, '2026-08-12', '2026-08-16', 'Paid',     'Delivered',   300),
(904, 803, 103, '2026-08-15', '2026-08-19', 'Paid',     'Delivered',   150),
(905, 804, 101, '2026-08-20', '2026-08-24', 'Partial',  'Delivered',   120),
(906, 802, 102, '2026-08-25', '2026-08-29', 'Paid',     'Delivered',   220),
(907, 803, 103, '2026-08-28', '2026-09-02', 'Paid',     'Delivered',   190),
(908, 801, 101, '2026-08-30', '2026-09-05', 'Pending',   'Processing',  140),
(909, 805, 103, '2026-09-01', '2026-09-06', 'Pending',   'Shipped',     200),
(910, 802, 102, '2026-09-02', NULL,         'Pending',   'Pending',     100),
(911, 804, 102, '2026-08-05', NULL,         'Refunded',  'Cancelled',    80),
(912, 805, 101, '2026-09-03', '2026-09-08', 'Pending',   'Processing',  160);

-- ----------------------------------------------------------------------------
-- 16. PRESCRIPTIONS (12 Clinical Prescriptions)
-- ----------------------------------------------------------------------------
INSERT INTO `PRESCRIPTION` (`Prescription_ID`, `Doctor_ID`, `Patient_ID`, `Date`) VALUES
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
(1011, 302, 401, '2026-09-02'), -- Patient 401 multiple prescriptions
(1012, 306, 407, '2026-09-03'); -- Patient 407 multiple prescriptions

-- ----------------------------------------------------------------------------
-- 17. PRESCRIPTION_ITEM (26 Detailed Itemized Medications)
-- ----------------------------------------------------------------------------
INSERT INTO `PRESCRIPTION_ITEM` (`Item_ID`, `Prescription_ID`, `Medicine_ID`, `Dosage`, `Frequency`, `Duration`) VALUES
(1,  1001, 501, '650mg', 'Thrice Daily (TDS)', '5 Days'),
(2,  1001, 506, '40mg',  'Once Daily Before Breakfast (OD)', '10 Days'),
(3,  1002, 502, '625mg', 'Twice Daily After Food (BD)', '7 Days'),
(4,  1002, 507, '10mg',  'Once Daily at Bedtime (HS)', '5 Days'),
(5,  1003, 503, '500mg', 'Twice Daily with Meals (BD)', '30 Days'),
(6,  1003, 504, '20mg',  'Once Daily at Night (OD)', '30 Days'),
(7,  1003, 510, '40mg',  'Once Daily Morning (OD)', '30 Days'),
(8,  1004, 501, '250mg', 'SOS As Needed', '3 Days'),
(9,  1004, 508, '5ml',   'Thrice Daily (TDS)', '5 Days'),
(10, 1005, 501, '650mg', 'Twice Daily (BD)', '5 Days'),
(11, 1005, 506, '40mg',  'Once Daily (OD)', '7 Days'),
(12, 1006, 507, '10mg',  'Once Daily (OD)', '10 Days'),
(13, 1006, 511, '10mg',  'Once Daily at Night (HS)', '14 Days'),
(14, 1007, 505, '500mg', 'Once Daily for 3 Days (OD)', '3 Days'),
(15, 1007, 508, '10ml',  'Thrice Daily (TDS)', '7 Days'),
(16, 1008, 503, '500mg', 'Twice Daily (BD)', '30 Days'),
(17, 1008, 509, '18 IU', 'Once Daily Subcutaneous (OD)', '30 Days'),
(18, 1009, 504, '20mg',  'Once Daily (OD)', '30 Days'),
(19, 1009, 510, '40mg',  'Once Daily Morning (OD)', '30 Days'),
(20, 1010, 502, '625mg', 'Twice Daily (BD)', '5 Days'),
(21, 1010, 506, '40mg',  'Once Daily (OD)', '7 Days'),
(22, 1011, 501, '650mg', 'Twice Daily (BD)', '3 Days'),
(23, 1011, 506, '40mg',  'Once Daily (OD)', '5 Days'),
(24, 1012, 504, '20mg',  'Once Daily (OD)', '30 Days'),
(25, 1012, 507, '10mg',  'Once Daily (OD)', '7 Days'),
(26, 1002, 501, '650mg', 'SOS (As Needed)', '3 Days');

-- ----------------------------------------------------------------------------
-- 18. BILL (12 Invoiced Records Linked to Pharmacies & Patients)
-- ----------------------------------------------------------------------------
INSERT INTO `BILL` (`Bill_ID`, `Pharmacy_ID`, `Patient_ID`, `Amount`) VALUES
(1101, 101, 401, 174.50),  -- Dolo + Pantocid
(1102, 101, 402, 285.50),  -- Augmentin + Cetzine + Dolo
(1103, 102, 403, 458.50),  -- Glycomet + Atorva + Telma
(1104, 102, 404, 147.50),  -- Dolo + Ascoril Syrup
(1105, 102, 405, 174.50),  -- Dolo + Pantocid
(1106, 103, 406, 226.00),  -- Cetzine + Montair LC
(1107, 103, 407, 239.00),  -- Azithral + Ascoril Syrup
(1108, 103, 408, 1008.50), -- Glycomet + Lantus Insulin
(1109, 101, 409, 340.00),  -- Atorva + Telma
(1110, 102, 410, 347.00),  -- Augmentin + Pantocid
(1111, 101, 401, 174.50),  -- Follow-up bill for Patient 401
(1112, 103, 407, 233.00);  -- Follow-up bill for Patient 407

-- ----------------------------------------------------------------------------
-- 19. INVENTORY (Implementation-Support: Realistic Stock Levels across Branches)
-- Demonstrates IN STOCK, LOW STOCK, and OUT OF STOCK states
-- ----------------------------------------------------------------------------
INSERT INTO `INVENTORY` (`Pharmacy_ID`, `Medicine_ID`, `Quantity`, `Reorder_Level`) VALUES
-- Apollo Mumbai (101)
(101, 501, 140, 25),  -- Dolo 650: Normal Stock
(101, 502, 42,  15),  -- Augmentin: Normal Stock
(101, 503, 85,  20),  -- Glycomet: Normal Stock
(101, 504, 12,  15),  -- Atorva 20: LOW STOCK (< Reorder_Level)
(101, 505, 30,  10),  -- Azithral: Normal Stock
(101, 506, 65,  20),  -- Pantocid: Normal Stock
(101, 507, 9,   15),  -- Cetzine: LOW STOCK (< Reorder_Level)
(101, 508, 0,   10),  -- Ascoril Syrup: OUT OF STOCK
(101, 509, 18,  5),   -- Lantus Insulin: Normal Stock
(101, 510, 50,  15),  -- Telma 40: Normal Stock
(101, 511, 28,  12),  -- Montair LC: Normal Stock
(101, 512, 15,  10),  -- Combiflam: Expired Batch Stock

-- MedPlus Bengaluru (102)
(102, 501, 185, 30),
(102, 502, 8,   15),  -- LOW STOCK
(102, 503, 90,  20),
(102, 504, 60,  15),
(102, 505, 45,  10),
(102, 506, 70,  20),
(102, 507, 80,  15),
(102, 508, 35,  12),
(102, 509, 4,   5),   -- LOW STOCK
(102, 510, 48,  15),

-- Fortis Delhi (103)
(103, 501, 210, 30),
(103, 502, 55,  15),
(103, 503, 110, 25),
(103, 504, 45,  15),
(103, 505, 5,   15),  -- LOW STOCK
(103, 506, 92,  20),
(103, 507, 65,  15),
(103, 508, 40,  15),
(103, 509, 12,  5),
(103, 510, 75,  20);

-- ----------------------------------------------------------------------------
-- 20. STOCK_LOG (Implementation-Support: Immutable Audit Trail of Mutations)
-- ----------------------------------------------------------------------------
INSERT INTO `STOCK_LOG` (`Pharmacy_ID`, `Medicine_ID`, `Quantity_Change`, `Change_Type`, `Change_Date`, `Reference_ID`) VALUES
(101, 501, 200, 'RESTOCK',   '2026-08-04 10:30:00', 'ORD-901'),
(101, 501, -30, 'DISPENSE',  '2026-08-10 11:15:00', 'BILL-1101'),
(101, 501, -30, 'DISPENSE',  '2026-08-12 14:20:00', 'BILL-1102'),
(101, 504, 30,  'RESTOCK',   '2026-08-14 09:00:00', 'ORD-902'),
(101, 504, -18, 'DISPENSE',  '2026-08-15 16:45:00', 'BILL-1109'),
(102, 501, 250, 'RESTOCK',   '2026-08-16 11:00:00', 'ORD-903'),
(102, 503, 120, 'RESTOCK',   '2026-08-16 11:05:00', 'ORD-903'),
(102, 503, -30, 'DISPENSE',  '2026-08-18 12:10:00', 'BILL-1103'),
(103, 505, 50,  'RESTOCK',   '2026-08-19 15:30:00', 'ORD-904'),
(103, 505, -45, 'DISPENSE',  '2026-08-25 17:00:00', 'BILL-1107'),
(101, 508, -15, 'DAMAGE',    '2026-08-28 10:00:00', 'AUDIT-LOG-1'),
(103, 509, 20,  'RESTOCK',   '2026-09-02 09:45:00', 'ORD-907');
