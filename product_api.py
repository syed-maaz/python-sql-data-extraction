import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import request


# @app.route("/")
# def main_page():
#     return "<center><h1>*** API making in progress ***</h1></center>"

conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)

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
    try:        
        _json = request.json
        _product_name = _json['product_name']
        _brand_id = _json['brand_id']
        _category_id = _json['category_id']
        _model_year = _json['model_year']	
        _list_price = _json['list_price']	
        if _product_name and _brand_id and _category_id and _model_year and _list_price and request.method == 'POST':
            sqlQuery = "INSERT INTO products(product_name, brand_id, category_id, model_year, list_price) VALUES(%s, %s, %s, %s, %s)"
            bindData = (_product_name, _brand_id,_category_id,_model_year,_list_price)
            cursor.execute("USE production")		
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Product added successfully!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
         

@app.route('/products/update', methods=['PUT'])
def update_product():
    try:
        _json = request.json
        _product_id = _json['product_id']
        _product_name = _json['product_name']
        _brand_id = _json['brand_id']
        _category_id = _json['category_id']
        _model_year = _json['model_year']	
        _list_price = _json['list_price']	
        if _product_id and _product_name and _brand_id and _category_id and _model_year and _list_price and request.method == 'PUT':			
            sqlQuery = "UPDATE products SET product_name=%s, brand_id=%s, category_id=%s, model_year=%s, list_price=%s WHERE product_id=%s"
            bindData = (_product_name, _brand_id,_category_id,_model_year,_list_price,_product_id)
            cursor.execute("USE production")
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Product updated successfully!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)


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
        
