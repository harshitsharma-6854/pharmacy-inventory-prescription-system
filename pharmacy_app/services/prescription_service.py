from datetime import date
from services.db import db

class PrescriptionService:
    @staticmethod
    def get_all(search=None, date_from=None, date_to=None):
        sql = """
        SELECT 
            PR.Prescription_ID,
            PR.Date,
            PR.Patient_ID,
            PR.Doctor_ID,
            P.First_Name AS Patient_First,
            P.Last_Name AS Patient_Last,
            D.First_Name AS Doctor_First,
            D.Last_Name AS Doctor_Last,
            D.Qualification,
            H.Name AS Hospital_Name,
            (SELECT COUNT(*) FROM PRESCRIPTION_ITEM PI WHERE PI.Prescription_ID = PR.Prescription_ID) AS Item_Count,
            (SELECT COALESCE(SUM(M.Price), 0.0) 
             FROM PRESCRIPTION_ITEM PI2 
             JOIN MEDICINE M ON PI2.Medicine_ID = M.Medicine_ID 
             WHERE PI2.Prescription_ID = PR.Prescription_ID) AS Estimated_Cost
        FROM PRESCRIPTION PR
        JOIN PATIENT P ON PR.Patient_ID = P.Patient_ID
        JOIN DOCTOR D ON PR.Doctor_ID = D.Doctor_ID
        JOIN HOSPITAL H ON D.Hospital_ID = H.Hospital_ID
        WHERE 1=1
        """
        params = []
        if search:
            sql += " AND (P.First_Name LIKE ? OR P.Last_Name LIKE ? OR D.First_Name LIKE ? OR D.Last_Name LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term, term, term])
        if date_from:
            sql += " AND PR.Date >= ?"
            params.append(date_from)
        if date_to:
            sql += " AND PR.Date <= ?"
            params.append(date_to)
            
        sql += " ORDER BY PR.Date DESC, PR.Prescription_ID DESC"
        return db.execute_query(sql, params)

    @staticmethod
    def get_by_id(prescription_id):
        sql = """
        SELECT 
            PR.Prescription_ID,
            PR.Date,
            P.Patient_ID,
            P.First_Name AS Patient_First,
            P.Last_Name AS Patient_Last,
            P.DOB,
            P.Sex,
            P.City AS Patient_City,
            D.Doctor_ID,
            D.First_Name AS Doctor_First,
            D.Last_Name AS Doctor_Last,
            D.Qualification,
            D.Contact_No AS Doctor_Contact,
            H.Name AS Hospital_Name,
            H.City AS Hospital_City
        FROM PRESCRIPTION PR
        JOIN PATIENT P ON PR.Patient_ID = P.Patient_ID
        JOIN DOCTOR D ON PR.Doctor_ID = D.Doctor_ID
        JOIN HOSPITAL H ON D.Hospital_ID = H.Hospital_ID
        WHERE PR.Prescription_ID = ?
        """
        prescription = db.execute_query(sql, (prescription_id,), fetchone=True)
        if not prescription:
            return None
            
        # Get itemized medications
        items = db.execute_query("""
            SELECT PI.Item_ID, PI.Dosage, PI.Frequency, PI.Duration,
                   M.Medicine_ID, M.Name AS Medicine_Name, M.Price, M.Exp_Date
            FROM PRESCRIPTION_ITEM PI
            JOIN MEDICINE M ON PI.Medicine_ID = M.Medicine_ID
            WHERE PI.Prescription_ID = ?
        """, (prescription_id,))
        prescription['items'] = items
        prescription['total_amount'] = sum(item['Price'] for item in items)
        
        # Check if billed
        bill = db.execute_query("""
            SELECT Bill_ID, Amount, Pharmacy_ID FROM BILL 
            WHERE Patient_ID = ? ORDER BY Bill_ID DESC LIMIT 1
        """, (prescription['Patient_ID'],), fetchone=True)
        prescription['linked_bill'] = bill
        
        return prescription

    @staticmethod
    def create(data):
        # 1. Determine next Prescription_ID
        presc_id = data.get('prescription_id')
        if not presc_id:
            max_row = db.execute_query("SELECT MAX(Prescription_ID) AS max_id FROM PRESCRIPTION", fetchone=True)
            presc_id = (max_row['max_id'] or 1000) + 1
            
        doctor_id = int(data['doctor_id'])
        patient_id = int(data['patient_id'])
        presc_date = data.get('date') or date.today().isoformat()
        
        # Call procedure create_prescription
        args = [int(presc_id), doctor_id, patient_id, presc_date]
        res = db.call_procedure('create_prescription', args)
        if not res.get('success'):
            return res
            
        # Insert prescription items
        items = data.get('items', [])
        for item in items:
            med_id = int(item['medicine_id'])
            dosage = item.get('dosage', 'Standard')
            frequency = item.get('frequency', 'Once Daily')
            duration = item.get('duration', '5 Days')
            
            db.execute_mutation("""
                INSERT INTO PRESCRIPTION_ITEM (Prescription_ID, Medicine_ID, Dosage, Frequency, Duration)
                VALUES (?, ?, ?, ?, ?)
            """, (presc_id, med_id, dosage, frequency, duration))
            
        return {
            "success": True, 
            "message": f"Prescription #{presc_id} created with {len(items)} medicines.",
            "prescription_id": presc_id
        }

    @staticmethod
    def get_all_items():
        sql = """
        SELECT PI.Item_ID, PI.Prescription_ID, PI.Dosage, PI.Frequency, PI.Duration,
               M.Medicine_ID, M.Name AS Medicine_Name, M.Price,
               P.First_Name AS Patient_First, P.Last_Name AS Patient_Last,
               PR.Date AS Prescription_Date
        FROM PRESCRIPTION_ITEM PI
        JOIN MEDICINE M ON PI.Medicine_ID = M.Medicine_ID
        JOIN PRESCRIPTION PR ON PI.Prescription_ID = PR.Prescription_ID
        JOIN PATIENT P ON PR.Patient_ID = P.Patient_ID
        ORDER BY PI.Item_ID DESC
        """
        return db.execute_query(sql)
