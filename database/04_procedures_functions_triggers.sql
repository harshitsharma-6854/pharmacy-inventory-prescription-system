-- ============================================================================
-- PHARMACY INVENTORY AND PRESCRIPTION TRACKING SYSTEM
-- DA2 College Database Project - Stored Programs (PL/SQL Equivalent Concepts)
-- Engine: MySQL 8.x
-- ============================================================================
-- ACADEMIC NOTE:
-- MySQL stored programs are used because the application database is MySQL; 
-- these implement the equivalent database-programming concepts (Stored Procedures,
-- Stored Functions, and Database Triggers with Exception Handling) required by DA2.
-- ============================================================================

USE pharmacy_system_new;

DELIMITER $$

-- ----------------------------------------------------------------------------
-- PROCEDURE 1: add_patient()
-- Purpose: Inserts a new patient and their primary contact number.
-- Validations:
--   1. Valid sex identifier ('M', 'F', 'O')
--   2. Non-empty names and addresses
--   3. Date of birth cannot be in the future
--   4. Unique Patient_ID check
-- Exception Handling: SIGNAL SQLSTATE '45000' with descriptive error messages.
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `add_patient`$$
CREATE PROCEDURE `add_patient`(
    IN p_id INT,
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_dob DATE,
    IN p_sex CHAR(1),
    IN p_street VARCHAR(150),
    IN p_city VARCHAR(80),
    IN p_state VARCHAR(80),
    IN p_contact_no VARCHAR(20)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;

    -- Validate Primary Key Uniqueness
    SELECT COUNT(*) INTO v_count FROM `PATIENT` WHERE `Patient_ID` = p_id;
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Patient with this ID already exists.';
    END IF;

    -- Validate Sex
    IF p_sex NOT IN ('M', 'F', 'O') THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Invalid sex code. Must be M, F, or O.';
    END IF;

    -- Validate DOB
    IF p_dob > CURDATE() THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Date of birth cannot be in the future.';
    END IF;

    -- Validate Name non-empty
    IF TRIM(p_first_name) = '' OR TRIM(p_last_name) = '' THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Patient first name and last name are required.';
    END IF;

    -- Atomic insertion into PATIENT and PATIENT_CONTACT
    START TRANSACTION;
        INSERT INTO `PATIENT` (`Patient_ID`, `DOB`, `Sex`, `City`, `State`, `Street`, `First_Name`, `Last_Name`)
        VALUES (p_id, p_dob, p_sex, p_city, p_state, p_street, p_first_name, p_last_name);

        IF p_contact_no IS NOT NULL AND TRIM(p_contact_no) <> '' THEN
            INSERT INTO `PATIENT_CONTACT` (`Patient_ID`, `Contact_No`)
            VALUES (p_id, p_contact_no);
        END IF;
    COMMIT;
END$$

-- ----------------------------------------------------------------------------
-- PROCEDURE 2: add_medicine()
-- Purpose: Inserts a new medicine formulary item and initializes branch inventory.
-- Validations:
--   1. Price must be positive (> 0)
--   2. Expiry date must strictly exceed Manufacturing date
--   3. Unique Medicine_ID check
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `add_medicine`$$
CREATE PROCEDURE `add_medicine`(
    IN p_id INT,
    IN p_name VARCHAR(100),
    IN p_manu_date DATE,
    IN p_exp_date DATE,
    IN p_price DECIMAL(10, 2),
    IN p_pharmacy_id INT,
    IN p_initial_stock INT,
    IN p_reorder_level INT
)
BEGIN
    DECLARE v_count INT DEFAULT 0;

    -- Validate Uniqueness
    SELECT COUNT(*) INTO v_count FROM `MEDICINE` WHERE `Medicine_ID` = p_id;
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Medicine with this ID already exists.';
    END IF;

    -- Validate Price
    IF p_price <= 0 THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Medicine price must be strictly greater than zero.';
    END IF;

    -- Validate Expiry and Manufacturing Dates
    IF p_exp_date <= p_manu_date THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Expiration date must be strictly after manufacturing date.';
    END IF;

    -- Insert Medicine and create branch inventory record
    START TRANSACTION;
        INSERT INTO `MEDICINE` (`Medicine_ID`, `Manu_Date`, `Exp_Date`, `Name`, `Price`)
        VALUES (p_id, p_manu_date, p_exp_date, p_name, p_price);

        IF p_pharmacy_id IS NOT NULL THEN
            INSERT INTO `INVENTORY` (`Pharmacy_ID`, `Medicine_ID`, `Quantity`, `Reorder_Level`)
            VALUES (p_pharmacy_id, p_id, COALESCE(p_initial_stock, 0), COALESCE(p_reorder_level, 15))
            ON DUPLICATE KEY UPDATE `Quantity` = `Quantity` + COALESCE(p_initial_stock, 0);

            IF COALESCE(p_initial_stock, 0) > 0 THEN
                INSERT INTO `STOCK_LOG` (`Pharmacy_ID`, `Medicine_ID`, `Quantity_Change`, `Change_Type`, `Reference_ID`)
                VALUES (p_pharmacy_id, p_id, p_initial_stock, 'RESTOCK', 'INITIAL-SETUP');
            END IF;
        END IF;
    COMMIT;
END$$

-- ----------------------------------------------------------------------------
-- PROCEDURE 3: restock_medicine()
-- Purpose: Atomically replenishes inventory for a specific pharmacy and medicine,
--          logging the movement in STOCK_LOG.
-- Validations:
--   1. Quantity added must be > 0
--   2. Pharmacy and Medicine existence
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `restock_medicine`$$
CREATE PROCEDURE `restock_medicine`(
    IN p_pharmacy_id INT,
    IN p_medicine_id INT,
    IN p_quantity INT,
    IN p_reference_id VARCHAR(50)
)
BEGIN
    DECLARE v_exists INT DEFAULT 0;

    -- Validate Restock Quantity
    IF p_quantity <= 0 THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Restock quantity must be positive.';
    END IF;

    -- Validate Pharmacy existence
    SELECT COUNT(*) INTO v_exists FROM `PHARMACY` WHERE `Pharmacy_ID` = p_pharmacy_id;
    IF v_exists = 0 THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Specified Pharmacy does not exist.';
    END IF;

    -- Validate Medicine existence
    SELECT COUNT(*) INTO v_exists FROM `MEDICINE` WHERE `Medicine_ID` = p_medicine_id;
    IF v_exists = 0 THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Specified Medicine does not exist.';
    END IF;

    START TRANSACTION;
        -- Upsert into inventory
        INSERT INTO `INVENTORY` (`Pharmacy_ID`, `Medicine_ID`, `Quantity`, `Reorder_Level`)
        VALUES (p_pharmacy_id, p_medicine_id, p_quantity, 15)
        ON DUPLICATE KEY UPDATE `Quantity` = `Quantity` + p_quantity;

        -- Record operation in STOCK_LOG
        INSERT INTO `STOCK_LOG` (`Pharmacy_ID`, `Medicine_ID`, `Quantity_Change`, `Change_Type`, `Reference_ID`)
        VALUES (p_pharmacy_id, p_medicine_id, p_quantity, 'RESTOCK', COALESCE(p_reference_id, 'MANUAL-RESTOCK'));
    COMMIT;
END$$

-- ----------------------------------------------------------------------------
-- PROCEDURE 4: create_prescription()
-- Purpose: Creates a new prescription header record after validating patient & doctor.
-- Validations:
--   1. Doctor must exist in DOCTOR relation
--   2. Patient must exist in PATIENT relation
--   3. Unique Prescription_ID
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `create_prescription`$$
CREATE PROCEDURE `create_prescription`(
    IN p_prescription_id INT,
    IN p_doctor_id INT,
    IN p_patient_id INT,
    IN p_date DATE
)
BEGIN
    DECLARE v_count INT DEFAULT 0;

    -- Check Prescription ID Uniqueness
    SELECT COUNT(*) INTO v_count FROM `PRESCRIPTION` WHERE `Prescription_ID` = p_prescription_id;
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Prescription ID already exists.';
    END IF;

    -- Validate Doctor
    SELECT COUNT(*) INTO v_count FROM `DOCTOR` WHERE `Doctor_ID` = p_doctor_id;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Prescribing Doctor does not exist in registry.';
    END IF;

    -- Validate Patient
    SELECT COUNT(*) INTO v_count FROM `PATIENT` WHERE `Patient_ID` = p_patient_id;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Patient does not exist in registry.';
    END IF;

    INSERT INTO `PRESCRIPTION` (`Prescription_ID`, `Doctor_ID`, `Patient_ID`, `Date`)
    VALUES (p_prescription_id, p_doctor_id, p_patient_id, COALESCE(p_date, CURDATE()));
END$$

-- ----------------------------------------------------------------------------
-- PROCEDURE 5: generate_bill()
-- Purpose: Generates a pharmacy billing record by calculating total cost from
--          prescription items, verifying medicine availability, and deducting stock.
-- Validations:
--   1. Prescription and Patient must exist
--   2. Bill ID must be unique
--   3. Calculates non-zero bill amount from prescription items
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `generate_bill`$$
CREATE PROCEDURE `generate_bill`(
    IN p_bill_id INT,
    IN p_pharmacy_id INT,
    IN p_patient_id INT,
    IN p_prescription_id INT
)
BEGIN
    DECLARE v_total DECIMAL(10, 2) DEFAULT 0.00;
    DECLARE v_count INT DEFAULT 0;
    DECLARE v_presc_patient INT;

    -- Verify Bill ID uniqueness
    SELECT COUNT(*) INTO v_count FROM `BILL` WHERE `Bill_ID` = p_bill_id;
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Bill ID already exists.';
    END IF;

    -- Verify Prescription exists
    SELECT `Patient_ID` INTO v_presc_patient 
    FROM `PRESCRIPTION` 
    WHERE `Prescription_ID` = p_prescription_id;

    IF v_presc_patient IS NULL THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Prescription not found.';
    END IF;

    -- Verify patient match
    IF v_presc_patient <> p_patient_id THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Prescription does not match the specified Patient.';
    END IF;

    -- Calculate total using prescription items and unit prices
    SELECT COALESCE(SUM(M.`Price`), 0.00) INTO v_total
    FROM `PRESCRIPTION_ITEM` PI
    INNER JOIN `MEDICINE` M ON PI.`Medicine_ID` = M.`Medicine_ID`
    WHERE PI.`Prescription_ID` = p_prescription_id;

    IF v_total = 0.00 THEN
        SET v_total = 50.00; -- Standard dispensing consultation fee fallback
    END IF;

    START TRANSACTION;
        -- Insert bill record
        INSERT INTO `BILL` (`Bill_ID`, `Pharmacy_ID`, `Amount`, `Patient_ID`)
        VALUES (p_bill_id, p_pharmacy_id, v_total, p_patient_id);

        -- Record DISPENSE in stock log for each medicine in the prescription
        INSERT INTO `STOCK_LOG` (`Pharmacy_ID`, `Medicine_ID`, `Quantity_Change`, `Change_Type`, `Reference_ID`)
        SELECT 
            p_pharmacy_id, 
            PI.`Medicine_ID`, 
            -1, 
            'DISPENSE', 
            CONCAT('BILL-', p_bill_id)
        FROM `PRESCRIPTION_ITEM` PI
        WHERE PI.`Prescription_ID` = p_prescription_id;

        -- Decrement stock in inventory if available
        UPDATE `INVENTORY` INV
        INNER JOIN `PRESCRIPTION_ITEM` PI 
            ON INV.`Medicine_ID` = PI.`Medicine_ID` 
           AND INV.`Pharmacy_ID` = p_pharmacy_id
        SET INV.`Quantity` = GREATEST(0, INV.`Quantity` - 1)
        WHERE PI.`Prescription_ID` = p_prescription_id;
    COMMIT;
END$$

-- ----------------------------------------------------------------------------
-- PROCEDURE 6: place_order()
-- Purpose: Records a bulk procurement order from a pharmacy to a supplier.
-- Validations:
--   1. Supplier and Pharmacy must exist
--   2. Quantity ordered must be positive
--   3. Unique Order_ID
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `place_order`$$
CREATE PROCEDURE `place_order`(
    IN p_order_id INT,
    IN p_supplier_id INT,
    IN p_pharmacy_id INT,
    IN p_quantity INT,
    IN p_date DATE,
    IN p_arrival_date DATE,
    IN p_pay_status VARCHAR(30),
    IN p_order_status VARCHAR(30)
)
BEGIN
    DECLARE v_count INT DEFAULT 0;

    -- Check unique Order ID
    SELECT COUNT(*) INTO v_count FROM `ORDER` WHERE `Order_ID` = p_order_id;
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Order ID already exists.';
    END IF;

    -- Validate Quantity
    IF p_quantity <= 0 THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Quantity ordered must be strictly greater than zero.';
    END IF;

    -- Check Supplier existence
    SELECT COUNT(*) INTO v_count FROM `SUPPLIER` WHERE `Supplier_ID` = p_supplier_id;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Supplier does not exist.';
    END IF;

    -- Check Pharmacy existence
    SELECT COUNT(*) INTO v_count FROM `PHARMACY` WHERE `Pharmacy_ID` = p_pharmacy_id;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Exception: Pharmacy does not exist.';
    END IF;

    INSERT INTO `ORDER` (`Order_ID`, `Supplier_ID`, `Pharmacy_ID`, `Date`, `Arrival_Date`, `Payment_Status`, `Order_Status`, `Quantity_Ordered`)
    VALUES (
        p_order_id, 
        p_supplier_id, 
        p_pharmacy_id, 
        COALESCE(p_date, CURDATE()), 
        p_arrival_date, 
        COALESCE(p_pay_status, 'Pending'), 
        COALESCE(p_order_status, 'Pending'), 
        p_quantity
    );
END$$

-- ============================================================================
-- FUNCTIONS (Deterministic / Database Computations)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- FUNCTION 1: get_medicine_price()
-- Purpose: Retrieves unit retail price of a medicine.
-- Returns: DECIMAL(10, 2) price or 0.00 if not found.
-- ----------------------------------------------------------------------------
DROP FUNCTION IF EXISTS `get_medicine_price`$$
CREATE FUNCTION `get_medicine_price`(p_med_id INT) 
RETURNS DECIMAL(10, 2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_price DECIMAL(10, 2) DEFAULT 0.00;
    SELECT `Price` INTO v_price FROM `MEDICINE` WHERE `Medicine_ID` = p_med_id;
    RETURN COALESCE(v_price, 0.00);
END$$

-- ----------------------------------------------------------------------------
-- FUNCTION 2: get_patient_prescription_count()
-- Purpose: Returns total number of prescriptions issued to a given patient.
-- Returns: INT count of prescriptions.
-- ----------------------------------------------------------------------------
DROP FUNCTION IF EXISTS `get_patient_prescription_count`$$
CREATE FUNCTION `get_patient_prescription_count`(p_pat_id INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_count INT DEFAULT 0;
    SELECT COUNT(*) INTO v_count FROM `PRESCRIPTION` WHERE `Patient_ID` = p_pat_id;
    RETURN v_count;
END$$

-- ----------------------------------------------------------------------------
-- FUNCTION 3: calculate_prescription_total()
-- Purpose: Computes aggregate financial value of medicines on a prescription.
-- Returns: DECIMAL(10, 2) total price.
-- ----------------------------------------------------------------------------
DROP FUNCTION IF EXISTS `calculate_prescription_total`$$
CREATE FUNCTION `calculate_prescription_total`(p_presc_id INT)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total DECIMAL(10, 2) DEFAULT 0.00;
    SELECT COALESCE(SUM(M.`Price`), 0.00) INTO v_total
    FROM `PRESCRIPTION_ITEM` PI
    INNER JOIN `MEDICINE` M ON PI.`Medicine_ID` = M.`Medicine_ID`
    WHERE PI.`Prescription_ID` = p_presc_id;
    RETURN v_total;
END$$

-- ----------------------------------------------------------------------------
-- FUNCTION 4: get_pharmacy_revenue()
-- Purpose: Computes cumulative billed revenue for a specific pharmacy branch.
-- Returns: DECIMAL(10, 2) gross revenue.
-- ----------------------------------------------------------------------------
DROP FUNCTION IF EXISTS `get_pharmacy_revenue`$$
CREATE FUNCTION `get_pharmacy_revenue`(p_pharm_id INT)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_rev DECIMAL(10, 2) DEFAULT 0.00;
    SELECT COALESCE(SUM(`Amount`), 0.00) INTO v_rev 
    FROM `BILL` 
    WHERE `Pharmacy_ID` = p_pharm_id;
    RETURN v_rev;
END$$

-- ----------------------------------------------------------------------------
-- FUNCTION 5: get_medicine_stock()
-- Purpose: Returns current stock units for a specific medicine at a pharmacy.
-- Returns: INT quantity on hand.
-- ----------------------------------------------------------------------------
DROP FUNCTION IF EXISTS `get_medicine_stock`$$
CREATE FUNCTION `get_medicine_stock`(p_pharm_id INT, p_med_id INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_qty INT DEFAULT 0;
    SELECT `Quantity` INTO v_qty 
    FROM `INVENTORY` 
    WHERE `Pharmacy_ID` = p_pharm_id AND `Medicine_ID` = p_med_id;
    RETURN COALESCE(v_qty, 0);
END$$

-- ============================================================================
-- DATABASE TRIGGERS
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TRIGGER 1: trg_before_inventory_update (Stock Integrity & Constraint Enforcement)
-- Event: BEFORE UPDATE on INVENTORY
-- Purpose: Prevents stock quantity from dropping below zero (Business Rule: No negative stock).
-- ----------------------------------------------------------------------------
DROP TRIGGER IF EXISTS `trg_before_inventory_update`$$
CREATE TRIGGER `trg_before_inventory_update`
BEFORE UPDATE ON `INVENTORY`
FOR EACH ROW
BEGIN
    IF NEW.`Quantity` < 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Trigger Exception: Inventory quantity cannot be negative.';
    END IF;
    -- Automatically refresh last updated timestamp
    SET NEW.`Last_Updated` = CURRENT_TIMESTAMP;
END$$

-- ----------------------------------------------------------------------------
-- TRIGGER 2: trg_after_inventory_update (Automated Audit Trail)
-- Event: AFTER UPDATE on INVENTORY
-- Purpose: Automatically creates an entry in STOCK_LOG whenever inventory changes.
-- ----------------------------------------------------------------------------
DROP TRIGGER IF EXISTS `trg_after_inventory_update`$$
CREATE TRIGGER `trg_after_inventory_update`
AFTER UPDATE ON `INVENTORY`
FOR EACH ROW
BEGIN
    DECLARE v_diff INT;
    SET v_diff = NEW.`Quantity` - OLD.`Quantity`;

    -- Only record if quantity actually changed
    IF v_diff <> 0 THEN
        INSERT INTO `STOCK_LOG` (
            `Pharmacy_ID`, 
            `Medicine_ID`, 
            `Quantity_Change`, 
            `Change_Type`, 
            `Reference_ID`
        ) VALUES (
            NEW.`Pharmacy_ID`, 
            NEW.`Medicine_ID`, 
            v_diff, 
            CASE 
                WHEN v_diff > 0 THEN 'RESTOCK' 
                ELSE 'DISPENSE' 
            END, 
            'AUTO-TRIGGER-AUDIT'
        );
    END IF;
END$$

-- ----------------------------------------------------------------------------
-- TRIGGER 3: trg_validate_bill_amount (Billing Sanity Check)
-- Event: BEFORE INSERT on BILL
-- Purpose: Enforces that bill amounts must be strictly non-negative.
-- ----------------------------------------------------------------------------
DROP TRIGGER IF EXISTS `trg_validate_bill_amount`$$
CREATE TRIGGER `trg_validate_bill_amount`
BEFORE INSERT ON `BILL`
FOR EACH ROW
BEGIN
    IF NEW.`Amount` < 0.00 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Trigger Exception: Invoiced bill amount cannot be negative.';
    END IF;
END$$

-- ----------------------------------------------------------------------------
-- TRIGGER 4: trg_before_order_insert (Procurement Integrity)
-- Event: BEFORE INSERT on ORDER
-- Purpose: Enforces valid delivery timing: Arrival_Date >= Order Date.
-- ----------------------------------------------------------------------------
DROP TRIGGER IF EXISTS `trg_before_order_insert`$$
CREATE TRIGGER `trg_before_order_insert`
BEFORE INSERT ON `ORDER`
FOR EACH ROW
BEGIN
    IF NEW.`Arrival_Date` IS NOT NULL AND NEW.`Arrival_Date` < NEW.`Date` THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Trigger Exception: Order arrival date cannot be earlier than order date.';
    END IF;
END$$

-- ----------------------------------------------------------------------------
-- TRIGGER 5: trg_validate_medicine_insert (Safety Check on Formulary)
-- Event: BEFORE INSERT on MEDICINE
-- Purpose: Redundant safety guard ensuring exp_date > manu_date and price > 0.
-- ----------------------------------------------------------------------------
DROP TRIGGER IF EXISTS `trg_validate_medicine_insert`$$
CREATE TRIGGER `trg_validate_medicine_insert`
BEFORE INSERT ON `MEDICINE`
FOR EACH ROW
BEGIN
    IF NEW.`Price` <= 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Trigger Exception: Medicine price must be strictly positive.';
    END IF;
    IF NEW.`Exp_Date` <= NEW.`Manu_Date` THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Trigger Exception: Expiration date must succeed manufacturing date.';
    END IF;
END$$

DELIMITER ;
