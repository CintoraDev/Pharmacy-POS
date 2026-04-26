from flask import Blueprint, render_template
from flask_login import login_required
from models import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
@login_required
def index():
    users = User.query.all()
    return render_template('users/index.html', users = users)