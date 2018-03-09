import json
import os
from ..cloudmigration.Mapper import Mapper

class Generic:
    def __init__(self, from_platform, to_platform, from_schema, to_schema, mapper: Mapper, from_schema_file_path=None, to_schema_file_path=None):
        self.path = os.path.dirname(__file__)
        self.mapper = mapper
        self.from_platform = from_platform
        self.to_platform = to_platform
        self.from_schema = from_schema
        self.to_schema = to_schema
        self.from_keys = from_schema["schema_metadata"]
        self.to_keys = to_schema["schema_metadata"]
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

    # def getSchemaMetadata(self, schema, key):
    #     return schema["metadata"[key]


    # CAN TRANSLATE AS MANY PROPERTIES AS I LIKE
    def translateProperties(self, _from, from_properties, from_schema_properties, _to, to_schema_properties, getMappingPair):
        to_properties = {}
        for from_property in from_properties:
            if from_properties[from_property] is not None: #NULL MAY BE IMPORTANT
                to_property = getMappingPair(_from, from_property, _to)
                if to_property is not None:
                    from_property_type = from_schema_properties[from_property]["type"]
                    to_property_type = to_schema_properties[to_property]["type"]
                    if to_property_type != 'special' and from_property_type != 'special':
                        if (from_property_type == "value" and to_property_type == "value") or (isinstance(from_property_type, list) and isinstance(to_property_type, list)):
                            to_properties[to_property] = from_properties[from_property]
                        elif from_property_type == "value" and isinstance(to_property_type, list):
                            to_properties.setdefault(to_property, []).append(from_properties[from_property])
                        elif isinstance(from_property_type, list) and to_property_type == "value":
                            to_properties[to_property] = from_properties[from_property][0] if from_properties[from_property] else None
        return to_properties

    # def translateResourceProperties(self, from_resource, from_properties, from_schema_properties, to_resource, to_schema_properties):
    #     to_properties = {}
    #     for from_property in from_properties:
    #         from_property_type = from_schema_properties[from_property]["type"]
    #         if from_properties[from_property] is not None and from_property_type != 'special':
    #             to_property = self.mapper.getPropertyPair(from_resource, from_property, to_resource)
    #             if to_property is not None:
    #                 to_property_type = to_schema_properties[to_property]["type"]
    #                 if to_property_type != 'special':
    #                     if (from_property_type == "value" and to_property_type == "value") or (isinstance(from_property_type, list) and isinstance(to_property_type, list)):
    #                         to_properties[to_property] = from_properties[from_property]
    #                     elif from_property_type == "value" and isinstance(to_property_type, list):
    #                         to_properties[to_property].append(from_properties[from_property])
    #                     elif isinstance(from_property_type, list) and to_property_type == "value":
    #                         to_properties[to_property] = from_properties[from_property][0]
    #     return to_properties
    #
    # def specialResourceFromGeneric(self, from_resource_type, from_resource_properties):
    #     return from_resource_type
    #
    # def specialResourceToGeneric(self, from_resource_type, from_resource_properties):
    #     return from_resource_type
    # #
    # def specialPropertiesFromGeneric(self, from_resource_type, from_resource, to_resource_type, to_resource):
    #     return to_resource
    #
    # def specialPropertiesToGeneric(self, from_resource_type, from_resource, to_resource_type, to_resource):
    #     return to_resource
    # # todo include parameter_property_type translation (string, boolean...)
    # # todo include parameters as list or dict
    #
    # def parameterFromGeneric(self, from_parameter):
    #     return from_parameter
    #
    # def parameterToGeneric(self, from_parameter):
    #     return from_parameter
    # todo replace fromGeneric and toGeneric with translateTemplate(from_template), uses self.to_generic: Bool variable or self.from_platform, self.to_platform
    # def fromGeneric(self, from_template):
    #     self.from_keys = self.from_schema["schema_metadata"]
    #     self.to_keys = self.to_schema["schema_metadata"]
    #     to_template = self.to_schema["template_structure"]
    #     to_template[self.to_keys["template_version"]] = from_template[self.from_keys["template_version"]]
    #     to_template[self.to_keys["description"]] = from_template[self.from_keys["description"]]
    #
    #     for parameter in from_template[self.from_keys["parameters"]]:
    #         to_template[self.to_keys["parameters"]][parameter] = self.parameterFromGeneric(from_template[self.from_keys["parameters"]][parameter])
    #
    #     for resource in from_template[self.from_keys["resources"]]:
    #         # todo if resources is list, if resources is dict
    #         from_resource = from_template[self.from_keys["resources"]][resource]
    #         from_resource_type = from_resource[self.from_keys["resource"]["type"]]
    #         to_resource_type = self.mapper.getResourcePair("Generic", from_resource_type, self.__class__.__name__)
    #         if to_resource_type is not None:
    #             # todo add in_properties to schemas --- if property is not in properties, push it higher
    #             # todo replace resource handling in function
    #             if self.to_schema[self.to_keys["resources"]][to_resource_type]["depends_on_properties"]:
    #                 to_resource_type = self.specialResourceFromGeneric(from_resource_type, from_resource[self.from_keys["properties"]])
    #             to_resource = {self.to_keys["type"]: to_resource_type}
    #             to_resource[self.to_keys["properties"]] = self.translateResourceProperties(from_resource_type, from_resource[self.from_keys["properties"]], self.from_schema[self.from_keys["resources"]][from_resource_type][self.from_keys["properties"]], to_resource_type, self.to_schema[self.to_keys["resources"]][to_resource_type][self.to_keys["properties"]])
    #             to_resource = self.specialPropertiesFromGeneric(from_resource_type, from_resource, to_resource_type, to_resource)
    #             to_template[self.to_keys["resources"]][resource] = to_resource
    #         else:
    #             to_template[self.to_keys["resources"]][resource] = "Not Implemented - {0}".format(from_resource[self.from_keys["type"]])
    #             pass
    #
    # def toGeneric(self, from_template):
    #     self.from_keys = self.from_schema["schema_metadata"]
    #     self.to_keys = self.to_schema["schema_metadata"]
    #     to_template = self.to_schema["template_structure"]
    #     to_template[self.to_keys["template_version"]] = from_template[self.from_keys["template_version"]]
    #     to_template[self.to_keys["description"]] = from_template[self.from_keys["description"]]
    #
    #     for parameter in from_template[self.from_keys["parameters"]]:
    #         to_template[self.to_keys["parameters"]][parameter] = self.parameterToGeneric(from_template[self.from_keys["parameters"]][parameter])
    #
    #     for resource in from_template[self.from_keys["resources"]]:
    #         from_resource = from_template[self.from_keys["resources"]][resource]
    #         from_resource_type = from_resource[self.from_keys["resource"]["type"]]
    #         to_resource_type = self.mapper.getResourcePair(self.__class__.__name__, from_resource_type, "Generic")
    #         if to_resource_type is not None:
    #             if self.to_schema[self.to_keys["resources"]][to_resource_type]["depends_on_properties"]: #!!! Generic never depends on properties
    #                 to_resource_type = self.specialResourceToGeneric(from_resource_type, from_resource[self.from_keys["properties"]])
    #             to_resource = {self.to_keys["type"]: to_resource_type}
    #             to_resource[self.to_keys["properties"]] = self.translateResourceProperties(from_resource_type, from_resource[self.from_keys["properties"]], self.from_schema[self.from_keys["resources"]][from_resource_type][self.from_keys["properties"]], to_resource_type, self.to_schema[self.to_keys["resources"]][to_resource_type][self.to_keys["properties"]])
    #             to_resource = self.specialPropertiesToGeneric(from_resource_type, from_resource, to_resource_type, to_resource)
    #             to_template[self.to_keys["resources"]][resource] = to_resource
    #         else:
    #             to_template[self.to_keys["resources"]][resource] = "Not Implemented - {0}".format(from_resource[self.from_keys["type"]])
    #             pass

    def translateParameter(self, from_parameter):
        to_parameter = self.translateProperties(self.from_platform, from_parameter, self.from_schema["parameter"], self.to_platform, self.to_schema["parameter"], self.mapper.getParameterPropertyPair)
        #     todo translate parameter types function
        return to_parameter

    # def translateResourceType(self, from_resource_type):
    #     self.from_keys = self.from_schema["schema_metadata"]
    #     self.to_keys = self.to_schema["schema_metadata"]
    #     from_resource_type = from_resource[self.from_keys["resource"]["type"]]
    #     to_resource_type = self.mapper.getResourcePair(self.from_platform, from_resource_type, self.to_platform)
    #     return to_resource_type

    def translateResourceType(self, from_resource_type, from_resource=None):
        to_resource_type = self.mapper.getResourcePair(self.from_platform, from_resource_type, self.to_platform)
        return to_resource_type

    def translateResource(self, from_resource):
        # self.from_keys = self.from_schema["schema_metadata"]
        # self.to_keys = self.to_schema["schema_metadata"]
        from_resource_type = from_resource[self.from_keys["resource"]["type"]]
        to_resource_type = self.translateResourceType(from_resource_type, from_resource)
        # to_resource_type = self.mapper.getResourcePair(self.from_platform, from_resource_type, self.to_platform)
        if to_resource_type is not None:
            to_resource = { self.to_keys["type"]: to_resource_type }
            to_resource[self.to_keys["properties"]] = self.translateProperties(from_resource_type,
                                                                          from_resource[self.from_keys["properties"]],
                                                                          self.from_schema[self.from_keys["resources"]][from_resource_type][self.from_keys["resource"]["properties"]],
                                                                          to_resource_type,
                                                                          self.to_schema[self.to_keys["resources"]][to_resource_type][self.to_keys["resource"]["properties"]],
                                                                          self.mapper.getResourcePair)
        else:
            to_resource = "Not Implemented - {0}".format(from_resource_type)
        return to_resource


    def translateTemplate(self, from_template):
        to_template = self.to_schema["template_structure"]
        to_template[self.to_keys["template_version"]] = from_template[self.from_keys["template_version"]]
        to_template[self.to_keys["description"]] = from_template[self.from_keys["description"]]
        # todo translateParameters method
        # In case of of different parameter configuration in template, create method translateParameters
        for parameter in from_template[self.from_keys["parameters"]]:
            to_template[self.to_keys["parameters"]][parameter] = self.translateParameter(from_template[self.from_keys["parameters"]][parameter])
        for resource in from_template[self.from_keys["resources"]]:
            from_resource = from_template[self.from_keys["resources"]]
            if isinstance(from_template[self.from_keys["resources"]], dict): #if resources are a dictionary
                to_resource = self.translateResource(from_resource)
                to_template[self.to_keys["resources"]][resource] = to_resource
        return to_template


