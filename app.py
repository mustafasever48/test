from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask_cors import CORS
import json
from datetime import datetime
from flask import jsonify

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
        ProductSoldDate = request.form['Product_Sold_Date']

        cur = mysql.cursor()

        brand_s = 'INSERT INTO Brand(Brand_Name) VALUES(%s);'
        cur.execute(brand_s, (brandName,))
        mysql.commit()

        model_s = 'INSERT INTO Model(Model_Name) VALUES(%s);'
        cur.execute(model_s, (modelName,))
        mysql.commit()

        product_s = 'INSERT INTO Product(Product_Name, Serial_Number, Product_Sold_Date) VALUES(%s, %s, %s);'
        cur.execute(product_s, (productName, serialNumber, ProductSoldDate))
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
        SELECT Brand.Brand_Name, Model.Model_Name, Product.Product_Name, Product.Serial_Number, Product.Product_Sold_Date
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
        Result['Product_Sold_Date'] = row[4].isoformat() if row[4] else None
        Results.append(Result)

    response = {'Results': Results, 'count': len(Results)}
    ret = app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )

    return ret

@app.route("/create_rma", methods=['GET'])
def create_rma():
    serial_number = request.args.get('serial_number', '')
    issue_description = request.args.get('issue_description', '')

    cur = mysql.cursor()

    product_query = 'SELECT Product_ID FROM Product WHERE Serial_Number = %s;'
    cur.execute(product_query, (serial_number,))
    product_id = cur.fetchone()[0]

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    rma_query = 'INSERT INTO RMA (Inspaction_Start_Date, Check_Issue, Product_ID) VALUES (%s, %s, %s);'
    cur.execute(rma_query, (current_date, issue_description, product_id))
    mysql.commit()

    cur.execute('SELECT LAST_INSERT_ID();')
    rma_id = cur.fetchone()[0]

    cur.close()

    response = {'RMA_ID': rma_id}
    ret = app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )

    return ret



@app.route("/", methods=['GET'])
def hello():
    serial_number = request.args.get('serial_number', '')

    cur = mysql.cursor()
    
    sql_query = '''
        SELECT RMA.RMA_ID, RMA.Inspaction_Start_Date, RMA.Inspeciton_Completion_Date,
               RMA.Product_Defect, RMA.Check_Issue, RMA.Result_Issue,
               RMA.Product_ID, RMA.Technician_ID, RMA.Return_Shipping_ID, RMA.Shipping_Brand_ID,
               Brand.Brand_Name, Model.Model_Name, Product.Product_Name, Product.Serial_Number, Product.Product_Sold_Date
        FROM RMA
        JOIN Product ON RMA.Product_ID = Product.Product_ID
        JOIN Model ON Product.Model_ID = Model.Model_ID
        JOIN Brand ON Model.Brand_ID = Brand.Brand_ID
        WHERE Product.Serial_Number = %s;
    '''

    cur.execute(sql_query, (serial_number,))
    rv = cur.fetchall()

    Results = []
    for row in rv:
        Result = {
            'RMA_ID': row[0],
            'Inspaction_Start_Date': row[1].isoformat() if row[1] else None,
            'Inspeciton_Completion_Date': row[2].isoformat() if row[2] else None,
            'Product_Defect': row[3],
            'Check_Issue': row[4],
            'Result_Issue': row[5],
            'Product_ID': row[6],
            'Technician_ID': row[7],
            'Return_Shipping_ID': row[8],
            'Shipping_Brand_ID': row[9],
            'Brand_Name': row[10].replace('\n', ' '),
            'Model_Name': row[11],
            'Product_Name': row[12],
            'Serial_Number': row[13],
            'Product_Sold_Date': row[14].isoformat() if row[14] else None
        }
        Results.append(Result)

    response = {'Results': Results, 'count': len(Results)}
    ret = jsonify(response)

    return ret

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True, ssl_context=('/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/cert.pem', '/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/privkey.pem'))
