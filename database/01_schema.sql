-- ============================================================================
-- PHARMACY INVENTORY AND PRESCRIPTION TRACKING SYSTEM
-- DA2 College Database Project - Database Schema Implementation
-- Source of Truth: DA1 Conceptual & Relational Design
-- Engine: MySQL 8.x InnoDB
-- ============================================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS pharmacy_system_new
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE pharmacy_system_new;

-- ----------------------------------------------------------------------------
-- Drop existing tables in reverse dependency order to avoid FK errors
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `STOCK_LOG`;
DROP TABLE IF EXISTS `INVENTORY`;
DROP TABLE IF EXISTS `ORDER`;
DROP TABLE IF EXISTS `SUPPLIER_PHARMACY`;
DROP TABLE IF EXISTS `SUPPLIER_WHOLESALE`;
DROP TABLE IF EXISTS `WHOLESALE_SUPPLIER`;
DROP TABLE IF EXISTS `SUPPLIER_MANUFACTURER`;
DROP TABLE IF EXISTS `MANUFACTURER`;
DROP TABLE IF EXISTS `SUPPLIER`;
DROP TABLE IF EXISTS `PHARMACIST`;
DROP TABLE IF EXISTS `BILL`;
DROP TABLE IF EXISTS `PRESCRIPTION_ITEM`;
DROP TABLE IF EXISTS `MEDICINE`;
DROP TABLE IF EXISTS `PRESCRIPTION`;
DROP TABLE IF EXISTS `DOCTOR`;
DROP TABLE IF EXISTS `HOSPITAL`;
DROP TABLE IF EXISTS `PATIENT_CONTACT`;
DROP TABLE IF EXISTS `PATIENT`;
DROP TABLE IF EXISTS `PHARMACY_CONTACT`;
DROP TABLE IF EXISTS `PHARMACY`;

-- ============================================================================
-- 1. PHARMACY
-- Master entity representing dispensing pharmacy branches
-- ============================================================================
CREATE TABLE `PHARMACY` (
    `Pharmacy_ID` INT NOT NULL,
    `Name` VARCHAR(100) NOT NULL,
    `Rating` DECIMAL(2, 1) NOT NULL DEFAULT 5.0,
    `City` VARCHAR(80) NOT NULL,
    `State` VARCHAR(80) NOT NULL,
    `Street` VARCHAR(150) NOT NULL,
    `Contact_No` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`Pharmacy_ID`),
    CONSTRAINT `chk_pharmacy_rating` CHECK (`Rating` >= 1.0 AND `Rating` <= 5.0)
) ENGINE=InnoDB;

-- ============================================================================
-- 2. PHARMACY_CONTACT
-- Multi-valued attribute resolution for additional pharmacy phone lines
-- ============================================================================
CREATE TABLE `PHARMACY_CONTACT` (
    `Pharmacy_ID` INT NOT NULL,
    `Contact_No` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`Pharmacy_ID`, `Contact_No`),
    CONSTRAINT `fk_pharmcontact_pharmacy` FOREIGN KEY (`Pharmacy_ID`) 
        REFERENCES `PHARMACY` (`Pharmacy_ID`) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ============================================================================