class AWS(Generic):
    def __init__(self, from_platform, to_platform, from_schema, to_schema, mapper, from_schema_file_path=None, to_schema_file_path=None):
        Generic.__init__(self, from_platform, to_platform, from_schema, to_schema, mapper, from_schema_file_path, to_schema_file_path)

    def translateResourceType(self, from_resource_type, from_resource=None):
        to_resource_type = None
        if from_resource_type == "Generic::VM::SecurityGroupRule":
            if from_resource[self.from_keys["properties"]]["direction"] == "ingress":
                to_resource_type = "AWS::EC2::SecurityGroupIngress"
            elif from_resource[self.from_keys["properties"]]["direction"] == "egress":
                to_resource_type = "AWS::EC2::SecurityGroupEgress"
        else:
            to_resource_type = super(self.__class__, self).translateResourceType(from_resource_type)
        return to_resource_type

    def translateResourceTags(self, from_resource):
        to_tags = []
        if self.to_platform == "Generic":
            from_tags = from_resource[self.from_keys["resource"]["properties"]].get("Tags", [])
            if from_tags is not None and from_tags:
                for from_tag in from_tags:
                    to_tags.append(
                        {"key": from_tag["Key"], "value": from_tag["Value"]})
        elif self.from_platform == "Generic":
            from_tags = from_resource[self.from_keys["resource"]["properties"]].get("tags", [])
            if from_tags is not None and from_tags:
                for from_tag in from_tags:
                    to_tags.append(
                        {"Key": from_tag["key"], "Value": from_tag["value"]})
        return to_tags

    def translateResource(self, from_resource):
        to_resource = super(self.__class__, self).translateResource(from_resource)
        tags = self.translateResourceTags(from_resource)
        from_resource_type=self.from_keys["resource"]["type"]

        # AWS instance
        if self.to_platform == "Generic":
            if from_resource_type == "AWS::EC2::Instance":
                ######## TODO check this!!!
                to_resource[self.to_keys["resource"]["properties"]]["name"] = [tag["Value"] for tag in from_resource[self.from_schema["resource"]["properties"]]["Tags"] if "Name" in tag["Key"]][0]
            elif from_resource_type == "AWS::EC2::SecurityGroupEgress":
                to_resource[self.to_keys["resource"]["properties"]]["direction"] = "egress"
            elif from_resource_type == "AWS::EC2::SecurityGroupIngress":
                to_resource[self.to_keys["resource"]["properties"]]["direction"] = "inress"
            "Generic::VM::SecurityGroupRule"

            if tags:
                to_resource[self.to_keys["resource"]["properties"]]["tags"] = tags



        elif self.from_platform == "Generic":
            if from_resource_type == "Generic::VM::Server":
                to_resource[self.to_keys["resource"]["properties"]].setdefault("Tags", []).append({"Key": "Name", "Value": from_resource[self.from_keys["resource"]["properties"]]["name"]})
            if tags:
                to_resource[self.to_keys["resource"]["properties"]]["Tags"] = tags


        # todo special cases to and from generic



        return to_resource

