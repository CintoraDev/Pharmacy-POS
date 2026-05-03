from flask_login import current_user
from models import Sale, SaleDetail
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import Product, db, Customer
from datetime import datetime

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/sales')
@login_required
def index():
    customers = Customer.query.filter_by(status=True).all()
    return render_template('sales/index.html', customers=customers)


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


@sales_bp.route('/sales/create', methods=['POST'])
@login_required
def create_sale():
    data = request.get_json()
    customer_id = data.get('customer_id')
    items = data.get('items')

    customer = Customer.query.get_or_404(customer_id)

    real_items = []
    for item in items:
        product = Product.query.get_or_404(item['id'])
        if product.stock < item['quantity']:
            return jsonify({'success': False, 'message': f'Stock insuficiente para {product.name}'})
        real_items.append({
            'product': product,
            'quantity': item['quantity']
        })

    subtotal = sum(item['product'].price_sale * item['quantity'] for item in real_items)
    discount = 0

    apply_discount = customer.points >= 50
    if apply_discount:
        discount = float(subtotal) * 0.10
        customer.points = 0

    total = float(subtotal) - discount

    new_sale = Sale(
        date=datetime.now(),
        id_user=current_user.id,
        id_customer=customer_id,
        subtotal=subtotal,
        discount=discount,
        total=total,
        generated_points=10 if total >= 500 else 0
    )

    db.session.add(new_sale)
    db.session.flush()

    for item in real_items:
        product = item['product']
        quantity = item['quantity']

        new_sale_detail = SaleDetail(
            id_sale=new_sale.id,
            id_product=product.id,
            quantity=quantity,
            unit_price=float(product.price_sale),
            subtotal=float(product.price_sale) * quantity,
        )
        db.session.add(new_sale_detail)
        product.stock -= quantity

    if total >= 500:
        customer.points += 10

    db.session.commit()
    return jsonify({'success': True, 'message': 'Venta realizada correctamente'})