-- 3. PATIENT
-- Master entity representing registered patients receiving clinical care
-- ============================================================================
CREATE TABLE `PATIENT` (
    `Patient_ID` INT NOT NULL,
    `DOB` DATE NOT NULL,
    `Sex` CHAR(1) NOT NULL,
    `City` VARCHAR(80) NOT NULL,
    `State` VARCHAR(80) NOT NULL,
    `Street` VARCHAR(150) NOT NULL,
    `First_Name` VARCHAR(50) NOT NULL,
    `Last_Name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`Patient_ID`),
    CONSTRAINT `chk_patient_sex` CHECK (`Sex` IN ('M', 'F', 'O'))
) ENGINE=InnoDB;

-- ============================================================================
-- 4. PATIENT_CONTACT
-- Multi-valued attribute resolution for patient contact telephone numbers
-- ============================================================================
CREATE TABLE `PATIENT_CONTACT` (
    `Patient_ID` INT NOT NULL,
    `Contact_No` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`Patient_ID`, `Contact_No`),
    CONSTRAINT `fk_patcontact_patient` FOREIGN KEY (`Patient_ID`) 
        REFERENCES `PATIENT` (`Patient_ID`) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ============================================================================
-- 5. HOSPITAL
-- Medical institutions affiliated with pharmacy network
-- ============================================================================
CREATE TABLE `HOSPITAL` (
    `Hospital_ID` INT NOT NULL,
    `Pharmacy_ID` INT NOT NULL,
    `City` VARCHAR(80) NOT NULL,
    `State` VARCHAR(80) NOT NULL,
    `Street` VARCHAR(150) NOT NULL,
    `Name` VARCHAR(120) NOT NULL,
    `Contact` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`Hospital_ID`),
    CONSTRAINT `fk_hospital_pharmacy` FOREIGN KEY (`Pharmacy_ID`) 
        REFERENCES `PHARMACY` (`Pharmacy_ID`) 
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ============================================================================
-- 6. DOCTOR
-- Medical practitioners affiliated with hospitals who prescribe medication
-- ============================================================================
CREATE TABLE `DOCTOR` (
    `Doctor_ID` INT NOT NULL,
    `Hospital_ID` INT NOT NULL,
    `Experience` INT NOT NULL DEFAULT 0,
    `Contact_No` VARCHAR(20) NOT NULL,
    `First_Name` VARCHAR(50) NOT NULL,
    `Last_Name` VARCHAR(50) NOT NULL,
    `Qualification` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`Doctor_ID`),
    CONSTRAINT `fk_doctor_hospital` FOREIGN KEY (`Hospital_ID`) 
        REFERENCES `HOSPITAL` (`Hospital_ID`) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `chk_doctor_experience` CHECK (`Experience` >= 0)
) ENGINE=InnoDB;

-- ============================================================================
-- 7. PRESCRIPTION
-- Clinical medical orders issued by doctors for patients
-- ============================================================================
CREATE TABLE `PRESCRIPTION` (
    `Prescription_ID` INT NOT NULL,
    `Doctor_ID` INT NOT NULL,
    `Patient_ID` INT NOT NULL,
    `Date` DATE NOT NULL,
    PRIMARY KEY (`Prescription_ID`),
    CONSTRAINT `fk_prescription_doctor` FOREIGN KEY (`Doctor_ID`) 
        REFERENCES `DOCTOR` (`Doctor_ID`) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_prescription_patient` FOREIGN KEY (`Patient_ID`) 
        REFERENCES `PATIENT` (`Patient_ID`) 
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ============================================================================
-- 8. MEDICINE
-- Pharmaceutical drug catalog with manufacturing, expiration & unit pricing
-- ============================================================================
CREATE TABLE `MEDICINE` (
    `Medicine_ID` INT NOT NULL,
    `Manu_Date` DATE NOT NULL,
    `Exp_Date` DATE NOT NULL,
    `Name` VARCHAR(100) NOT NULL,
    `Price` DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (`Medicine_ID`),
    CONSTRAINT `chk_med_expiry` CHECK (`Exp_Date` > `Manu_Date`),
    CONSTRAINT `chk_med_price` CHECK (`Price` > 0)
) ENGINE=InnoDB;

-- ============================================================================
-- 9. PRESCRIPTION_ITEM
-- Associative entity resolving M:N relationship between Prescription and Medicine
-- ============================================================================
CREATE TABLE `PRESCRIPTION_ITEM` (
    `Item_ID` INT NOT NULL AUTO_INCREMENT,
    `Prescription_ID` INT NOT NULL,
    `Medicine_ID` INT NOT NULL,
    `Dosage` VARCHAR(50) NOT NULL,
    `Frequency` VARCHAR(50) NOT NULL,
    `Duration` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`Item_ID`),
    CONSTRAINT `fk_prescitem_presc` FOREIGN KEY (`Prescription_ID`) 
        REFERENCES `PRESCRIPTION` (`Prescription_ID`) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_prescitem_med` FOREIGN KEY (`Medicine_ID`) 
        REFERENCES `MEDICINE` (`Medicine_ID`) 
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ============================================================================
-- 10. BILL
-- Financial records generated for patients by dispensing pharmacies
-- ============================================================================
CREATE TABLE `BILL` (
    `Bill_ID` INT NOT NULL,
    `Pharmacy_ID` INT NOT NULL,
    `Amount` DECIMAL(10, 2) NOT NULL,
    `Patient_ID` INT NOT NULL,
    PRIMARY KEY (`Bill_ID`),
    CONSTRAINT `fk_bill_pharmacy` FOREIGN KEY (`Pharmacy_ID`) 
        REFERENCES `PHARMACY` (`Pharmacy_ID`) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_bill_patient` FOREIGN KEY (`Patient_ID`) 
        REFERENCES `PATIENT` (`Patient_ID`) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `chk_bill_amount` CHECK (`Amount` >= 0)
) ENGINE=InnoDB;

-- ============================================================================
-- 11. PHARMACIST
-- Licensed pharmaceutical staff operating at specific pharmacy branches
-- ============================================================================
CREATE TABLE `PHARMACIST` (
    `Pharmacist_ID` INT NOT NULL,
    `Pharmacy_ID` INT NOT NULL,
    `Shift` VARCHAR(30) NOT NULL,
    `Name` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`Pharmacist_ID`),
    CONSTRAINT `fk_pharmacist_pharmacy` FOREIGN KEY (`Pharmacy_ID`) 
        REFERENCES `PHARMACY` (`Pharmacy_ID`) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `chk_pharmacist_shift` CHECK (`Shift` IN ('Morning', 'Evening', 'Night', 'General'))
) ENGINE=InnoDB;

