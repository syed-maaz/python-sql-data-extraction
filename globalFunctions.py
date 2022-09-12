import errno
from tkinter import Y


def error_validation(json, modulename):
    json_schema = {
        'product_id': int,
        'product_name': str,
        'brand_id': int,
        'category_id': int,
        'model_year': int,
        'list_price': float,
        'brand_name': str,
        'category_name': str
    }

    json_count = {
        'products':['product_name', 'brand_id', 'category_id', 'model_year','list_price'],
        'brands': ['brand_name'],
        'categories': ['category_name']
    }
    y={}
    try:
        er=''
        if len(json) != len(json_count[modulename]):
            er = [x for x in json_count[modulename] if x not in json]
            er = f"Requires {len(json_count[modulename])} fields , and Provided {len(json)}. {er} missing."
        for key, value in json.items():
            if not isinstance(value, json_schema[key]):
                y[key] = f"Only accepts {json_schema[key]} you entered {type(value)}"
        if (er=='' and y == {}):
            err = False
        else:
            if er =='':
                er ='Number of fields provided is correct.'
            if y == {}:
                y= 'JSON format is valid'
            err = {"Number of Fields":er,"JSON Field Values":y}
        return err

    except Exception as e:
        return 'fieldname error:' +str(e)  