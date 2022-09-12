from turtle import update
from sql_flask_connection import *
from globalFunctions import error_validation


class products(db.Model):
    product_id = db.Column(db.Integer,primary_key=True)
    product_name = db.Column(db.String(),unique=True,nullable=False)
    brand_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    model_year = db.Column(db.Integer)
    list_price = db.Column(db.DECIMAL(10,2))

    def __repr__(self):
        return f'{self.product_id} - {self.product_name}'


@app.route("/products")
def get_products_details():
    cursor.execute('USE production')
    cursor.execute('SELECT products.product_id,products.product_name,products.brand_id,products.category_id,products.model_year,products.list_price FROM production.products')
    output=[]
    for prod in cursor:
        prod_data = {'product_id':prod[0] ,'product_name':prod[1],'brand_id':prod[2],'category_id':prod[3],"model_year":prod[4],"list_price":prod[5]}
        output.append(prod_data)
    return jsonify({ 'products':output}),200

@app.route('/products/<int:id>')
def get_product_details(id):
    prod = products.query.get_or_404(id)
    return jsonify({'product_id':prod.product_id ,'product_name':prod.product_name,'brand_id':prod.brand_id,'category_id':prod.category_id,"model_year":prod.model_year,"list_price":prod.list_price})

@app.post('/products')
def add_product_details():
    er = error_validation(request.get_json(),'products')
    if er == False:
        product = products(product_name=request.json['product_name'],category_id=request.json['category_id'],brand_id=request.json['brand_id'],model_year=request.json['model_year'],list_price=request.json['list_price'])
        db.session.add(product)
        db.session.commit()
        return{'Added Product ID':product.product_id},201
    else:
        return {"Error":422,"Message":er},422

@app.route('/products/<int:id>',methods=['PUT'])
def modify_product(id):
    er = error_validation(request.get_json(),'products')
    if er == False:
        product = products.query.filter_by(product_id=id).first()
        name=request.json['product_name']
        bid=request.json['brand_id']
        cid=request.json['category_id']
        mear=request.json['model_year']
        lice=request.json['list_price']
        product.product_name = name
        product.brand_id = bid
        product.category_id = cid
        product.model_year = mear
        product.list_price = lice
        db.session.commit()
        return jsonify({"Updated Product":product.product_id})
    else:
        return {"Error":422,"Message":er},422

@app.delete('/products/<int:id>')
def delete_product(id):
    product = products.query.get(id)
    if product is None:
        return {"Error":"404","Message":"Not Found"}
    db.session.delete(product)
    db.session.commit()
    return{"Deleted product":id}



