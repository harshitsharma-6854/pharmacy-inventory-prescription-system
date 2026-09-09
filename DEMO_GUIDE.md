# DA2 PROJECT DEMONSTRATION GUIDE (10–15 MINUTE VIVA SCRIPT)
## Pharmacy Inventory and Prescription Tracking System
### Prepared for College Evaluators, Reviewers & Viva Examination

---

## Overview & Demonstration Strategy

This document provides an exact, step-by-step **10 to 15 minute presentation script** that guarantees you hit every single academic evaluation parameter:
- **Conceptual Integrity:** Demonstrating how DA2 implements your exact DA1 ER Diagram and Relational Schema.
- **Relational Operations:** Showing queries, joins, group aggregations, and subqueries.
- **Stored Programs:** Live execution of MySQL Stored Procedures, Functions, and Triggers.
- **Exception Handling:** Demonstrating error catching (`SIGNAL SQLSTATE '45000'`).
- **Software Architecture:** Clean separation of concerns (Flask services + parameter-sanitized SQL + SaaS UI).

---

## Timed Demonstration Script

### Minute 0:00 – 1:30 | Introduction & Problem Context
* **What to say:**
  > "Good morning, Respected Evaluators. Today I am demonstrating **DA2** of my DBMS project: the **Pharmacy Inventory and Prescription Tracking System**."
  > "In healthcare, disconnected systems lead to prescription transcription errors, dangerous stockouts of life-saving therapeutics, and dispensing of expired medications. My project implements a centralized, relational database management system that synchronizes doctor prescriptions, localized pharmacy inventory holdings, multi-tiered pharmaceutical procurement, and patient billing."

### Minute 1:30 – 3:00 | DA1 Conceptual Model & Relational Mapping
* **What to say:**
  > "For DA2, my **DA1 ER Diagram and Relational Mapping were treated as the strict source of truth**. Every entity is preserved."
  > "We have 17 core relations including `PHARMACY`, `PATIENT`, `DOCTOR`, `HOSPITAL`, `PRESCRIPTION`, `MEDICINE`, `BILL`, `SUPPLIER`, `MANUFACTURER`, `WHOLESALE_SUPPLIER`, and `ORDER`."
  > "We resolved multi-valued contact attributes into `PATIENT_CONTACT` and `PHARMACY_CONTACT` with composite primary keys, satisfying 1NF."
  > "M:N relationships like Prescription to Medicine are resolved via the associative entity `PRESCRIPTION_ITEM`. Similarly, Supplier distribution rights are resolved through `SUPPLIER_MANUFACTURER`, `SUPPLIER_WHOLESALE`, and `SUPPLIER_PHARMACY`."
  > "To satisfy the project title and operational requirements of DA2, two implementation-support tables were added: `INVENTORY` (for branch-level quantities and reorder thresholds) and `STOCK_LOG` (for an immutable audit trail of mutations)."
* **What to show:** Open `SCHEMA_ANALYSIS.md` briefly or point to the Schema Analysis table.

### Minute 3:00 – 4:30 | Launching the Application & Dashboard Tour
* **Action:** Open browser at `http://127.0.0.1:5000/`.
* **What to say:**
  > "Here is the running application. At the top right, notice the live status pill confirming our active connection to **MySQL 8.x Enterprise**."
  > "The executive dashboard presents 8 real-time KPI cards: Total Patients, Active Formulary Medicines, Clinical Prescriptions, Operating Pharmacies, Low Stock Alerts, Pending Orders, and Gross Billed Revenue."
  > "Below that, 6 dynamic charts powered by Chart.js visualize live aggregated MySQL data: Revenue by Branch, Prescription Frequency Timelines, Therapeutics Share, Procurement Pipelines, and the Top 5 Most Prescribed Drugs."

### Minute 4:30 – 6:00 | Patient Registration & Contact Resolution
* **Action:** Click **Patients** in the sidebar. Click **Add New Patient**.
* **Input Values:**
  - First Name: `Aryan`
  - Last Name: `Kapoor`
  - DOB: `1994-05-12`
  - Sex: `M`
  - Contact: `+91 98200 77112`
  - City: `Mumbai`
* **Action:** Click **Register Patient**.
* **What to say:**
  > "When I submit this form, it does not do a plain SQL insert. The Flask backend invokes the MySQL stored procedure `add_patient()`."
  > "The procedure validates that the DOB is not in the future, verifies the sex code, checks unique patient constraints, and inserts into both `PATIENT` and `PATIENT_CONTACT` within an atomic transaction."
* **Action:** Click the eye icon on the newly created patient to show their medical profile modal with contact details.

### Minute 6:00 – 7:30 | Medicine Catalog & Instant Restock
* **Action:** Click **Medicines** in the sidebar.
* **What to say:**
  > "The medicine catalog computes stock health in real time: badges show `IN STOCK`, `LOW STOCK`, `OUT OF STOCK`, and `EXPIRED` based on physical quantities against `Reorder_Level`."
* **Action:** Click the **Quick Restock** icon on a medicine (e.g. *Atorva 20*).
* **Input Values:** Quantity: `40`, Ref ID: `DEMO-RESTOCK-01`.
* **Action:** Click **Apply Restock**.
* **What to say:**
  > "This calls `restock_medicine()`. The stock level immediately updates, and as we will see shortly, a trigger automatically created an audit record in `STOCK_LOG`."

