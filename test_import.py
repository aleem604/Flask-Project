# test_import.py
try:
    from flask import Flask
    print("✅ Flask is installed!")
    print(f"   Version: {Flask.__version__}")
    
    from flask_sqlalchemy import SQLAlchemy
    print("✅ Flask-SQLAlchemy is installed!")
    
    from flask_migrate import Migrate
    print("✅ Flask-Migrate is installed!")
    
    from flask_login import LoginManager
    print("✅ Flask-Login is installed!")
    
    import psycopg2
    print("✅ psycopg2 is installed!")
    
    import dotenv
    print("✅ python-dotenv is installed!")
    
except ImportError as e:
    print(f"❌ Missing module: {e}")