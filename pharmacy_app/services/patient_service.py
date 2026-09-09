from services.db import db

class PatientService:
    @staticmethod
    def get_all(search=None, city=None, gender=None):
        sql = """
        SELECT 
            P.Patient_ID,
            P.First_Name,
            P.Last_Name,
            CONCAT(P.First_Name, ' ', P.Last_Name) AS Full_Name,
            P.DOB,
            P.Sex,
            P.City,
            P.State,
            P.Street,
            (SELECT GROUP_CONCAT(Contact_No SEPARATOR ', ') 
             FROM PATIENT_CONTACT PC WHERE PC.Patient_ID = P.Patient_ID) AS Contacts,
            (SELECT COUNT(*) FROM PRESCRIPTION PR WHERE PR.Patient_ID = P.Patient_ID) AS Prescription_Count,
            (SELECT COALESCE(SUM(B.Amount), 0.0) FROM BILL B WHERE B.Patient_ID = P.Patient_ID) AS Total_Spent
        FROM PATIENT P
        WHERE 1=1
        """
        # In SQLite GROUP_CONCAT syntax doesn't have SEPARATOR keyword
        if not db.get_status()['is_mysql']:
            sql = """
            SELECT 
                P.Patient_ID,
                P.First_Name,
                P.Last_Name,
                (P.First_Name || ' ' || P.Last_Name) AS Full_Name,
                P.DOB,
                P.Sex,
                P.City,
                P.State,
                P.Street,
                (SELECT GROUP_CONCAT(Contact_No) 
                 FROM PATIENT_CONTACT PC WHERE PC.Patient_ID = P.Patient_ID) AS Contacts,
                (SELECT COUNT(*) FROM PRESCRIPTION PR WHERE PR.Patient_ID = P.Patient_ID) AS Prescription_Count,
                (SELECT COALESCE(SUM(B.Amount), 0.0) FROM BILL B WHERE B.Patient_ID = P.Patient_ID) AS Total_Spent
            FROM PATIENT P
            WHERE 1=1
            """
        params = []
        if search:
            sql += " AND (P.First_Name LIKE ? OR P.Last_Name LIKE ? OR P.City LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term, term])
        if city:
            sql += " AND P.City = ?"
            params.append(city)
        if gender:
            sql += " AND P.Sex = ?"
            params.append(gender)
            
        sql += " ORDER BY P.Patient_ID ASC"
        return db.execute_query(sql, params)

    @staticmethod
    def get_by_id(patient_id):
        patient = db.execute_query(
            "SELECT * FROM PATIENT WHERE Patient_ID = ?", 
            (patient_id,), 
            fetchone=True
        )
        if not patient:
            return None
            
        contacts = db.execute_query(
            "SELECT Contact_No FROM PATIENT_CONTACT WHERE Patient_ID = ?", 
            (patient_id,)
        )
        patient['contacts'] = [c['Contact_No'] for c in contacts]
        
        # Prescriptions
        prescriptions = db.execute_query("""
            SELECT PR.Prescription_ID, PR.Date, 
                   D.First_Name AS Doctor_First, D.Last_Name AS Doctor_Last,
                   D.Qualification, H.Name AS Hospital_Name
            FROM PRESCRIPTION PR
            JOIN DOCTOR D ON PR.Doctor_ID = D.Doctor_ID
            JOIN HOSPITAL H ON D.Hospital_ID = H.Hospital_ID
            WHERE PR.Patient_ID = ?
            ORDER BY PR.Date DESC
        """, (patient_id,))
        patient['prescriptions'] = prescriptions
        
        # Bills
        bills = db.execute_query("""
            SELECT B.Bill_ID, B.Amount, PH.Name AS Pharmacy_Name, PH.City AS Pharmacy_City
            FROM BILL B
            JOIN PHARMACY PH ON B.Pharmacy_ID = PH.Pharmacy_ID
            WHERE B.Patient_ID = ?
            ORDER BY B.Bill_ID DESC
        """, (patient_id,))
        patient['bills'] = bills
        patient['total_spent'] = sum(b['Amount'] for b in bills)
        
        return patient

    @staticmethod
    def create(data):
        # Determine next ID if not provided
        patient_id = data.get('patient_id')
        if not patient_id:
            max_row = db.execute_query("SELECT MAX(Patient_ID) AS max_id FROM PATIENT", fetchone=True)
            patient_id = (max_row['max_id'] or 400) + 1
            
        args = [
            int(patient_id),
            data['first_name'].strip(),
            data['last_name'].strip(),
            data['dob'],
            data['sex'].upper(),
            data.get('street', 'Medical Enclave'),
            data.get('city', 'Mumbai'),
            data.get('state', 'Maharashtra'),
            data.get('contact_no', '')
        ]
        
        result = db.call_procedure('add_patient', args)
        if result.get('success'):
            result['patient_id'] = patient_id
        return result

    @staticmethod
    def update(patient_id, data):
        db.execute_mutation("""
            UPDATE PATIENT 
            SET First_Name = ?, Last_Name = ?, DOB = ?, Sex = ?, Street = ?, City = ?, State = ?
            WHERE Patient_ID = ?
        """, (
            data['first_name'], data['last_name'], data['dob'],
            data['sex'], data.get('street', ''), data.get('city', ''),
            data.get('state', ''), patient_id
        ))
        if data.get('contact_no'):
            db.execute_mutation("DELETE FROM PATIENT_CONTACT WHERE Patient_ID = ?", (patient_id,))
            db.execute_mutation("INSERT INTO PATIENT_CONTACT VALUES (?, ?)", (patient_id, data['contact_no']))
        return {"success": True, "message": "Patient record updated successfully."}

    @staticmethod
    def delete(patient_id):
        # Verify dependent bills/prescriptions
        bills = db.execute_query("SELECT COUNT(*) AS c FROM BILL WHERE Patient_ID = ?", (patient_id,), fetchone=True)
        if bills and bills['c'] > 0:
            return {"success": False, "error": "Cannot delete patient with existing billing transactions."}
        prescriptions = db.execute_query("SELECT COUNT(*) AS c FROM PRESCRIPTION WHERE Patient_ID = ?", (patient_id,), fetchone=True)
        if prescriptions and prescriptions['c'] > 0:
            return {"success": False, "error": "Cannot delete patient with registered medical prescriptions."}
            
        db.execute_mutation("DELETE FROM PATIENT_CONTACT WHERE Patient_ID = ?", (patient_id,))
        db.execute_mutation("DELETE FROM PATIENT WHERE Patient_ID = ?", (patient_id,))
        return {"success": True, "message": f"Patient #{patient_id} removed from system."}
