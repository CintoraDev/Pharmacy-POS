from flask import Blueprint, render_template
from flask_login import login_required

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
@login_required
def index():
    return render_template('products/index.html')