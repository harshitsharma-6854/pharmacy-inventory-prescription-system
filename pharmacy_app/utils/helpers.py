import decimal
from datetime import date, datetime
from flask import jsonify

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def format_currency(val):
    """Format decimal/float as Indian Rupee (INR)."""
    try:
        fval = float(val or 0.0)
        return f"₹{fval:,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"

def success_response(data=None, message="Operation completed successfully", status_code=200):
    """Standardized JSON API success envelope."""
    payload = {
        "success": True,
        "message": message,
        "data": data
    }
    return jsonify(payload), status_code

def error_response(message="An error occurred", errors=None, status_code=400):
    """Standardized JSON API error envelope."""
    payload = {
        "success": False,
        "message": message,
        "errors": errors or []
    }
    return jsonify(payload), status_code
