import json
import os
from cloudmigration.Mapper import Mapper

class Generic:
    def __init__(self, from_schema, to_schema, mapper: Mapper, from_schema_file_path=None, to_schema_file_path=None):
        self.path = os.path.dirname(__file__)
        self.mapper = mapper
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

    def getSchemaMetadata(self, schema, key):
        return schema["metadata"][key]

    def translateProperties(self, from_resource, from_properties, from_schema_properties, to_resource, to_schema_properties):
        to_properties = {}
        for from_property in from_properties:
            from_property_type = from_schema_properties[from_property]["type"]
            if from_properties[from_property] is not None and from_property_type != 'special':
                to_property = self.mapper.getPropertyPair(from_resource, from_property, to_resource)
                to_property_type = to_schema_properties[to_property]["type"]
                if to_property_type != 'special':
                    if (from_property_type == "value" and to_property_type == "value") or (isinstance(from_property_type, list) and isinstance(to_property_type, list)):
                        to_properties[to_property] = from_properties[from_property]
                    elif from_property_type == "value" and isinstance(to_property_type, list):
                        to_properties[to_property].append(from_properties[from_property])
                    elif isinstance(from_property_type, list) and to_property_type == "value":
                        to_properties[to_property] = from_properties[from_property][0]
        return to_properties

    def specialResourceFromGeneric(self, from_resource_type, from_resource_properties):
        return from_resource_type

    def specialResourceToGeneric(self, from_resource_type, from_resource_properties):
        return from_resource_type

    def specialPropertiesFromGeneric(self, from_resource_type, from_resource, to_resource_type, to_resource):
        return to_resource

    def specialPropertiesToGeneric(self, from_resource_type, from_resource, to_resource_type, to_resource):
        return to_resource

    def parameterFromGeneric(self, from_parameter):
        return from_parameter

    def parameterToGeneric(self, from_parameter):
        return from_parameter

    def fromGeneric(self, from_template):
        from_keys = self.from_schema["schema_metadata"]
        to_keys = self.to_schema["schema_metadata"]
        to_template = self.to_schema["template_structure"]
        to_template[to_keys["template_version"]] = from_template[from_keys["template_version"]]
        to_template[to_keys["description"]] = from_template[from_keys["description"]]

        for parameter in from_template[from_keys["parameters"]]:
            to_template[to_keys["parameters"]][parameter] = self.parameterFromGeneric(from_template[from_keys["parameters"]][parameter])

        for resource in from_template[from_keys["resources"]]:
            from_resource = from_template[from_keys["resources"]][resource]
            from_resource_type = from_resource[from_keys["resource"]["type"]]
            to_resource_type = self.mapper.getResourcePair("Generic", from_resource_type, self.__class__.__name__)
            if to_resource_type is not None:
                if self.to_schema[to_keys["resources"]][to_resource_type]["depends_on_properties"]:
                    to_resource_type = self.specialResourceFromGeneric(from_resource_type, from_resource[from_keys["properties"]])
                to_resource = {to_keys["type"]: to_resource_type}
                to_resource[to_keys["properties"]] = self.translateProperties(from_resource_type, from_resource[from_keys["properties"]], self.from_schema[from_keys["resources"]][from_resource_type][from_keys["properties"]], to_resource_type, self.to_schema[to_keys["resources"]][to_resource_type][to_keys["properties"]])
                to_resource = self.specialPropertiesFromGeneric(from_resource_type, from_resource, to_resource_type, to_resource)
                to_template[to_keys["resources"]][resource] = to_resource
            else:
                to_template[to_keys["resources"]][resource] = "Not Implemented - {0}".format(from_resource[from_keys["type"]])
                pass

    def toGeneric(self, from_template):
        from_keys = self.from_schema["schema_metadata"]
        to_keys = self.to_schema["schema_metadata"]
        to_template = self.to_schema["template_structure"]
        to_template[to_keys["template_version"]] = from_template[from_keys["template_version"]]
        to_template[to_keys["description"]] = from_template[from_keys["description"]]

        for parameter in from_template[from_keys["parameters"]]:
            to_template[to_keys["parameters"]][parameter] = self.parameterToGeneric(from_template[from_keys["parameters"]][parameter])

        for resource in from_template[from_keys["resources"]]:
            from_resource = from_template[from_keys["resources"]][resource]
            from_resource_type = from_resource[from_keys["resource"]["type"]]
            to_resource_type = self.mapper.getResourcePair(self.__class__.__name__, from_resource_type, "Generic")
            if to_resource_type is not None:
                if self.to_schema[to_keys["resources"]][to_resource_type]["depends_on_properties"]: #!!! Generic never depends on properties
                    to_resource_type = self.specialResourceToGeneric(from_resource_type, from_resource[from_keys["properties"]])
                to_resource = {to_keys["type"]: to_resource_type}
                to_resource[to_keys["properties"]] = self.translateProperties(from_resource_type, from_resource[from_keys["properties"]], self.from_schema[from_keys["resources"]][from_resource_type][from_keys["properties"]], to_resource_type, self.to_schema[to_keys["resources"]][to_resource_type][to_keys["properties"]])
                to_resource = self.specialPropertiesToGeneric(from_resource_type, from_resource, to_resource_type, to_resource)
                to_template[to_keys["resources"]][resource] = to_resource
            else:
                to_template[to_keys["resources"]][resource] = "Not Implemented - {0}".format(from_resource[from_keys["type"]])
                pass


