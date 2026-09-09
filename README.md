# Pharmacy Inventory and Prescription Tracking System

## DA2 College Database Management System (DBMS) Project

**Academic Source of Truth:** Approved DA1 Conceptual (ER) and Logical (Relational Mapping) Design

---

## 1. Project Overview

The **Pharmacy Inventory and Prescription Tracking System** is a comprehensive database management solution designed to manage pharmacy inventory, prescriptions, billing, suppliers, and related operations.

The system models the major pharmaceutical and healthcare workflows, including:

- Patient registration and multi-valued patient contact information.
- Doctor and hospital affiliations.
- Prescription creation and prescription medication details.
- Pharmacy-level medicine inventory and reorder thresholds.
- Automatic stock movement auditing through database triggers.
- Manufacturer, supplier, wholesale supplier, and pharmacy relationships.
- Prescription-based billing and invoice generation.
- Procurement and purchase order management.

The database architecture is implemented using **MySQL 8.x with the InnoDB storage engine** and is designed and analyzed for normalization up to **Boyce-Codd Normal Form (BCNF)**. The project also demonstrates MySQL stored procedures, functions, and triggers for database programming and integrity enforcement.

---

## 2. Technology Stack

| Component | Technology |
|---|---|
| Database | MySQL 8.x |
| Storage Engine | InnoDB |
| Database Driver | mysql-connector-python 8.3.0 |
| Backend | Python 3.9+ / Flask 3.0.3 |
| Frontend | HTML5, CSS3, JavaScript ES6+ |
| UI Framework | Bootstrap 5.3 |
| Icons | Font Awesome 6.5 |
| Dashboard Charts | Chart.js 4.4 |
| Database Programming | MySQL Stored Procedures, Functions and Triggers |

---

## 3. Project Structure

```text
pharmacy_system/
├── database/
│   ├── 01_schema.sql
│   ├── 02_sample_data.sql
│   ├── 03_queries.sql
│   ├── 04_procedures_functions_triggers.sql
│   └── 05_test_cases.sql
│
├── pharmacy_app/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── services/
│   │   ├── db.py
│   │   ├── patient_service.py
│   │   ├── medicine_service.py
│   │   ├── prescription_service.py
│   │   ├── billing_service.py
│   │   ├── order_service.py
│   │   ├── analytics_service.py
│   │   └── db_ops_service.py
│   │
│   ├── utils/
│   │   ├── validators.py
│   │   └── helpers.py
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       ├── main.js
│   │       ├── dashboard.js
│   │       ├── prescription.js
│   │       ├── billing.js
│   │       └── db_ops.js
│   │
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── patients.html
│       ├── doctors.html
│       ├── pharmacists.html
│       ├── pharmacies.html
│       ├── hospitals.html
│       ├── medicines.html
│       ├── stock.html
│       ├── suppliers.html
│       ├── orders.html
│       ├── prescriptions.html
│       ├── prescription_items.html
│       ├── bills.html
│       ├── reports.html
│       ├── db_operations.html
│       └── settings.html
│
├── SCHEMA_ANALYSIS.md
├── REPORT.md
├── DEMO_GUIDE.md
├── VIVA_QUESTIONS.md
└── README.md
```

---

## 4. Database Architecture

The implemented database contains **20 tables**:

### Core DA1 relational tables

1. `BILL`
2. `DOCTOR`
3. `HOSPITAL`
4. `MANUFACTURER`
5. `MEDICINE`
6. `ORDER`
7. `PATIENT`
8. `PATIENT_CONTACT`
9. `PHARMACIST`
10. `PHARMACY`
11. `PHARMACY_CONTACT`
12. `PRESCRIPTION`
13. `PRESCRIPTION_ITEM`
14. `SUPPLIER`
15. `SUPPLIER_MANUFACTURER`
16. `SUPPLIER_PHARMACY`
17. `SUPPLIER_WHOLESALE`
18. `WHOLESALE_SUPPLIER`

### Implementation/support tables

19. `INVENTORY`
20. `STOCK_LOG`

`INVENTORY` and `STOCK_LOG` are implementation/support tables introduced to support branch-level inventory management and automatic stock auditing.

---

## 5. Database Setup

### Step 1: Start MySQL Server

On macOS with the MySQL installer:

```bash
sudo /usr/local/mysql/support-files/mysql.server start
```

On Linux:

```bash
sudo systemctl start mysql
```

---

### Step 2: Create and Populate the Database

From the project root, execute the SQL scripts in the following order:

