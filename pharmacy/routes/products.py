from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from models import Product, ProductCategory, db, Provider
from utils import role_required

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
@login_required
def index():
    products = Product.query.filter_by(status = True).all()
    product_categories = ProductCategory.query.all()
    providers = Provider.query.filter_by(status=True).all()
    return render_template('products/index.html', products = products, product_categories = product_categories, providers = providers)
    
@products_bp.route('/products/create', methods=['POST'])
@role_required('admin', 'gerente')
@login_required
def create():
    name = request.form.get('name')
    description = request.form.get('description')
    price_sale = request.form.get('price_sale')
    price_purchase = request.form.get('price_purchase')
    unit = request.form.get('unit')
    id_category = request.form.get('id_category')
    id_provider = request.form.get('id_provider')


    existing_product = Product.query.filter_by(name=name).first()
    if existing_product:
        flash('El producto ya existe', 'error')
        return redirect(url_for('products.index'))

    new_product = Product(
        name = name,
        description = description,
        price_sale = price_sale,
        price_purchase = price_purchase,
        stock=0,
        unit = unit,
        id_category = id_category,
        id_provider = id_provider
    )

    db.session.add(new_product)
    db.session.commit()
    flash('Producto creado correctamente', 'success')
    return redirect(url_for('products.index'))


@products_bp.route('/products/update/<int:id>', methods=['POST'])
@role_required('admin', 'gerente')
@login_required
def update(id):
    product = Product.query.get_or_404(id)
    product.name = request.form.get('name')
    product.description = request.form.get('description')
    product.price_sale = request.form.get('price_sale')
    product.price_purchase = request.form.get('price_purchase')
    product.unit = request.form.get('unit')
    product.id_category = request.form.get('id_category')
    product.id_provider = request.form.get('id_provider')
    db.session.commit()
    flash('Producto actualizado correctamente', 'success')
    return redirect(url_for('products.index'))


@products_bp.route('/products/desactivate/<int:id>', methods=['POST'])
@role_required('admin', 'gerente')
@login_required
def desactivate(id):
    product = Product.query.get_or_404(id)
    product.status = False
    db.session.commit()
    flash('Producto desactivado correctamente', 'success')
    return redirect(url_for('products.index'))