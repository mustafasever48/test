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


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        brandName = request.form['Brand_Name']
        modelName = request.form['Mode_Name']
        productName = request.form['Product_Name']
        serialNumber = request.form['Serial_Number']
        print(brandName, modelName, productName, serialNumber)
        cur = mysql.cursor()

        s_brand = '''INSERT INTO Brand(Brand_Name) VALUES('{}');'''.format(brandName)
        cur.execute(s_brand)
        s_model = '''INSERT INTO Model(Model_Name) VALUES('{}');'''.format(modelName)
        cur.execute(s_model)
        s_product = '''INSERT INTO Product(Product_Name, Serial_Number) VALUES('{}', '{}');'''.format(productName, serialNumber)
        cur.execute(s_product)
        mysql.commit()
    else:
        return render_template('add.html')

    return '{"Result":"Success"}'


@app.route("/")  # Default - Show Data
def hello():
    cur = mysql.cursor()

    cur.execute('''SELECT * FROM Brand''')  # execute an SQL statment
    brand_results = cur.fetchall()

    cur.execute('''SELECT * FROM Model''')  # execute an SQL statment
    model_results = cur.fetchall()

    cur.execute('''SELECT * FROM Product''')  # execute an SQL statment
    product_results = cur.fetchall()

    Results = {
        'Brand': brand_results,
        'Model': model_results,
        'Product': product_results
    }

    response = {'Results': Results, 'count': len(brand_results)}
    ret = app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )
    return ret  # Return the data in a string format


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True,
            ssl_context=('/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/cert.pem',
                          '/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/privkey.pem'))
