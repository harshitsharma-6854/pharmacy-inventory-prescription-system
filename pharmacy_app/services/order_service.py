from datetime import date
from services.db import db

class OrderService:
    @staticmethod
    def get_all(search=None, status=None, supplier_id=None):
        sql = """
        SELECT 
            O.Order_ID,
            O.Supplier_ID,
            O.Pharmacy_ID,
            O.Date,
            O.Arrival_Date,
            O.Payment_Status,
            O.Order_Status,
            O.Quantity_Ordered,
            S.Name AS Supplier_Name,
            S.Contact AS Supplier_Contact,
            PH.Name AS Pharmacy_Name,
            PH.City AS Pharmacy_City
        FROM `ORDER` O
        JOIN SUPPLIER S ON O.Supplier_ID = S.Supplier_ID
        JOIN PHARMACY PH ON O.Pharmacy_ID = PH.Pharmacy_ID
        WHERE 1=1
        """
        params = []
        if status:
            sql += " AND O.Order_Status = ?"
            params.append(status)
        if supplier_id:
            sql += " AND O.Supplier_ID = ?"
            params.append(supplier_id)
        if search:
            sql += " AND (S.Name LIKE ? OR PH.Name LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term])
            
        sql += " ORDER BY O.Order_ID DESC"
        return db.execute_query(sql, params)

    @staticmethod
    def create(data):
        order_id = data.get('order_id')
        if not order_id:
            max_row = db.execute_query("SELECT MAX(Order_ID) AS max_id FROM `ORDER`", fetchone=True)
            order_id = (max_row['max_id'] or 900) + 1
            
        supplier_id = int(data['supplier_id'])
        pharmacy_id = int(data['pharmacy_id'])
        quantity = int(data['quantity_ordered'])
        order_date = data.get('date') or date.today().isoformat()
        arrival_date = data.get('arrival_date')
        pay_status = data.get('payment_status', 'Pending')
        order_status = data.get('order_status', 'Pending')
        
        args = [
            int(order_id), supplier_id, pharmacy_id, quantity,
            order_date, arrival_date, pay_status, order_status
        ]
        res = db.call_procedure('place_order', args)
        if res.get('success'):
            res['order_id'] = order_id
        return res

    @staticmethod
    def update_status(order_id, order_status, payment_status=None):
        if payment_status:
            db.execute_mutation("""
                UPDATE `ORDER` 
                SET Order_Status = ?, Payment_Status = ?
                WHERE Order_ID = ?
            """, (order_status, payment_status, order_id))
        else:
            db.execute_mutation("""
                UPDATE `ORDER` 
                SET Order_Status = ?
                WHERE Order_ID = ?
            """, (order_status, order_id))
        return {"success": True, "message": f"Order #{order_id} status updated to {order_status}."}

    @staticmethod
    def get_suppliers_full():
        suppliers = db.execute_query("SELECT * FROM SUPPLIER ORDER BY Supplier_ID ASC")
        for s in suppliers:
            # Manufacturers distributed
            mfg = db.execute_query("""
                SELECT M.Manufacturer_ID, M.Brand_Name, M.City
                FROM SUPPLIER_MANUFACTURER SM
                JOIN MANUFACTURER M ON SM.Manufacturer_ID = M.Manufacturer_ID
                WHERE SM.Supplier_ID = ?
            """, (s['Supplier_ID'],))
            s['manufacturers'] = mfg
            
            # Wholesale GST affiliations
            ws = db.execute_query("""
                SELECT W.GST_No, W.City, W.State
                FROM SUPPLIER_WHOLESALE SW
                JOIN WHOLESALE_SUPPLIER W ON SW.GST_No = W.GST_No
                WHERE SW.Supplier_ID = ?
            """, (s['Supplier_ID'],))
            s['wholesale'] = ws
            
            # Pharmacies serviced
            pharm = db.execute_query("""
                SELECT P.Pharmacy_ID, P.Name, P.City
                FROM SUPPLIER_PHARMACY SP
                JOIN PHARMACY P ON SP.Pharmacy_ID = P.Pharmacy_ID
                WHERE SP.Supplier_ID = ?
            """, (s['Supplier_ID'],))
            s['pharmacies'] = pharm
            
            # Order performance
            stats = db.execute_query("""
                SELECT COUNT(*) AS total_orders,
                       COALESCE(SUM(Quantity_Ordered), 0) AS total_qty
                FROM `ORDER` WHERE Supplier_ID = ?
            """, (s['Supplier_ID'],), fetchone=True)
            s['stats'] = stats
            
        return suppliers
