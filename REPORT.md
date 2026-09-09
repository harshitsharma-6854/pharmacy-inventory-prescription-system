# DA2 LABORATORY REPORT: PHARMACY INVENTORY AND PRESCRIPTION TRACKING SYSTEM
## Course: CSE2004 / IT2004 — Database Management Systems (DBMS Lab)
### Digital Assignment 2 (DA2) Comprehensive Submission

---

# SECTION 1: COVER PAGE & STUDENT PARTICULARS

* **Project Title:** PHARMACY INVENTORY AND PRESCRIPTION TRACKING SYSTEM
* **Course Code & Name:** CSE2004 - Database Management Systems Laboratory
* **Evaluation Cycle:** Digital Assignment 2 (DA2) Implementation & Viva
* **Student Name:** Harshit Sharma
* **Registration Number:** 22BCE10000
* **Class & Section:** B.Tech Computer Science & Engineering
* **Faculty Reviewer:** Respected Course Faculty
* **Department:** Department of Computer Science & Engineering
* **Database Engine:** MySQL 8.x (InnoDB ACID Storage Engine)
* **Application Framework:** Python 3.9+ / Flask 3.0 / Bootstrap 5.3 / Chart.js 4.4
* **Source of Truth:** Approved DA1 Conceptual ER/EER Diagrams & 1NF-to-BCNF Normalization

---

# SECTION 2: BONAFIDE DECLARATION & CERTIFICATE

This is to certify that the work presented in this report entitled **"PHARMACY INVENTORY AND PRESCRIPTION TRACKING SYSTEM"** is an authentic record of original project work completed by **Harshit Sharma (Reg No: 22BCE10000)** for the academic assessment of DA2 in Database Management Systems.

The physical implementation strictly operationalizes the **DA1 Conceptual (ER), Enhanced Entity-Relationship (EER), Relational Mapping, and 1NF-to-BCNF Normalization proofs** previously submitted and approved. All 17 core relations, 2 implementation-support tables, 25 SQL queries, 6 stored procedures, 5 functions, 5 triggers with `SIGNAL SQLSTATE '45000'`, and 15 verification test cases have been executed and verified under MySQL 8.x.

**Student Signature:** ____________________  
**Faculty Evaluator Signature:** ____________________  
**Date:** September 04, 2026

---

# SECTION 3: EXECUTIVE SUMMARY & OBJECTIVES

The **Pharmacy Inventory and Prescription Tracking System** provides a centralized, relational database management solution designed for hospital-affiliated and community pharmacy networks. The system bridges clinical medicine prescribing with physical dispensary inventory holding, multi-tiered wholesale procurement, and financial settlement.

The database is built on **MySQL 8.x InnoDB** satisfying normalization up to **Boyce-Codd Normal Form (BCNF)**. It comprises 17 core relations derived from the student's DA1 conceptual design, 2 formally justified implementation-support tables (`INVENTORY` and `STOCK_LOG`), 25 analytical SQL queries, 6 stored procedures, 5 deterministic functions, 5 automated triggers with user-defined exception handling, and an interactive Flask web application running on port 5050 tailored for project demonstration and viva defense.

---

# SECTION 4: DA1 CONCEPTUAL ER DIAGRAM (PAGES 1 & 2)

As submitted in **Page 1 and Page 2 of DA1**, the conceptual ER diagram models the healthcare network with the following specific semantic elements:

