from flask import Flask, render_template, request
import mysql.connector
from flask_cors import CORS
import json
from datetime import datetime

mysql = mysql.connector.connect(
    user='web',
    password='webPass',
    host='127.0.0.1',
    database='rma'
)

app = Flask(__name__)
CORS(app)

@app.route("/add", methods=['POST'])
def add():
    if request.method == 'POST':
        brandName = request.form['Brand_Name']
        modelName = request.form['Model_Name']
        productName = request.form['Product_Name']
        serialNumber = request.form['Serial_Number']
        ProductSoldDate = request.form['ProductSoldDate']

        cur = mysql.cursor()

        
        brand_s = 'INSERT INTO Brand(Brand_Name) VALUES(%s);'
        cur.execute(brand_s, (brandName,))
        mysql.commit()

        
        model_s = 'INSERT INTO Model(Model_Name) VALUES(%s);'
        cur.execute(model_s, (modelName,))
        mysql.commit()

        
        product_s = 'INSERT INTO Product(Product_Name, Serial_Number, ProductSoldDate) VALUES(%s, %s, %s);'
        cur.execute(product_s, (productName, serialNumber,ProductSoldDate))
        mysql.commit()

        cur.close()

    else:
        return render_template('add.html')

    return '{"Result":"Success"}'


@app.route("/", methods=['GET'])
def hello():
    serial_number = request.args.get('serial_number', '')

    cur = mysql.cursor()

   
    sql_query = '''
        SELECT Brand.Brand_Name, Model.Model_Name, Product.Product_Name, Product.Serial_Number,Product.ProductSoldDate
        FROM Product
        JOIN Model ON Product.Model_ID = Model.Model_ID
        JOIN Brand ON Model.Brand_ID = Brand.Brand_ID
        WHERE Product.Serial_Number = %s;
    '''

    cur.execute(sql_query, (serial_number,))
    rv = cur.fetchall()

    Results = []
    for row in rv:
        Result = {}
        Result['Brand_Name'] = row[0].replace('\n', ' ')
        Result['Model_Name'] = row[1]
        Result['Product_Name'] = row[2]
        Result['Serial_Number'] = row[3]
        Result['ProductSoldDate'] = row[4]
        Results.append(Result)

    response = {'Results': Results, 'count': len(Results)}
    ret = app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )

    return ret


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True, ssl_context=('/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/cert.pem', '/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/privkey.pem'))
