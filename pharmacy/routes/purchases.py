from flask import Blueprint, render_template
from flask_login import login_required

purchases_bp = Blueprint('purchases', __name__)

@purchases_bp.route('/purchases')
@login_required
def index():
    return render_template('purchases/index.html')