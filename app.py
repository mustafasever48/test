from flask import Flask
from flask import render_template
from flask import request
import mysql.connector
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

mysql = mysql.connector.connect(user='web', password='webPass',
  host='127.0.0.1',
  database='rma')

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
app = Flask(__name__)
CORS(app)

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
class Sold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rma = db.relationship('RMA', backref='product', lazy=True)
    sold_id = db.Column(db.Integer, db.ForeignKey('sold.id'), nullable=False)

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



@app.route('/')
def customer_page():
    return render_template('customer_page.html')

@app.route('/check_warranty', methods=['POST'])
def check_warranty():
    serial_number = request.form.get('serial_number')
    model_name = request.form.get('model_name')

    product = Product.query.filter_by(serial_number=serial_number).first()
    if product:
        warranty_expiration_date = product.purchase_date + timedelta(days=365 * 2)  # 2 yıllık garanti
        return jsonify({
            'message': 'Warranty Information',
            'warranty_status': 'In Warranty' if datetime.utcnow() <= warranty_expiration_date else 'Out of Warranty'
        })
    else:
        return jsonify({'message': 'Product not found'})



if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
