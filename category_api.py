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

@app.route('/categories', methods=['GET'])
def view_category():
    try:
        cursor.execute("USE production")
        cursor.execute("SELECT category_id, category_name FROM categories")
        empRows = cursor.fetchall()
        response = jsonify(empRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
      

@app.route('/categories/<int:pro_id>', methods=['GET'])
def view_category_details(pro_id):
    try:
        cursor.execute("USE production")
        cursor.execute(f"SELECT category_id, category_name FROM categories WHERE category_id ={pro_id}")
        empRow = cursor.fetchone()
        response = jsonify(empRow)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
     

@app.route('/categories/create', methods=['POST'])
def create_category():
    try:        
        _json = request.json
        _category_name = _json['category_name']
        if _category_name and request.method == 'POST':
            sqlQuery = "INSERT INTO categories(category_name) VALUES(%s)"
            bindData = (_category_name)
            cursor.execute("USE production")		
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Category added successfully!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
              

@app.route('/categories/update', methods=['PUT'])
def update_category():
    try:
        _json = request.json
        _category_id = _json['category_id']
        _category_name = _json['category_name']	
        if _category_id and _category_name and request.method == 'PUT':			
            sqlQuery = "UPDATE categories SET category_name=%s WHERE category_id=%s"
            bindData = (_category_name,_category_id)
            cursor.execute("USE production")
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Category updated successfully!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
     

@app.route('/categories/delete/<int:id>', methods=['DELETE'])
def delete_category(id):
    try:
        cursor.execute("USE production")
        cursor.execute("DELETE FROM categories WHERE category_id =%s", (id))
        conn.commit()
        response = jsonify('Category deleted successfully!')
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
        
