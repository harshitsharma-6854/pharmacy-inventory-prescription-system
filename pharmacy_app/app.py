import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for

# Ensure base directory is on sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import Config
from services.db import db
from services.patient_service import PatientService
from services.medicine_service import MedicineService
from services.prescription_service import PrescriptionService
from services.billing_service import BillingService
from services.order_service import OrderService
from services.analytics_service import AnalyticsService
from services.db_ops_service import DBOpsService
from utils.helpers import format_currency, success_response, error_response
from utils.validators import validate_patient_data, validate_medicine_data, validate_restock_data

app = Flask(__name__)
app.config.from_object(Config)

# Register custom template filters
@app.template_filter('currency')
def currency_filter(val):
    return format_currency(val)

# Global context processor
@app.context_processor
def inject_global_vars():
    status = db.get_status()
    return {
        "db_status": status,
        "app_name": "PHARMA Care & Inventory"
    }

# ============================================================================
# HTML VIEW ROUTES
# ============================================================================

@app.route('/')
def dashboard_view():
    metrics = AnalyticsService.get_dashboard_metrics()
    return render_template('dashboard.html', metrics=metrics, active_page='dashboard')

@app.route('/patients')
def patients_view():
    search = request.args.get('search')
    city = request.args.get('city')
    gender = request.args.get('gender')
    patients = PatientService.get_all(search, city, gender)
    cities = db.execute_query("SELECT DISTINCT City FROM PATIENT ORDER BY City")
    return render_template('patients.html', patients=patients, cities=cities, active_page='patients')

@app.route('/doctors')
def doctors_view():
    sql = """
    SELECT D.Doctor_ID, D.First_Name, D.Last_Name, D.Qualification, D.Experience, D.Contact_No,
           H.Name AS Hospital_Name, H.City AS Hospital_City,
           (SELECT COUNT(*) FROM PRESCRIPTION P WHERE P.Doctor_ID = D.Doctor_ID) AS Prescriptions_Count
    FROM DOCTOR D
    JOIN HOSPITAL H ON D.Hospital_ID = H.Hospital_ID
    ORDER BY D.Experience DESC
    """
    doctors = db.execute_query(sql)
    hospitals = db.execute_query("SELECT Hospital_ID, Name FROM HOSPITAL ORDER BY Name")
    return render_template('doctors.html', doctors=doctors, hospitals=hospitals, active_page='doctors')

@app.route('/pharmacists')
def pharmacists_view():
    sql = """
    SELECT PHR.Pharmacist_ID, PHR.Name, PHR.Shift,
           PH.Name AS Pharmacy_Name, PH.City AS Pharmacy_City
    FROM PHARMACIST PHR
    JOIN PHARMACY PH ON PHR.Pharmacy_ID = PH.Pharmacy_ID
    ORDER BY PHR.Pharmacist_ID ASC
    """
    pharmacists = db.execute_query(sql)
    pharmacies = db.execute_query("SELECT Pharmacy_ID, Name FROM PHARMACY ORDER BY Name")
    return render_template('pharmacists.html', pharmacists=pharmacists, pharmacies=pharmacies, active_page='pharmacists')

@app.route('/pharmacies')
def pharmacies_view():
    sql = """
    SELECT PH.Pharmacy_ID, PH.Name, PH.Rating, PH.Street, PH.City, PH.State, PH.Contact_No,
           (SELECT COUNT(*) FROM PHARMACIST P WHERE P.Pharmacy_ID = PH.Pharmacy_ID) AS Pharmacist_Count,
           (SELECT COUNT(*) FROM BILL B WHERE B.Pharmacy_ID = PH.Pharmacy_ID) AS Bills_Count,
           (SELECT COALESCE(SUM(B.Amount), 0.0) FROM BILL B WHERE B.Pharmacy_ID = PH.Pharmacy_ID) AS Revenue
    FROM PHARMACY PH
    ORDER BY PH.Pharmacy_ID ASC
    """
    pharmacies = db.execute_query(sql)
    return render_template('pharmacies.html', pharmacies=pharmacies, active_page='pharmacies')

@app.route('/hospitals')
def hospitals_view():
    sql = """
    SELECT H.Hospital_ID, H.Name, H.City, H.State, H.Street, H.Contact,
           PH.Name AS Affiliated_Pharmacy,
           (SELECT COUNT(*) FROM DOCTOR D WHERE D.Hospital_ID = H.Hospital_ID) AS Doctor_Count
    FROM HOSPITAL H
    JOIN PHARMACY PH ON H.Pharmacy_ID = PH.Pharmacy_ID
    ORDER BY H.Hospital_ID ASC
    """
    hospitals = db.execute_query(sql)
    return render_template('hospitals.html', hospitals=hospitals, active_page='hospitals')

