import pymysql
from app import app
from config import mysql
from flask import jsonify, request
from global_functions import validate_schema


conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)


products_schema = {
    "type":"object",
    "properties":{
        "product name": {"type":"string"},
        "brand_id": {"type":"integer"},
        "category_id": {"type":"integer"},
        "model_year": {"type":"integer"},
        "list_price": {"type":"integer"}
    },
    'required':['product_name','brand_id','category_id','model_year','list_price']
}

@app.route('/products', methods=['GET'])
def view_product():
    try:
        cursor.execute("USE production")
        cursor.execute("SELECT product_id, product_name, brand_id, category_id, model_year, list_price FROM products")
        empRows = cursor.fetchall()
        response = jsonify(empRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
 

@app.route('/products/<int:pro_id>', methods=['GET'])
def view_product_details(pro_id):
    try:
        cursor.execute("USE production")
        cursor.execute(f"SELECT product_id, product_name, brand_id, category_id, model_year, list_price FROM products WHERE product_id ={pro_id}")
        empRow = cursor.fetchone()
        response = jsonify(empRow)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)


@app.route('/products/create', methods=['POST'])
def create_product():
    _json = request.json
    validation_repsonse = validate_schema(_json,products_schema)
    if validation_repsonse == None:
        try:        
            _product_name = _json['product_name']
            _brand_id = _json['brand_id']
            _category_id = _json['category_id']
            _model_year = _json['model_year']	
            _list_price = _json['list_price']
            if request.method == 'POST':
                sqlQuery = "INSERT INTO products(product_name, brand_id, category_id, model_year, list_price) VALUES(%s, %s, %s, %s, %s)"
                bindData = (_product_name, _brand_id,_category_id,_model_year,_list_price)
                cursor.execute("USE production")		
                cursor.execute(sqlQuery, bindData)
                id = cursor.lastrowid
                conn.commit()
                response = str(f'Product added successfully! \nNew generated ID: {id}')
                return response,200
            else:
                # return showMessage()
                return "Error due to wrong HTTP method selection"
        except Exception as e:
            return e
    elif validation_repsonse != None :
        return validation_repsonse
  
    
         

@app.route('/products/update', methods=['PUT'])
def update_product():
    _json = request.json
    validation_repsonse = validate_schema(_json,products_schema)
    _product_id = _json['product_id']
    if validation_repsonse == None and _product_id:
        try:
            _product_name = _json['product_name']
            _brand_id = _json['brand_id']
            _category_id = _json['category_id']
            _model_year = _json['model_year']	
            _list_price = _json['list_price']	
            if  request.method == 'PUT':			
                sqlQuery = "UPDATE products SET product_name=%s, brand_id=%s, category_id=%s, model_year=%s, list_price=%s WHERE product_id=%s"
                bindData = (_product_name, _brand_id,_category_id,_model_year,_list_price,_product_id)
                cursor.execute("USE production")
                cursor.execute(sqlQuery, bindData)
                conn.commit()
                response = jsonify('Product updated successfully!')
                response.status_code = 200
                return response
            else:
                return "Error due to wrong HTTP method selection"
        except Exception as e:
            return e
    elif validation_repsonse != None :
        return validation_repsonse


@app.route('/products/delete/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        cursor.execute("USE production")
        cursor.execute("DELETE FROM products WHERE product_id =%s", (id))
        conn.commit()
        response = jsonify('Product deleted successfully!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
       

@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response


@app.errorhandler(400)
def handle_400(e):
    message = {
        'status': 400,
        'message': 'Error in JSON body format'
    }
    response = jsonify(message)
    response.status_code = 400
    return response