1. **PHARMACY** (Rating, Name, Address [City, State, Street], Contact_No)
2. **PATIENT** (DOB, Age [Derived Attribute with Dashed Ellipse], Sex, Contact_No [Multi-valued Attribute with Double Ellipse], Address [City, State, Street], Name [First_Name, Last_Name])
3. **HOSPITAL** (Name, Contact, Address [City, State, Street], Hospital_ID) &mdash; 1:N *Affiliated With* Pharmacy
4. **DOCTOR** (Experience, Contact_No, Name [First_Name, Last_Name], Qualification, Doctor_ID, Hospital_ID) &mdash; N:1 *Works For* Hospital
5. **PRESCRIPTION** (Date, Doctor_ID, Patient_ID, Prescription_ID) &mdash; 1:N *Prescribes* from Doctor; 1:N *Receives* from Patient
6. **MEDICINE** (Manufacture_Date, Exp_Date, Name, Price, Available_Qty, Medicine_ID)
7. **PRESCRIPTION_ITEM** (Weak / Associative Entity with Double Rectangle: Item_ID [Discriminator], Prescription_ID, Medicine_ID, Frequency, Duration, Dosage) &mdash; 1:N *Contains* from Prescription; 1:1/1:N *Has* with Medicine
8. **BILL** (Weak Entity with Double Rectangle: Bill_ID [Discriminator], Pharmacy_ID, Patient_ID, Amount) &mdash; 1:N *Issues* from Pharmacy; 1:N *Receives* from Patient
9. **PHARMACIST** (Shift, Name, Pharmacist_ID, Pharmacy_ID) &mdash; N:1 *Works For* Pharmacy
10. **SUPPLIER** (Name, Contact, Address [City, State, Street], Supplier_ID) &mdash; M:N *Supplies* to Pharmacy
11. **ORDER** (Quantity_Ordered, Date, Arrival_Date, Payment_Status, Order_Status, Order_ID, Supplier_ID, Pharmacy_ID) &mdash; N:1 *Takes Order* from Supplier; 1:N *Gives Order* from Pharmacy
12. **MANUFACTURER** (Brand_Name, Address [City, State, Street], Manufacturer_ID) &mdash; M:N *Get Supplies From* with Supplier
13. **WHOLE SALE SUPPLIER** (GST_No, Warehouse Address [City, State, Street]) &mdash; M:N *Get Supplies From* with Supplier

---

# SECTION 5: DA1 ENHANCED ER (EER) MODELING (PAGES 3 & 4)

As submitted in **Page 3 and Page 4 of DA1**, advanced conceptual modeling concepts were incorporated:

### 1. Bottom-Up Disjoint Generalization / Specialization (`d`)
```
                 +-----------------------------------------------+
                 |                    PERSON                     |
                 | (Person_ID [PK], Name, Address, Contact)      |
                 +-----------------------------------------------+
                                        |
                                       (d)  [Disjoint Specialization]
                       +----------------+----------------+
                       |                                 |
                       v                                 v
      +---------------------------------+  +---------------------------------+
      |             DOCTOR              |  |             PATIENT             |
      | - Doctor_ID [PK]                |  | - Patient_ID [PK]               |
      | - Hospital_ID [FK]              |  | - DOB, Sex, Age [Derived]       |
      | - Qualification, Experience     |  | - Contact_No [Multi-valued]     |
      | - Name (First, Last), Contact   |  | - Address (City, State, Street) |
      +---------------------------------+  +---------------------------------+
                       |
                       v
      +---------------------------------+
      |           PHARMACIST            |
      | - Pharmacist_ID [PK]            |
      | - Pharmacy_ID [FK]              |
      | - Shift, Name (First, Last)     |
      +---------------------------------+
```

### 2. EER Aggregation
In **Page 3 of DA1**, the relationship `PRESCRIPTION` &mdash; `INCLUDES` &mdash; `MEDICINE` is enclosed in an aggregation boundary. This aggregated clinical regimen participates in the relationship `ISSUED BY` with `PHARMACIST`, representing that pharmacists dispense an aggregated regimen.

### 3. Category / Union Modeling
Circle `o` (Union) models that `SUPPLIER` procures goods from either a `WHOLESALE_SUPPLIER` or directly from a `MANUFACTURER`, and `MEDICINE` originates from either source.

---

# SECTION 6: DA1 RELATIONAL MAPPING (PAGES 5 & 6)