@app.route('/medicines')
def medicines_view():
    search = request.args.get('search')
    status = request.args.get('status')
    pharmacy_id = request.args.get('pharmacy_id')
    medicines = MedicineService.get_all(search, status, pharmacy_id)
    pharmacies = db.execute_query("SELECT Pharmacy_ID, Name FROM PHARMACY ORDER BY Name")
    return render_template('medicines.html', medicines=medicines, pharmacies=pharmacies, active_page='medicines')

@app.route('/stock')
def stock_view():
    sql = """
    SELECT INV.Inventory_ID, INV.Pharmacy_ID, INV.Quantity, INV.Reorder_Level, INV.Last_Updated,
           PH.Name AS Pharmacy_Name, PH.City AS Pharmacy_City,
           M.Medicine_ID, M.Name AS Medicine_Name, M.Price
    FROM INVENTORY INV
    JOIN PHARMACY PH ON INV.Pharmacy_ID = PH.Pharmacy_ID
    JOIN MEDICINE M ON INV.Medicine_ID = M.Medicine_ID
    ORDER BY INV.Quantity ASC
    """
    inventory = db.execute_query(sql)
    logs = MedicineService.get_stock_logs(20)
    pharmacies = db.execute_query("SELECT Pharmacy_ID, Name FROM PHARMACY ORDER BY Name")
    medicines = db.execute_query("SELECT Medicine_ID, Name FROM MEDICINE ORDER BY Name")
    return render_template('stock.html', inventory=inventory, logs=logs, pharmacies=pharmacies, medicines=medicines, active_page='stock')

@app.route('/suppliers')
def suppliers_view():
    suppliers = OrderService.get_suppliers_full()
    return render_template('suppliers.html', suppliers=suppliers, active_page='suppliers')

@app.route('/orders')
def orders_view():
    status = request.args.get('status')
    supplier_id = request.args.get('supplier_id')
    search = request.args.get('search')
    orders = OrderService.get_all(search, status, supplier_id)
    suppliers = db.execute_query("SELECT Supplier_ID, Name FROM SUPPLIER ORDER BY Name")
    pharmacies = db.execute_query("SELECT Pharmacy_ID, Name FROM PHARMACY ORDER BY Name")
    return render_template('orders.html', orders=orders, suppliers=suppliers, pharmacies=pharmacies, active_page='orders')

@app.route('/prescriptions')
def prescriptions_view():
    search = request.args.get('search')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    prescriptions = PrescriptionService.get_all(search, date_from, date_to)
    patients = db.execute_query("SELECT Patient_ID, First_Name, Last_Name FROM PATIENT ORDER BY First_Name")
    doctors = db.execute_query("SELECT Doctor_ID, First_Name, Last_Name, Qualification FROM DOCTOR ORDER BY First_Name")
    medicines = db.execute_query("SELECT Medicine_ID, Name, Price FROM MEDICINE ORDER BY Name")
    return render_template('prescriptions.html', prescriptions=prescriptions, patients=patients, doctors=doctors, medicines=medicines, active_page='prescriptions')

@app.route('/prescription-items')
def prescription_items_view():
    items = PrescriptionService.get_all_items()
    return render_template('prescription_items.html', items=items, active_page='prescriptions')

@app.route('/bills')
def bills_view():
    search = request.args.get('search')
    pharmacy_id = request.args.get('pharmacy_id')
    bills = BillingService.get_all(search, pharmacy_id)
    pharmacies = db.execute_query("SELECT Pharmacy_ID, Name FROM PHARMACY ORDER BY Name")
    prescriptions = db.execute_query("""
        SELECT PR.Prescription_ID, PR.Date, P.Patient_ID, P.First_Name, P.Last_Name
        FROM PRESCRIPTION PR
        JOIN PATIENT P ON PR.Patient_ID = P.Patient_ID
        ORDER BY PR.Prescription_ID DESC
    """)
    return render_template('bills.html', bills=bills, pharmacies=pharmacies, prescriptions=prescriptions, active_page='bills')

@app.route('/reports')
def reports_view():
    report_type = request.args.get('type', 'inventory')
    pharmacy_id = request.args.get('pharmacy_id')
    data = AnalyticsService.get_report(report_type, pharmacy_id)
    pharmacies = db.execute_query("SELECT Pharmacy_ID, Name FROM PHARMACY ORDER BY Name")
    return render_template('reports.html', report_type=report_type, report_data=data, pharmacies=pharmacies, active_page='reports')

