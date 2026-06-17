from flask import render_template, request, jsonify, abort, session
from models.models import User
from database.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import users_bp

@users_bp.route('/profile')
def profile():
    """User profile page"""
    # Get current user from session
    user_id = session.get('user_id')
    if not user_id:
        abort(401)
    
    user = User.query.get_or_404(user_id)
    return render_template('users/profile.html', user=user)

@users_bp.route('/api')
def api_list():
    """API endpoint for users (admin only)"""
    # Add admin check here
    users = User.query.filter_by(is_active=True).all()
    return jsonify([u.to_dict() for u in users])

@users_bp.route('/api/<int:id>')
def api_detail(id):
    """API endpoint for single user"""
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())