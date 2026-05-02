from flask import url_for
from flask import redirect
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import Product, db, Customer

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/sales')
@login_required
def index():
    customers = Customer.query.filter_by(status = True).all()
    return render_template('sales/index.html', customers = customers)



@sales_bp.route('/sales/search')
@login_required
def search_products():
    q = request.args.get('q', '')

    products = Product.query.filter(Product.name.ilike(f'%{q}%')).limit(10).all()

    return jsonify([
    {
        "id": product.id,
        "name": product.name,
        "price": float(product.price_sale),
        "stock": product.stock
    }
    
    for product in products
])




    