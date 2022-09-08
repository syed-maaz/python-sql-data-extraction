def error_validation(json,modulename):
    json_schema = {
        'product_id' : int,
        'product_name' : str,
        'brand_id' : int,
        'category_id' : int,
        'model_year' : int,
        'list_price' : float,
        'brand_name':str,
        'category_name':str
    }

    json_count = {
            'products' :5,
            'brands':1,
            'categories':1
        }

    err = []
    if len(json) == json_count[modulename]:
        for key,value in json.items():
            if not isinstance(value,json_schema[key]):
                err.append(f"The value for {key} is invalid. Only accepts {json_schema[key]} you entered {type(value)}")
        if err == []:
            err = True
        return err
    else:
        return f"The number of fields provided is incorrect. Requires {json_count[modulename]} fields. Provided {len(json)}."