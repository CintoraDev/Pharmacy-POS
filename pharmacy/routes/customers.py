from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required
from models import Customer, db
from utils import role_required

customers_bp = Blueprint('customers', __name__)
@customers_bp.route('/customers')
@login_required
def index():
    customers = Customer.query.filter_by(status = True).all()
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


@customers_bp.route('/customers/desactivate/<int:id>', methods=['POST'])
@role_required('admin', 'gerente')
@login_required
def desactivate(id):
    customer = Customer.query.get_or_404(id)
    customer.status = False
    db.session.commit()
    flash('Cliente desactivado correctamente', 'success')
    return redirect(url_for('customers.index'))

    
@customers_bp.route('/customers/update/<int:id>', methods=['POST'])
@role_required('admin', 'gerente')
@login_required
def update(id):
    customer = Customer.query.get_or_404(id)
    customer.name = request.form.get('name')   
    customer.rfc = request.form.get('rfc')
    customer.email = request.form.get('email')
    customer.phone = request.form.get('phone')
    customer.address = request.form.get('address')
    customer.city = request.form.get('city')
    customer.state = request.form.get('state')
    customer.zip_code = request.form.get('zip_code')
    customer.fiscal_regimen = request.form.get('fiscal_regimen')
    customer.birth_date = request.form.get('birth_date') or None
    
    db.session.commit()
    flash('Cliente actualizado correctamente', 'success')
    return redirect(url_for('customers.index'))



@customers_bp.route('/customers/points/<int:id>', methods=['GET'])
@login_required 
def get_customer_points(id):
    customer = Customer.query.get_or_404(id)
    points = customer.points
    
    return jsonify({'points': points})
    

