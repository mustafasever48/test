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
    
    print(brandName)
    cur = mysql.cursor()
    
    s = '''INSERT INTO Brand(Brand_Name) VALUES('{}');'''.format(brandName)
    app.logger.info(s)
    cur.execute(s)
    mysql.commit()
    
  else:
    return render_template('add.html')
    
  return '{"Result":"Success"}'


@app.route("/") #Default - Show Data
def hello(): # Name of the method
  cur = mysql.cursor() #create a connection to the SQL instance
  
  cur.execute('''SELECT * FROM Brand''') # execute an SQL statment

  
  rv = cur.fetchall() #Retreive all rows returend by the SQL statment
  Results=[]
  for row in rv: #Format the Output Results and add to return string
    Result={}
    Result['Brand_Name']=row[1].replace('\n',' ')
    Result['Brand_ID ']=row[0]


    Results.append(Result)
  response={'Results':Results, 'count':len(Results)}
  ret=app.response_class(
    response=json.dumps(response),
    status=200,
    mimetype='application/json'
  )
  return ret #Return the data in a string format




if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True, ssl_context=('/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/cert.pem', '/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/privkey.pem'))
