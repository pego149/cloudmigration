import json
import os
from cloudmigration.Mapper import Mapper
import re



class Generic:
    def __init__(self, from_platform, to_platform, from_schema, to_schema, mapper: Mapper, from_schema_file_path=None, to_schema_file_path=None):
        """
        Constructor of class Generic. Sets attributes of the translation module
        :param from_platform: Platform from which the template should be translated
        :param to_platform: Platform to which the template should be translated
        :param from_schema: Schema of the ingoing template
        :param to_schema: Schema of the outgoing template
        :param mapper: Instance of Mapper
        :param from_schema_file_path: File from which the ingoing shcema should be loaded. Defaults to None.
        :param to_schema_file_path: File from which the outgoing shcema should be loaded. Defaults to None.
        """
        self.path = os.path.dirname(__file__)
        self.mapper = mapper
        self.from_platform = from_platform
        self.to_platform = to_platform
        self.from_schema = dict(from_schema)
        self.to_schema = dict(to_schema)
        self.from_keys = from_schema["schema_metadata"]
        self.to_keys = to_schema["schema_metadata"]
        self.to_template = None
        self.translateSpecial = {}
        if from_schema_file_path is not None:
            with open(from_schema_file_path, 'r') as read_file:
                self.from_schema = json.load(read_file)
        if to_schema_file_path is not None:
            with open(to_schema_file_path, 'r') as read_file:
                self.to_schema = json.load(read_file)

    def listJoin(self, delimiter, from_list):
        """
        Method to simulate Fn::Join and list_join template functions.
        Creates a string containing from_list elements separated by delimiter.
        :param delimiter: The delimiter which separates the elements of the list
        :param from_list: List to be joined
        :return: String of joined list elements
        """
        to_string = ""
        for element in from_list[:-1]:
            if isinstance(element, list):
                to_string += "{0}{1}".format(self.listJoin(delimiter, element), delimiter)
            else:
                to_string += "{0}{1}".format(str(element), delimiter)
        to_string += self.listJoin(delimiter, from_list[-1]) if isinstance(from_list[-1], list) else str(from_list[-1])
        return to_string

    def changeKeys(self, obj, convert):
        """
        Recursivly goes through the dictionary obj and replaces keys with the convert function.
        :param obj: Dict in which the keys should be replaced
        :param convert: Function which handles the translation
        :return: Object with translated keys
        """
        if isinstance(obj, dict):
            new = {}
            for k, v in obj.items():
                new[convert(k, v)] = self.changeKeys(v, convert)
        elif isinstance(obj, list):
            new = []
            for v in obj:
                new.append(self.changeKeys(v, convert))
        else:
            return obj
        return new

    def str_replace(self):
        pass

    def loadFromSchema(self, from_schema=None, from_schema_file_path=None):
        """
        Method to load from_schema from a specified file or dict
        :param from_schema: dict containing from_schema
        :param from_schema_file_path: File path to file containing schema in json format
        """
        if from_schema is not None:
            self.from_schema = from_schema
        elif from_schema_file_path is not None:
            with open(from_schema_file_path, 'r') as read_file:
                self.from_schema = json.load(read_file)

    def loadToSchema(self, to_schema=None, to_schema_file_path=None):
        """
        Method to load from_schema from a specified file or dict
        :param to_schema: dict containing from_schema
        :param to_schema_file_path: File path to file containing schema in json format
        """
        if to_schema is not None:
            self.to_schema = to_schema
        elif to_schema_file_path is not None:
            with open(to_schema_file_path, 'r') as read_file:
                self.to_schema = json.load(read_file)

    # def getSchemaMetadata(self, schema, key):
    #     return schema["metadata"[key]


    # CAN TRANSLATE AS MANY PROPERTIES AS I LIKE
    def translateProperties(self, _from, from_properties, from_schema_properties, _to, to_schema_properties, getMappingPair):

        """
        Method to translate a dict of from_properties to a dict of to_properties. Properties of type different from "value" or [] will not be translated.
        :param _from: Platform or resource type of the ingoing properties.
        :param from_properties: Dict of template parameter or resource properties
        :param from_schema_properties: Schema of the ingoing properties used for property type check.
        :param _to: Platform or resource type of the ougoing properties.
        :param to_schema_properties: Schema of the outgoing properties used for property type check.
        :param getMappingPair: Function which finds property pairs. Usually supplied functions in the mapper module.
        :return: Dict of translated properties
        """
        to_properties = {}
        for from_property in from_properties:
            if from_properties[from_property] is not None: #NULL MAY BE IMPORTANT
                to_property = getMappingPair(_from, from_property, _to)
                if to_property is not None:
                    from_property_type = from_schema_properties[from_property]["type"]
                    to_property_type = to_schema_properties[to_property]["type"]
                    if to_property_type != 'special' and from_property_type != 'special':
                        if (from_property_type == "value" and to_property_type == "value") or (isinstance(from_property_type, list) and isinstance(to_property_type, list) and not from_property_type and not to_property_type):
                            to_properties[to_property] = from_properties[from_property]
                        elif from_property_type == "value" and isinstance(to_property_type, list):
                            to_properties.setdefault(to_property, []).append(from_properties[from_property])
                        elif isinstance(from_property_type, list) and to_property_type == "value":
                            to_properties[to_property] = from_properties[from_property][0] if from_properties[from_property] else None
        return to_properties

    def translateParameter(self, from_parameter):
        """
        Method to translate parameter properties.
        :param from_parameter: Dict of parameter properties
        :return: Dict of translated parameter properties
        """
        to_parameter = self.translateProperties(self.from_platform, from_parameter, self.from_schema["parameter"], self.to_platform, self.to_schema["parameter"], self.mapper.getParameterPropertyPair)
        #     todo translate parameter types function
        return to_parameter

    def translateResourceType(self, from_resource_type, from_resource=None):
        """
        Method to translate resource type.
        :param from_resource_type: Resource type of the ingoing resource
        :param from_resource: The resource to be translated. Added in case outgoing resource type depends on resource properties. Defaults to None.
        :return: Resource type of the outgoing resource.
        """
        to_resource_type = self.mapper.getResourcePair(self.from_platform, from_resource_type, self.to_platform)
        return to_resource_type

    def translateResource(self, from_resource):
        """
        Method to translate the ingoing resource. Method first translates the type of the resource and then its properties.
        :param from_resource: Resource to be translated
        :return: Translated resource (dict)
        """
        from_resource_type = from_resource[self.from_keys["resource"]["type"]]
        to_resource_type = self.translateResourceType(from_resource_type, from_resource)
        if to_resource_type is not None:
            to_resource = { self.to_keys["resource"]["type"]: to_resource_type }
            to_resource[self.to_keys["resource"]["properties"]] = self.translateProperties(from_resource_type,
                                                                          from_resource[self.from_keys["resource"]["properties"]],
                                                                          self.from_schema[self.from_keys["resources"]][from_resource_type][self.from_keys["resource"]["properties"]],
                                                                          to_resource_type,
                                                                          self.to_schema[self.to_keys["resources"]][to_resource_type][self.to_keys["resource"]["properties"]],
                                                                          self.mapper.getPropertyPair)
        else:
            to_resource = None
        return to_resource

    def translateReference(self, ref, value):
        """
        Method to translate references and special functions in a template.
        :param ref: The key to be translated
        :param value: The value assigne to the key.
        :return: Returns translated reference.
        """
        return ref

    def translateTemplate(self, from_template):
        """
        Method to translate the template.
        :param from_template: Dict containing the template to be translated
        :return: Dict containing the translated template
        """
        self.to_template = self.to_schema["template_structure"]
        self.to_template[self.to_keys["template_version"]] = from_template[self.from_keys["template_version"]]
        self.to_template[self.to_keys["description"]] = from_template[self.from_keys["description"]]
        # todo translateParameters method
        # In case of of different parameter configuration in template, create method translateParameters
        for parameter in from_template[self.from_keys["parameters"]]:
            self.to_template[self.to_keys["parameters"]][parameter] = self.translateParameter(from_template[self.from_keys["parameters"]][parameter])
        for resource in from_template[self.from_keys["resources"]]:
            from_resource = from_template[self.from_keys["resources"]][resource]
            if isinstance(from_template[self.from_keys["resources"]], dict): #if resources are a dictionary
                to_resource = self.translateResource(from_resource)
                self.to_template[self.to_keys["resources"]][resource] = to_resource if to_resource is not None else "Not Implemented - {0}".format(from_resource[self.from_keys["resource"]["type"]])
        self.to_template = self.changeKeys(self.to_template, self.translateReference)
        return self.to_template


