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

class products(db.Model):
    product_id = db.Column(db.Integer,primary_key=True)
    product_name = db.Column(db.String,unique=True,nullable=False)
    brand_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    model_year = db.Column(db.Integer)
    list_price = db.Column(db.DECIMAL(10,2))

    def __repr__(self):
        return f'{self.product_id} - {self.product_name}'

class categories(db.Model):
    category_id = db.Column(db.Integer,primary_key=True)
    category_name = db.Column(db.String)

    def __repr__(self):
        return f'{self.category_id} - {self.category_name}'

class brands(db.Model):
    brand_id = db.Column(db.Integer,primary_key=True)
    brand_name = db.Column(db.String)

    def __repr__(self):
        return f'{self.brand_id} - {self.brand_name}'


###################################################################################################################################
#################################################   API ENDPOINTS  ################################################################
###################################################################################################################################
@app.route("/")
def index():
    return "Hello. View products using endpoint'products'"

##################################################### CHECK STATUS ################################################################
@app.route("/status")
def get_status():
    response = requests.get("http://127.0.0.1:5000")
    return jsonify({"Response": "Running OK","Status Code": response.status_code})

##################################################### GET ALL METHODS #############################################################
@app.route("/production")
def get_products():
    cursor.execute('USE production')
    cursor.execute('SELECT productsdata.product_id,productsdata.product_name,productsdata.category_name,productsdata.brand_name FROM production.productsdata')
    output=[]
    for prod in cursor:
        prod_data = {'product_id':prod[0] ,'product_name':prod[1],'category_name':prod[2],'brand_name':prod[3]}
        output.append(prod_data)
    return jsonify({ 'products':output}),200

@app.route("/products")
def get_products_details():
    cursor.execute('USE production')
    cursor.execute('SELECT products.product_id,products.product_name,products.brand_id,products.category_id,products.model_year,products.list_price FROM production.products')
    output=[]
    for prod in cursor:
        prod_data = {'product_id':prod[0] ,'product_name':prod[1],'brand_id':prod[2],'category_id':prod[3],"model_year":prod[4],"list_price":prod[5]}
        output.append(prod_data)
    return jsonify({ 'products':output}),200

@app.route("/categories")
def get_categories():
    cursor.execute('USE production')
    cursor.execute('SELECT categories.category_id,categories.category_name FROM production.categories')
    output=[]
    for prod in cursor:
        prod_data = {'category_id':prod[0] ,'category_name':prod[1]}
        output.append(prod_data)
    return jsonify({ 'categories':output}),200

@app.route("/brands")
def get_brands():
    cursor.execute('USE production')
    cursor.execute('SELECT brands.brand_id,brands.brand_name FROM production.brands')
    output=[]
    for prod in cursor:
        prod_data = {'brand_id':prod[0] ,'brand_name':prod[1]}
        output.append(prod_data)
    return jsonify({ 'brands':output}),200

##################################################### GET SINGLE METHODS ###########################################################
    
@app.route('/production/<int:id>')
def get_product(id):
    prod = productsdata.query.get_or_404(id)
    # cursor.execute('USE production')
    # cursor.execute(f'SELECT productsdata.product_id,productsdata.product_name,productsdata.category_name,productsdata.brand_name FROM production.productsdata WHERE product_id = {id}')
    # prod = cursor.fetchone()
    return jsonify({'product_id':prod.product_id ,'product_name':prod.product_name,'category_name':prod.category_name,'brand_name':prod.brand_name})

@app.route('/products/<int:id>')
def get_product_details(id):
    prod = products.query.get_or_404(id)
    return jsonify({'product_id':prod.product_id ,'product_name':prod.product_name,'brand_id':prod.brand_id,'category_id':prod.category_id,"model_year":prod.model_year,"list_price":prod.list_price})

@app.route('/categories/<int:id>')
def get_category(id):
    prod = categories.query.get_or_404(id)
    return jsonify({'category_id':prod.category_id,'category_name':prod.category_name})

@app.route('/brands/<int:id>')
def get_brand(id):
    prod = brands.query.get_or_404(id)

    return jsonify({'brands_id':prod.brand_id,'brands_name':prod.brand_name})

##################################################### POST METHODS ##################################################################

@app.post('/brands')
def add_brands():
    product = brands(brand_name=request.json['brand_name'])
    db.session.add(product)
    db.session.commit()
    return{'id':product.brand_id}

@app.post('/categories')
def add_category():
    product = categories(category_name=request.json['category_name'])
    db.session.add(product)
    db.session.commit()
    return{'id':product.category_id}

@app.post('/products')
def add_product_details():
    product = products(product_name=request.json['product_name'],category_id=request.json['category_id'],brand_id=request.json['brand_id'],model_year=request.json['model_year'],list_price=request.json['list_price'])
    db.session.add(product)
    db.session.commit()
    return{'id':product.product_id},201


##################################################### PUT METHODS ###################################################################

@app.route('/products/<int:id>',methods=['PUT'])
def modify_product(id):
    if not isinstance(id,int):
        return{"error":"422","message":"ID type incorrect","idtype":f'{type(id)}'},422
    product = products.query.filter_by(product_id=id).first()
    if product is None:
        return {"Error":"404","Message":"Not Found"}
    res = request.get_json()
    if not isinstance(res['product_id'], int) or not isinstance(res['product_name'],str):
        return{"error":"422","message":"Data type incorrect"},422
    pid=request.json['product_id']
    name=request.json['product_name']
    bid=request.json['brand_id']
    cid=request.json['category_id']
    mear=request.json['model_year']
    lice=request.json['list_price']
    product.product_id = pid
    product.product_name = name
    product.brand_id = bid
    product.category_id = cid
    product.model_year = mear
    product.list_price = lice
    db.session.commit()
    return {"Updated Product":product}

@app.route('/categories/<int:id>',methods=['PUT'])
def modify_category(id):
    product = categories.query.filter_by(product_id=id).first()
    cid=request.json['category_id']
    name=request.json['category_name']
    product.category_id = cid
    product.category_name = name
    db.session.commit()
    return {"Updated Category":product}

@app.route('/brands/<int:id>',methods=['PUT'])
def modify_brand(id):
    product = brands.query.filter_by(product_id=id).first()
    cid=request.json['brand_id']
    name=request.json['brand_name']
    product.brand_id = cid
    product.brand_name = name
    db.session.commit()
    return {"Updated Brand":product}


##################################################### DELETE METHODS ################################################################
@app.delete('/products/<int:id>')
def delete_product(id):
    product = products.query.get(id)
    if product is None:
        return {"Error":"404","Message":"Not Found"}
    db.session.delete(product)
    db.session.commit()
    return{"Deleted product":id}

@app.delete('/categories/<int:id>')
def delete_category(id):
    product = categories.query.get(id)
    if product is None:
        return {"Error":"404","Message":"Not Found"}
    db.session.delete(product)


    db.session.commit()
    return{"Deleted category":id}

@app.delete('/brands/<int:id>')
def delete_brand(id):
    product = brands.query.get(id)
    if product is None:
        return {"Error":"404","Message":"Not Found"}
    db.session.delete(product)
    db.session.commit()
    return{"Deleted brand":id}

##################################################### ERROR - HANDLING ############################################################

# @app.errorhandler(404)
# def handle_404(e):
#     return jsonify({"Error":"404", "Message":"Not Found"},404)

# @app.errorhandler(404)
# def handle_404(e):
#     return jsonify({"Error":"404", "Message":"Not Found"},404)

if __name__=="__main__":
    app.run(debug=True)

