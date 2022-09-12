import requests
from flask import Flask,jsonify,request
import mysql.connector
from flask_sqlalchemy import SQLAlchemy

########################################### FLASK SQLALCHEMY AND DATABASE SETUP ##################################################
app = Flask(__name__) 
cnx = mysql.connector.connect(user='root',
                             password='8380',
                             host='localhost')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:8380@localhost/production'
db = SQLAlchemy(app)
cursor =cnx.cursor()

########################################### TABLE OBJECT MODEL ###################################################################

class productsdata(db.Model):
    product_id = db.Column(db.Integer,primary_key=True)
    product_name = db.Column(db.String,unique=True,nullable=False)
    category_id = db.Column(db.Integer)
    category_name = db.Column(db.String)
    brand_id = db.Column(db.Integer)
    brand_name = db.Column(db.String)

    def __repr__(self):
        return f'{self.product_id} - {self.product_name}'

@app.route("/")
def get_products():
    cursor.execute('USE production')
    cursor.execute('SELECT productsdata.product_id,productsdata.product_name,productsdata.category_name,productsdata.brand_name FROM production.productsdata')
    output=[]
    for prod in cursor:
        prod_data = {'product_id':prod[0] ,'product_name':prod[1],'category_name':prod[2],'brand_name':prod[3]}
        output.append(prod_data)
    return jsonify({ 'products':output}),200

@app.route("/status")
def get_status():
    response = requests.get("http://127.0.0.1:5000")
    return jsonify({"Response": "Running OK","Status Code": response.status_code})

@app.route('/<int:id>')
def get_product(id):
    prod = productsdata.query.get_or_404(id)
    return jsonify({'product_id':prod.product_id ,'product_name':prod.product_name,'category_name':prod.category_name,'brand_name':prod.brand_name})

@app.errorhandler(404)
def handle_404(e):
    return jsonify({"Error":"404", "Response":" The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."})

@app.errorhandler(400)
def handle_400(e):
    return jsonify({"Error":"400", "Response":" Invalid JSON body request format. Missing delimiter ',' ,  ';' , ':' or either '{','}' "})

@app.errorhandler(500)
def handle_500(e):
    return jsonify({"Error":"500", "Response":"Field names are incorrect "})
