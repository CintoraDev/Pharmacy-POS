from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Boolean, default=True)

    sales = db.relationship('Sale', backref='user')
    purchases = db.relationship('Purchase', backref='user')


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rfc = db.Column(db.String(13), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(10))
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(5), nullable=False)
    fiscal_regimen = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    points = db.Column(db.Integer, default=0)
    status = db.Column(db.Boolean, default=True)

    sales = db.relationship('Sale', backref='customer')
    invoices = db.relationship('Invoice', backref='customer')


class Provider(db.Model):
    __tablename__ = 'providers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rfc = db.Column(db.String(13), unique=True)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(10))
    address = db.Column(db.String(255))
    status = db.Column(db.Boolean, default=True)

    purchases = db.relationship('Purchase', backref='provider')


class ProductCategory(db.Model):
    __tablename__ = 'product_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    products = db.relationship('Product', backref='category')


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price_sale = db.Column(db.Numeric(10, 2), nullable=False)
    price_purchase = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    discount = db.Column(db.Numeric(5, 2), default=0)
    sat_key = db.Column(db.String(20))
    unit = db.Column(db.String(20))
    id_category = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    status = db.Column(db.Boolean, default=True)

    sale_details = db.relationship('SaleDetail', backref='product')
    purchase_details = db.relationship('PurchaseDetail', backref='product')


class Purchase(db.Model):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    id_provider = db.Column(db.Integer, db.ForeignKey('providers.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    details = db.relationship('PurchaseDetail', backref='purchase')


class PurchaseDetail(db.Model):
    __tablename__ = 'purchase_details'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    id_purchase = db.Column(db.Integer, db.ForeignKey('purchases.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))


class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    generated_points = db.Column(db.Integer, default=0)
    id_customer = db.Column(db.Integer, db.ForeignKey('customers.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    details = db.relationship('SaleDetail', backref='sale')
    invoice = db.relationship('Invoice', backref='sale', uselist=False)


class SaleDetail(db.Model):
    __tablename__ = 'sale_details'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    id_sale = db.Column(db.Integer, db.ForeignKey('sales.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'))


class Emisor(db.Model):
    __tablename__ = 'emisor'

    id = db.Column(db.Integer, primary_key=True)
    rfc = db.Column(db.String(13), nullable=False)
    razon_social = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(100))
    fiscal_regimen = db.Column(db.String(100))

    invoices = db.relationship('Invoice', backref='emisor')


class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(20))
    fiscal_folio = db.Column(db.String(100))
    emission_date = db.Column(db.DateTime, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    iva = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50))
    payment_type = db.Column(db.String(50))
    cfdi_use = db.Column(db.String(50))
    fiscal_regimen = db.Column(db.String(100))
    zip_expedition = db.Column(db.String(5))
    id_sale = db.Column(db.Integer, db.ForeignKey('sales.id'))
    id_customer = db.Column(db.Integer, db.ForeignKey('customers.id'))
    id_emisor = db.Column(db.Integer, db.ForeignKey('emisor.id'))