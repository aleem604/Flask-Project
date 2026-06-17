from flask import render_template, request, jsonify, abort
from models import Category, Product
from database import database as db
from . import categories_bp

@categories_bp.route('/')
def index():
    """List all categories"""
    categories = Category.query.filter_by(is_active=True).order_by(Category.display_order).all()
    
    # Get featured categories (with products)
    featured_categories = Category.query.filter(
        Category.is_active == True,
        Category.products.any(Product.is_featured == True)
    ).limit(6).all()
    
    return render_template('categories/index.html', 
                          categories=categories,
                          featured_categories=featured_categories)

@categories_bp.route('/<slug>')
def detail(slug):
    """Show category details with products"""
    category = Category.query.filter_by(slug=slug, is_active=True).first_or_404()
    
    # Get products in this category
    products = Product.query.filter_by(
        category_id=category.id,
        status='published',
        is_active=True
    ).order_by(Product.created_at.desc()).paginate(page=1, per_page=20)
    
    # Get subcategories
    subcategories = Category.query.filter_by(parent_id=category.id, is_active=True).all()
    
    return render_template('categories/detail.html',
                          category=category,
                          products=products,
                          subcategories=subcategories)

@categories_bp.route('/api')
def api_list():
    """API endpoint for categories"""
    categories = Category.query.filter_by(is_active=True).all()
    return jsonify([c.to_dict() for c in categories])

@categories_bp.route('/api/<int:id>')
def api_detail(id):
    """API endpoint for single category"""
    category = Category.query.get_or_404(id)
    return jsonify(category.to_dict())

@categories_bp.route('/api/<int:id>/products')
def api_products(id):
    """API endpoint for category products"""
    category = Category.query.get_or_404(id)
    products = Product.query.filter_by(
        category_id=id,
        status='published',
        is_active=True
    ).limit(20).all()
    return jsonify([p.to_dict() for p in products])