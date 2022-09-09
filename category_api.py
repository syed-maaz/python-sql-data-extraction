import pymysql
from app import app
from config import mysql
from flask import jsonify, request
from global_functions import validate_schema



conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)

categories_schema = {
    "type":"object",
    "properties":{
        "category name": {"type":"string"},
        "category_id": {"type":"integer"}
    },
    'required':['category_name']
}

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
        _json = request.json
        validation_response = validate_schema(_json,categories_schema)
        if validation_response == None:
            try:
                _category_name = _json['category_name']
                if request.method == 'POST':
                    sqlQuery = "INSERT INTO categories(category_name) VALUES(%s)"
                    bindData = (_category_name)
                    cursor.execute("USE production")		
                    cursor.execute(sqlQuery, bindData)
                    id = cursor.lastrowid
                    conn.commit()
                    response = str(f'Category added successfully! \nNew generated ID: {id}')
                    return response,200
                else:
                    return "Error due to wrong HTTP method selection"
            except Exception as e:
                return e
        elif validation_response != None:
            return validation_response
 

@app.route('/categories/update', methods=['PUT'])
def update_category():
        _json = request.json
        validation_response = validate_schema(_json, categories_schema)
        _category_id = _json['category_id']
        if validation_response == None and _category_id:
            try:
                _category_name = _json['category_name']	
                if request.method == 'PUT':			
                    sqlQuery = "UPDATE categories SET category_name=%s WHERE category_id=%s"
                    bindData = (_category_name,_category_id)
                    cursor.execute("USE production")
                    cursor.execute(sqlQuery, bindData)
                    conn.commit()
                    response = jsonify('Category updated successfully!')
                    response.status_code = 200
                    return response
                else:
                    return "Error due to wrong HTTP method selection"
            except Exception as e:
                return e
        elif validation_response != None:
            return validation_response
        

     

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
        
@app.errorhandler(400)
def handle_400(e):
    message = {
        'status': 400,
        'message': 'Error in JSON body format'
    }
    response = jsonify(message)
    response.status_code = 400
    return response