```bash
mysql -u root -p < database/01_schema.sql
mysql -u root -p < database/02_sample_data.sql
mysql -u root -p < database/03_queries.sql
mysql -u root -p < database/04_procedures_functions_triggers.sql
mysql -u root -p < database/05_test_cases.sql
```

The scripts perform the following tasks:

| Script | Purpose |
|---|---|
| `01_schema.sql` | Creates tables, primary keys, foreign keys, constraints and indexes |
| `02_sample_data.sql` | Inserts the sample healthcare dataset |
| `03_queries.sql` | Contains 25 academic SQL queries |
| `04_procedures_functions_triggers.sql` | Creates stored procedures, functions and triggers |
| `05_test_cases.sql` | Contains documented verification and boundary test cases |

> **Note:** `03_queries.sql` primarily contains demonstration/query statements, while `05_test_cases.sql` contains database mutation and validation scenarios.

---

## 6. Web Application Setup

### Step 1: Create a Virtual Environment

Run these commands from the project root:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 2: Install Dependencies

```bash
pip install -r pharmacy_app/requirements.txt
```

---

### Step 3: Configure Database Credentials

The application can read MySQL configuration from environment variables or a `.env` file inside `pharmacy_app/`.

Example:

```bash
export MYSQL_HOST="localhost"
export MYSQL_PORT=3306
export MYSQL_USER="root"
export MYSQL_PASSWORD="your_password"
export MYSQL_DATABASE="pharmacy_system_new"
```

Do not commit real database passwords or other secrets to GitHub.

---

### Step 4: Run the Flask Application

```bash
cd pharmacy_app
PORT=5050 python3 app.py
```

Then open:

```text
http://127.0.0.1:5050
```

The application connects to the configured MySQL database when MySQL is available. A zero-configuration fallback demo database is also available for application-level demonstration when the MySQL environment is unavailable.

---

## 7. Database Programming

The project demonstrates database programming using **MySQL Stored Procedures, Functions and Triggers**.

### 7.1 Stored Procedures

The project contains six stored procedures:

1. `add_patient(...)`  
   Validates and inserts a patient and associated contact information.

2. `add_medicine(...)`  
   Validates medicine information and initializes branch inventory.

3. `restock_medicine(...)`  
   Increases inventory and records the stock movement.

4. `create_prescription(...)`  
   Validates the patient and doctor before creating a prescription.

5. `generate_bill(...)`  
   Calculates the prescription bill, updates inventory and creates the bill record.

6. `place_order(...)`  
   Validates procurement information and creates a purchase order.

---

### 7.2 Stored Functions

The project contains five stored functions:

1. `get_medicine_price(med_id)`  
   Returns the retail price of a medicine.

2. `get_patient_prescription_count(pat_id)`  
   Returns the number of prescriptions associated with a patient.

3. `calculate_prescription_total(presc_id)`  
   Calculates the total medication cost of a prescription.

4. `get_pharmacy_revenue(pharm_id)`  
   Returns the cumulative billed revenue of a pharmacy.

5. `get_medicine_stock(pharm_id, med_id)`  
   Returns the current inventory quantity for a medicine at a pharmacy.

---

### 7.3 Database Triggers

The project contains five triggers:

1. `trg_after_inventory_update`  
   Automatically records inventory changes in `STOCK_LOG`.

2. `trg_before_inventory_update`  
   Prevents inventory from becoming negative.

3. `trg_validate_bill_amount`  
   Prevents negative bill amounts.

4. `trg_before_order_insert`  
   Validates the relationship between order and expected arrival dates.

5. `trg_validate_medicine_insert`  
   Enforces positive medicine prices and ensures the expiry date is after the manufacturing date.

---

## 8. SQL Query Demonstration

The project contains **25 academic SQL queries** demonstrating different relational database concepts, including:

- `SELECT`
- `WHERE`
- `ORDER BY`
- `DISTINCT`
- `LIKE`
- `BETWEEN`
- `IN`
- Aggregate functions
- `COUNT`
- `SUM`
- `AVG`
- `MIN`
- `MAX`
- `GROUP BY`
- `HAVING`
- Multi-table joins
- Subqueries
- Correlated subqueries
- `EXISTS`
- `NOT EXISTS`
- `CASE`
- Date-based queries
- Conditional aggregation
- Complex supply-chain joins

The queries are available in:

```text
database/03_queries.sql
```

---

## 9. Verification Test Cases

The project contains **15 documented verification test cases** covering positive and boundary scenarios.

