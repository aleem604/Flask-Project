from app import app
from database.database import db
from models.models import User, Category, Supplier, Product
import hashlib
import os
import binascii
from datetime import datetime

def generate_password_hash(password, method='pbkdf2:sha256', salt_length=16):
    if method.startswith('pbkdf2:'):
        algorithm = method.split(':', 1)[1]
        salt = binascii.hexlify(os.urandom(salt_length)).decode('ascii')
        hash_bytes = hashlib.pbkdf2_hmac(algorithm, password.encode('utf-8'), salt.encode('ascii'), 260000)
        hash_value = binascii.hexlify(hash_bytes).decode('ascii')
        return f"pbkdf2:{algorithm}:260000${salt}${hash_value}"
    raise ValueError('Unsupported hash method')

def seed_database():
    with app.app_context():
        # Create admin user
        admin = User(
            username='admin',
            email='admin@gmail.com',
            password_hash=generate_password_hash('admin123'),
            full_name='Admin User',
            role='admin',
            is_active=True
        )
        #db.session.add(admin)
        
        customer = User(
            username='customer',
            email='customer@gmail.com',
            password_hash=generate_password_hash('customer123'),
            full_name='Customer User',
            role='customer',
            is_active=True
        )
        #db.session.add(customer)
        
        # Create categories
        categories = [
            Category(name='Electronics', slug='electronics', description='Electronic devices and gadgets', icon_class='fas fa-laptop'),
            Category(name='Audio', slug='audio', description='Headphones and audio equipment', icon_class='fas fa-headphones'),
            Category(name='Books', slug='books', description='Books and publications', icon_class='fas fa-book'),
            Category(name='Accessories', slug='accessories', description='Tech accessories', icon_class='fas fa-watch'),
        ]
        
        # for cat in categories:
        #     db.session.add(cat)
        
        db.session.commit()
        print('Database seeded successfully!')

if __name__ == '__main__':
    seed_database()