from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MySQL bağlantısı için gerekli bilgiler
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://web:webPass@127.0.0.1/rma'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    models = db.relationship('Model', backref='brand', lazy=True)

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    products = db.relationship('Product', backref='model', lazy=True)

class Technician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    rmas = db.relationship('RMA', backref='technician', lazy=True)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    products = db.relationship('Product', backref='customer', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rma = db.relationship('RMA', backref='product', lazy=True)

class RMA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspection_start_date = db.Column(db.DateTime)
    inspection_completion_date = db.Column(db.DateTime)
    product_defect = db.Column(db.Text)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    check_issue = db.Column(db.Text)
    result_issue = db.Column(db.Text)
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'))

class Shipping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rma_id = db.Column(db.Integer, db.ForeignKey('rma.id'), nullable=False)
    shipping_date = db.Column(db.DateTime)
