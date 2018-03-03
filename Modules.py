import json
import os
from cloudmigration.Mapper import Mapper

class Generic:
    def __init__(self, from_schema, to_schema, from_schema_file_path=None, to_schema_file_path=None):
        self.path = os.path.dirname(__file__)
        # self.mapping = mapping
        self.from_schema = from_schema
        self.to_schema = to_schema
        if from_schema_file_path is not None:
            with open(from_schema_file_path, 'r') as read_file:
                self.from_schema = json.load(read_file)
        if to_schema_file_path is not None:
            with open(to_schema_file_path, 'r') as read_file:
                self.to_schema = json.load(read_file)

    def loadFromSchema(self, from_schema=None, from_schema_file_path=None):
        if from_schema is not None:
            self.from_schema = from_schema
        elif from_schema_file_path is not None:
            with open(from_schema_file_path, 'r') as read_file:
                self.from_schema = json.load(read_file)

    def loadToSchema(self, to_schema=None, to_schema_file_path=None):
        if to_schema is not None:
            self.to_schema = to_schema
        elif to_schema_file_path is not None:
            with open(to_schema_file_path, 'r') as read_file:
                self.to_schema = json.load(read_file)

    def translateProperties(self, from_resource, from_properties, from_schema_properties, to_resource, to_schema_properties, mapper: Mapper):
        to_properties = {}
        for from_property in from_properties:
            from_property_type = from_schema_properties[from_property]["type"]
            if from_properties[from_property] is not None and from_property_type != 'special':
                to_property = mapper.getPropertyPair(from_resource, from_property, to_resource)
                to_property_type = to_schema_properties[to_property]["type"]
                if to_property_type != 'special':
                    if (from_property_type == "value" and to_property_type == "value") or (isinstance(from_property_type, list) and isinstance(to_property_type, list)):
                        to_properties[to_property] = from_properties[from_property]
                    elif from_property_type == "value" and isinstance(to_property_type, list):
                        to_properties[to_property].append(from_properties[from_property])
                    elif isinstance(from_property_type, list) and to_property_type == "value":
                        to_properties[to_property] = from_properties[from_property][0]
        return to_properties

    def fromGeneric(self, from_template, mapper):
        pass

    def toGeneric(self, from_template, mapper):
        pass

    # def setResourceProperties(self, paFromResource, paToResource, paMapper=Mapper()):
    #     for from_property, to_property in paMapper.mapping["resources"][paFromResource], paMapper.mapping["resources"][paToResource]:
    #         if from_property
    #


class AWS(Generic):
    def __init__(self, from_schema, to_schema, from_schema_file_path=None, to_schema_file_path=None):
        Generic.__init__(self, from_schema, to_schema, from_schema_file_path, to_schema_file_path)

    def fromGeneric(self, from_template, mapper):
        pass

    def toGeneric(self, from_template, mapper):
        pass

class OpenStack(Generic):
    def __init__(self, from_schema, to_schema, from_schema_file_path=None, to_schema_file_path=None):
        Generic.__init__(self, from_schema, to_schema, from_schema_file_path, to_schema_file_path)

    def fromGeneric(self, from_template, mapper):
        pass

    def toGeneric(self, from_template, mapper):
        pass
