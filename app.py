from flask import Flask, render_template, request
import mysql.connector
from flask_cors import CORS
import json
from datetime import datetime
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)


mysql = mysql.connector.connect(
    user='web',
    password='webPass',
    host='127.0.0.1',
    database='rma'
)

@app.route("/add", methods=['POST'])
def add():
    if request.method == 'POST':
        brand_name = request.form['Brand_Name']
        model_name = request.form['Model_Name']
        product_name = request.form['Product_Name']
        serial_number = request.form['Serial_Number']
        product_sold_date = request.form['Product_Sold_Date']

    
        brand_result = db.Brand.insert_one({"Brand_Name": brand_name})
        brand_id = brand_result.inserted_id

     
        model_result = db.Model.insert_one({"Model_Name": model_name, "Brand_ID": brand_id})
        model_id = model_result.inserted_id


        db.Product.insert_one({
            "Product_Name": product_name,
            "Serial_Number": serial_number,
            "Product_Sold_Date": datetime.strptime(product_sold_date, "%Y-%m-%d"),
            "Model_ID": model_id
        })

    else:
        return render_template('add.html')

    return '{"Result":"Success"}'

@app.route("/", methods=['GET'])
def hello():
    serial_number = request.args.get('serial_number', '')

    # MongoDB sorgusu
    results = db.Product.aggregate([
        {"$match": {"Serial_Number": serial_number}},
        {"$lookup": {
            "from": "Model",
            "localField": "Model_ID",
            "foreignField": "_id",
            "as": "model_info"
        }},
        {"$unwind": "$model_info"},
        {"$lookup": {
            "from": "Brand",
            "localField": "model_info.Brand_ID",
            "foreignField": "_id",
            "as": "brand_info"
        }},
        {"$unwind": "$brand_info"},
        {"$project": {
            "_id": 0,
            "Brand_Name": "$brand_info.Brand_Name",
            "Model_Name": "$model_info.Model_Name",
            "Product_Name": "$Product_Name",
            "Serial_Number": "$Serial_Number",
            "Product_Sold_Date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$Product_Sold_Date"}}
        }}
    ])

    response = {"Results": list(results), "count": results.length()}
    ret = app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )

    return ret

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True, ssl_context=('/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/cert.pem', '/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/privkey.pem'))
