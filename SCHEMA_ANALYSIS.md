# SCHEMA ANALYSIS: PHARMACY INVENTORY AND PRESCRIPTION TRACKING SYSTEM
## Academic Database Design Analysis (DA1 to DA2 Reconstruction)

---

### Executive Summary

This document serves as the formal **Source of Truth and Relational Reconstruction** for the **Pharmacy Inventory and Prescription Tracking System (DA2)** based upon the approved **DA1 Conceptual (ER) and Logical (Relational Mapping)** artifacts.

The database design strictly preserves the 17 entities and associative structures established during DA1, while rigorously documenting the normalization status, primary/foreign/composite keys, cardinality constraints, multi-valued representations, and academically justified implementation-support tables required for operational inventory tracking.

---

### 1. Complete Entity & Attribute Specification

| # | Entity Name | Attributes (DA1 Mapping) | Data Type (MySQL 8.x) | Nullability / Constraints | Key Classification |
|---|---|---|---|---|---|
| **1** | **PHARMACY** | `Pharmacy_ID` | `INT` | `NOT NULL` | **Primary Key (PK)** |
| | | `Name` | `VARCHAR(100)` | `NOT NULL` | - |
| | | `Rating` | `DECIMAL(2,1)` | `DEFAULT 5.0, CHECK (Rating >= 1.0 AND Rating <= 5.0)` | - |
| | | `Street` | `VARCHAR(150)` | `NOT NULL` | Composite component of Address |
| | | `City` | `VARCHAR(80)` | `NOT NULL` | Composite component of Address |
| | | `State` | `VARCHAR(80)` | `NOT NULL` | Composite component of Address |
| | | `Contact_No` | `VARCHAR(20)` | `NOT NULL` | Primary Phone / Landline |
| **2** | **PHARMACY_CONTACT** | `Pharmacy_ID` | `INT` | `NOT NULL, FK -> PHARMACY(Pharmacy_ID)` | **Composite PK / FK** |
| | *(Multi-valued resolution)* | `Contact_No` | `VARCHAR(20)` | `NOT NULL` | **Composite PK** |
| **3** | **PATIENT** | `Patient_ID` | `INT` | `NOT NULL` | **Primary Key (PK)** |
| | | `First_Name` | `VARCHAR(50)` | `NOT NULL` | Composite component of Name |
| | | `Last_Name` | `VARCHAR(50)` | `NOT NULL` | Composite component of Name |
| | | `DOB` | `DATE` | `NOT NULL` | Date of Birth |
| | | `Sex` | `CHAR(1)` | `NOT NULL, CHECK (Sex IN ('M','F','O'))` | Biological sex |
| | | `Street` | `VARCHAR(150)` | `NOT NULL` | Composite component of Address |
| | | `City` | `VARCHAR(80)` | `NOT NULL` | Composite component of Address |
| | | `State` | `VARCHAR(80)` | `NOT NULL` | Composite component of Address |
| **4** | **PATIENT_CONTACT** | `Patient_ID` | `INT` | `NOT NULL, FK -> PATIENT(Patient_ID)` | **Composite PK / FK** |
| | *(Multi-valued Contact)* | `Contact_No` | `VARCHAR(20)` | `NOT NULL` | **Composite PK** |
| **5** | **HOSPITAL** | `Hospital_ID` | `INT` | `NOT NULL` | **Primary Key (PK)** |
| | | `Pharmacy_ID` | `INT` | `NOT NULL, FK -> PHARMACY(Pharmacy_ID)` | **Foreign Key (FK)** |
| | | `Name` | `VARCHAR(120)` | `NOT NULL` | Hospital Name |
| | | `Street` | `VARCHAR(150)` | `NOT NULL` | Composite Address |
| | | `City` | `VARCHAR(80)` | `NOT NULL` | Composite Address |
| | | `State` | `VARCHAR(80)` | `NOT NULL` | Composite Address |
| | | `Contact` | `VARCHAR(20)` | `NOT NULL` | Official Contact Number |
| **6** | **DOCTOR** | `Doctor_ID` | `INT` | `NOT NULL` | **Primary Key (PK)** |
| | | `Hospital_ID` | `INT` | `NOT NULL, FK -> HOSPITAL(Hospital_ID)` | **Foreign Key (FK)** |
| | | `First_Name` | `VARCHAR(50)` | `NOT NULL` | Doctor First Name |
| | | `Last_Name` | `VARCHAR(50)` | `NOT NULL` | Doctor Last Name |
| | | `Qualification` | `VARCHAR(100)` | `NOT NULL` | Medical Degree (MBBS, MD, MS) |
| | | `Experience` | `INT` | `NOT NULL, CHECK (Experience >= 0)` | Years of Practice |
| | | `Contact_No` | `VARCHAR(20)` | `NOT NULL` | Doctor Phone |
| **7** | **PRESCRIPTION** | `Prescription_ID` | `INT` | `NOT NULL` | **Primary Key (PK)** |
| | | `Doctor_ID` | `INT` | `NOT NULL, FK -> DOCTOR(Doctor_ID)` | **Foreign Key (FK)** |
| | | `Patient_ID` | `INT` | `NOT NULL, FK -> PATIENT(Patient_ID)` | **Foreign Key (FK)** |
| | | `Date` | `DATE` | `NOT NULL` | Prescription Date |
| **8** | **MEDICINE** | `Medicine_ID` | `INT` | `NOT NULL` | **Primary Key (PK)** |
| | | `Name` | `VARCHAR(100)` | `NOT NULL` | Generic / Brand Name |
| | | `Manu_Date` | `DATE` | `NOT NULL` | Manufacturing Date |
| | | `Exp_Date` | `DATE` | `NOT NULL, CHECK (Exp_Date > Manu_Date)`| Expiry Date |
| | | `Price` | `DECIMAL(10,2)` | `NOT NULL, CHECK (Price > 0)` | Unit Selling Price (INR) |
| **9** | **PRESCRIPTION_ITEM** | `Item_ID` | `INT` | `NOT NULL AUTO_INCREMENT` | **Primary Key (PK)** |
| | *(M:N Junction Presc-Med)*| `Prescription_ID` | `INT` | `NOT NULL, FK -> PRESCRIPTION(Prescription_ID)` | **Foreign Key (FK)** |
| | | `Medicine_ID` | `INT` | `NOT NULL, FK -> MEDICINE(Medicine_ID)` | **Foreign Key (FK)** |
| | | `Dosage` | `VARCHAR(50)` | `NOT NULL` | e.g., 500mg, 10ml |
| | | `Frequency` | `VARCHAR(50)` | `NOT NULL` | e.g., Twice Daily (BD) |
| | | `Duration` | `VARCHAR(50)` | `NOT NULL` | e.g., 5 Days |
| **10**| **BILL** | `Bill_ID` | `INT` | `NOT NULL` | **Primary Key (PK)** |
| | | `Pharmacy_ID` | `INT` | `NOT NULL, FK -> PHARMACY(Pharmacy_ID)` | **Foreign Key (FK)** |
| | | `Patient_ID` | `INT` | `NOT NULL, FK -> PATIENT(Patient_ID)` | **Foreign Key (FK)** |
| | | `Amount` | `DECIMAL(10,2)` | `NOT NULL, CHECK (Amount >= 0)` | Total Invoiced Amount |
| **11**| **PHARMACIST** | `Pharmacist_ID` | `INT` | `NOT NULL` | **Primary Key (PK)** |
| | | `Pharmacy_ID` | `INT` | `NOT NULL, FK -> PHARMACY(Pharmacy_ID)` | **Foreign Key (FK)** |
| | | `Name` | `VARCHAR(100)` | `NOT NULL` | Pharmacist Full Name |
| | | `Shift` | `VARCHAR(30)` | `NOT NULL, CHECK (Shift IN ('Morning','Evening','Night','General'))` | Assigned Work Shift |
| **12**| **MANUFACTURER** | `Manufacturer_ID` | `INT` | `NOT NULL` | **Primary Key (PK)** |
| | | `Brand_Name` | `VARCHAR(100)` | `NOT NULL` | Company / Brand Name |
| | | `Street` | `VARCHAR(150)` | `NOT NULL` | Composite Address |
| | | `City` | `VARCHAR(80)` | `NOT NULL` | Composite Address |
| | | `State` | `VARCHAR(80)` | `NOT NULL` | Composite Address |
| **13**| **SUPPLIER** | `Supplier_ID` | `INT` | `NOT NULL` | **Primary Key (PK)** |
| | | `Name` | `VARCHAR(100)` | `NOT NULL` | Supplier Agency Name |
| | | `Contact` | `VARCHAR(20)` | `NOT NULL` | Supplier Phone Number |
| | | `Street` | `VARCHAR(150)` | `NOT NULL` | Composite Address |
| | | `City` | `VARCHAR(80)` | `NOT NULL` | Composite Address |
| | | `State` | `VARCHAR(80)` | `NOT NULL` | Composite Address |
| **14**| **SUPPLIER_MANUFACTURER**| `Supplier_ID` | `INT` | `NOT NULL, FK -> SUPPLIER(Supplier_ID)` | **Composite PK / FK** |
| | *(M:N Junction)* | `Manufacturer_ID` | `INT` | `NOT NULL, FK -> MANUFACTURER(Manufacturer_ID)`| **Composite PK / FK** |
| **15**| **WHOLESALE_SUPPLIER** | `GST_No` | `VARCHAR(20)` | `NOT NULL` | **Primary Key (PK)** |
| | | `Street` | `VARCHAR(150)` | `NOT NULL` | Composite Address |
| | | `City` | `VARCHAR(80)` | `NOT NULL` | Composite Address |
| | | `State` | `VARCHAR(80)` | `NOT NULL` | Composite Address |
| **16**| **SUPPLIER_WHOLESALE** | `Supplier_ID` | `INT` | `NOT NULL, FK -> SUPPLIER(Supplier_ID)` | **Composite PK / FK** |
| | *(M:N Junction)* | `GST_No` | `VARCHAR(20)` | `NOT NULL, FK -> WHOLESALE_SUPPLIER(GST_No)` | **Composite PK / FK** |
| **17**| **SUPPLIER_PHARMACY** | `Supplier_ID` | `INT` | `NOT NULL, FK -> SUPPLIER(Supplier_ID)` | **Composite PK / FK** |
| | *(M:N Junction)* | `Pharmacy_ID` | `INT` | `NOT NULL, FK -> PHARMACY(Pharmacy_ID)` | **Composite PK / FK** |
| **18**| **ORDER (Purchase Order)**| `Order_ID` | `INT` | `NOT NULL` | **Primary Key (PK)** |
| | | `Supplier_ID` | `INT` | `NOT NULL, FK -> SUPPLIER(Supplier_ID)` | **Foreign Key (FK)** |
| | | `Pharmacy_ID` | `INT` | `NOT NULL, FK -> PHARMACY(Pharmacy_ID)` | **Foreign Key (FK)** |
| | | `Date` | `DATE` | `NOT NULL` | Order Date |
| | | `Arrival_Date` | `DATE` | `DEFAULT NULL` | Delivery / Arrival Date |
| | | `Payment_Status`| `VARCHAR(30)` | `NOT NULL, CHECK (Payment_Status IN ('Pending','Paid','Partial','Refunded'))` | Payment State |
| | | `Order_Status` | `VARCHAR(30)` | `NOT NULL, CHECK (Order_Status IN ('Pending','Processing','Shipped','Delivered','Cancelled'))` | Fulfillment State |
| | | `Quantity_Ordered`| `INT` | `NOT NULL, CHECK (Quantity_Ordered > 0)` | Total Units Ordered |
| **19**| **INVENTORY** *(Support)* | `Inventory_ID` | `INT` | `NOT NULL AUTO_INCREMENT` | **Primary Key (PK)** |
| | *(Stock Tracking Support)* | `Pharmacy_ID` | `INT` | `NOT NULL, FK -> PHARMACY(Pharmacy_ID)` | **Foreign Key (FK)** |
| | | `Medicine_ID` | `INT` | `NOT NULL, FK -> MEDICINE(Medicine_ID)` | **Foreign Key (FK)** |
| | | `Quantity` | `INT` | `NOT NULL DEFAULT 0, CHECK (Quantity >= 0)`| Current In-stock Units |
| | | `Reorder_Level`| `INT` | `NOT NULL DEFAULT 15, CHECK (Reorder_Level >= 0)` | Threshold Trigger |
| | | `Last_Updated` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | Audit Timestamp |
| | | *Unique Constraint* | - | `UNIQUE KEY (Pharmacy_ID, Medicine_ID)` | Single Stock Row Per Drug |
| **20**| **STOCK_LOG** *(Support)*| `Log_ID` | `INT` | `NOT NULL AUTO_INCREMENT` | **Primary Key (PK)** |
| | *(Audit Log Support)* | `Pharmacy_ID` | `INT` | `NOT NULL, FK -> PHARMACY(Pharmacy_ID)` | **Foreign Key (FK)** |
| | | `Medicine_ID` | `INT` | `NOT NULL, FK -> MEDICINE(Medicine_ID)` | **Foreign Key (FK)** |
| | | `Quantity_Change` | `INT` | `NOT NULL` | +/- Deltas |
| | | `Change_Type` | `VARCHAR(30)` | `NOT NULL, CHECK (Change_Type IN ('RESTOCK','DISPENSE','DAMAGE','RETURN','CORRECTION'))` | Action Category |
| | | `Change_Date` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Mutation Timestamp |
| | | `Reference_ID` | `VARCHAR(50)` | `DEFAULT NULL` | Bill / Order / Dispense ID |

