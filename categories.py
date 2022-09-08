import imp
from sql_flask_connection import *
from globalFunctions import error_validation

class categories(db.Model):
    category_id = db.Column(db.Integer,primary_key=True)
    category_name = db.Column(db.String)

    def __repr__(self):
        return f'{self.category_id} - {self.category_name}'

@app.route("/categories")
def get_categories():
    cursor.execute('USE production')
    cursor.execute('SELECT categories.category_id,categories.category_name FROM production.categories')
    output=[]
    for prod in cursor:
        prod_data = {'category_id':prod[0] ,'category_name':prod[1]}
        output.append(prod_data)
    return jsonify({ 'categories':output}),200

@app.route('/categories/<int:id>')
def get_category(id):
    prod = categories.query.get_or_404(id)
    return jsonify({'category_id':prod.category_id,'category_name':prod.category_name})

@app.post('/categories')
def add_category():
    er = error_validation(request.get_json(),'categories')
    if er == True:
        product = categories(category_name=request.json['category_name'])
        db.session.add(product)
        db.session.commit()
        return {'Added Category ID':product.category_id},201
    else:
        return {"Error":422,"Response":er},422

@app.route('/categories/<int:id>',methods=['PUT'])
def modify_category(id):
    er = error_validation(request.get_json(),'categories')
    if er == True:
        product = categories.query.filter_by(product_id=id).first()
        name=request.json['category_name']
        product.category_name = name
        db.session.commit()
        return {"Updated Category":product}
    else:
        return {"Error":422,"Response":er},422


@app.delete('/categories/<int:id>')
def delete_category(id):
    product = categories.query.get(id)
    if product is None:
        return {"Error":"404","Message":"Not Found"}
    db.session.delete(product)
    db.session.commit()
    return{"Deleted category":id}

