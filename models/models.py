from database.database import db  # This imports from database.py
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from flask_login import UserMixin

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    image_url = db.Column(db.String(500))
    icon_class = db.Column(db.String(100))
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    products = db.relationship(
        'Product', 
        foreign_keys='Product.category_id',
        backref='category', 
        lazy='dynamic'
    )
    
    # For products where this is a subcategory
    subcategory_products = db.relationship(
        'Product',
        foreign_keys='Product.subcategory_id',
        backref='subcategory',
        lazy='dynamic'
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'parent_id': self.parent_id,
            'image_url': self.image_url,
            'icon_class': self.icon_class,
            'display_order': self.display_order,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'product_count': self.products.filter_by(status='published', is_active=True).count()
        }

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(100))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    website = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    products = db.relationship('Product', backref='supplier', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact_person': self.contact_person,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'website': self.website,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'product_count': self.products.filter_by(status='published').count()
        }

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(200))
    role = db.Column(db.String(50), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    short_description = db.Column(db.String(500))
    
    # Pricing
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    original_price = db.Column(db.Numeric(10, 2))
    cost_price = db.Column(db.Numeric(10, 2))
    
    # Inventory
    sku = db.Column(db.String(100), unique=True, nullable=False)
    quantity_in_stock = db.Column(db.Integer, nullable=False, default=0)
    low_stock_threshold = db.Column(db.Integer, default=5)
    is_in_stock = db.Column(db.Boolean, default=True)
    
    # Categories
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'))
    brand = db.Column(db.String(100))
    tags = db.Column(ARRAY(db.String), default=[])
    
    # Media
    main_image_url = db.Column(db.String(500))
    gallery_images = db.Column(ARRAY(db.String), default=[])
    video_url = db.Column(db.String(500))
    
    # Specifications
    specifications = db.Column(JSONB, default={})
    attributes = db.Column(JSONB, default={})
    
    # Ratings
    average_rating = db.Column(db.Numeric(3, 2), default=0.00)
    total_reviews = db.Column(db.Integer, default=0)
    
    # Marketing
    is_featured = db.Column(db.Boolean, default=False)
    is_best_seller = db.Column(db.Boolean, default=False)
    is_new_arrival = db.Column(db.Boolean, default=False)
    is_on_sale = db.Column(db.Boolean, default=False)
    discount_percentage = db.Column(db.Numeric(5, 2), default=0.00)
    sale_start_date = db.Column(db.DateTime)
    sale_end_date = db.Column(db.DateTime)
    
    # SEO
    meta_title = db.Column(db.String(255))
    meta_description = db.Column(db.Text)
    meta_keywords = db.Column(ARRAY(db.String), default=[])
    
    # Status
    status = db.Column(db.String(50), default='draft')
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # Foreign Keys
    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='SET NULL'))
    
    # Additional
    weight = db.Column(db.Numeric(10, 2))
    dimensions = db.Column(JSONB, default={'length': 0, 'width': 0, 'height': 0, 'unit': 'cm'})
    shipping_class = db.Column(db.String(50))
    tax_class = db.Column(db.String(50), default='standard')
    upc = db.Column(db.String(50))
    ean = db.Column(db.String(50))
    mpn = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'short_description': self.short_description,
            'price': float(self.price) if self.price else 0,
            'original_price': float(self.original_price) if self.original_price else None,
            'sku': self.sku,
            'quantity_in_stock': self.quantity_in_stock,
            'is_in_stock': self.is_in_stock,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'brand': self.brand,
            'tags': self.tags,
            'main_image_url': self.main_image_url,
            'gallery_images': self.gallery_images,
            'specifications': self.specifications,
            'average_rating': float(self.average_rating) if self.average_rating else 0,
            'total_reviews': self.total_reviews,
            'is_featured': self.is_featured,
            'is_best_seller': self.is_best_seller,
            'is_new_arrival': self.is_new_arrival,
            'is_on_sale': self.is_on_sale,
            'discount_percentage': float(self.discount_percentage) if self.discount_percentage else 0,
            'status': self.status,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'supplier_name': self.supplier.name if self.supplier else None,
            'supplier_id': self.supplier_id
        }