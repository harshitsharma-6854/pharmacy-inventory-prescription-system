import re
from datetime import datetime

def validate_patient_data(data):
    """Validates patient payload before insertion."""
    errors = []
    
    if not data.get('first_name') or not str(data['first_name']).strip():
        errors.append("First name is required.")
    if not data.get('last_name') or not str(data['last_name']).strip():
        errors.append("Last name is required.")
        
    sex = (data.get('sex') or '').upper()
    if sex not in ('M', 'F', 'O'):
        errors.append("Sex must be M, F, or O.")
        
    dob_str = data.get('dob')
    if not dob_str:
        errors.append("Date of Birth is required.")
    else:
        try:
            dob = datetime.strptime(str(dob_str), '%Y-%m-%d').date()
            if dob > datetime.now().date():
                errors.append("Date of Birth cannot be in the future.")
        except ValueError:
            errors.append("Invalid Date of Birth format (must be YYYY-MM-DD).")
            
    contact = data.get('contact_no')
    if contact and not re.match(r'^[+\d\s-]{7,20}$', str(contact).strip()):
        errors.append("Invalid contact phone format.")
        
    return errors

def validate_medicine_data(data):
    """Validates medicine payload before insertion."""
    errors = []
    
    if not data.get('name') or not str(data['name']).strip():
        errors.append("Medicine name is required.")
        
    try:
        price = float(data.get('price', 0))
        if price <= 0:
            errors.append("Medicine price must be strictly greater than 0.")
    except (ValueError, TypeError):
        errors.append("Valid numeric price is required.")
        
    manu_str = data.get('manu_date')
    exp_str = data.get('exp_date')
    
    if not manu_str or not exp_str:
        errors.append("Manufacturing and Expiration dates are required.")
    else:
        try:
            manu_date = datetime.strptime(str(manu_str), '%Y-%m-%d').date()
            exp_date = datetime.strptime(str(exp_str), '%Y-%m-%d').date()
            if exp_date <= manu_date:
                errors.append("Expiration date must be strictly after manufacturing date.")
        except ValueError:
            errors.append("Invalid date format (must be YYYY-MM-DD).")
            
    return errors

def validate_restock_data(data):
    """Validates restock payload."""
    errors = []
    try:
        qty = int(data.get('quantity', 0))
        if qty <= 0:
            errors.append("Restock quantity must be greater than zero.")
    except (ValueError, TypeError):
        errors.append("Quantity must be a positive integer.")
        
    if not data.get('pharmacy_id'):
        errors.append("Pharmacy selection is required.")
    if not data.get('medicine_id'):
        errors.append("Medicine selection is required.")
        
    return errors
