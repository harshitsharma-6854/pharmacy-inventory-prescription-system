from datetime import date
from services.db import db

class AnalyticsService:
    @staticmethod
    def get_dashboard_metrics():
        # 1. Patients count
        pat_row = db.execute_query("SELECT COUNT(*) AS c FROM PATIENT", fetchone=True)
        total_patients = pat_row['c'] if pat_row else 0
        
        # 2. Medicines count
        med_row = db.execute_query("SELECT COUNT(*) AS c FROM MEDICINE", fetchone=True)
        total_medicines = med_row['c'] if med_row else 0
        
        # 3. Prescriptions count
        presc_row = db.execute_query("SELECT COUNT(*) AS c FROM PRESCRIPTION", fetchone=True)
        total_prescriptions = presc_row['c'] if presc_row else 0
        
        # 4. Pharmacies count
        pharm_row = db.execute_query("SELECT COUNT(*) AS c FROM PHARMACY", fetchone=True)
        total_pharmacies = pharm_row['c'] if pharm_row else 0
        
        # 5. Low Stock count
        low_row = db.execute_query("""
            SELECT COUNT(*) AS c FROM INVENTORY WHERE Quantity <= Reorder_Level
        """, fetchone=True)
        low_stock_count = low_row['c'] if low_row else 0
        
        # 6. Pending Orders count
        pending_row = db.execute_query("""
            SELECT COUNT(*) AS c FROM `ORDER` WHERE Order_Status IN ('Pending', 'Processing')
        """, fetchone=True)
        pending_orders = pending_row['c'] if pending_row else 0
        
        # 7. Total Revenue
        rev_row = db.execute_query("SELECT COALESCE(SUM(Amount), 0.0) AS s FROM BILL", fetchone=True)
        total_revenue = rev_row['s'] if rev_row else 0.0
        
        # 8. Today's Revenue (or recent billing slice)
        today_rev_row = db.execute_query("""
            SELECT COALESCE(SUM(Amount), 0.0) AS s FROM BILL WHERE Bill_ID >= 1110
        """, fetchone=True)
        today_revenue = today_rev_row['s'] if today_rev_row else 0.0
        
        return {
            "total_patients": total_patients,
            "total_medicines": total_medicines,
            "total_prescriptions": total_prescriptions,
            "total_pharmacies": total_pharmacies,
            "low_stock_count": low_stock_count,
            "pending_orders": pending_orders,
            "total_revenue": total_revenue,
            "today_revenue": today_revenue
        }

    @staticmethod
    def get_dashboard_charts():
        # Chart 1: Revenue by Pharmacy Branch
        rev_data = db.execute_query("""
            SELECT PH.Name AS pharmacy, COALESCE(SUM(B.Amount), 0.0) AS revenue
            FROM PHARMACY PH
            LEFT JOIN BILL B ON PH.Pharmacy_ID = B.Pharmacy_ID
            GROUP BY PH.Pharmacy_ID, PH.Name
            ORDER BY revenue DESC
        """)
        chart_revenue = {
            "labels": [r['pharmacy'].split()[0] for r in rev_data],
            "full_labels": [r['pharmacy'] for r in rev_data],
            "values": [float(r['revenue']) for r in rev_data]
        }
        
        # Chart 2: Prescription Trends (By Date)
        presc_trend = db.execute_query("""
            SELECT Date, COUNT(*) AS count
            FROM PRESCRIPTION
            GROUP BY Date
            ORDER BY Date ASC
        """)
        chart_prescriptions = {
            "labels": [r['Date'] for r in presc_trend],
            "values": [r['count'] for r in presc_trend]
        }
        
        # Chart 3: Inventory Distribution (Top Formulations on Hand)
        inv_dist = db.execute_query("""
            SELECT M.Name AS medicine, SUM(INV.Quantity) AS quantity
            FROM MEDICINE M
            JOIN INVENTORY INV ON M.Medicine_ID = INV.Medicine_ID
            GROUP BY M.Medicine_ID, M.Name
            ORDER BY quantity DESC
            LIMIT 7
        """)
        chart_inventory = {
            "labels": [r['medicine'].split('(')[0].strip() for r in inv_dist],
            "values": [r['quantity'] for r in inv_dist]
        }
        
        # Chart 4: Order Status Breakdown
        order_status = db.execute_query("""
            SELECT Order_Status, COUNT(*) AS count
            FROM `ORDER`
            GROUP BY Order_Status
        """)
        chart_orders = {
            "labels": [r['Order_Status'] for r in order_status],
            "values": [r['count'] for r in order_status]
        }
        
        # Chart 5: Low Stock Medicines Alert (< Reorder Level)
        low_stock = db.execute_query("""
            SELECT M.Name AS medicine, INV.Quantity, INV.Reorder_Level, PH.Name AS pharmacy
            FROM INVENTORY INV
            JOIN MEDICINE M ON INV.Medicine_ID = M.Medicine_ID
            JOIN PHARMACY PH ON INV.Pharmacy_ID = PH.Pharmacy_ID
            WHERE INV.Quantity <= INV.Reorder_Level
            ORDER BY INV.Quantity ASC
            LIMIT 6
        """)
        chart_low_stock = {
            "labels": [f"{r['medicine'].split('(')[0].strip()} ({r['pharmacy'].split()[0]})" for r in low_stock],
            "stock": [r['Quantity'] for r in low_stock],
            "reorder": [r['Reorder_Level'] for r in low_stock]
        }
        
        # Chart 6: Top 5 Most Prescribed Medicines
        top_presc = db.execute_query("""
            SELECT M.Name AS medicine, COUNT(PI.Item_ID) AS freq
            FROM MEDICINE M
            JOIN PRESCRIPTION_ITEM PI ON M.Medicine_ID = PI.Medicine_ID
            GROUP BY M.Medicine_ID, M.Name
            ORDER BY freq DESC
            LIMIT 5
        """)
        chart_top_medicines = {
            "labels": [r['medicine'].split('(')[0].strip() for r in top_presc],
            "values": [r['freq'] for r in top_presc]
        }
        
        return {
            "revenue": chart_revenue,
            "prescriptions": chart_prescriptions,
            "inventory": chart_inventory,
            "orders": chart_orders,
            "low_stock": chart_low_stock,
            "top_medicines": chart_top_medicines
        }

    @staticmethod
    def get_report(report_type, pharmacy_id=None, date_from=None, date_to=None):
        if report_type == 'inventory':
            sql = """
            SELECT M.Medicine_ID, M.Name AS Medicine_Name, M.Price, M.Exp_Date,
                   PH.Name AS Pharmacy_Name, INV.Quantity, INV.Reorder_Level,
                   (INV.Quantity * M.Price) AS Total_Stock_Valuation
            FROM INVENTORY INV
            JOIN MEDICINE M ON INV.Medicine_ID = M.Medicine_ID
            JOIN PHARMACY PH ON INV.Pharmacy_ID = PH.Pharmacy_ID
            WHERE 1=1
            """
            params = []
            if pharmacy_id:
                sql += " AND INV.Pharmacy_ID = ?"
                params.append(pharmacy_id)
            sql += " ORDER BY INV.Quantity ASC"
            return db.execute_query(sql, params)
            
        elif report_type == 'low_stock':
            sql = """
            SELECT M.Medicine_ID, M.Name AS Medicine_Name, M.Price,
                   PH.Name AS Pharmacy_Name, INV.Quantity, INV.Reorder_Level,
                   (INV.Reorder_Level - INV.Quantity) AS Units_Deficit
            FROM INVENTORY INV
            JOIN MEDICINE M ON INV.Medicine_ID = M.Medicine_ID
            JOIN PHARMACY PH ON INV.Pharmacy_ID = PH.Pharmacy_ID
            WHERE INV.Quantity <= INV.Reorder_Level
            """
            params = []
            if pharmacy_id:
                sql += " AND INV.Pharmacy_ID = ?"
                params.append(pharmacy_id)
            sql += " ORDER BY INV.Quantity ASC"
            return db.execute_query(sql, params)

        elif report_type == 'expired':
            today_str = date.today().isoformat()
            return db.execute_query("""
                SELECT M.Medicine_ID, M.Name AS Medicine_Name, M.Exp_Date, M.Price,
                       PH.Name AS Pharmacy_Name, INV.Quantity
                FROM MEDICINE M
                LEFT JOIN INVENTORY INV ON M.Medicine_ID = INV.Medicine_ID
                LEFT JOIN PHARMACY PH ON INV.Pharmacy_ID = PH.Pharmacy_ID
                WHERE M.Exp_Date < ?
                ORDER BY M.Exp_Date ASC
            """, (today_str,))

        elif report_type == 'revenue':
            sql = """
            SELECT B.Bill_ID, B.Amount, PH.Name AS Pharmacy_Name,
                   CONCAT(P.First_Name, ' ', P.Last_Name) AS Patient_Name,
                   P.City AS Patient_City
            FROM BILL B
            JOIN PHARMACY PH ON B.Pharmacy_ID = PH.Pharmacy_ID
            JOIN PATIENT P ON B.Patient_ID = P.Patient_ID
            WHERE 1=1
            """
            params = []
            if pharmacy_id:
                sql += " AND B.Pharmacy_ID = ?"
                params.append(pharmacy_id)
            sql += " ORDER BY B.Bill_ID DESC"
            return db.execute_query(sql, params)

        elif report_type == 'doctor_perf':
            return db.execute_query("""
                SELECT D.Doctor_ID, CONCAT(D.First_Name, ' ', D.Last_Name) AS Doctor_Name,
                       D.Qualification, D.Experience, H.Name AS Hospital_Name,
                       COUNT(PR.Prescription_ID) AS Prescriptions_Issued
                FROM DOCTOR D
                JOIN HOSPITAL H ON D.Hospital_ID = H.Hospital_ID
                LEFT JOIN PRESCRIPTION PR ON D.Doctor_ID = PR.Doctor_ID
                GROUP BY D.Doctor_ID, D.First_Name, D.Last_Name, D.Qualification, D.Experience, H.Name
                ORDER BY Prescriptions_Issued DESC
            """)

        elif report_type == 'supplier_perf':
            return db.execute_query("""
                SELECT S.Supplier_ID, S.Name AS Supplier_Name, S.City,
                       COUNT(O.Order_ID) AS Orders_Handled,
                       COALESCE(SUM(O.Quantity_Ordered), 0) AS Units_Supplied,
                       SUM(CASE WHEN O.Order_Status = 'Delivered' THEN 1 ELSE 0 END) AS Completed_Deliveries
                FROM SUPPLIER S
                LEFT JOIN `ORDER` O ON S.Supplier_ID = O.Supplier_ID
                GROUP BY S.Supplier_ID, S.Name, S.City
                ORDER BY Units_Supplied DESC
            """)

        else:
            return []
