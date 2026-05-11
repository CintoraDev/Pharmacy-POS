from flask import Blueprint, render_template, request 
from flask_login import login_required, current_user
from models import Sale,Purchase,Customer,Invoice
from sqlalchemy.orm import joinedload
from utils import CITIES,STATES

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports')
@login_required
def index():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    #Modulo Ventas
    sales_query = Sale.query.options(
        joinedload(Sale.user),
        joinedload(Sale.customer),
        joinedload(Sale.invoice)
    )
    if start_date and end_date:
        sales_query = sales_query.filter(
            Sale.date >= start_date,
            Sale.date <= end_date
        )
    sales = sales_query.order_by(Sale.date.desc()).all()

   #Modulo Compras
    purchases_query = Purchase.query.options(
        joinedload(Purchase.provider),
        joinedload(Purchase.user),
        joinedload(Purchase.details)
    )

    if start_date and end_date:
        purchases_query = purchases_query.filter(
            Purchase.date >= start_date,
            Purchase.date <= end_date
        )

    purchases = purchases_query.order_by(
        Purchase.date.desc()
    ).all()


    #Modulo Clientes
    city = request.args.get('city', '')
    state = request.args.get('state', '')

    customers = Customer.query
    if city:
        customers = customers.filter(Customer.city == city)
    if state:
        customers = customers.filter(Customer.state == state)
    customers = customers.all()

    
    
    #Modulo Facturas
    
    invoices = Invoice.query.options(
        joinedload(Invoice.customer),
        joinedload(Invoice.sale)
    ).order_by(
        Invoice.emission_date.desc()
    ).all()
    
    return render_template('reports/index.html', sales=sales, purchases = purchases, invoices = invoices,customers = customers, cities = CITIES, states = STATES) 



@reports_bp.route('/reports/customers/filter')
@login_required
def filter_customers():
    city = request.args.get('city', '')
    state = request.args.get('state', '')
    customers = Customer.query
    if city:
        customers = customers.filter(Customer.city == city)
    if state:
        customers = customers.filter(Customer.state == state)
    customers = customers.all()
    return render_template('reports/_customers_rows.html', customers=customers)
