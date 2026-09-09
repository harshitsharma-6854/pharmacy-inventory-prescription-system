-- ============================================================================
-- PHARMACY INVENTORY AND PRESCRIPTION TRACKING SYSTEM
-- DA2 College Database Project - Verification & Test Cases Suite
-- 15 Comprehensive Test Scenarios (Positive and Negative Boundary Tests)
-- ============================================================================

USE pharmacy_system_new;

-- ----------------------------------------------------------------------------
-- TEST CASE 1: Insert Valid Patient (Procedure: add_patient)
-- Expected Result: SUCCESS - Patient 411 and contact inserted cleanly.
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 1: Insert Valid Patient ===' AS `Running_Test`;
CALL add_patient(411, 'Aditya', 'Saxena', '1992-06-15', 'M', 'Flat 502, Lotus Towers, Andheri West', 'Mumbai', 'Maharashtra', '+91 98200 88990');
SELECT * FROM `PATIENT` WHERE `Patient_ID` = 411;
SELECT * FROM `PATIENT_CONTACT` WHERE `Patient_ID` = 411;

-- ----------------------------------------------------------------------------
-- TEST CASE 2: Insert Duplicate Patient (Exception Test)
-- Expected Result: FAILURE - SIGNAL SQLSTATE '45000' "Patient already exists"
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 2: Duplicate Patient ID Exception ===' AS `Running_Test`;
-- CALL add_patient(411, 'Duplicate', 'User', '1990-01-01', 'M', 'Street', 'City', 'State', '+91 99999 99999');
-- Expected: Error 1644 (45000): Exception: Patient with this ID already exists.

-- ----------------------------------------------------------------------------
-- TEST CASE 3: Insert Valid Medicine (Procedure: add_medicine)
-- Expected Result: SUCCESS - Medicine 515 cataloged and initial inventory set.
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 3: Insert Valid Medicine ===' AS `Running_Test`;
CALL add_medicine(515, 'Pan-D Capsule (Pantoprazole + Domperidone)', '2024-05-01', '2026-11-30', 165.00, 101, 50, 15);
SELECT * FROM `MEDICINE` WHERE `Medicine_ID` = 515;
SELECT * FROM `INVENTORY` WHERE `Medicine_ID` = 515 AND `Pharmacy_ID` = 101;

-- ----------------------------------------------------------------------------
-- TEST CASE 4: Invalid Medicine Price (Zero or Negative Check)
-- Expected Result: FAILURE - Exception: Medicine price must be strictly greater than zero.
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 4: Invalid Medicine Price Exception ===' AS `Running_Test`;
-- CALL add_medicine(516, 'Zero Price Drug', '2024-01-01', '2026-01-01', -10.00, 101, 10, 5);
-- Expected: Error 1644 (45000): Exception: Medicine price must be strictly greater than zero.

-- ----------------------------------------------------------------------------
-- TEST CASE 5: Invalid Expiry Date (Exp <= Manu Date)
-- Expected Result: FAILURE - Exception: Expiration date must be strictly after manufacturing date.
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 5: Invalid Expiry Date Check ===' AS `Running_Test`;
-- CALL add_medicine(517, 'Backward Time Drug', '2025-01-01', '2023-01-01', 50.00, 101, 10, 5);
-- Expected: Error 1644 (45000): Exception: Expiration date must be strictly after manufacturing date.

-- ----------------------------------------------------------------------------
-- TEST CASE 6: Create Valid Prescription (Procedure: create_prescription)
-- Expected Result: SUCCESS - Prescription 1015 created for Doctor 301 and Patient 401.
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 6: Create Valid Prescription ===' AS `Running_Test`;
CALL create_prescription(1015, 301, 401, '2026-09-04');
SELECT * FROM `PRESCRIPTION` WHERE `Prescription_ID` = 1015;

-- ----------------------------------------------------------------------------
-- TEST CASE 7: Invalid Patient ID in Prescription
-- Expected Result: FAILURE - Exception: Patient does not exist in registry.
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 7: Invalid Patient Reference Exception ===' AS `Running_Test`;
-- CALL create_prescription(1016, 301, 99999, '2026-09-04');
-- Expected: Error 1644 (45000): Exception: Patient does not exist in registry.

-- ----------------------------------------------------------------------------
-- TEST CASE 8: Invalid Doctor ID in Prescription
-- Expected Result: FAILURE - Exception: Prescribing Doctor does not exist in registry.
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 8: Invalid Doctor Reference Exception ===' AS `Running_Test`;
-- CALL create_prescription(1017, 88888, 401, '2026-09-04');
-- Expected: Error 1644 (45000): Exception: Prescribing Doctor does not exist in registry.

