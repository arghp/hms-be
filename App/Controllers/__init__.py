from flask import Blueprint
from .user_controller import register_user

bp = Blueprint('user', __name__)
bp.route('/register', methods=['POST'])(register_user)

def register_blueprint(app):
    app.register_blueprint(bp)
