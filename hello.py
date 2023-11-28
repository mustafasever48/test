from flask import Flask
app = Flask(__name__)
@app.route("/")#URL leading to method
def hello(): # Name of the method
 return("Hello World!") #indent this line
if __name__ == "__main__":
  app.run(host='0.0.0.0',port='8080', ssl_context=('/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/cert.pem','/etc/letsencrypt/live/msubuntu.northeurope.cloudapp.azure.com/privkey.pem')) #Run the flask app at port 8080