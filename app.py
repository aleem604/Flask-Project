import os
from flask import Flask, render_template, jsonify  # type: ignore[import]
from config import config
from database.database import db, init_db
from models.models import Category, Product
from routes import categories_bp, products_bp, suppliers_bp, users_bp, home_bp

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(categories_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(suppliers_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(home_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return render_template('errors/500.html'), 500
    
    # Context processor
    @app.context_processor
    def inject_globals():
        return {
            'site_name': 'MyFlaskApp',
            'version': '1.0.0'
        }
    
    return app

# Create app instance
app = create_app()

# @app.route('/')
# def home():
#     """Home page"""
    
#     # Get featured products
#     featured_products = Product.query.filter_by(
#         is_featured=True,
#         status='published',
#         is_active=True
#     ).limit(6).all()
    
#     # Get new arrivals
#     new_arrivals = Product.query.filter_by(
#         is_new_arrival=True,
#         status='published',
#         is_active=True
#     ).order_by(Product.created_at.desc()).limit(6).all()
    
#     # Get categories
#     categories = Category.query.filter_by(is_active=True).limit(8).all()
    
#     return render_template('common/index.html',
#                           featured_products=featured_products,
#                           new_arrivals=new_arrivals,
#                           categories=categories)
    


@app.route('/test-db')
def test_db():
        try:
            categories_count = Category.query.count()
            return jsonify({
                'status': 'success',
                'message': 'Database connected!',
                'categories_count': categories_count
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

if __name__ == '__main__':
    app.run(debug=True)