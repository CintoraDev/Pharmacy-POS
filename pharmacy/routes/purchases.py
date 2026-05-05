from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Product, Provider, Purchase, PurchaseDetail, db

purchases_bp = Blueprint('purchases', __name__)

@purchases_bp.route('/purchases')
@login_required
def index():
    providers = Provider.query.filter_by(status=True).all()
    purchases = Purchase.query.order_by(Purchase.date.desc()).all()
    return render_template('purchases/index.html', providers=providers, purchases=purchases)


@purchases_bp.route('/purchases/products-by-provider')
@login_required
def products_by_provider():
    provider_id = request.args.get('id_provider')
    products = Product.query.filter_by(id_provider=provider_id, status=True).all()
    return render_template('purchases/partials/products_options.html', products=products)


@purchases_bp.route('/purchases/create', methods = ['POST'])
@login_required
def createPurchase():
    try:
        data = request.get_json()

        products = data.get('products')
        total = sum(float(product.get('price')) * int(product.get('quantity')) for product in products)
        new_purchase = Purchase(
            date = data.get('date'),
            id_provider = data.get('id_provider'),
            id_user = current_user.id,
            total = total
        )

        db.session.add(new_purchase)
        db.session.flush()

        for product in products:
            product_id = product.get('id')
            quantity = product.get('quantity')
            price = product.get('price')

            new_purchase_detail = PurchaseDetail(
                id_purchase = new_purchase.id,
                id_product = product_id,
                quantity = int(quantity),
                unit_price = float(price),
                subtotal = float(price) * int(quantity)
            )
            db.session.add(new_purchase_detail)

            product_db = Product.query.get(product_id)
            product_db.stock += int(quantity)
            product_db.price_purchase = price

        db.session.commit()
        return jsonify({'success': True, 'message': 'Compra realizada correctamente'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


