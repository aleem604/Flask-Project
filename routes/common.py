from flask import Flask, render_template, jsonify, request  # type: ignore[import]
from models.models import Product, Category, Order, User
from database.database import db
from datetime import datetime, timedelta
from . import home_bp

@home_bp.route('/')
def index():
    # Get statistics
    stats = {
        'total_revenue': Order.query.filter_by(status='completed').with_entities(db.func.sum(Order.total_amount)).scalar() or 0,
        'total_orders': Order.query.count(),
        'total_products': Product.query.filter_by(is_active=True).count(),
        'total_customers': User.query.filter_by(role='customer').count(),
        'total_reviews': db.session.query(db.func.sum(Product.total_reviews)).scalar() or 0,
        'conversion_rate': 3.2  # Example
    }
    
    # Get recent activity
    recent_activities = [
        {'type': 'order', 'icon': 'fa-shopping-bag', 'text': 'New order #1234 placed by John Doe', 'time': '5 minutes ago'},
        {'type': 'product', 'icon': 'fa-box', 'text': 'Product "MacBook Pro" added to inventory', 'time': '15 minutes ago'},
        {'type': 'user', 'icon': 'fa-user-plus', 'text': 'New user Sarah Smith registered', 'time': '1 hour ago'},
        {'type': 'review', 'icon': 'fa-star', 'text': 'New 5-star review for "AirPods Pro"', 'time': '2 hours ago'},
        {'type': 'payment', 'icon': 'fa-credit-card', 'text': 'Payment received for order #1230', 'time': '3 hours ago'},
    ]
    
    # Get top products
    top_products = Product.query.filter_by(is_active=True, status='published').order_by(Product.total_reviews.desc()).limit(5).all()

    # Get user
    user = User.query.filter_by(id=3).first()
    if not user:
        user = User.query.first()
        if not user:
            # Fallback user data
            user = {'full_name': 'Guest User', 'username': 'guest', 'email': 'guest@example.com'}
    
    user = {'full_name': user.full_name, 'username': user.username, 'email': user.email}
    
    # Get category sales
    categories = Category.query.filter_by(is_active=True).all()
    category_sales = []
    total = len(categories) or 1
    
    colors = ['#667eea', '#764ba2', '#2ecc71', '#f39c12', '#ff4757', '#3498db', '#a29bfe', '#00b894']
    
    for i, cat in enumerate(categories):
        product_count = cat.products.filter_by(status='published').count()
        category_sales.append({
            'name': cat.name,
            'icon': cat.icon_class or 'fa-tag',
            'percentage': (product_count / total) * 100 if total > 0 else 0,
            'color': colors[i % len(colors)]
        })
    
    # Revenue data for chart
    revenue_data = {
        'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'values': [1200, 1900, 1500, 2200, 2800, 2500, 3200]
    }
    
    # Orders data for chart
    orders_data = {
        'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'values': [12, 19, 15, 22, 28, 20, 30]
    }
    
    # Add category data for the chart
    category_data = {
        'labels': [cat['name'] for cat in category_sales],
        'values': [cat['percentage'] for cat in category_sales],
        'colors': [cat['color'] for cat in category_sales]
    }
    
    # Debug print before render
    debug_data = {
        'user': user,
        'stats': stats,
        'activities': len(recent_activities),
        'products': len(top_products),
        'category_sales':len(category_sales),
        'revenue_data': revenue_data,
        'orders_data': orders_data
    }
    print(debug_data)
    
    return render_template('common/index.html',
                          user = user,
                          stats=stats,
                          recent_activities=recent_activities,
                          top_products=top_products,
                          category_sales=category_sales,
                          revenue_data=revenue_data,
                          orders_data=orders_data,
                          category_data=category_data
                          )
    
    
@home_bp.route('/about')
def about():
    """About page"""
    return render_template('common/about.html')

@home_bp.route('/contact')
def contact():
    """About page"""
    return render_template('common/contact.html')

@home_bp.route('/api/revenue')
def api_revenue():
    period = request.args.get('period', 30, type=int)
    # Fetch real data from database
    # This is just example data
    return jsonify({
        'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'values': [1200, 1900, 1500, 2200, 2800, 2500, 3200]
    })

@home_bp.route('/api/orders')
def api_orders():
    period = request.args.get('period', 30, type=int)
    return jsonify({
        'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'values': [12, 19, 15, 22, 28, 20, 30]
    })