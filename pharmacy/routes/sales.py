from flask import Blueprint, render_template
from flask_login import login_required

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/sales')
@login_required
def index():
    return render_template('sales/index.html')