| # | Relation / Table Name | Primary Key (PK) | Foreign Keys (FK) | Relational Description |
|---|---|---|---|---|
| 1 | `PHARMACY` | `Pharmacy_ID` | - | Master dispensing pharmacy branch |
| 2 | `BILL (weak)` | `Bill_ID` | `Pharmacy_ID`, `Patient_ID` | Invoiced financial receipts |
| 3 | `PATIENT` | `Patient_ID` | - | Master patient registry |
| 4 | `PATIENT_CONTACT` | `(Patient_ID, Contact_No)` | `Patient_ID` &rarr; `PATIENT` | 1NF multi-valued phone lines decomposition |
| 5 | `HOSPITAL` | `Hospital_ID` | `Pharmacy_ID` &rarr; `PHARMACY` | Partner clinical medical centers |
| 6 | `DOCTOR` | `Doctor_ID` | `Hospital_ID` &rarr; `HOSPITAL` | Qualified medical specialists |
| 7 | `PRESCRIPTION` | `Prescription_ID` | `Doctor_ID`, `Patient_ID` | Clinical prescription headers |
| 8 | `PRESCRIPTION_ITEM` | `Item_ID` | `Prescription_ID`, `Medicine_ID` | M:N associative entity (Dosage, Freq, Dur) |
| 9 | `MEDICINE` | `Medicine_ID` | - | Formulary catalog with price & batch dates |
| 10 | `PHARMACIST` | `Pharmacist_ID` | `Pharmacy_ID` &rarr; `PHARMACY` | Licensed pharmacists & shift assignments |
| 11 | `SUPPLIER` | `Supplier_ID` | - | Logistics & distribution agencies |
| 12 | `ORDER` | `Order_ID` | `Supplier_ID`, `Pharmacy_ID` | Bulk purchase procurement orders |
| 13 | `MANUFACTURER` | `Manufacturer_ID` | - | Pharmaceutical manufacturing companies |
| 14 | `WHOLESALE_SUPPLIER` | `GST_No` | - | Regional wholesale depots with GST identity |
| 15 | `SUPPLIER_MANUFACTURER` | `(Supplier_ID, Manufacturer_ID)` | FKs to `SUPPLIER`, `MANUFACTURER` | M:N distribution licensing junction |
| 16 | `SUPPLIER_WHOLESALE` | `(Supplier_ID, GST_No)` | FKs to `SUPPLIER`, `WHOLESALE_SUPPLIER` | M:N wholesale commercial link |
| 17 | `SUPPLIER_PHARMACY` | `(Supplier_ID, Pharmacy_ID)` | FKs to `SUPPLIER`, `PHARMACY` | M:N procurement channel junction |
| 18 | `INVENTORY` *(Support)* | `Inventory_ID` | `Pharmacy_ID`, `Medicine_ID` | Localized stock on hand & reorder thresholds |
| 19 | `STOCK_LOG` *(Support)* | `Log_ID` | `Pharmacy_ID`, `Medicine_ID` | Immutable mutation audit trail (Restock/Dispense) |

---

# SECTION 7: DA1 NORMALIZATION PROOFS (ALL 17 TABLES AUDITED)

In **Pages 7 through 15 of DA1**, every table was audited using functional dependencies and sample data (P01&ndash;P05, D01&ndash;D05, M01&ndash;M05):

### 1. Decomposed Tables (Fixing Normal Form Violations):
1. **Table 1: PHARMACY (Pages 7 & 8):**
   - *Initial FDs:* { Pharmacy_ID &rarr; Rating, Name, City, Street, Contact_No }, { City &rarr; State }
   - *Violation:* Transitive Dependency: Pharmacy_ID &rarr; City and City &rarr; State (Not in 3NF).
   - *Decomposition:* `R1(Pharmacy_ID, Rating, Name, City, Street, Contact_No)` and `R2(City, State)` &rarr; Both in BCNF.
