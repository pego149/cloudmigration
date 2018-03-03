import os
import json

def getSchema(paPlatform):
    path_to_schemas = os.path.dirname(__file__)
    schema_file = "{0}.json".format(paPlatform)
    schema = None
    if schema_file in os.listdir(path_to_schemas):
        with open(os.path.join(path_to_schemas, schema_file), 'r') as read_file:
            schema = json.load(read_file)
    return schema
