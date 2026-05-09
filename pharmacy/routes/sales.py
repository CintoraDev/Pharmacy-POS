from flask_login import current_user
from models import Sale, SaleDetail, Invoice, Emisor
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import Product, db, Customer
from datetime import datetime
import uuid
from flask_mail import Mail, Message
from flask import current_app
from weasyprint import HTML



sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/sales')
@login_required
def index():
    sales = Sale.query.all()
    customers = Customer.query.filter_by(status=True).all()
    return render_template('sales/index.html', customers=customers, sales=sales)


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




@sales_bp.route('/sales/invoices/create', methods=['POST'])
@login_required
def createInvoice():
    data = request.get_json()
    sale_id = data.get('sale_id')
    sale = Sale.query.get_or_404(sale_id)

    customer = Customer.query.get(sale.id_customer)
    if not customer.rfc or not customer.email:
        return jsonify({'success': False, 'message': 'Cliente sin datos fiscales'})



    emisor = Emisor.query.first()

    subtotal = float(sale.subtotal) - float(sale.discount)
    iva = round(subtotal * 0.16, 2)
    total = round(subtotal + iva, 2)
    
    new_invoice = Invoice(
        emission_date=datetime.now(),
        id_sale=sale.id,
        id_customer=sale.id_customer,
        subtotal=round(subtotal, 2),
        iva = iva,
        total = total,
        cfdi_use = "G03",
        payment_method = "PUE",
        payment_type = "01",
        fiscal_regimen = "601",
        zip_expedition = "00000",
        id_emisor = emisor.id,
        folio = f"F-{sale.id:04d}",
        fiscal_folio = str(uuid.uuid4())
    )
    
    db.session.add(new_invoice)
    db.session.commit()
    
    html_string = render_template('invoices/invoice_pdf.html', invoice=new_invoice)
    pdf_bytes = HTML(string=html_string).write_pdf()
    
    msg = Message(
    subject=f"Factura {new_invoice.folio} - Farmacia CUCEI",
    recipients=[customer.email],
    body=f"Estimado {customer.name}, adjunto encontrará su factura {new_invoice.folio}."
)
    msg.attach(
        f"{new_invoice.folio}.pdf",
        "application/pdf",
        pdf_bytes
    )
    mail = Mail(current_app)
    mail.send(msg)

    return jsonify({'success': True, 'message': 'Factura creada correctamente', 'invoice_id': new_invoice.id})




@sales_bp.route('/sales/invoices/<int:invoice_id>', methods=['GET'])
@login_required
def showInvoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template('invoices/invoice_pdf.html', invoice=invoice)