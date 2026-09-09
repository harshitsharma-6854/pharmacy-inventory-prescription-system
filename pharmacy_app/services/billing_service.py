from services.db import db

class BillingService:
    @staticmethod
    def get_all(search=None, pharmacy_id=None):
        sql = """
        SELECT 
            B.Bill_ID,
            B.Amount,
            B.Pharmacy_ID,
            B.Patient_ID,
            PH.Name AS Pharmacy_Name,
            PH.City AS Pharmacy_City,
            P.First_Name AS Patient_First,
            P.Last_Name AS Patient_Last,
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
        if search:
            sql += " AND (P.First_Name LIKE ? OR P.Last_Name LIKE ? OR PH.Name LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term, term])
            
        sql += " ORDER BY B.Bill_ID DESC"
        return db.execute_query(sql, params)

    @staticmethod
    def get_by_id(bill_id):
        sql = """
        SELECT 
            B.Bill_ID,
            B.Amount,
            B.Pharmacy_ID,
            B.Patient_ID,
            PH.Name AS Pharmacy_Name,
            PH.Street AS Pharmacy_Street,
            PH.City AS Pharmacy_City,
            PH.State AS Pharmacy_State,
            PH.Contact_No AS Pharmacy_Contact,
            P.First_Name AS Patient_First,
            P.Last_Name AS Patient_Last,
            P.Street AS Patient_Street,
            P.City AS Patient_City,
            P.State AS Patient_State
        FROM BILL B
        JOIN PHARMACY PH ON B.Pharmacy_ID = PH.Pharmacy_ID
        JOIN PATIENT P ON B.Patient_ID = P.Patient_ID
        WHERE B.Bill_ID = ?
        """
        bill = db.execute_query(sql, (bill_id,), fetchone=True)
        if not bill:
            return None
            
        # Look up prescription for this patient around billing
        presc = db.execute_query("""
            SELECT PR.Prescription_ID, PR.Date, 
                   D.First_Name AS Doctor_First, D.Last_Name AS Doctor_Last
            FROM PRESCRIPTION PR
            JOIN DOCTOR D ON PR.Doctor_ID = D.Doctor_ID
            WHERE PR.Patient_ID = ?
            ORDER BY PR.Prescription_ID DESC
            LIMIT 1
        """, (bill['Patient_ID'],), fetchone=True)
        
        bill['prescription'] = presc
        
        if presc:
            items = db.execute_query("""
                SELECT PI.Item_ID, PI.Dosage, PI.Frequency, PI.Duration,
                       M.Name AS Medicine_Name, M.Price
                FROM PRESCRIPTION_ITEM PI
                JOIN MEDICINE M ON PI.Medicine_ID = M.Medicine_ID
                WHERE PI.Prescription_ID = ?
            """, (presc['Prescription_ID'],))
            bill['items'] = items
        else:
            bill['items'] = []
            
        return bill

    @staticmethod
    def generate_bill(data):
        bill_id = data.get('bill_id')
        if not bill_id:
            max_row = db.execute_query("SELECT MAX(Bill_ID) AS max_id FROM BILL", fetchone=True)
            bill_id = (max_row['max_id'] or 1100) + 1
            
        pharmacy_id = int(data['pharmacy_id'])
        patient_id = int(data['patient_id'])
        prescription_id = int(data['prescription_id'])
        
        args = [int(bill_id), pharmacy_id, patient_id, prescription_id]
        res = db.call_procedure('generate_bill', args)
        if res.get('success'):
            res['bill_id'] = bill_id
        return res
