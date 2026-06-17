from flask import render_template, request, jsonify
from models.models import Supplier, Product
from database.database import db
from . import suppliers_bp

@suppliers_bp.route('/')
def index():
    """List all suppliers"""
    suppliers = Supplier.query.filter_by(is_active=True).order_by(Supplier.name).all()
    return render_template('suppliers/index.html', suppliers=suppliers)

@suppliers_bp.route('/<int:id>')
def detail(id):
    """Show supplier details with products"""
    supplier = Supplier.query.get_or_404(id)
    products = Product.query.filter_by(
        supplier_id=id,
        status='published',
        is_active=True
    ).order_by(Product.created_at.desc()).limit(20).all()
    
    return render_template('suppliers/detail.html',
                          supplier=supplier,
                          products=products)

@suppliers_bp.route('/api')
def api_list():
    """API endpoint for suppliers"""
    suppliers = Supplier.query.filter_by(is_active=True).all()
    return jsonify([s.to_dict() for s in suppliers])

@suppliers_bp.route('/api/<int:id>')
def api_detail(id):
    """API endpoint for single supplier"""
    supplier = Supplier.query.get_or_404(id)
    return jsonify(supplier.to_dict())

@suppliers_bp.route('/api/<int:id>/products')
def api_products(id):
    """API endpoint for supplier products"""
    products = Product.query.filter_by(
        supplier_id=id,
        status='published',
        is_active=True
    ).limit(20).all()
    return jsonify([p.to_dict() for p in products])