from datetime import date
from services.db import db

class MedicineService:
    @staticmethod
    def get_all(search=None, status_filter=None, pharmacy_id=None):
        sql = """
        SELECT 
            M.Medicine_ID,
            M.Name,
            M.Price,
            M.Manu_Date,
            M.Exp_Date,
            COALESCE(SUM(INV.Quantity), 0) AS Total_Stock,
            COALESCE(AVG(INV.Reorder_Level), 15) AS Avg_Reorder,
            (SELECT COUNT(*) FROM PRESCRIPTION_ITEM PI WHERE PI.Medicine_ID = M.Medicine_ID) AS Prescribed_Count
        FROM MEDICINE M
        LEFT JOIN INVENTORY INV ON M.Medicine_ID = INV.Medicine_ID
        """
        params = []
        if pharmacy_id:
            sql += " AND INV.Pharmacy_ID = ?"
            params.append(pharmacy_id)
            
        sql += " WHERE 1=1"
        if search:
            sql += " AND M.Name LIKE ?"
            params.append(f"%{search}%")
            
        sql += " GROUP BY M.Medicine_ID, M.Name, M.Price, M.Manu_Date, M.Exp_Date"
        rows = db.execute_query(sql, params)
        
        # Calculate status badge
        today_str = date.today().isoformat()
        results = []
        for r in rows:
            stock = r['Total_Stock']
            reorder = r['Avg_Reorder']
            exp = str(r['Exp_Date'])
            
            if exp < today_str:
                status = "EXPIRED"
                badge_class = "danger"
            elif stock == 0:
                status = "OUT OF STOCK"
                badge_class = "dark"
            elif stock <= reorder:
                status = "LOW STOCK"
                badge_class = "warning"
            else:
                status = "IN STOCK"
                badge_class = "success"
                
            r['status'] = status
            r['badge_class'] = badge_class
            
            if not status_filter or status_filter.upper() == status.replace(" ", "_"):
                results.append(r)
                
        return results

    @staticmethod
    def get_by_id(medicine_id):
        medicine = db.execute_query(
            "SELECT * FROM MEDICINE WHERE Medicine_ID = ?", 
            (medicine_id,), 
            fetchone=True
        )
        if not medicine:
            return None
            
        # Inventory per pharmacy branch
        inventory = db.execute_query("""
            SELECT INV.Inventory_ID, INV.Pharmacy_ID, INV.Quantity, INV.Reorder_Level, INV.Last_Updated,
                   PH.Name AS Pharmacy_Name, PH.City AS Pharmacy_City
            FROM INVENTORY INV
            JOIN PHARMACY PH ON INV.Pharmacy_ID = PH.Pharmacy_ID
            WHERE INV.Medicine_ID = ?
        """, (medicine_id,))
        medicine['inventory'] = inventory
        
        # Stock mutation logs
        logs = db.execute_query("""
            SELECT SL.Log_ID, SL.Quantity_Change, SL.Change_Type, SL.Change_Date, SL.Reference_ID,
                   PH.Name AS Pharmacy_Name
            FROM STOCK_LOG SL
            JOIN PHARMACY PH ON SL.Pharmacy_ID = PH.Pharmacy_ID
            WHERE SL.Medicine_ID = ?
            ORDER BY SL.Change_Date DESC
            LIMIT 10
        """, (medicine_id,))
        medicine['logs'] = logs
        
        # Prescription items
        presc_stats = db.execute_query("""
            SELECT COUNT(*) AS total_prescribed
            FROM PRESCRIPTION_ITEM
            WHERE Medicine_ID = ?
        """, (medicine_id,), fetchone=True)
        medicine['prescribed_count'] = presc_stats['total_prescribed'] if presc_stats else 0
        
        return medicine

    @staticmethod
    def create(data):
        medicine_id = data.get('medicine_id')
        if not medicine_id:
            max_row = db.execute_query("SELECT MAX(Medicine_ID) AS max_id FROM MEDICINE", fetchone=True)
            medicine_id = (max_row['max_id'] or 500) + 1
            
        args = [
            int(medicine_id),
            data['name'].strip(),
            data['manu_date'],
            data['exp_date'],
            float(data['price']),
            int(data.get('pharmacy_id', 101)),
            int(data.get('initial_stock', 50)),
            int(data.get('reorder_level', 15))
        ]
        
        result = db.call_procedure('add_medicine', args)
        if result.get('success'):
            result['medicine_id'] = medicine_id
        return result

    @staticmethod
    def restock(data):
        pharmacy_id = int(data['pharmacy_id'])
        medicine_id = int(data['medicine_id'])
        quantity = int(data['quantity'])
        reference_id = data.get('reference_id', 'WEB-RESTOCK')
        
        args = [pharmacy_id, medicine_id, quantity, reference_id]
        return db.call_procedure('restock_medicine', args)

    @staticmethod
    def get_stock_logs(limit=30):
        sql = """
        SELECT SL.Log_ID, SL.Quantity_Change, SL.Change_Type, SL.Change_Date, SL.Reference_ID,
               M.Name AS Medicine_Name, PH.Name AS Pharmacy_Name
        FROM STOCK_LOG SL
        JOIN MEDICINE M ON SL.Medicine_ID = M.Medicine_ID
        JOIN PHARMACY PH ON SL.Pharmacy_ID = PH.Pharmacy_ID
        ORDER BY SL.Log_ID DESC
        LIMIT ?
        """
        return db.execute_query(sql, (limit,))