---

### 2. Primary, Foreign, and Composite Keys

#### A. Single Attribute Primary Keys
- `PHARMACY.Pharmacy_ID`
- `PATIENT.Patient_ID`
- `HOSPITAL.Hospital_ID`
- `DOCTOR.Doctor_ID`
- `PRESCRIPTION.Prescription_ID`
- `MEDICINE.Medicine_ID`
- `BILL.Bill_ID`
- `PHARMACIST.Pharmacist_ID`
- `MANUFACTURER.Manufacturer_ID`
- `SUPPLIER.Supplier_ID`
- `WHOLESALE_SUPPLIER.GST_No`
- `ORDER.Order_ID`
- `PRESCRIPTION_ITEM.Item_ID`
- `INVENTORY.Inventory_ID`
- `STOCK_LOG.Log_ID`

#### B. Composite Primary Keys
- `PATIENT_CONTACT`: `(Patient_ID, Contact_No)` — prevents duplicate contacts for the same patient while enforcing 1NF normalization for the multi-valued contact attribute.
- `PHARMACY_CONTACT`: `(Pharmacy_ID, Contact_No)` — accommodates multi-branch / multi-phone configurations.
- `SUPPLIER_MANUFACTURER`: `(Supplier_ID, Manufacturer_ID)` — models M:N distribution rights between suppliers and pharmaceutical manufacturers.
- `SUPPLIER_WHOLESALE`: `(Supplier_ID, GST_No)` — models M:N business links between suppliers and regional registered wholesale dealers.
- `SUPPLIER_PHARMACY`: `(Supplier_ID, Pharmacy_ID)` — models authorized supplier-to-pharmacy procurement channels.