class AWS(Generic):
    def __init__(self, from_platform, to_platform, from_schema, to_schema, mapper, from_schema_file_path=None, to_schema_file_path=None):
        """
        Constructor of class AWS. Sets attributes of the translation module
        :param from_platform: Platform from which the template should be translated
        :param to_platform: Platform to which the template should be translated
        :param from_schema: Schema of the ingoing template
        :param to_schema: Schema of the outgoing template
        :param mapper: Instance of Mapper
        :param from_schema_file_path: File from which the ingoing shcema should be loaded. Defaults to None.
        :param to_schema_file_path: File from which the outgoing shcema should be loaded. Defaults to None.
        """
        Generic.__init__(self, from_platform, to_platform, from_schema, to_schema, mapper, from_schema_file_path, to_schema_file_path)
        self.translateSpecial = {
            "Generic::VM::SecurityGroupRule": self.translateSecurityGroupRule,
            "Generic::VM::Server": self.translateInstance,
            "AWS::EC2::Instance": self.translateInstance,
            "Generic::VM::SecurityGroup": self.translateSecurityGroup,
            "AWS::EC2::SecurityGroup": self.translateSecurityGroup
        }

    def translateResourceType(self, from_resource_type, from_resource=None):
        """
        Method to translate resource type. Overrides parent method.
        :param from_resource_type: Resource type of the ingoing resource
        :param from_resource: The resource to be translated.
        Added in case outgoing resource type depends on resource properties. Defaults to None.
        :return: Resource type of the outgoing resource.
        """
        to_resource_type = None
        if from_resource_type == "Generic::VM::SecurityGroupRule":
            if from_resource[self.from_keys["properties"]]["direction"] == "ingress":
                to_resource_type = "AWS::EC2::SecurityGroupIngress"
            elif from_resource[self.from_keys["properties"]]["direction"] == "egress":
                to_resource_type = "AWS::EC2::SecurityGroupEgress"
        else:
            to_resource_type = super(self.__class__, self).translateResourceType(from_resource_type)
        return to_resource_type

    def translateInstance(self, from_resource, to_resource):
        """
        Method to translate special properties of an instance.
        :param from_resource: Ingoing resource
        :param to_resource: Outgoing resource which will be updated.
        :return: Updated to_resource
        """
        if from_resource[self.from_keys["resource"]["type"]] == "AWS::EC2::Instance":
            ######## TODO check this!!!
            names = [tag.get("Value", None) for tag in from_resource[self.from_schema["resource"]["properties"]].get("Tags", {}) if "Name" in tag.get("Key", None)]
            to_resource[self.to_keys["resource"]["properties"]]["name"] = names[0] if names else None
        #UserData
            from_property = "UserData"
            from_user_data = from_resource[self.from_keys["resource"]["properties"]].get(from_property, None)
            if from_user_data is not None:
                if "Fn::Base64" in from_user_data:
                    bare_data = self.listJoin(from_user_data["Fn::Base64"]["Fn::Join"][0], from_user_data["Fn::Base64"]["Fn::Join"][1:]) if "Fn::Join" in from_user_data["Fn::Base64"] else from_user_data["Fn::Base64"]
                    user_data_params = {}
                    pattern = "\{'Ref'.+?\}"
                    p = re.compile(pattern)
                    found_references = p.findall(bare_data)
                    if found_references:
                        for from_reference in found_references:
                            dict_reference = json.loads(from_reference)
                            to_reference = "${0}".format(dict_reference["Ref"])
                            user_data_params[to_reference] = dict_reference #Ref to ref will be handled by reference replacement method
                            bare_data = bare_data.replace(from_reference, to_reference)
                    to_property = self.mapper.getPropertyPair(from_resource[self.from_keys["resource"]["type"]], from_property, to_resource[self.to_keys["resource"]["type"]])
                    to_resource[self.to_keys["resource"]["properties"]].setdefault(to_property, {})["bare_data"] = bare_data
                    if user_data_params:
                        to_resource[self.to_keys["resource"]["properties"]].setdefault(to_property, {})["params"] = user_data_params

        elif from_resource[self.from_keys["resource"]["type"]] == "Generic::VM::Server":
            if from_resource[self.from_keys["resource"]["properties"]]["name"] is not None:
                to_resource[self.to_keys["resource"]["properties"]].setdefault("Tags", []).append(
                    {"Key": "Name", "Value": from_resource[self.from_keys["resource"]["properties"]]["name"]})
            from_property = "user_data"
            from_user_data = from_resource[self.from_keys["resource"]["properties"]].get(from_property, None)
            if from_user_data is not None and "bare_data" in from_user_data:
                to_user_data = from_user_data["bare_data"]
                if "params" in from_user_data:
                    from_params = from_user_data["params"]
                    join_list = re.split('|'.join(list(from_params)), to_user_data)
                    join_list = [{'Ref': from_params[element]['ref']} if element in from_params else element for element in join_list]
                    to_user_data = {"Fn::Join": ["", join_list]}
                to_property = self.mapper.getPropertyPair(from_resource[self.from_keys["resource"]["type"]],
                                                          from_property,
                                                          to_resource[self.to_keys["resource"]["type"]])
                to_resource[self.to_keys["resource"]["properties"]].setdefault(to_property, {})["Fn::Base64"] = to_user_data

        return to_resource

    def translateSecurityGroup(self, from_resource, to_resource):
        """
        Method to translate special properties of a security group.
        :param from_resource: Ingoing resource
        :param to_resource: Outgoing resource which will be updated.
        :return: Updated to_resource
        """
        from_resource_type = from_resource[self.from_keys["resource"]["type"]]
        to_resource_type = to_resource[self.to_keys["resource"]["type"]]
        if from_resource_type == "AWS::EC2::SecurityGroup":
            for from_rules in ["SecurityGroupIngress", "SecurityGroupEgress"]:
                from_rule_type = self.from_schema[self.from_keys["resource"]["properties"]][from_rules]["type"]
                to_rules = self.mapper.getPropertyPair(from_resource_type, from_rules, to_resource_type)
                to_rule_type = self.translateResourceType(from_rule_type)
                for from_rule in from_rules:
                    to_rule = self.translateProperties(from_rule_type, from_rule, self.from_schema[self.from_keys["resources"]][from_rule_type], to_rule_type, self.to_schema[self.to_keys["resources"]][to_rule_type], self.mapper.getPropertyPair)
                    to_rule["direction"] = "ingress" if from_rules == "SecurityGroupIngress" else "egress"
                    to_resource[self.to_keys["resource"]["properties"]].setdefault(to_rules, []).append(to_rule)

        elif from_resource_type == "Generic::VM::SecurityGroup":
            for from_rule in from_resource[self.from_keys["resource"]["properties"]["rules"]]:
                if from_rule.get("direction", None) in ["ingress", "egress"]:
                    from_rule_type = self.from_schema[self.from_keys["resource"]["properties"]]["rules"]["type"]
                    to_rules = "SecurityGroupIngress" if from_rule.get("direction", None) == "ingress" else "SecurityGroupEgress"
                    to_rule_type = to_resource[self.to_keys["resource"]["properties"]][to_rules]["type"]
                    to_rule = self.translateProperties(from_rule_type, from_rule, self.from_schema[self.from_keys["resources"]][from_rule_type], to_rule_type, self.to_schema[self.to_keys["resources"]][to_rule_type], self.mapper.getPropertyPair)
                    to_resource[self.to_keys["resource"]["properties"]].setdefault(to_rules, []).append(to_rule)
        return to_resource

    def translateSecurityGroupRule(self, from_resource, to_resource):
        """
        Method to translate special properties of a security group rule.
        :param from_resource: Ingoing resource
        :param to_resource: Outgoing resource which will be updated.
        :return: Updated to_resource
        """
        if from_resource[self.from_keys["resource"]["type"]] == "AWS::EC2::SecurityGroupEgress":
            to_resource[self.to_keys["resource"]["properties"]]["direction"] = "egress"
        elif from_resource[self.from_keys["resource"]["type"]] == "AWS::EC2::SecurityGroupIngress":
            to_resource[self.to_keys["resource"]["properties"]]["direction"] = "ingress"
        return to_resource

    def translateResourceTags(self, from_resource, to_resource):
        """
        Method to translate resource tags if the ingoing or outgoing resource contains them.
        :param from_resource: Ingoing resource
        :param to_resource: Outgoing resource which will be updated.
        :return: Updated to_resource
        """
        if self.to_platform == "Generic":
            if self.mapper.getPropertyPair(from_resource[self.from_keys["resource"]["type"]], "Tags", to_resource[self.to_keys["resource"]["type"]]) is not None:
                from_tags = from_resource[self.from_keys["resource"]["properties"]].get("Tags", [])
                if from_tags is not None and from_tags:
                    for from_tag in from_tags:
                        to_resource[self.to_keys["resource"]["properties"]].setdefault("tags", []).append({"key": from_tag["Key"], "value": from_tag["Value"]})
        elif self.from_platform == "Generic":
            if self.mapper.getPropertyPair(from_resource[self.from_keys["resource"]["type"]], "tags", to_resource[self.to_keys["resource"]["type"]]) is not None:
                from_tags = from_resource[self.from_keys["resource"]["properties"]].get("tags", [])
                if from_tags is not None and from_tags:
                    for from_tag in from_tags:
                        to_resource[self.to_keys["resource"]["properties"]].setdefault("Tags", []).append({"Key": from_tag["key"], "Value": from_tag["value"]})
        return to_resource

    def translateResource(self, from_resource):
        """
        Method to translate the ingoing resource. Uses and overrides perent method.
        :param from_resource: Resource to be translated
        :return: Translated resource (dict)
        """
        to_resource = super(self.__class__, self).translateResource(from_resource)
        if to_resource is not None:
            to_resource = self.translateResourceTags(from_resource, to_resource)
            from_resource_type = from_resource[self.from_keys["resource"]["type"]]
            to_resource = self.translateSpecial[from_resource_type](from_resource, to_resource) if self.translateSpecial.get(from_resource_type, None) is not None else to_resource
        return to_resource

    def translateReference(self, ref, value):
        """
        Method to translate references and special functions in a template.
        :param ref: The key to be translated
        :param value: The value assigne to the key.
        :return: Returns translated reference.
        """
        if self.from_platform == "Generic":
            if ref == "ref":
                ref = "Ref"
            elif ref == "list_join":
                ref = "Fn::Join"
        elif self.to_platform == "Generic":
            if ref == "Ref":
                ref = "ref"
            elif ref == "Fn::Join":
                ref = "list_join"
        return ref

