from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from models import Customer, db


customers_bp = Blueprint('customers', __name__)
@customers_bp.route('/customers')
@login_required
def index():
    customers = Customer.query.all()
    return render_template('customers/index.html' , customers=customers)

@customers_bp.route('/customers/create', methods=['POST'])
@login_required
def create():
    name = request.form.get('name')
    rfc = request.form.get('rfc')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    zip_code = request.form.get('zip_code')
    fiscal_regimen = request.form.get('fiscal_regimen')
    birth_date = request.form.get('birth_date') or None

    existing_customer = Customer.query.filter_by(rfc=rfc).first()
    if existing_customer:
        flash('El cliente ya existe', 'error')
        return redirect(url_for('customers.index'))

    new_customer = Customer(
        name = name,
        rfc = rfc,
        email = email,
        phone = phone,
        address = address,
        city = city,
        state = state,
        zip_code = zip_code,
        fiscal_regimen = fiscal_regimen,
        birth_date = birth_date
    )
    db.session.add(new_customer)
    db.session.commit()
    flash('Cliente creado correctamente', 'success')
    return redirect(url_for('customers.index'))
    