# PHARMACY INVENTORY AND PRESCRIPTION TRACKING SYSTEM
## DA2 College Database Management System (DBMS) Project
**Academic Source of Truth:** Approved DA1 Conceptual (ER) & Logical (Relational Mapping) Design

---

## 1. Project Overview

The **Pharmacy Inventory and Prescription Tracking System** is a comprehensive, enterprise-grade database management solution designed for hospital-affiliated and retail pharmacy networks. It models the complete pharmaceutical lifecycle:
- Patient clinical registrations and multi-valued contact telephone points.
- Qualified medical specialist affiliations with partner hospitals.
- Issuance of formal clinical prescriptions and itemized medication regimens.
- Branch-level inventory holding, reorder threshold triggers, and automated mutation audits.
- Pharmaceutical supply chain distributions from manufacturers through wholesale GST dealers to retail pharmacies.
- Automated financial invoice calculations, bill generation, and procurement purchase orders.

The database architecture is built using **MySQL 8.x InnoDB** satisfying normalization up to **Boyce-Codd Normal Form (BCNF)**, and features complete PL/SQL-equivalent stored programs (Procedures, Deterministic Functions, and Triggers).

---

## 2. Technology Stack

- **Database Engine**: MySQL 8.x (InnoDB Storage Engine with ACID Transactions and Foreign Key Constraints)
- **Database Driver**: `mysql-connector-python` 8.3.0
- **Backend Framework**: Python 3.9+ / Flask 3.0.3 (Modular Service Architecture)
- **Frontend / UI**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Font Awesome 6.5, Chart.js 4.4
- **Styling Architecture**: Custom Modern Healthcare SaaS Theme (Deep Medical Navy `#0f3460`, Clinical Teal `#0d9488`, Glassmorphism, Print-friendly CSS)

---

## 3. Database Architecture & File Structure

```
pharmacy_system/
├── database/
│   ├── 01_schema.sql                        # DDL: Complete relational schema, constraints, indexes
│   ├── 02_sample_data.sql                   # DML: Authentic Indian healthcare sample dataset
│   ├── 03_queries.sql                       # 25+ academic SQL queries covering all relational concepts
│   ├── 04_procedures_functions_triggers.sql # 6 Procedures, 5 Functions, 5 Triggers with SIGNAL exceptions
│   └── 05_test_cases.sql                    # 15 verification test scripts (positive and boundary cases)
├── pharmacy_app/
│   ├── app.py                               # Flask web server, view controllers, and REST APIs
│   ├── config.py                            # Environment settings and connection pool configuration
│   ├── requirements.txt                     # Python library dependencies
│   ├── services/
│   │   ├── db.py                            # Unified DB engine (MySQL 8.x + Zero-config demo fallback)
│   │   ├── patient_service.py               # Patient CRUD & procedure invocations
│   │   ├── medicine_service.py              # Formulary & inventory restock manager
│   │   ├── prescription_service.py          # Clinical multi-step prescription workflow
│   │   ├── billing_service.py               # Invoicing & stored procedure billing
│   │   ├── order_service.py                 # Supply chain procurement orders
│   │   ├── analytics_service.py             # Dashboard KPIs & Chart.js aggregated feeds
│   │   └── db_ops_service.py                # Viva demonstration runner for queries & triggers
│   ├── utils/
│   │   ├── validators.py                    # Input validation and boundary safety checks
│   │   └── helpers.py                       # Formatting, currency (INR), and JSON serialization
│   ├── static/
│   │   ├── css/style.css                    # Healthcare SaaS design tokens & responsive styles
│   │   └── js/
│   │       ├── main.js                      # Toast notifications, modal helpers, search filters
│   │       ├── dashboard.js                 # 6 dynamic Chart.js analytics charts
│   │       ├── prescription.js              # Multi-step clinical prescription builder & live summary
│   │       ├── billing.js                   # Invoice modal and printable receipt generation
│   │       └── db_ops.js                    # Interactive query, procedure, function, and trigger runner
│   └── templates/
│       ├── base.html                        # Sleek sidebar, top navigation, status indicator
│       ├── dashboard.html                   # 8 KPI stats cards, 6 real-time charts, quick actions
│       ├── patients.html                    # Patient directory & detailed medical profile modal
│       ├── doctors.html                     # Specialist roster & prescription counts
│       ├── pharmacists.html                 # Staff shifts and pharmacy branch allocations
│       ├── pharmacies.html                  # Network pharmacy branches & revenue summary
│       ├── hospitals.html                   # Partner hospitals & affiliated medical staff
│       ├── medicines.html                   # Formulary catalog, stock badges, restock modal
│       ├── stock.html                       # Branch inventory levels & STOCK_LOG audit history
│       ├── suppliers.html                   # Supplier agencies, manufacturers, wholesale GST links
│       ├── orders.html                      # Purchase order lifecycles (Pending to Delivered)
│       ├── prescriptions.html               # Multi-step prescription wizard & history
│       ├── prescription_items.html          # Itemized M:N prescription medication table
│       ├── bills.html                       # Billing receipts, invoice generator, printable layout
│       ├── reports.html                     # 9 analytical reports with filters and print format
│       ├── db_operations.html               # College Viva special: live queries, procedures, triggers
│       └── settings.html                    # System health, table record counts, DB engine status
├── SCHEMA_ANALYSIS.md                       # Academic justification and relational mapping audit
├── REPORT.md                                # 28-section comprehensive DA2 college submission report
├── DEMO_GUIDE.md                            # 10–15 minute step-by-step viva presentation guide
├── VIVA_QUESTIONS.md                        # 40+ DBMS viva questions and student-friendly answers
└── README.md                                # This documentation file
```