@app.route('/db-operations')
def db_operations_view():
    queries = DBOpsService.PREDEFINED_QUERIES
    pharmacies = db.execute_query("SELECT Pharmacy_ID, Name FROM PHARMACY ORDER BY Name")
    medicines = db.execute_query("SELECT Medicine_ID, Name, Price FROM MEDICINE ORDER BY Name")
    patients = db.execute_query("SELECT Patient_ID, First_Name, Last_Name FROM PATIENT ORDER BY First_Name")
    doctors = db.execute_query("SELECT Doctor_ID, First_Name, Last_Name FROM DOCTOR ORDER BY First_Name")
    prescriptions = db.execute_query("SELECT Prescription_ID, Patient_ID FROM PRESCRIPTION ORDER BY Prescription_ID DESC")
    suppliers = db.execute_query("SELECT Supplier_ID, Name FROM SUPPLIER ORDER BY Name")
    return render_template(
        'db_operations.html', 
        queries=queries, 
        pharmacies=pharmacies, 
        medicines=medicines,
        patients=patients,
        doctors=doctors,
        prescriptions=prescriptions,
        suppliers=suppliers,
        active_page='db_operations'
    )

@app.route('/settings')
def settings_view():
    status = db.get_status()
    table_counts = {}
    tables = ['PHARMACY', 'PATIENT', 'HOSPITAL', 'DOCTOR', 'PRESCRIPTION', 'MEDICINE', 
              'PRESCRIPTION_ITEM', 'BILL', 'PHARMACIST', 'MANUFACTURER', 'SUPPLIER', 'ORDER', 'INVENTORY', 'STOCK_LOG']
    for t in tables:
        try:
            r = db.execute_query(f"SELECT COUNT(*) AS c FROM `{t}`", fetchone=True)
            table_counts[t] = r['c'] if r else 0
        except Exception:
            table_counts[t] = 0
            
    return render_template('settings.html', status=status, table_counts=table_counts, active_page='settings')


# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@app.route('/api/system/status')
def api_system_status():
    return jsonify(db.get_status())

@app.route('/api/dashboard/metrics')
def api_dashboard_metrics():
    return jsonify(AnalyticsService.get_dashboard_metrics())

@app.route('/api/dashboard/charts')
def api_dashboard_charts():
    return jsonify(AnalyticsService.get_dashboard_charts())

@app.route('/api/patients', methods=['GET', 'POST'])
def api_patients():
    if request.method == 'GET':
        search = request.args.get('search')
        city = request.args.get('city')
        gender = request.args.get('gender')
        patients = PatientService.get_all(search, city, gender)
        return success_response(patients)
    else:
        data = request.json or request.form.to_dict()
        errors = validate_patient_data(data)
        if errors:
            return error_response("Validation failed", errors, 400)
        res = PatientService.create(data)
        if res.get('success'):
            return success_response(res, "Patient registered successfully", 201)
        return error_response(res.get('error', 'Registration failed'), status_code=400)

@app.route('/api/patients/<int:patient_id>', methods=['GET', 'PUT', 'DELETE'])
def api_patient_detail(patient_id):
    if request.method == 'GET':
        patient = PatientService.get_by_id(patient_id)
        if not patient:
            return error_response("Patient not found", status_code=404)
        return success_response(patient)
    elif request.method == 'PUT':
        data = request.json or request.form.to_dict()
        res = PatientService.update(patient_id, data)
        return success_response(res, "Patient updated successfully")
    elif request.method == 'DELETE':
        res = PatientService.delete(patient_id)
        if res.get('success'):
            return success_response(res, "Patient deleted successfully")
        return error_response(res.get('error'), status_code=400)

@app.route('/api/medicines', methods=['GET', 'POST'])
def api_medicines():
    if request.method == 'GET':
        search = request.args.get('search')
        status = request.args.get('status')
        pharmacy_id = request.args.get('pharmacy_id')
        medicines = MedicineService.get_all(search, status, pharmacy_id)
        return success_response(medicines)
    else:
        data = request.json or request.form.to_dict()
        errors = validate_medicine_data(data)
        if errors:
            return error_response("Validation failed", errors, 400)
        res = MedicineService.create(data)
        if res.get('success'):
            return success_response(res, "Medicine added successfully", 201)
        return error_response(res.get('error', 'Failed to add medicine'), status_code=400)

@app.route('/api/medicines/<int:medicine_id>', methods=['GET'])
def api_medicine_detail(medicine_id):
    med = MedicineService.get_by_id(medicine_id)
    if not med:
        return error_response("Medicine not found", status_code=404)
    return success_response(med)

@app.route('/api/medicines/restock', methods=['POST'])
def api_medicines_restock():
    data = request.json or request.form.to_dict()
    errors = validate_restock_data(data)
    if errors:
        return error_response("Validation failed", errors, 400)
    res = MedicineService.restock(data)
    if res.get('success'):
        return success_response(res, res.get('message', 'Restock successful'))
    return error_response(res.get('error', 'Restock failed'), status_code=400)