#### C. Foreign Key Reference Mappings
- `HOSPITAL(Pharmacy_ID)` references `PHARMACY(Pharmacy_ID)`
- `DOCTOR(Hospital_ID)` references `HOSPITAL(Hospital_ID)`
- `PRESCRIPTION(Doctor_ID)` references `DOCTOR(Doctor_ID)`
- `PRESCRIPTION(Patient_ID)` references `PATIENT(Patient_ID)`
- `PRESCRIPTION_ITEM(Prescription_ID)` references `PRESCRIPTION(Prescription_ID)`
- `PRESCRIPTION_ITEM(Medicine_ID)` references `MEDICINE(Medicine_ID)`
- `BILL(Pharmacy_ID)` references `PHARMACY(Pharmacy_ID)`
- `BILL(Patient_ID)` references `PATIENT(Patient_ID)`
- `PHARMACIST(Pharmacy_ID)` references `PHARMACY(Pharmacy_ID)`
- `ORDER(Supplier_ID)` references `SUPPLIER(Supplier_ID)`
- `ORDER(Pharmacy_ID)` references `PHARMACY(Pharmacy_ID)`
- `INVENTORY(Pharmacy_ID)` references `PHARMACY(Pharmacy_ID)`
- `INVENTORY(Medicine_ID)` references `MEDICINE(Medicine_ID)`
- `STOCK_LOG(Pharmacy_ID)` references `PHARMACY(Pharmacy_ID)`
- `STOCK_LOG(Medicine_ID)` references `MEDICINE(Medicine_ID)`

