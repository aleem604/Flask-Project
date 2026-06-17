from flask import render_template, request, jsonify, abort, g
from models import Category, Product
from database import database as db
from sqlalchemy import or_, and_
from . import products_bp

@products_bp.route('/')
def index():
    """List all products with filtering and sorting"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category')
    search = request.args.get('search')
    sort = request.args.get('sort', 'newest')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    # Base query
    query = Product.query.filter_by(status='published', is_active=True)
    
    # Filter by category
    if category:
        category_obj = Category.query.filter_by(slug=category).first()
        if category_obj:
            query = query.filter_by(category_id=category_obj.id)
    
    # Search
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
                Product.brand.ilike(search_term),
                Product.short_description.ilike(search_term)
            )
        )
    
    # Price range
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    # Sorting
    if sort == 'newest':
        query = query.order_by(Product.created_at.desc())
    elif sort == 'price-low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price-high':
        query = query.order_by(Product.price.desc())
    elif sort == 'popular':
        query = query.order_by(Product.total_reviews.desc())
    elif sort == 'rating':
        query = query.order_by(Product.average_rating.desc())
    else:
        query = query.order_by(Product.created_at.desc())
    
    # Paginate
    products = query.paginate(page=page, per_page=per_page)
    
    # Get categories for filter
    categories = Category.query.filter_by(is_active=True).order_by(Category.name).all()
    
    return render_template('products/index.html',
                          products=products,
                          categories=categories,
                          current_category=category,
                          search=search,
                          sort=sort)

@products_bp.route('/<slug>')
def detail(slug):
    """Show product details"""
    product = Product.query.filter_by(slug=slug, status='published', is_active=True).first_or_404()
    
    # Get related products (same category, exclude current)
    related = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.status == 'published',
        Product.is_active == True
    ).limit(6).all()
    
    # Get product reviews (if you have a reviews table)
    # reviews = Review.query.filter_by(product_id=product.id).order_by(Review.created_at.desc()).all()
    
    return render_template('products/detail.html',
                          product=product,
                          related=related)

@products_bp.route('/api')
def api_list():
    """API endpoint for products"""
    limit = request.args.get('limit', 20, type=int)
    category = request.args.get('category')
    
    query = Product.query.filter_by(status='published', is_active=True)
    
    if category:
        query = query.filter_by(category_id=category)
    
    products = query.limit(limit).all()
    return jsonify([p.to_dict() for p in products])

@products_bp.route('/api/<int:id>')
def api_detail(id):
    """API endpoint for single product"""
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

@products_bp.route('/api/featured')
def api_featured():
    """API endpoint for featured products"""
    products = Product.query.filter_by(
        is_featured=True,
        status='published',
        is_active=True
    ).limit(10).all()
    return jsonify([p.to_dict() for p in products])

@products_bp.route('/api/best-sellers')
def api_best_sellers():
    """API endpoint for best sellers"""
    products = Product.query.filter_by(
        is_best_seller=True,
        status='published',
        is_active=True
    ).order_by(m.Product.total_reviews.desc()).limit(10).all()
    return jsonify([p.to_dict() for p in products])

@products_bp.route('/api/new-arrivals')
def api_new_arrivals():
    """API endpoint for new arrivals"""
    products = Product.query.filter_by(
        is_new_arrival=True,
        status='published',
        is_active=True
    ).order_by(Product.created_at.desc()).limit(10).all()
    return jsonify([p.to_dict() for p in products])