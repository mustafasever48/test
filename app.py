from flask import Flask, render_template, request, jsonify
import mysql.connector
from flask_cors import CORS
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

mysql = mysql.connector.connect(
    user='web',
    password='webPass',
    host='127.0.0.1',
    database='rma'
)

cursor = mysql.cursor(dictionary=True)

@app.route('/')
def customer_page():
    return render_template('customer_page.html')

@app.route('/check_warranty', methods=['POST'])
def check_warranty():
    serial_number = request.form.get('serial_number')
    model_name = request.form.get('model_name')

    cursor.execute("SELECT * FROM Product WHERE serial_number = %s", (serial_number,))
    product = cursor.fetchone()

    if product:
        warranty_expiration_date = product['purchase_date'] + timedelta(days=365 * 2)
        return jsonify({
            'message': 'Warranty Information',
            'warranty_status': 'In Warranty' if datetime.utcnow() <= warranty_expiration_date else 'Out of Warranty'
        })
    else:
        return jsonify({'message': 'Product not found'})

if __name__ == "__main__":
     app.run(host='0.0.0.0', port='8080', debug=True, ssl_context=('/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/cert.pem','/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/privkey.pem'))
