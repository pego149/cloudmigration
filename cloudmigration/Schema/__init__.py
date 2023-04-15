import os
import json


class Schema:
    def getSchema(platform: str):
        """
        Function to load the schema for the given platform.
        :param platform: Platform name
        :return: Dict containing the schema
        """
        path_to_schemas = os.path.dirname(__file__)
        schema_file = platform + ".json"
        schema = None
        if schema_file in os.listdir(path_to_schemas):
            with open(os.path.join(path_to_schemas, schema_file), 'r') as read_file:
                schema = json.load(read_file)
        return schema
