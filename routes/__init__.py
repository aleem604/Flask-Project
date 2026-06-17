from flask import Blueprint

# Create blueprints
categories_bp = Blueprint('categories', __name__, url_prefix='/categories')
products_bp = Blueprint('products', __name__, url_prefix='/products')
suppliers_bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')
users_bp = Blueprint('users', __name__, url_prefix='/users')
# carts_bp = Blueprint('carts', __name__, url_prefix='/carts')

# Import routes
from . import categories, products, suppliers, users