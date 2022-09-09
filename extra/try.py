import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema import ValidationError
import jsonschema
import gladiator as gl

def validatejson(j):
    try:
        x= json.loads(j)
        print(x)
        return True
    except ValueError as err:
        print(err, "\nirtiza is good")
        return False



j_schema = {
    "type":"object",
    "properties":{
        "product name": {"type":"string"},
        "brand_id": {"type":"number"},
        "category_id": {"type":"number"},
        "model_year": {"type":"number"},
        "list-price": {"type":"integer"}
    },
    'minItems': 5,
    'required':['brand_id']
}

j = """{
        "product_name":"This is new Dell",
        "category_id": 8,
        "model_year": 2022,
        "list_price": 1495
        "brand_id": "12"
    }"""
    

validatejson(j)
# validatejson(json.dumps(j))
# x= validate(instance=j,schema=j_schema)
# print(x)

# print(len(j))

# print(len(j_schema['properties']))
# print(len(j_schema))

# result = gl.validate(field_validation,json)
# print(result)


