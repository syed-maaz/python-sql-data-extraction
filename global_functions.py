from jsonschema import ValidationError, validate
import json

def validate_schema(instance,schema):
    try:
        validate(instance=instance,schema=schema)
        print("JSON has been successfully validated.")
    except ValidationError as err:
       return "Validation Error:\n" + str(err).split('\n')[0]

def validate_json(_json):
    try:
        x = json.dumps(_json)
        json.loads(x)
        print("Following JSON is of VALID format")
        return True
    except ValueError as err:
        print("Following JSON is of INVALID format")
        return str(err)