2. **Table 4: DOCTOR (Pages 9 & 10):**
   - *Initial FDs:* { (Doctor_ID, Hospital_ID) &rarr; Experience, Contact_No, First_Name, Last_Name, Qualification }, { Qualification &rarr; Hospital_ID }
   - *Violation:* `Qualification &rarr; Hospital_ID` violates BCNF (Qualification is not a superkey).
   - *Decomposition:* `R1(Doctor_ID, Hospital_ID, Experience, Contact_No, First_Name, Last_Name)` and `R2(Qualification, Hospital_ID)` &rarr; Both in BCNF.
3. **Table 8: BILL (Page 11):**
   - *Key:* (Bill_ID, Pharmacy_ID, Patient_ID)
   - *Initial FDs:* { Bill_ID &rarr; Patient_ID }, { Patient_ID &rarr; Amount }
   - *Violation:* Partial dependency on candidate key subset (Not in 2NF).
   - *Decomposition:* `R1(Bill_ID, Pharmacy_ID, Patient_ID)` and `R2(Patient_ID, Amount)` &rarr; Both in BCNF.
4. **Table 9: HOSPITAL (Page 12):**
   - *Key:* (Hospital_ID, Pharmacy_ID)
   - *Violation:* Partial dependency on `Hospital_ID &rarr; City, State, Street, Name, Contact` (Not in 2NF).
   - *Decomposition:* `R1(Hospital_ID, City, State, Street, Name, Contact)` and `R2(Hospital_ID, Pharmacy_ID)` &rarr; Both in BCNF.

### 2. Tables Verified Already in BCNF:
- **Table 2: PRESCRIPTION (Page 8):** Single CK &rarr; Already in BCNF.
- **Table 3: MEDICINE (Page 8 & 9):** Single PK &rarr; Already in BCNF.
- **Table 5: SUPPLIER_MANUFACTURER (Page 10):** All key attributes &rarr; Already in BCNF.
- **Table 6: SUPPLIER_WHOLESALE (Page 10):** All key attributes &rarr; Already in BCNF.
- **Table 7: SUPPLIER_PHARMACY (Page 10):** All key attributes &rarr; Already in BCNF.
- **Table 10: PRESCRIPTION_ITEM (Page 13):** (Prescription_ID, Item_ID) &rarr; No violation &rarr; In BCNF.
- **Table 11: SUPPLIER (Page 13):** Single CK &rarr; In BCNF.
- **Table 12: ORDER (Page 13 & 14):** Single CK &rarr; In BCNF.
- **Table 13: MANUFACTURER (Page 14):** Single CK &rarr; In BCNF.
- **Table 14: WHOLESALE_SUPPLIER (Page 14):** Single CK &rarr; In BCNF.
- **Table 15: PHARMACIST (Page 15):** Single CK &rarr; In BCNF.
- **Table 16: PATIENT (Page 15):** Single CK &rarr; In BCNF.
- **Table 17: PATIENT_CONTACT (Page 15):** All key attributes &rarr; In BCNF.

---

# SECTION 8: STORED PROGRAMS & TRIGGERS SPECIFICATION

### Stored Procedures:
1. `add_patient(...)`: Validates DOB &le; CURDATE(), sex in ('M','F','O'), and creates patient and primary contact row atomically.
2. `add_medicine(...)`: Enforces `Price > 0` and `Exp_Date > Manu_Date`, cataloging the drug and initializing branch inventory in `INVENTORY`.
3. `restock_medicine(...)`: Atomically increments inventory stock and logs transaction in `STOCK_LOG`.
4. `create_prescription(...)`: Validates that both Doctor and Patient exist in master registries before creating the clinical prescription header.
5. `generate_bill(...)`: Computes bill total by querying prescribed medicine prices, verifies stock availability, decrements stock, logs `DISPENSE`, and records the bill.
6. `place_order(...)`: Validates supplier/pharmacy links, quantity &gt; 0, and records the purchase procurement order.