@app.route('/api/prescriptions', methods=['GET', 'POST'])
def api_prescriptions():
    if request.method == 'GET':
        search = request.args.get('search')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        prescriptions = PrescriptionService.get_all(search, date_from, date_to)
        return success_response(prescriptions)
    else:
        data = request.json or {}
        if not data.get('patient_id') or not data.get('doctor_id'):
            return error_response("Patient and Doctor are required.", status_code=400)
        res = PrescriptionService.create(data)
        if res.get('success'):
            return success_response(res, res.get('message'), 201)
        return error_response(res.get('error', 'Prescription creation failed'), status_code=400)

@app.route('/api/prescriptions/<int:presc_id>', methods=['GET'])
def api_prescription_detail(presc_id):
    p = PrescriptionService.get_by_id(presc_id)
    if not p:
        return error_response("Prescription not found", status_code=404)
    return success_response(p)

@app.route('/api/bills', methods=['GET'])
def api_bills():
    search = request.args.get('search')
    pharmacy_id = request.args.get('pharmacy_id')
    bills = BillingService.get_all(search, pharmacy_id)
    return success_response(bills)

@app.route('/api/bills/<int:bill_id>', methods=['GET'])
def api_bill_detail(bill_id):
    b = BillingService.get_by_id(bill_id)
    if not b:
        return error_response("Bill not found", status_code=404)
    return success_response(b)

@app.route('/api/bills/generate', methods=['POST'])
def api_bills_generate():
    data = request.json or request.form.to_dict()
    if not data.get('pharmacy_id') or not data.get('patient_id') or not data.get('prescription_id'):
        return error_response("Pharmacy, Patient, and Prescription are required.", status_code=400)
    res = BillingService.generate_bill(data)
    if res.get('success'):
        return success_response(res, res.get('message', 'Bill generated successfully'), 201)
    return error_response(res.get('error', 'Bill generation failed'), status_code=400)

@app.route('/api/orders', methods=['GET', 'POST'])
def api_orders():
    if request.method == 'GET':
        orders = OrderService.get_all()
        return success_response(orders)
    else:
        data = request.json or request.form.to_dict()
        if not data.get('supplier_id') or not data.get('pharmacy_id') or not data.get('quantity_ordered'):
            return error_response("Supplier, Pharmacy, and Quantity are required.", status_code=400)
        res = OrderService.create(data)
        if res.get('success'):
            return success_response(res, res.get('message'), 201)
        return error_response(res.get('error', 'Order placement failed'), status_code=400)

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def api_order_update_status(order_id):
    data = request.json or {}
    order_status = data.get('order_status')
    payment_status = data.get('payment_status')
    if not order_status:
        return error_response("Order status is required.", status_code=400)
    res = OrderService.update_status(order_id, order_status, payment_status)
    return success_response(res, res.get('message'))

@app.route('/api/db-ops/query', methods=['POST'])
def api_db_ops_query():
    data = request.json or {}
    query_key = data.get('query_key')
    if not query_key:
        return error_response("Query key is required.", status_code=400)
    res = DBOpsService.execute_predefined_query(query_key)
    if res.get('success'):
        return success_response(res)
    return error_response(res.get('error', 'Query execution failed'), status_code=400)

@app.route('/api/db-ops/procedure', methods=['POST'])
def api_db_ops_procedure():
    data = request.json or {}
    proc_name = data.get('proc_name')
    args = data.get('args', [])
    if not proc_name:
        return error_response("Procedure name is required.", status_code=400)
    res = db.call_procedure(proc_name, args)
    if res.get('success'):
        return success_response(res, res.get('message'))
    return error_response(res.get('error', 'Procedure call failed'), status_code=400)

@app.route('/api/db-ops/function', methods=['POST'])
def api_db_ops_function():
    data = request.json or {}
    func_name = data.get('func_name')
    arg_val = data.get('arg')
    secondary_arg = data.get('secondary_arg')
    if not func_name or not arg_val:
        return error_response("Function name and argument are required.", status_code=400)
    res = DBOpsService.execute_function_demo(func_name, arg_val, secondary_arg)
    if res.get('success'):
        return success_response(res)
    return error_response(res.get('error', 'Function execution failed'), status_code=400)

@app.route('/api/db-ops/trigger-demo', methods=['POST'])
def api_db_ops_trigger_demo():
    data = request.json or {}
    pharmacy_id = int(data.get('pharmacy_id', 101))
    medicine_id = int(data.get('medicine_id', 501))
    delta = int(data.get('delta', 25))
    res = DBOpsService.trigger_demo_step(pharmacy_id, medicine_id, delta)
    if res.get('success'):
        return success_response(res, res.get('message'))
    return error_response(res.get('error', 'Trigger demo failed'), status_code=400)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    print(f"[*] Starting Pharmacy Inventory System on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)