### Minute 7:30 – 9:30 | Multi-Step Clinical Prescription Workflow
* **Action:** Click **Prescriptions** in the sidebar. Scroll to the **Clinical Prescription Builder**.
* **Steps:**
  1. Step 1: Select Patient: `Aryan Kapoor`
  2. Step 2: Select Doctor: `Dr. Rajesh Kulkarni`
  3. Step 3: Date: `2026-09-04`
  4. Step 4: Choose Medicine `Dolo 650`, Dosage `650mg`, Frequency `Twice Daily (BD)`, Duration `5 Days`. Click `(+)`.
  5. Add second Medicine: `Pantocid 40`, Dosage `40mg`, Frequency `Once Daily (OD)`, Duration `7 Days`. Click `(+)`.
* **What to say:**
  > "Notice the **Live Clinical Summary Card** on the right updating dynamically as we add medications."
* **Action:** Click **Create Prescription**.
* **What to say:**
  > "The system invokes `create_prescription()`, validating that both Doctor and Patient exist in their respective master registries, and inserts the medication lines into the M:N table `PRESCRIPTION_ITEM`."

### Minute 9:30 – 10:30 | Automated Billing & Invoice Generation
* **Action:** In the Prescriptions table, find the new prescription and click **Bill**.
* **Action:** Select Pharmacy `Apollo HealthCity Pharmacy` and click **Compute & Issue Bill**.
* **What to say:**
  > "This calls stored procedure `generate_bill()`. Notice what just happened behind the scenes:
  > 1. The procedure queried `PRESCRIPTION_ITEM` and joined `MEDICINE` to compute the exact price total.
  > 2. It decremented the on-hand stock in `INVENTORY`.
  > 3. It recorded a `DISPENSE` entry in `STOCK_LOG`.
  > 4. It inserted the settled bill into `BILL`."
* **Action:** Click **View / Print** on the generated bill to display the formal invoice receipt sheet with GST calculation.

### Minute 10:30 – 13:00 | THE VIVA HIGHLIGHT: Database Operations Console
* **Action:** Click **DB Operations** in the sidebar.
* **What to say:**
  > "Respected Professor, this page was built specifically for the DA2 evaluation to demonstrate my SQL queries, stored procedures, functions, and triggers in real time."

#### Part A: Predefined SQL Queries
* **Action:** Click **"Top 5 Most Prescribed Medicines"**.
* **What to say:**
  > "Here is the exact SQL code. It demonstrates an `INNER JOIN` between `MEDICINE` and `PRESCRIPTION_ITEM`, `COUNT()`, `GROUP BY`, and `ORDER BY DESC LIMIT 5`. Below is the live tabular output."
* **Action:** Click **"Patients with Multiple Prescriptions"**.
* **What to say:**
  > "This demonstrates `GROUP BY` paired with the `HAVING` clause (`HAVING COUNT(P.Prescription_ID) >= 2`) to identify regular patients."

#### Part B: Deterministic Functions
* **Action:** Under Stored Functions, select a medicine and click **Evaluate Function** on `get_medicine_price()`.
* **Action:** Select a patient and evaluate `get_patient_prescription_count()`.
* **What to say:**
  > "These invoke deterministic MySQL stored functions returning scalar values directly."

#### Part C: Live Trigger Verification
* **Action:** Scroll to **Section 4: Live Trigger Execution & Verification**.
* **Action:** Select Pharmacy `Apollo Mumbai`, Medicine `Dolo 650`, Delta `+25`, and click **Run Trigger Test**.
* **What to say:**
  > "Look at this before-and-after demonstration:
  > - **Step 1:** Initial stock was 140 units.
  > - **Step 2:** A mutation of +25 units was applied via `restock_medicine()`.
  > - **Step 3:** The stock increased to 165 units.
  > - **Step 4:** Look at the table below! The trigger `trg_after_inventory_update` automatically captured this delta and inserted an audit record into `STOCK_LOG` with timestamp and action category `RESTOCK` without any manual insert statement!"

### Minute 13:00 – 14:30 | Reports & Supply Chain Verification
* **Action:** Click **Reports** in the sidebar.
* **What to say:**
  > "We have 9 analytical reports including Inventory Valuation, Low Stock Alerts, Expired Batches Quarantine, Revenue Audits, and Doctor/Supplier Performance."
* **Action:** Click **Suppliers & Mfg** to show the M:N distribution mapping connecting Distributors, Manufacturers (`SUPPLIER_MANUFACTURER`), and Wholesale GST registrants (`SUPPLIER_WHOLESALE`).

### Minute 14:30 – 15:00 | Conclusion & Q&A
* **What to say:**
  > "To conclude, the **Pharmacy Inventory and Prescription Tracking System** demonstrates a complete, BCNF-normalized relational database with full PL/SQL stored programs, triggers, exception handling, and a modern healthcare application. All 15 test cases in `05_test_cases.sql` have been verified. I am now open to any viva questions."

---
*Follow this script confidently to achieve top marks in your DA2 evaluation!*