class OpenStack(Generic):
    def __init__(self, from_platform, to_platform, from_schema, to_schema, mapper, from_schema_file_path=None, to_schema_file_path=None):
        Generic.__init__(self, from_platform, to_platform, from_schema, to_schema, mapper, from_schema_file_path, to_schema_file_path)

    def translateParameter(self, from_parameter):
        to_parameter = super(self.__class__, self).translateParameter(from_parameter)
        if self.to_platform == "Generic":
            for constraint in from_parameter.get("constraints", []):
                # if "allowed_pattern" in constraint:
                #     to_parameter["allowed_pattern"] = constraint["allowed_pattern"]
                # elif "allowed_values" in constraint:
                #     to_parameter["allowed_values"] = constraint["allowed_values"]
                if "length" in constraint:
                    to_parameter["min_length"] = constraint["length"].get("min", None)
                    to_parameter["max_length"] = constraint["length"].get("max", None)
                elif "range" in constraint:
                    to_parameter["min_value"] = constraint["range"].get("min", None)
                    to_parameter["max_value"] = constraint["range"].get("max", None)
                else:
                    to_parameter.update(
                        self.translateProperties(self.from_platform, constraint, self.from_schema["parameter"],
                                                 self.to_platform, self.to_schema["parameter"],
                                                 self.mapper.getParameterPropertyPair))
        elif self.from_platform == "Generic":
            length = {}
            range = {}
            if from_parameter.get("min_length", None) is not None:
                length["min"] = from_parameter.get("min_length")
            if from_parameter.get("max_length", None) is not None:
                length["max"] = from_parameter.get("max_length")
            if from_parameter.get("min_value", None) is not None:
                range["min"] = from_parameter.get("min_value")
            if from_parameter.get("max_value", None) is not None:
                range["max"] = from_parameter.get("max_value")
            for to_property in list(to_parameter):
                if self.to_schema["parameter"][to_property].get("in_constraints", False):
                    if to_parameter.get(to_property, None) is not None:
                        to_parameter.setdefault("constraints", []).append({to_property: to_parameter.pop(to_property)})
            if length:
                to_parameter.setdefault("constraints", []).append({"length": length})
            if range:
                to_parameter.setdefault("constraints", []).append({"range": range})
        return to_parameter

    def translateResourceTags(self, from_resource):
        to_tags = []
        if self.to_platform == "Generic":
            from_tags = from_resource[self.from_keys["resource"]["properties"]].get("tags", [])
            if from_tags:
                for from_tag in from_tags:
                    i = 1
                    to_tags.append({"key": "Key{0}".format(i), "value": from_tag})
                    i += 1
        elif self.from_platform == "Generic":
            from_tags = from_resource[self.from_keys["resource"]["properties"]].get("tags", [])
            if from_tags:
                for from_tag in from_tags:
                    to_tags.append(from_tag["value"])
        return to_tags

    def translateResource(self, from_resource):
        to_resource = super(self.__class__, self).translateResource(from_resource)
        tags = self.translateResourceTags(from_resource)
        # todo special cases to and from generic
        if self.to_platform == "Generic":
            if tags:
                to_resource[self.to_keys["resource"]["properties"]]["tags"] = tags
        elif self.to_platform == "Generic":
            if tags:
                to_resource[self.to_keys["resource"]["properties"]]["tags"] = tags
        return to_resource

#todo securitygrouprules
#todo userdata
#todo network/subnet
#todo securitygroup
#in Openstack tags are only string values, in AWS {"Key": bla, "Value": bla}
