from flask import Blueprint, render_template
from flask_login import login_required

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/customers')
@login_required
def index():
    return render_template('customers/index.html')