from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta

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

# Flask uygulamasının rotalarını aşağıdaki gibi güncelleyebilirsiniz

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

# Diğer rotaları ve işlevleri de benzer şekilde güncelleyebilirsiniz

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