### Stored Functions:
1. `get_medicine_price(med_id)`: Returns `DECIMAL(10,2)` unit retail price.
2. `get_patient_prescription_count(pat_id)`: Returns `INT` count of prescriptions issued to patient.
3. `calculate_prescription_total(presc_id)`: Returns `DECIMAL(10,2)` aggregated price of prescribed drugs.
4. `get_pharmacy_revenue(pharm_id)`: Returns `DECIMAL(10,2)` cumulative billed revenue for a branch.
5. `get_medicine_stock(pharm_id, med_id)`: Returns `INT` physical units on hand in branch inventory.

### Database Triggers:
1. `trg_before_inventory_update`: Enforces `NEW.Quantity >= 0`. Throws `SIGNAL SQLSTATE '45000'` if quantity drops below zero.
2. `trg_after_inventory_update`: Computes delta (`NEW.Quantity - OLD.Quantity`) and automatically writes an immutable audit record into `STOCK_LOG` with movement type `RESTOCK` or `DISPENSE`.
3. `trg_validate_bill_amount`: Guarantees non-negative invoice values.
4. `trg_before_order_insert`: Enforces `Arrival_Date >= Order_Date`.
5. `trg_validate_medicine_insert`: Redundant safety guard enforcing chronological expiration and positive pricing.

---

# SECTION 9: 15 TEST CASES EXECUTION MATRIX

| Test # | Description | Target Mechanism | Expected Result | Status |
|---|---|---|---|---|
| TC-01 | Insert Valid Patient | Procedure `add_patient` | Patient + Contact stored | **PASSED** |
| TC-02 | Duplicate Patient ID | Constraint `PRIMARY KEY` | Caught with SQLSTATE 45000 | **PASSED** |
| TC-03 | Insert Valid Medicine | Procedure `add_medicine` | Cataloged & stock set | **PASSED** |
| TC-04 | Negative Price | Constraint `CHECK (Price > 0)` | Rejected with SQLSTATE 45000 | **PASSED** |
| TC-05 | Inverted Expiry Date | Constraint `Exp_Date > Manu_Date`| Rejected with SQLSTATE 45000 | **PASSED** |
| TC-06 | Create Valid Prescription | Procedure `create_prescription` | Prescription registered | **PASSED** |
| TC-07 | Non-Existent Patient | Referential Check | Rejected with error | **PASSED** |
| TC-08 | Non-Existent Doctor | Referential Check | Rejected with error | **PASSED** |
| TC-09 | Bill Generation | Procedure `generate_bill` | Auto-calculated from items | **PASSED** |
| TC-10 | Negative Stock Prevention | Trigger `trg_before_inventory_update`| Rejected with SQLSTATE 45000 | **PASSED** |
| TC-11 | Restock Inventory | Procedure `restock_medicine` | Increments & logs audit | **PASSED** |
| TC-12 | Auto Audit Logging | Trigger `trg_after_inventory_update` | Row auto-created in STOCK_LOG | **PASSED** |
| TC-13 | Foreign Key Enforcement | Referential Integrity | Child insertion blocked | **PASSED** |
| TC-14 | Invalid Order Quantity | Constraint `CHECK (Qty > 0)` | Rejected with SQLSTATE 45000 | **PASSED** |
| TC-15 | Stored Functions | Deterministic Functions | Returns accurate scalars | **PASSED** |

---

# SECTION 10: RUNNING THE APPLICATION

The application server is actively running in the background on **Port 5050**:
```bash
cd /Users/harshitsharma/.gemini/antigravity/scratch/pharmacy_system
source venv/bin/activate
cd pharmacy_app
python app.py
```
Open **`http://127.0.0.1:5050`** in any web browser to view the live dashboard.

---

*Verified and Prepared for Academic Review & Evaluation.*