-- ============================================================================
-- 12. MANUFACTURER
-- Pharmaceutical manufacturing corporations producing brand-name medicines
-- ============================================================================
CREATE TABLE `MANUFACTURER` (
    `Manufacturer_ID` INT NOT NULL,
    `Brand_Name` VARCHAR(100) NOT NULL,
    `City` VARCHAR(80) NOT NULL,
    `State` VARCHAR(80) NOT NULL,
    `Street` VARCHAR(150) NOT NULL,
    PRIMARY KEY (`Manufacturer_ID`)
) ENGINE=InnoDB;

-- ============================================================================
-- 13. SUPPLIER
-- Logistics and distribution agencies supplying pharmaceutical products
-- ============================================================================
CREATE TABLE `SUPPLIER` (
    `Supplier_ID` INT NOT NULL,
    `Contact` VARCHAR(20) NOT NULL,
    `City` VARCHAR(80) NOT NULL,
    `State` VARCHAR(80) NOT NULL,
    `Street` VARCHAR(150) NOT NULL,
    `Name` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`Supplier_ID`)
) ENGINE=InnoDB;

-- ============================================================================
-- 14. SUPPLIER_MANUFACTURER
-- Associative entity modeling M:N relationship between Supplier and Manufacturer
-- ============================================================================
CREATE TABLE `SUPPLIER_MANUFACTURER` (
    `Supplier_ID` INT NOT NULL,
    `Manufacturer_ID` INT NOT NULL,
    PRIMARY KEY (`Supplier_ID`, `Manufacturer_ID`),
    CONSTRAINT `fk_suppmfg_supplier` FOREIGN KEY (`Supplier_ID`) 
        REFERENCES `SUPPLIER` (`Supplier_ID`) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_suppmfg_mfg` FOREIGN KEY (`Manufacturer_ID`) 
        REFERENCES `MANUFACTURER` (`Manufacturer_ID`) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ============================================================================
-- 15. WHOLESALE_SUPPLIER
-- Registered wholesale entities with GST identification
-- ============================================================================
CREATE TABLE `WHOLESALE_SUPPLIER` (
    `GST_No` VARCHAR(20) NOT NULL,
    `City` VARCHAR(80) NOT NULL,
    `State` VARCHAR(80) NOT NULL,
    `Street` VARCHAR(150) NOT NULL,
    PRIMARY KEY (`GST_No`)
) ENGINE=InnoDB;

-- ============================================================================
-- 16. SUPPLIER_WHOLESALE
-- Associative entity modeling M:N relationship between Supplier and Wholesale Supplier
-- ============================================================================
CREATE TABLE `SUPPLIER_WHOLESALE` (
    `Supplier_ID` INT NOT NULL,
    `GST_No` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`Supplier_ID`, `GST_No`),
    CONSTRAINT `fk_suppws_supplier` FOREIGN KEY (`Supplier_ID`) 
        REFERENCES `SUPPLIER` (`Supplier_ID`) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_suppws_wholesale` FOREIGN KEY (`GST_No`) 
        REFERENCES `WHOLESALE_SUPPLIER` (`GST_No`) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ============================================================================
-- 17. SUPPLIER_PHARMACY
-- Associative entity modeling M:N relationship between Supplier and Pharmacy
-- ============================================================================
CREATE TABLE `SUPPLIER_PHARMACY` (
    `Supplier_ID` INT NOT NULL,
    `Pharmacy_ID` INT NOT NULL,
    PRIMARY KEY (`Supplier_ID`, `Pharmacy_ID`),
    CONSTRAINT `fk_supppharm_supplier` FOREIGN KEY (`Supplier_ID`) 
        REFERENCES `SUPPLIER` (`Supplier_ID`) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_supppharm_pharmacy` FOREIGN KEY (`Pharmacy_ID`) 
        REFERENCES `PHARMACY` (`Pharmacy_ID`) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ============================================================================
-- 18. ORDER (Procurement Purchase Order)
-- Bulk procurement transactions placed by Pharmacies to Suppliers
-- Escaped with backticks as `ORDER` is an ANSI SQL reserved keyword
-- ============================================================================
CREATE TABLE `ORDER` (
    `Order_ID` INT NOT NULL,
    `Supplier_ID` INT NOT NULL,
    `Arrival_Date` DATE DEFAULT NULL,
    `Payment_Status` VARCHAR(30) NOT NULL,
    `Date` DATE NOT NULL,
    `Order_Status` VARCHAR(30) NOT NULL,
    `Pharmacy_ID` INT NOT NULL,
    `Quantity_Ordered` INT NOT NULL,
    PRIMARY KEY (`Order_ID`),
    CONSTRAINT `fk_order_supplier` FOREIGN KEY (`Supplier_ID`) 
        REFERENCES `SUPPLIER` (`Supplier_ID`) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_order_pharmacy` FOREIGN KEY (`Pharmacy_ID`) 
        REFERENCES `PHARMACY` (`Pharmacy_ID`) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `chk_order_qty` CHECK (`Quantity_Ordered` > 0),
    CONSTRAINT `chk_order_pay_status` CHECK (`Payment_Status` IN ('Pending', 'Paid', 'Partial', 'Refunded')),
    CONSTRAINT `chk_order_status` CHECK (`Order_Status` IN ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'))
) ENGINE=InnoDB;

-- ============================================================================
-- 19. INVENTORY (Implementation-Support Entity)
-- Tracks stock quantity on hand and threshold levels per pharmacy & medicine
-- Academic Justification: Essential for operational inventory tracking in DA2
-- ============================================================================
CREATE TABLE `INVENTORY` (
    `Inventory_ID` INT NOT NULL AUTO_INCREMENT,
    `Pharmacy_ID` INT NOT NULL,
    `Medicine_ID` INT NOT NULL,
    `Quantity` INT NOT NULL DEFAULT 0,
    `Reorder_Level` INT NOT NULL DEFAULT 15,
    `Last_Updated` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`Inventory_ID`),
    UNIQUE KEY `uk_pharmacy_medicine` (`Pharmacy_ID`, `Medicine_ID`),
    CONSTRAINT `fk_inv_pharmacy` FOREIGN KEY (`Pharmacy_ID`) 
        REFERENCES `PHARMACY` (`Pharmacy_ID`) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_inv_medicine` FOREIGN KEY (`Medicine_ID`) 
        REFERENCES `MEDICINE` (`Medicine_ID`) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `chk_inv_qty` CHECK (`Quantity` >= 0),
    CONSTRAINT `chk_inv_reorder` CHECK (`Reorder_Level` >= 0)
) ENGINE=InnoDB;

-- ============================================================================
-- 20. STOCK_LOG (Implementation-Support Entity)
-- Immutable audit log recording all stock delta movements (restock, dispensing)
-- Academic Justification: Essential for trigger verification and auditing in DA2
-- ============================================================================
CREATE TABLE `STOCK_LOG` (
    `Log_ID` INT NOT NULL AUTO_INCREMENT,
    `Pharmacy_ID` INT NOT NULL,
    `Medicine_ID` INT NOT NULL,
    `Quantity_Change` INT NOT NULL,
    `Change_Type` VARCHAR(30) NOT NULL,
    `Change_Date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `Reference_ID` VARCHAR(50) DEFAULT NULL,
    PRIMARY KEY (`Log_ID`),
    CONSTRAINT `fk_log_pharmacy` FOREIGN KEY (`Pharmacy_ID`) 
        REFERENCES `PHARMACY` (`Pharmacy_ID`) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_log_medicine` FOREIGN KEY (`Medicine_ID`) 
        REFERENCES `MEDICINE` (`Medicine_ID`) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `chk_log_type` CHECK (`Change_Type` IN ('RESTOCK', 'DISPENSE', 'DAMAGE', 'RETURN', 'CORRECTION'))
) ENGINE=InnoDB;

-- ============================================================================
-- PERFORMANCE & OPERATIONAL INDEXES
-- Index frequently queried columns for joins, searches, and range filters
-- ============================================================================
CREATE INDEX `idx_patient_name` ON `PATIENT` (`Last_Name`, `First_Name`);
CREATE INDEX `idx_doctor_hospital` ON `DOCTOR` (`Hospital_ID`);
CREATE INDEX `idx_prescription_date` ON `PRESCRIPTION` (`Date`);
CREATE INDEX `idx_prescitem_presc` ON `PRESCRIPTION_ITEM` (`Prescription_ID`);
CREATE INDEX `idx_prescitem_med` ON `PRESCRIPTION_ITEM` (`Medicine_ID`);
CREATE INDEX `idx_medicine_name` ON `MEDICINE` (`Name`);
CREATE INDEX `idx_medicine_exp` ON `MEDICINE` (`Exp_Date`);
CREATE INDEX `idx_order_status` ON `ORDER` (`Order_Status`, `Payment_Status`);
CREATE INDEX `idx_bill_patient` ON `BILL` (`Patient_ID`);
CREATE INDEX `idx_inv_stock` ON `INVENTORY` (`Quantity`, `Reorder_Level`);
CREATE INDEX `idx_stocklog_date` ON `STOCK_LOG` (`Change_Date`);