class OpenStack(Generic):
    def __init__(self, from_platform, to_platform, from_schema, to_schema, mapper, from_schema_file_path=None, to_schema_file_path=None):
        """
        Constructor of class OpenStack. Sets attributes of the translation module
        :param from_platform: Platform from which the template should be translated
        :param to_platform: Platform to which the template should be translated
        :param from_schema: Schema of the ingoing template
        :param to_schema: Schema of the outgoing template
        :param mapper: Instance of Mapper
        :param from_schema_file_path: File from which the ingoing shcema should be loaded. Defaults to None.
        :param to_schema_file_path: File from which the outgoing shcema should be loaded. Defaults to None.
        """
        Generic.__init__(self, from_platform, to_platform, from_schema, to_schema, mapper, from_schema_file_path, to_schema_file_path)
        self.translateSpecial = {
            "Generic::VM::SecurityGroup": self.translateSecurityGroup,
            "OS::Neutron::SecurityGroup": self.translateSecurityGroup
        }
    def translateParameter(self, from_parameter):
        """
        Method to translate parameter properties. Uses and overrides parent method.
        :param from_parameter: Dict of parameter properties
        :return: Dict of translated parameter properties
        """
        to_parameter = super(self.__class__, self).translateParameter(from_parameter)
        if self.to_platform == "Generic":
            for constraint in from_parameter.get("constraints", []):
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
    # todo prerobit aby kontrolovalo ci dany resource ma tagy!!! mapper.tranlateproperty is None...
    def translateResourceTags(self, from_resource, to_resource):
        if self.to_platform == "Generic":
            if self.mapper.getPropertyPair(from_resource[self.from_keys["resource"]["type"]], "tags", to_resource[self.to_keys["resource"]["type"]]) is not None:
                from_tags = from_resource[self.from_keys["resource"]["properties"]].get("tags", [])
                if from_tags:
                    for from_tag in from_tags:
                        i = 1
                        to_resource[self.to_keys["resource"]["properties"]].setdefault("tags", []).append({"key": "Key{0}".format(i), "value": from_tag})
                        i += 1
        elif self.from_platform == "Generic":
            if self.mapper.getPropertyPair(from_resource[self.from_keys["resource"]["type"]], "tags", to_resource[self.to_keys["resource"]["type"]]) is not None:
                from_tags = from_resource[self.from_keys["resource"]["properties"]].get("tags", [])
                if from_tags:
                    for from_tag in from_tags:
                        to_resource[self.to_keys["resource"]["properties"]].setdefault("tags", []).append(from_tag["value"])
        return to_resource

    def translateInstance(self, from_resource, to_resource):
        """
        Method to translate special properties of an instance.
        :param from_resource: Ingoing resource
        :param to_resource: Outgoing resource which will be updated.
        :return: Updated to_resource
        """
        if from_resource[self.from_keys["resource"]["type"]] == "OS::Nova::Server":
            from_property = "user_data"
            from_user_data = from_resource[self.from_keys["resource"]["properties"]].get(from_property, None)
            if from_user_data is not None:
                to_user_data = from_user_data["str_replace"]["template"] if "str_replace" in from_user_data else from_user_data
                to_params = from_user_data["str_replace"]["params"] if "str_replace" in from_user_data else None
                to_property = self.mapper.getPropertyPair(from_resource[self.from_keys["resource"]["type"]],
                                                          from_property, to_resource[self.to_keys["resource"]["type"]])
                to_resource[self.to_keys["resource"]["properties"]].setdefault(to_property, {})["bare_data"] = to_user_data
                if to_params is not None:
                    to_resource[self.to_keys["resource"]["properties"]].setdefault(to_property, {})["params"] = to_params

        elif from_resource[self.from_keys["resource"]["type"]] == "Generic::VM::Server":
            from_property = "user_data"
            from_user_data = from_resource[self.from_keys["resource"]["properties"]].get(from_property, None)
            if from_user_data is not None:
                to_user_data = from_user_data.get("bare_data", None)
                to_params = from_user_data.get("params", None)
                if to_user_data is not None:
                    to_property = self.mapper.getPropertyPair(from_resource[self.from_keys["resource"]["type"]],
                                                              from_property,
                                                              to_resource[self.to_keys["resource"]["type"]])
                    to_resource[self.to_keys["resource"]["properties"]][to_property] = {}
                    if to_params is not None:
                        to_resource[self.to_keys["resource"]["properties"]][to_property]["str_replace"] = {"template": to_user_data, "params": to_params}
                    else:
                        to_resource[self.to_keys["resource"]["properties"]][to_property] = to_user_data
        return to_resource

    def translateSecurityGroup(self, from_resource, to_resource):
        """
        Method to translate special properties of a security group.
        :param from_resource: Ingoing resource
        :param to_resource: Outgoing resource which will be updated.
        :return: Updated to_resource
        """
        from_resource_type = from_resource[self.from_keys["resource"]["type"]]
        if from_resource_type == "Generic::VM::SecurityGroup" or from_resource_type == "OS::Neutron::SecurityGroup": #"rules" have the same name
            from_rule_type = self.from_schema[self.from_keys["resource"]["properties"]]["rules"]["type"]
            to_rule_type = self.translateResourceType(from_rule_type)
            to_resource[self.to_keys["resource"]["properties"]]["rules"] = [self.translateProperties(from_rule_type, from_rule,
                                     self.from_schema[self.from_keys["resources"]][from_rule_type], to_rule_type,
                                     self.to_schema[self.to_keys["resources"]][to_rule_type],
                                     self.mapper.getPropertyPair) for from_rule in from_resource[self.from_keys["resource"]["properties"]]["rules"]]

        return to_resource

    def translateResource(self, from_resource):
        """
        Method to translate the ingoing resource. Uses and overrides perent method.
        :param from_resource: Resource to be translated
        :return: Translated resource (dict)
        """
        to_resource = super(self.__class__, self).translateResource(from_resource)
        if to_resource is not None:
            from_resource_type = from_resource[self.from_keys["resource"]["type"]]
            to_resource = self.translateResourceTags(from_resource, to_resource)
            to_resource = self.translateSpecial[from_resource_type](from_resource, to_resource) if self.translateSpecial.get(from_resource_type, None) is not None else to_resource

        return to_resource

    def translateReference(self, ref, value):
        """
        Method to translate references and special functions in a template.
        :param ref: The key to be translated
        :param value: The value assigne to the key.
        :return: Returns translated reference.
        """
        if self.from_platform == "Generic":
            if ref == "ref":
                if value in self.to_template[self.to_keys["parameters"]]:
                    ref = "get_param"
                else:
                    ref = "get_resource"
        elif self.to_platform == "Generic":
            if ref in ["get_param", "get_resource"]:
                ref = "ref"
        return ref

#todo network/subnet
#in Openstack tags are only string values, in AWS {"Key": bla, "Value": bla}
# https://docs.openstack.org/heat/pike/api/heat.engine.cfn.functions.html#heat.engine.cfn.functions.Ref