---

### 3. Detailed Cardinality & Relationship Analysis

#### 1. `HOSPITAL` ↔ `PHARMACY` (1:N)
- A Pharmacy can service or be affiliated with multiple Hospitals (e.g., central health cluster supply).
- Each Hospital is associated with exactly one primary dispensing Pharmacy (`Pharmacy_ID` in `HOSPITAL`).

#### 2. `HOSPITAL` ↔ `DOCTOR` (1:N)
- A Hospital employs many Doctors.
- Each Doctor is formally affiliated with one Hospital (`Hospital_ID` in `DOCTOR`).

#### 3. `DOCTOR` ↔ `PRESCRIPTION` (1:N)
- A Doctor issues multiple Prescriptions over time.
- Each Prescription is authorized by exactly one Doctor (`Doctor_ID` in `PRESCRIPTION`).

#### 4. `PATIENT` ↔ `PRESCRIPTION` (1:N)
- A Patient receives multiple Prescriptions across treatments.
- Each Prescription belongs to exactly one Patient (`Patient_ID` in `PRESCRIPTION`).

#### 5. `PRESCRIPTION` ↔ `MEDICINE` (M:N)
- A Prescription specifies multiple Medicines with unique dosage regimens.
- A Medicine is prescribed across many Prescriptions.
- **Resolution**: Resolved via `PRESCRIPTION_ITEM` associative entity (`Item_ID`, `Prescription_ID`, `Medicine_ID`, `Dosage`, `Frequency`, `Duration`).