-- ----------------------------------------------------------------------------
-- TEST CASE 9: Generate Bill for Prescription (Procedure: generate_bill)
-- Expected Result: SUCCESS - Bill created with auto-calculated items, stock log updated.
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 9: Generate Bill & Auto Calculation ===' AS `Running_Test`;
-- Add items to prescription 1015 first
INSERT INTO `PRESCRIPTION_ITEM` (`Prescription_ID`, `Medicine_ID`, `Dosage`, `Frequency`, `Duration`) 
VALUES (1015, 501, '650mg', 'Twice Daily (BD)', '5 Days');

CALL generate_bill(1120, 101, 401, 1015);
SELECT * FROM `BILL` WHERE `Bill_ID` = 1120;
SELECT * FROM `STOCK_LOG` WHERE `Reference_ID` = 'BILL-1120';

-- ----------------------------------------------------------------------------
-- TEST CASE 10: Insufficient Stock Check / Negative Quantity Prevention
-- Expected Result: FAILURE - Trigger signals SQLSTATE '45000': Inventory quantity cannot be negative.
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 10: Negative Inventory Trigger Enforcement ===' AS `Running_Test`;
-- UPDATE `INVENTORY` SET `Quantity` = -5 WHERE `Pharmacy_ID` = 101 AND `Medicine_ID` = 501;
-- Expected: Error 1644 (45000): Trigger Exception: Inventory quantity cannot be negative.

-- ----------------------------------------------------------------------------
-- TEST CASE 11: Restock Medicine (Procedure: restock_medicine)
-- Expected Result: SUCCESS - Inventory increments by +40, logged in STOCK_LOG.
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 11: Restock Medicine Verification ===' AS `Running_Test`;
SELECT `Quantity` AS `Quantity_Before_Restock` FROM `INVENTORY` WHERE `Pharmacy_ID` = 101 AND `Medicine_ID` = 501;
CALL restock_medicine(101, 501, 40, 'RESTOCK-DEMO-ORD1');
SELECT `Quantity` AS `Quantity_After_Restock` FROM `INVENTORY` WHERE `Pharmacy_ID` = 101 AND `Medicine_ID` = 501;
SELECT * FROM `STOCK_LOG` WHERE `Pharmacy_ID` = 101 AND `Medicine_ID` = 501 ORDER BY `Log_ID` DESC LIMIT 1;

-- ----------------------------------------------------------------------------
-- TEST CASE 12: Trigger Execution Verification (trg_after_inventory_update)
-- Expected Result: SUCCESS - Direct UPDATE on inventory automatically logs audit row.
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 12: Automatic Audit Trigger Verification ===' AS `Running_Test`;
UPDATE `INVENTORY` SET `Quantity` = `Quantity` + 10 WHERE `Pharmacy_ID` = 102 AND `Medicine_ID` = 501;
SELECT * FROM `STOCK_LOG` WHERE `Pharmacy_ID` = 102 AND `Medicine_ID` = 501 AND `Reference_ID` = 'AUTO-TRIGGER-AUDIT' ORDER BY `Log_ID` DESC LIMIT 1;

-- ----------------------------------------------------------------------------
-- TEST CASE 13: Foreign Key Constraint Enforcement
-- Expected Result: FAILURE - Cannot add order referencing non-existent supplier.
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 13: Foreign Key Constraint on Order ===' AS `Running_Test`;
-- INSERT INTO `ORDER` (`Order_ID`, `Supplier_ID`, `Pharmacy_ID`, `Date`, `Payment_Status`, `Order_Status`, `Quantity_Ordered`)
-- VALUES (9999, 99999, 101, CURDATE(), 'Pending', 'Pending', 50);
-- Expected: Error 1452 (23000): Cannot add or update a child row: a foreign key constraint fails.

-- ----------------------------------------------------------------------------
-- TEST CASE 14: Invalid Order Quantities (CHECK Constraint)
-- Expected Result: FAILURE - Check constraint `chk_order_qty` fails if quantity <= 0.
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 14: Invalid Order Quantity Check ===' AS `Running_Test`;
-- CALL place_order(995, 801, 101, -50, CURDATE(), NULL, 'Pending', 'Pending');
-- Expected: Error 1644 (45000): Exception: Quantity ordered must be strictly greater than zero.

-- ----------------------------------------------------------------------------
-- TEST CASE 15: Stored Function Evaluation
-- Expected Result: Returns verified scalar numeric values.
-- ----------------------------------------------------------------------------
SELECT '=== TEST CASE 15: Stored Functions Verification ===' AS `Running_Test`;
SELECT 
    get_medicine_price(501) AS `Price_Dolo_650`,
    get_patient_prescription_count(401) AS `Prescriptions_Patient_401`,
    calculate_prescription_total(1001) AS `Calculated_Prescription_1001_Total`,
    get_pharmacy_revenue(101) AS `Gross_Revenue_Apollo_Mumbai`,
    get_medicine_stock(101, 501) AS `Current_Stock_Apollo_Dolo`;
