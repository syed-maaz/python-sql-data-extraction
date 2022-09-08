from tkinter import E
from globalFunctions import error_validation
from sql_flask_connection import *

class brands(db.Model):
    brand_id = db.Column(db.Integer,primary_key=True)
    brand_name = db.Column(db.String)

    def __repr__(self):
        return f'{self.brand_id} - {self.brand_name}'

@app.route("/brands")
def get_brands():
    cursor.execute('USE production')
    cursor.execute('SELECT brands.brand_id,brands.brand_name FROM production.brands')
    output=[]
    for prod in cursor:
        prod_data = {'brand_id':prod[0] ,'brand_name':prod[1]}
        output.append(prod_data)
    return jsonify({ 'brands':output}),200

@app.route('/brands/<int:id>')
def get_brand(id):
    prod = brands.query.get_or_404(id)

    return jsonify({'brands_id':prod.brand_id,'brands_name':prod.brand_name})

@app.post('/brands')
def add_brands():
    er = error_validation(request.get_json(),'brands')
    if er == True:
        product = brands(brand_name=request.json['brand_name'])
        db.session.add(product)
        db.session.commit() 
        return{'Added brand ID':product.brand_id},201
    else:
        return {"Error":422,"Response":er},422

@app.route('/brands/<int:id>',methods=['PUT'])
def modify_brand(id):
    er = error_validation(request.get_json(),'brands')
    if er == True:
        product = brands.query.filter_by(product_id=id).first()
        name=request.json['brand_name']
        product.brand_name = name
        db.session.commit()
        return {"Updated Brand":product}
    else:
        return {"Error":422,"Response":er},422

@app.delete('/brands/<int:id>')
def delete_brand(id):
    product = brands.query.get(id)
    if product is None:
        return {"Error":"404","Message":"Not Found"}
    db.session.delete(product)
    db.session.commit()
    return{"Deleted brand":id}