#### 6. `PHARMACY` ↔ `BILL` (1:N)
- A Pharmacy generates many Bills.
- Each Bill is recorded at a specific Pharmacy branch (`Pharmacy_ID` in `BILL`).

#### 7. `PATIENT` ↔ `BILL` (1:N)
- A Patient settles multiple Bills over different transactions.
- Each Bill is issued to a specific Patient (`Patient_ID` in `BILL`).

#### 8. `PHARMACY` ↔ `PHARMACIST` (1:N)
- A Pharmacy employs several Pharmacists across rotating shifts.
- Each Pharmacist is registered to a specific Pharmacy branch (`Pharmacy_ID` in `PHARMACIST`).

#### 9. `SUPPLIER` ↔ `MANUFACTURER` (M:N)
- A Supplier distributes drugs from multiple Manufacturers.
- A Manufacturer contracts multiple authorized Suppliers.
- **Resolution**: Resolved via `SUPPLIER_MANUFACTURER` junction table.

#### 10. `SUPPLIER` ↔ `WHOLESALE_SUPPLIER` (M:N)
- A Supplier can partner with multiple GST-registered Wholesale entities.
- A Wholesale dealer works with multiple Suppliers.
- **Resolution**: Resolved via `SUPPLIER_WHOLESALE` junction table.

#### 11. `SUPPLIER` ↔ `PHARMACY` (M:N)
- A Supplier delivers pharmaceutical supplies to multiple Pharmacies.
- A Pharmacy procures inventory from multiple Suppliers.
- **Resolution**: Resolved via `SUPPLIER_PHARMACY` junction table.

