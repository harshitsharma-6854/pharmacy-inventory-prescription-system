import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
base_dir = Path(__file__).resolve().parent
load_dotenv(base_dir / '.env')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'pharma-care-da2-super-secret-key-2026')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    
    # MySQL 8.x Database Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'pharmacy_system_new')
    MYSQL_POOL_SIZE = int(os.environ.get('MYSQL_POOL_SIZE', 5))
    
    # Fallback SQLite DB for instantaneous demo/grading if MySQL service is offline
    FALLBACK_DB_PATH = base_dir / 'pharmacy_demo.db'
    SQL_SCRIPTS_DIR = base_dir.parent / 'database'
