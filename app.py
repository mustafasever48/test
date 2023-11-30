from flask import Flask
from flask import render_template
from flask import request
import mysql.connector
from flask_cors import CORS
import json
from datetime import datetime, timedelta

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

app = Flask(__name__)
CORS(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}, "supports_credentials": True})




@app.route("/add", methods=['POST'])
def add():
    data = request.get_json()

    brandName = data['Brand_Name']
    modelID = data['Model_ID']
    productName = data['Product_Name']
    productSerial = data['Serial_Number']

    cur = mysql.cursor()

    brand_s = f"INSERT INTO Brand(Brand_Name) VALUES ('{brandName}')"
    cur.execute(brand_s)
    mysql.commit()

    model_s = f"INSERT INTO Model(Model_Name, Brand_ID) VALUES ('{modelID}', (SELECT Brand_ID FROM Brand WHERE Brand_Name = '{brandName}'))"
    cur.execute(model_s)
    mysql.commit()

    product_s = f"INSERT INTO Product(Product_Name, Serial_Number, Model_ID) VALUES ('{productName}', '{productSerial}', '{modelID}')"
    cur.execute(product_s)
    mysql.commit()

    return jsonify({"Result": "Success"})

@app.route("/brands")
def get_brands():
    cur = mysql.cursor(dictionary=True)
    cur.execute("SELECT * FROM Brand")
    results = cur.fetchall()
    return jsonify(results)

@app.route("/models/<int:brand_id>")
def get_models(brand_id):
    cur = mysql.cursor(dictionary=True)
    cur.execute(f"SELECT * FROM Model WHERE Brand_ID = {brand_id}")
    results = cur.fetchall()
    return jsonify(results)

@app.route("/products/<int:model_id>")
def get_products(model_id):
    cur = mysql.cursor(dictionary=True)
    cur.execute(f"SELECT * FROM Product WHERE Model_ID = {model_id}")
    results = cur.fetchall()
    return jsonify(results)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True, ssl_context=('/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/cert.pem', '/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/privkey.pem'))
