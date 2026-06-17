from app import app
from database import db
from models import User, Category, Supplier, Product
from werkzeug.security import generate_password_hash
from datetime import datetime

def seed_database():
    with app.app_context():
        # Create admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            full_name='Admin User',
            role='admin',
            is_active=True
        )
        db.session.add(admin)
        
        # Create categories
        categories = [
            Category(name='Electronics', slug='electronics', description='Electronic devices and gadgets', icon_class='fas fa-laptop'),
            Category(name='Audio', slug='audio', description='Headphones and audio equipment', icon_class='fas fa-headphones'),
            Category(name='Books', slug='books', description='Books and publications', icon_class='fas fa-book'),
            Category(name='Accessories', slug='accessories', description='Tech accessories', icon_class='fas fa-watch'),
        ]
        
        for cat in categories:
            db.session.add(cat)
        
        db.session.commit()
        print('Database seeded successfully!')

if __name__ == '__main__':
    seed_database()