class AWS(Generic):
    def __init__(self, from_schema, to_schema, mapper, from_schema_file_path=None, to_schema_file_path=None):
        Generic.__init__(self, from_schema, to_schema, mapper, from_schema_file_path, to_schema_file_path)

    def specialResourceFromGeneric(self, from_resource_type, from_resource_properties):
        to_resource_type = None
        if from_resource_type == "Generic::VM::SecurityGroupRule":
            if from_resource_properties["direction"] == "ingress":
                to_resource_type = "AWS::EC2::SecurityGroupIngress"
            elif from_resource_properties["direction"] == "egress":
                to_resource_type = "AWS::EC2::SecurityGroupEgress"
        return to_resource_type

    def fromGeneric(self, from_template):
        pass

    def toGeneric(self, from_template):
        pass


class OpenStack(Generic):
    def __init__(self, from_schema, to_schema, mapper, from_schema_file_path=None, to_schema_file_path=None):
        Generic.__init__(self, from_schema, to_schema, mapper, from_schema_file_path, to_schema_file_path)

    def parameterFromGeneric(self, from_parameter):
        to_parameter = {}
        to_parameter["type"] = from_parameter.get("type", None)
        to_parameter["name"] = from_parameter.get("name", None)
        to_parameter["default"] = from_parameter.get("default", None)
        to_parameter["constraints"] = []
        if "allowed_pattern" in from_parameter:
            to_parameter["constraints"].append(from_parameter["allowed_pattern"])
        if "allowed_values" in from_parameter:
            to_parameter["constraints"].append(from_parameter["allowed_values"])
        if "min_length" in from_parameter or "max_length" in from_parameter:
            length_dict = {}
            if from_parameter["min_length"] is not None:
                length_dict["min"] = from_parameter["min"]
            if from_parameter["mix_length"] is not None:
                length_dict["max"] = from_parameter["max"]
            to_parameter["constraints"].append({"length": length_dict})
        return to_parameter

    def parameterToGeneric(self, from_parameter):
        to_parameter = {}
        to_parameter["type"] = from_parameter.get("type", None)
        to_parameter["name"] = from_parameter.get("name", None)
        to_parameter["default"] = from_parameter.get("default", None)
        for constraint in from_parameter["constraints"]:
            if "allowed_pattern" in constraint:
                to_parameter["allowed_pattern"] = constraint["allowed_pattern"]
            elif "allowed_values" in constraint:
                to_parameter["allowed_values"] = constraint["allowed_values"]
            elif "length" in constraint:
                to_parameter["min_length"] = constraint["length"].get("min", None)
                to_parameter["max_length"] = constraint["length"].get("max", None)
        return to_parameter




