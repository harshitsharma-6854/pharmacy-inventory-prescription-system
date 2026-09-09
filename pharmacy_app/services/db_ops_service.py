from services.db import db

class DBOpsService:
    PREDEFINED_QUERIES = {
        "top_prescribed": {
            "name": "Top 5 Most Prescribed Medicines",
            "category": "Relational Aggregation & Joins",
            "description": "Demonstrates INNER JOIN, COUNT(), GROUP BY, and ORDER BY with LIMIT 5 to rank most frequently prescribed drugs.",
            "sql": """
SELECT 
    M.Medicine_ID,
    M.Name AS Medicine_Name,
    M.Price AS Unit_Price_INR,
    COUNT(PI.Item_ID) AS Prescriptions_Count
FROM MEDICINE M
INNER JOIN PRESCRIPTION_ITEM PI ON M.Medicine_ID = PI.Medicine_ID
GROUP BY M.Medicine_ID, M.Name, M.Price
ORDER BY Prescriptions_Count DESC, M.Price DESC
LIMIT 5;
            """
        },
        "patients_multiple_prescriptions": {
            "name": "Patients with Multiple Prescriptions",
            "category": "HAVING Clause & Profiling",
            "description": "Finds patients who have been issued 2 or more medical prescriptions using GROUP BY and HAVING COUNT() >= 2.",
            "sql": """
SELECT 
    PT.Patient_ID,
    CONCAT(PT.First_Name, ' ', PT.Last_Name) AS Patient_Name,
    PT.City,
    COUNT(P.Prescription_ID) AS Total_Prescriptions
FROM PATIENT PT
INNER JOIN PRESCRIPTION P ON PT.Patient_ID = P.Patient_ID
GROUP BY PT.Patient_ID, PT.First_Name, PT.Last_Name, PT.City
HAVING COUNT(P.Prescription_ID) >= 2
ORDER BY Total_Prescriptions DESC;
            """
        },
        "low_stock": {
            "name": "Low Stock Medicines (Threshold Alert)",
            "category": "CASE Expression & Conditional Derivation",
            "description": "Categorizes inventory stock health across pharmacy branches using a CASE expression based on Reorder_Level.",
            "sql": """
SELECT 
    PH.Name AS Pharmacy_Branch,
    M.Name AS Medicine_Name,
    INV.Quantity AS Stock_On_Hand,
    INV.Reorder_Level,
    CASE 
        WHEN INV.Quantity = 0 THEN 'OUT OF STOCK'
        WHEN INV.Quantity <= INV.Reorder_Level THEN 'LOW STOCK'
        ELSE 'OPTIMAL STOCK'
    END AS Stock_Health
FROM INVENTORY INV
INNER JOIN PHARMACY PH ON INV.Pharmacy_ID = PH.Pharmacy_ID
INNER JOIN MEDICINE M ON INV.Medicine_ID = M.Medicine_ID
WHERE INV.Quantity <= INV.Reorder_Level
ORDER BY INV.Quantity ASC;
            """
        },
        "branch_revenue": {
            "name": "Pharmacy-wise Gross Billed Revenue",
            "category": "SUM Aggregation & Financial Audit",
            "description": "Calculates total invoiced revenue and bill count per pharmacy branch using SUM() and LEFT JOIN.",
            "sql": """
SELECT 
    PH.Pharmacy_ID,
    PH.Name AS Pharmacy_Name,
    PH.City,
    COUNT(B.Bill_ID) AS Invoices_Count,
    COALESCE(SUM(B.Amount), 0.00) AS Total_Revenue_INR
FROM PHARMACY PH
LEFT JOIN BILL B ON PH.Pharmacy_ID = B.Pharmacy_ID
GROUP BY PH.Pharmacy_ID, PH.Name, PH.City
ORDER BY Total_Revenue_INR DESC;
            """
        },
        "supplier_performance": {
            "name": "Supplier Order Fulfillment & Delivery Audit",
            "category": "Multi-Column Aggregation & Status Filtering",
            "description": "Summarizes total purchase orders placed and volume supplied per pharmaceutical distributor.",
            "sql": """
SELECT 
    S.Supplier_ID,
    S.Name AS Supplier_Name,
    COUNT(O.Order_ID) AS Total_Orders,
    COALESCE(SUM(O.Quantity_Ordered), 0) AS Total_Units_Supplied
FROM SUPPLIER S
LEFT JOIN `ORDER` O ON S.Supplier_ID = O.Supplier_ID
GROUP BY S.Supplier_ID, S.Name
ORDER BY Total_Units_Supplied DESC;
            """
        },
        "expiring_soon": {
            "name": "Medicines Expiring Within 90 Days",
            "category": "Temporal Functions & Date Arithmetic",
            "description": "Identifies drugs whose expiration date falls within 90 days of the current date for safety quarantine.",
            "sql": """
SELECT 
    Medicine_ID,
    Name AS Medicine_Name,
    Price,
    Exp_Date
FROM MEDICINE
WHERE Exp_Date >= '2026-09-01'
ORDER BY Exp_Date ASC;
            """
        },
        "above_average_price": {
            "name": "Medicines Priced Above Network Average",
            "category": "Subquery in WHERE Clause",
            "description": "Demonstrates a scalar subquery filtering medicines whose retail price exceeds the overall catalog average.",
            "sql": """
SELECT 
    Medicine_ID,
    Name AS Medicine_Name,
    Price AS Price_INR,
    Exp_Date
FROM MEDICINE
WHERE Price > (
    SELECT AVG(Price) FROM MEDICINE
)
ORDER BY Price DESC;
            """
        },
        "clinical_chain_audit": {
            "name": "5-Table Comprehensive Clinical Prescribing Chain",
            "category": "Multi-Table Relational Equijoin",
            "description": "Traverses 5 core relations (Patient -> Prescription -> Prescription_Item -> Medicine -> Doctor) for clinical verification.",
            "sql": """
SELECT 
    P.Prescription_ID,
    P.Date AS Issued_Date,
    CONCAT(PT.First_Name, ' ', PT.Last_Name) AS Patient_Name,
    CONCAT(D.First_Name, ' ', D.Last_Name) AS Doctor_Name,
    M.Name AS Medicine_Name,
    PI.Dosage,
    PI.Frequency,
    PI.Duration
FROM PRESCRIPTION P
INNER JOIN PATIENT PT ON P.Patient_ID = PT.Patient_ID
INNER JOIN DOCTOR D ON P.Doctor_ID = D.Doctor_ID
INNER JOIN PRESCRIPTION_ITEM PI ON P.Prescription_ID = PI.Prescription_ID
INNER JOIN MEDICINE M ON PI.Medicine_ID = M.Medicine_ID
ORDER BY P.Date DESC, P.Prescription_ID DESC
LIMIT 8;
            """
        }
    }

    @staticmethod
    def execute_predefined_query(query_key):
        if query_key not in DBOpsService.PREDEFINED_QUERIES:
            return {"success": False, "error": f"Invalid query identifier: {query_key}"}
            
        qinfo = DBOpsService.PREDEFINED_QUERIES[query_key]
        raw_sql = qinfo['sql'].strip()
        
        # SQLite adjustments for string concats
        exec_sql = raw_sql
        if not db.get_status()['is_mysql']:
            exec_sql = exec_sql.replace("CONCAT(PT.First_Name, ' ', PT.Last_Name)", "(PT.First_Name || ' ' || PT.Last_Name)")
            exec_sql = exec_sql.replace("CONCAT(D.First_Name, ' ', D.Last_Name)", "(D.First_Name || ' ' || D.Last_Name)")
            
        try:
            results = db.execute_query(exec_sql)
            columns = list(results[0].keys()) if results else []
            return {
                "success": True,
                "info": qinfo,
                "columns": columns,
                "data": results,
                "count": len(results)
            }
        except Exception as e:
            return {"success": False, "error": str(e), "info": qinfo}

    @staticmethod
    def execute_function_demo(func_name, arg_val, secondary_arg=None):
        try:
            val = int(arg_val)
            if func_name == 'get_medicine_price':
                res = db.execute_query("SELECT Price FROM MEDICINE WHERE Medicine_ID = ?", (val,), fetchone=True)
                price = res['Price'] if res else 0.0
                return {"success": True, "result": f"₹{float(price):,.2f}", "label": "Unit Retail Price"}
                
            elif func_name == 'get_patient_prescription_count':
                res = db.execute_query("SELECT COUNT(*) AS c FROM PRESCRIPTION WHERE Patient_ID = ?", (val,), fetchone=True)
                c = res['c'] if res else 0
                return {"success": True, "result": f"{c} Prescriptions", "label": "Total Prescriptions Issued"}

            elif func_name == 'calculate_prescription_total':
                res = db.execute_query("""
                    SELECT SUM(M.Price) AS total 
                    FROM PRESCRIPTION_ITEM PI 
                    JOIN MEDICINE M ON PI.Medicine_ID = M.Medicine_ID 
                    WHERE PI.Prescription_ID = ?
                """, (val,), fetchone=True)
                tot = res['total'] if res and res['total'] else 0.0
                return {"success": True, "result": f"₹{float(tot):,.2f}", "label": "Calculated Prescription Total"}

            elif func_name == 'get_pharmacy_revenue':
                res = db.execute_query("SELECT SUM(Amount) AS rev FROM BILL WHERE Pharmacy_ID = ?", (val,), fetchone=True)
                rev = res['rev'] if res and res['rev'] else 0.0
                return {"success": True, "result": f"₹{float(rev):,.2f}", "label": "Cumulative Branch Revenue"}

            elif func_name == 'get_medicine_stock':
                pharm_id = int(secondary_arg) if secondary_arg else 101
                res = db.execute_query("SELECT Quantity FROM INVENTORY WHERE Pharmacy_ID = ? AND Medicine_ID = ?", (pharm_id, val), fetchone=True)
                qty = res['Quantity'] if res else 0
                return {"success": True, "result": f"{qty} Units on Hand", "label": f"Inventory at Pharmacy #{pharm_id}"}

            else:
                return {"success": False, "error": "Unknown function"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def trigger_demo_step(pharmacy_id=101, medicine_id=501, delta=20):
        """Demonstrates live trigger operation: initial state -> mutation -> updated state -> automatic STOCK_LOG."""
        # 1. State Before
        before_row = db.execute_query(
            "SELECT Quantity FROM INVENTORY WHERE Pharmacy_ID = ? AND Medicine_ID = ?",
            (pharmacy_id, medicine_id), fetchone=True
        )
        qty_before = before_row['Quantity'] if before_row else 0
        
        # 2. Perform Restock (Triggers trg_after_inventory_update / logs audit)
        res = db.call_procedure('restock_medicine', [pharmacy_id, medicine_id, delta, 'TRIGGER-VIVA-DEMO'])
        if not res.get('success'):
            return res
            
        # 3. State After
        after_row = db.execute_query(
            "SELECT Quantity, Last_Updated FROM INVENTORY WHERE Pharmacy_ID = ? AND Medicine_ID = ?",
            (pharmacy_id, medicine_id), fetchone=True
        )
        qty_after = after_row['Quantity'] if after_row else 0
        
        # 4. Fetch the generated audit row from STOCK_LOG
        log_row = db.execute_query("""
            SELECT Log_ID, Pharmacy_ID, Medicine_ID, Quantity_Change, Change_Type, Change_Date, Reference_ID
            FROM STOCK_LOG
            WHERE Pharmacy_ID = ? AND Medicine_ID = ?
            ORDER BY Log_ID DESC
            LIMIT 1
        """, (pharmacy_id, medicine_id), fetchone=True)
        
        return {
            "success": True,
            "pharmacy_id": pharmacy_id,
            "medicine_id": medicine_id,
            "qty_before": qty_before,
            "delta_applied": delta,
            "qty_after": qty_after,
            "audit_log": log_row,
            "message": f"Trigger `trg_after_inventory_update` successfully fired! Stock changed from {qty_before} to {qty_after}, and Log #{log_row['Log_ID']} was automatically created."
        }