The test cases demonstrate:

- Patient insertion.
- Medicine insertion.
- Prescription creation.
- Prescription item creation.
- Bill generation.
- Inventory restocking.
- Automatic stock auditing.
- Stored function evaluation.
- Input validation and boundary conditions.

The negative validation scenarios are documented in the test-case script and are intentionally kept controlled so that invalid operations do not corrupt the demonstration database.

Test cases are available in:

```text
database/05_test_cases.sql
```

---

## 10. Web Application Features

The Flask application provides an interactive interface for the database system.

### Dashboard

Provides:

- Patient statistics.
- Medicine statistics.
- Prescription statistics.
- Pharmacy statistics.
- Low-stock indicators.
- Pending order information.
- Analytical charts.

### Patient Management

- Patient directory.
- Patient information.
- Contact details.
- Patient-related prescription information.

### Medicine and Inventory

- Medicine catalog.
- Medicine pricing.
- Branch-level inventory.
- Reorder thresholds.
- Stock status.
- Stock movement history.

### Prescription Management

- Prescription creation.
- Doctor and patient association.
- Prescription medication items.
- Prescription history.

### Billing

- Prescription-based bill generation.
- Invoice records.
- Bill totals.
- Printable billing information.

### Supplier and Order Management

- Supplier information.
- Manufacturer relationships.
- Wholesale supplier relationships.
- Purchase orders.
- Order status tracking.

### Reports

The application provides analytical reports for studying:

- Inventory.
- Prescriptions.
- Medicines.
- Billing.
- Pharmacy performance.
- Suppliers.
- Orders.
- Other database statistics.

---

## 11. DBMS Viva Demonstration Console

The application includes a dedicated **DB Operations** page for academic demonstration.

Navigate to:

```text
/db-operations
```

The console can demonstrate:

1. Execution of selected academic SQL queries.
2. Stored procedure invocation.
3. Stored function evaluation.
4. Trigger execution and verification.
5. Automatic `STOCK_LOG` creation.
6. Before-and-after database state verification.

This page is specifically designed to make the DBMS concepts visible during the project demonstration.

---

## 12. Documentation

Additional project documentation is available in the repository:

| File | Description |
|---|---|
| `REPORT.md` | Comprehensive DA2 project report |
| `SCHEMA_ANALYSIS.md` | Database schema and normalization analysis |
| `DEMO_GUIDE.md` | Step-by-step project demonstration guide |
| `VIVA_QUESTIONS.md` | DBMS viva questions and student-friendly answers |

---

## 13. Academic Concepts Demonstrated

The project demonstrates the following DBMS concepts:

- ER/EER modelling.
- Entity-to-relational mapping.
- Primary keys.
- Foreign keys.
- Candidate and composite keys.
- Referential integrity.
- Domain constraints.
- Functional dependencies.
- Normalization.
- BCNF analysis.
- SQL DDL.
- SQL DML.
- SQL queries and joins.
- Aggregate functions.
- Subqueries.
- Grouping and filtering.
- Stored procedures.
- Stored functions.
- Database triggers.
- Transactional inventory updates.
- Audit logging.
- CRUD operations.
- Database-backed web application development.

---

## 14. Security and Configuration

Sensitive configuration files should not be committed to the repository.

The `.gitignore` file excludes:

```text
.env
venv/
__pycache__/
*.pyc
.DS_Store
pharmacy_app/pharmacy_demo.db
```

Database credentials should always be supplied through local environment configuration rather than being hard-coded into the repository.

---

## 15. Running the Project Quickly

For an already-configured environment:

### Start MySQL

```bash
sudo /usr/local/mysql/support-files/mysql.server start
```

### Start the application

```bash
cd ~/.gemini/antigravity/scratch/pharmacy_system/pharmacy_app
PORT=5050 python3 app.py
```

### Open the application

```text
http://127.0.0.1:5050
```

---

## 16. Project Objective

The primary objective of this project is to demonstrate how a properly structured relational database can be integrated with a web application to manage pharmacy operations while maintaining data integrity, minimizing redundancy, and supporting practical database programming concepts.

---

## 17. Conclusion

The Pharmacy Inventory and Prescription Tracking System integrates database design, SQL, MySQL stored programs, triggers, inventory management, prescription processing, billing, procurement and a Flask-based web interface into a single academic DBMS project.

The project provides both an implementation of the approved DA1 database design and a practical DA2 demonstration of SQL, database programming, integrity constraints and application-level database interaction.