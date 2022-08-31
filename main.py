import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request


@app.route("/")
def main_page():
    return "<center><h1>*** API making in progress ***</h1></center>"

@app.route('/products', methods=['GET'])
def view_product():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT product_id, product_name, brand_id, category_id, model_year, list_price FROM products")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

@app.route('/products/<int:pro_id>', methods=['GET'])
def view_product_details(pro_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(f"SELECT product_id, product_name, brand_id, category_id, model_year, list_price FROM products WHERE product_id ={pro_id}")
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()