from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

mysql = mysql.connector.connect(
    user='web',
    password='webPass',
    host='127.0.0.1',
    database='rma'
)

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

cursor = mysql.cursor(dictionary=True)
@app.route('/')
def index():
    cursor.execute("SELECT * FROM Brand")
    brands = cursor.fetchall()
    return render_template('index.html', brands=brands)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_warranty', methods=['POST'])
def check_warranty():
    brand_name = request.form.get('Brand_Name')
    serial_number = request.form.get('Serial_Number')
    
    if brand_name is None or serial_number is None or serial_number.strip() == '':
        return jsonify({'message': 'Brand name or serial number is missing'})

    try:
        cursor.execute("SELECT * FROM Product WHERE Brand_Name = %s AND Serial_Number = %s", (brand_name, serial_number.upper()))
        product = cursor.fetchone()

        print('Product:', product)
        
        if product:
            purchase_date_str = product['ProductSoldDate']
            purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d')
            warranty_expiration_date = purchase_date + timedelta(days=365 * 2)
            return jsonify({
                'message': 'Warranty Information',
                'warranty_status': 'In Warranty' if datetime.utcnow() <= warranty_expiration_date else 'Out of Warranty'
            })
        else:
            return jsonify({'message': 'Product not found'})
    except mysql.connector.Error as err:
        return jsonify({'message': f'Error executing SQL query: {str(err)}'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True, ssl_context=('/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/cert.pem', '/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/privkey.pem'))