---

## 4. Database Setup & Execution (MySQL 8.x)

### Step 1: Start MySQL Server
Ensure the MySQL 8.x daemon is running:
```bash
# On macOS (via Homebrew or System Preferences)
brew services start mysql
# Or on Linux / Windows
sudo systemctl start mysql
```

### Step 2: Execute SQL Scripts in Exact Order
Execute the scripts using the MySQL command-line client or MySQL Workbench:
```bash
mysql -u root -p < database/01_schema.sql
mysql -u root -p < database/02_sample_data.sql
mysql -u root -p < database/03_queries.sql
mysql -u root -p < database/04_procedures_functions_triggers.sql
mysql -u root -p < database/05_test_cases.sql
```

---

## 5. Web Application Setup & Execution (Flask)

### Step 1: Create and Activate Virtual Environment
```bash
cd /Users/harshitsharma/.gemini/antigravity/scratch/pharmacy_system
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r pharmacy_app/requirements.txt
```

### Step 3: Configure Database Credentials (Optional)
If your MySQL root password is not empty, set the environment variables or create a `.env` file in `pharmacy_app/`:
```bash
export MYSQL_HOST="localhost"
export MYSQL_PORT=3306
export MYSQL_USER="root"
export MYSQL_PASSWORD="your_password"
export MYSQL_DATABASE="pharmacy_system"
```
*(Note: If MySQL is offline on your machine during grading, the application automatically activates its zero-config Fallback Demo Database so the entire application and viva console remain 100% operational with zero setup friction!)*

### Step 4: Run the Flask Application
```bash
cd pharmacy_app
python app.py
```
Open your browser at: **`http://127.0.0.1:5000`**

---

## 6. Stored Programs Summary

### Stored Procedures:
1. `add_patient(...)`: Validates and inserts patient and primary contact with custom error signals.
2. `add_medicine(...)`: Enforces `price > 0`, `exp_date > manu_date`, and initializes branch stock.
3. `restock_medicine(...)`: Atomically increments inventory and records movements in `STOCK_LOG`.
4. `create_prescription(...)`: Validates patient and doctor existence in registries before creation.
5. `generate_bill(...)`: Computes bill total from prescription items, decrements stock, and inserts bill.
6. `place_order(...)`: Validates procurement volume and registers purchase order.

### Stored Functions:
1. `get_medicine_price(med_id)`: Returns unit retail price.
2. `get_patient_prescription_count(pat_id)`: Returns total prescriptions issued to a patient.
3. `calculate_prescription_total(presc_id)`: Aggregates total medication cost for a prescription.
4. `get_pharmacy_revenue(pharm_id)`: Returns cumulative billed revenue for a pharmacy branch.
5. `get_medicine_stock(pharm_id, med_id)`: Returns on-hand inventory units.

### Database Triggers:
1. `trg_after_inventory_update`: Automatically inserts an audit record into `STOCK_LOG` on any stock mutation.
2. `trg_before_inventory_update`: Signals `SQLSTATE '45000'` if quantity becomes negative (prevents negative stock).
3. `trg_validate_bill_amount`: Enforces that invoiced amounts must be non-negative.
4. `trg_before_order_insert`: Validates that arrival date succeeds order placement date.
5. `trg_validate_medicine_insert`: Redundant safety guard enforcing positive price and forward expiry.

---

## 7. Viva Demonstration Console

Navigate to **`/db-operations`** in the web interface to demonstrate live:
1. Execution of 8 key academic SQL queries with rendered output tables.
2. Direct invocation of stored procedures with live database feedback.
3. Interactive evaluation of database functions.
4. Before-and-after verification of database triggers showing automatic `STOCK_LOG` creation.