#### 12. `ORDER` (Purchase Procurement) (N:1 to Supplier, N:1 to Pharmacy)
- An Order is placed by a Pharmacy and fulfilled by a Supplier.
- Represents the transactional flow of bulk procurement.

---

### 4. Multi-Valued Attributes & 1NF Normalization

In the DA1 conceptual model:
- `PATIENT.Contact_No` is multi-valued (patients often have home landline, personal mobile, or emergency contact). In strict 1NF relational mapping, multi-valued attributes cannot reside within the atomic relation. Hence, the decomposed table `PATIENT_CONTACT (Patient_ID, Contact_No)` is introduced with composite PK `(Patient_ID, Contact_No)`.
- `PHARMACY.Contact_No` possesses a primary contact phone number directly in `PHARMACY`, and `PHARMACY_CONTACT` is provided to allow additional branch telephone extensions or emergency night desk lines.

---

### 5. Academic Assumptions & Ambiguity Resolution

1. **Table Naming for `ORDER`**: In MySQL 8.x, `ORDER` is a reserved SQL keyword (as in `ORDER BY`). The table name is enclosed in backticks (`` `ORDER` ``) in SQL DDL and referenced in queries as `` `ORDER` `` or aliased as `PO` to guarantee 100% ANSI/MySQL compatibility without altering the DA1 naming standard.
2. **Composite Address Attributes**: In the DA1 diagram, addresses are conceptual composite attributes (`City`, `State`, `Street`). In relational implementation, they are decomposed into atomic columns (`Street VARCHAR(150)`, `City VARCHAR(80)`, `State VARCHAR(80)`) adhering to First Normal Form (1NF).
3. **Inventory Tracking Justification**:
   - *Observation*: The DA1 diagram establishes `MEDICINE` (catalog metadata) and `ORDER` (procurement), but lacks a localized quantity-on-hand tracking structure per physical branch.
   - *Academic Justification*: As dictated by the project title (*"Pharmacy Inventory and Prescription Tracking System"*), tracking quantities, reorder thresholds, and dispensed stock is mathematically impossible without localized inventory state.
   - *Resolution*: We introduce `INVENTORY (Inventory_ID, Pharmacy_ID, Medicine_ID, Quantity, Reorder_Level, Last_Updated)` with `UNIQUE(Pharmacy_ID, Medicine_ID)` and `STOCK_LOG` for transactional audit trails. These are formally classified as *Implementation-Support Entities* that do not alter the DA1 conceptual model.
4. **Prescription Item Primary Key**: In DA1, `PRESCRIPTION_ITEM` represents the M:N associative entity. Adding a surrogate `Item_ID (PK)` while enforcing foreign keys `Prescription_ID` and `Medicine_ID` provides optimal indexing performance and cleaner REST API manipulation.

---

### 6. Normalization Audit (Up to BCNF)

1. **First Normal Form (1NF)**:
   - All attribute values are atomic (no comma-separated phones, composite address split into Street/City/State).
   - Multi-valued contacts segregated into dedicated tables (`PATIENT_CONTACT`, `PHARMACY_CONTACT`).
   - Every relation has a well-defined Primary Key.
2. **Second Normal Form (2NF)**:
   - The tables are in 1NF.
   - No non-prime attribute is partially dependent on any candidate key. In all junction tables (`SUPPLIER_MANUFACTURER`, `SUPPLIER_WHOLESALE`, `SUPPLIER_PHARMACY`), all attributes are part of the composite primary key; thus no partial dependency exists.
3. **Third Normal Form (3NF)**:
   - The tables are in 2NF.
   - No transitive functional dependencies exist ($X \to Y$ and $Y \to Z$ where $X$ is key and $Y$ is non-prime).
   - In `DOCTOR`, `Hospital_ID` is FK; doctor attributes depend solely on `Doctor_ID`.
   - In `MEDICINE`, price and dates depend directly on `Medicine_ID`.
4. **Boyce-Codd Normal Form (BCNF)**:
   - For every non-trivial functional dependency $X \to Y$, $X$ is a superkey.
   - All relational entities satisfy BCNF criteria.

---
*Verified against DA1 Source of Truth by College Database Architecture Review.*
