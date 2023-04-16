import collections.abc
import json
import os
import ast
from typing import MutableMapping, MutableSequence
from dotty_dict import dotty
from cloudmigration.Mapper import Mapper


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
        self.from_meta = from_schema["schema_metadata"]
        self.to_meta = to_schema["schema_metadata"]
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
    def translateProperties(self, _from, from_properties, from_schema_properties, _to, to_schema_properties, getMappingPair, recursion=""):

        """
        Method to translate a dict of from_properties to a dict of to_properties. Properties of type different from "value" or [] will not be translated.
        :param _from: Platform or resource type of the ingoing properties.
        :param from_properties: Dict of template parameter or resource properties
        :param from_schema_properties: Schema of the ingoing properties used for property type check.
        :param _to: Platform or resource type of the outgoing properties.
        :param to_schema_properties: Schema of the outgoing properties used for property type check.
        :param getMappingPair: Function which finds property pairs. Usually supplied functions in the mapper module.
        :return: Dict of translated properties
        """

        to_property_path = ""
        to_properties = {}
        for from_property, value in from_properties.items():
            if from_property in self.from_meta["resource"]["ref"]:#or isinstance(value, str) and any(x in value for x in self.from_meta["resource"]["ref"]):
                return self.translateKeys(from_property, value)
            if from_property == self.from_meta["resource"]["tags"] or from_property == self.from_meta["resource"]["type"]:
                continue
            if not recursion == '':
                from_property_splited = recursion + '.' + from_property
                to_property = getMappingPair(_from, from_property_splited, _to)
            else:
                from_property_splited = from_property
                to_property = getMappingPair(_from, from_property, _to)
            if to_property is None and isinstance(from_properties[from_property], dict):
                if recursion == '':
                    nested_properties = self.translateProperties(_from, from_properties[from_property],
                                                                 from_schema_properties, _to, to_schema_properties,
                                                                 getMappingPair, from_property)
                else:
                    nested_properties = self.translateProperties(_from, from_properties[from_property],
                                                                 from_schema_properties, _to, to_schema_properties,
                                                                 getMappingPair, recursion + "." + from_property)
                if nested_properties:
                    to_property = getMappingPair(_from, from_property, _to)
                    nested = False
                    if to_property is None:
                        nested = True
                        from_property_path = from_property + "." + list(nested_properties.keys())[0]
                        to_property = getMappingPair(_from, from_property_path, _to)
                    if to_property is not None:
                        if not recursion == '':
                            to_property_splited = to_property.replace(recursion + '.', '')
                        else:
                            to_property_splited = to_property
                        to_property_path = self.print_path_to_key(to_property_splited, to_schema_properties)
                        if not self.key_exists(to_property_path, to_properties) and not nested:
                            self.set_nested(to_property_path, to_properties, nested_properties)
                        elif nested:
                            self.set_nested(to_property_path, to_properties, list(nested_properties.values())[0])
                        else:
                            to_properties.update(nested_properties)

            elif to_property is not None:
                to_property_splited = to_property
                if not recursion == '':
                    from_property_path = self.print_path_to_key(from_property_splited, from_schema_properties)
                else:
                    from_property_path = self.print_path_to_key(recursion + from_property_splited, from_schema_properties)
                to_property_path = self.print_path_to_key(to_property_splited, to_schema_properties)
                if from_properties[from_property] is not None and not isinstance(from_properties[from_property], dict) and from_property_splited != "type":  # NULL MAY BE IMPORTANT
                    from_property_type = self.get_nested(from_property_path, from_schema_properties)["type"]
                    to_property_type = self.get_nested(to_property, to_schema_properties)["type"]
                    if to_property_type != 'special' and from_property_type != 'special':
                        if (from_property_type == "value" and to_property_type == "value") or (isinstance(from_property_type, list) and isinstance(to_property_type, list) and not from_property_type and not to_property_type):
                            if isinstance(value, str) and any(x in value for x in self.from_meta["resource"]["ref"]):
                                value = self.translateKeys("."+from_property, value)
                            self.set_nested(to_property_path, to_properties, value)
                        elif from_property_type == "value" and isinstance(to_property_type, list):
                            to_properties.setdefault(to_property_path, []).append(from_properties[from_property])
                        elif isinstance(from_property_type, list) and to_property_type == "value":
                            to_property_path = ''.join(to_property.rsplit("."+str(list(from_properties[from_property][0].keys())[0]), 1))
                            self.set_nested(to_property_path, to_properties, from_properties[from_property][0])

                elif isinstance(from_properties[from_property], dict):
                    if recursion == '':
                        nested_properties = self.translateProperties(_from, from_properties[from_property], from_schema_properties, _to, to_schema_properties, getMappingPair, from_property)
                    else:
                        nested_properties = self.translateProperties(_from, from_properties[from_property], from_schema_properties, _to, to_schema_properties, getMappingPair, recursion + "." + from_property)
                    if isinstance(nested_properties, str):
                        self.set_nested(to_property_path, to_properties, nested_properties)
                    elif isinstance(nested_properties, dict):
                        if not self.key_exists(to_property_path, nested_properties) and not self.key_exists(self.to_meta["resource"]["properties"] + "." + to_property_path, nested_properties):
                            self.set_nested(to_property_path, to_properties, nested_properties)
                        else:
                            self.update(to_properties, nested_properties)
        if len(to_properties) > 0 and isinstance(list(to_properties.values())[0], dict) and all(k in to_schema_properties for k in list(to_properties.values())[0]):
            to_properties = list(to_properties.values())[0]
        return to_properties

    def translateParameterType(self, from_parameter_type):
        to_parameter_type = self.mapper.getParameterTypePair(self.from_platform, from_parameter_type, self.to_platform)
        return to_parameter_type if from_parameter_type is not None else self.to_meta["parameter"]["default_type"]

    def translateParameter(self, from_parameter):
        """
        Method to translate parameter properties.
        :param from_parameter: Dict of parameter properties
        :return: Dict of translated parameter properties
        """
        #from_parameter_type = from_parameter[self.from_meta["parameter"]["type"]]
        #to_parameter_type = self.translateParameterType(from_parameter[self.from_meta["parameter"]["type"]])
        #to_parameter = self.translateProperties(from_parameter_type,
        #                                        from_parameter,
        #                                        self.from_schema[self.from_meta["parameters"]],
        #                                        to_parameter_type,
        #                                        self.to_schema[self.to_meta["parameters"]],
        #                                        self.mapper.getParameterPropertyPair)
        to_parameter = self.translateProperties(self.from_platform, from_parameter, self.from_schema[self.from_meta["parameters"]], self.to_platform, self.to_schema[self.to_meta["parameters"]], self.mapper.getParameterPropertyPair)
        if self.to_meta["parameter"]["type"] in to_parameter:
            to_parameter[self.to_meta["parameter"]["type"]] = self.translateParameterType(from_parameter[self.from_meta["parameter"]["type"]])
        #     todo translate parameter types function
        return to_parameter

    def translateResourceType(self, from_resource_type, from_resource=None):
        """
        Method to translate resource type.
        :param from_resource_type: Resource type of the ingoing resource
        :param from_resource: The resource to be translated. Added in case outgoing resource type depends on resource properties. Defaults to None.
        :return: Resource type of the outgoing resource.
        """
        to_resource_type = self.mapper.getResourceTypePair(self.from_platform, from_resource_type, self.to_platform)
        return to_resource_type

    def translateResourceTags(self, from_resource, to_resource):
        """
        Method to translate resource tags if the ingoing or outgoing resource contains them.
        :param from_resource: Ingoing resource
        :param to_resource: Outgoing resource which will be updated.
        :return: Updated to_resource
        """
        return to_resource

    def translateResource(self, from_resource):
        """
        Method to translate the ingoing resource. Method first translates the type of the resource and then its properties.
        :param from_resource: Resource to be translated
        :return: Translated resource (dict)
        """
        from_resource_type = from_resource[self.from_meta["resource"]["type"]]
        to_resource_type = self.translateResourceType(from_resource_type, from_resource)
        if to_resource_type is not None:
            to_resource = self.translateProperties(from_resource_type,
                                                       from_resource, #TODO check
                                                       self.from_schema[self.from_meta["resources"]][from_resource_type],
                                                       to_resource_type,
                                                       self.to_schema[self.to_meta["resources"]][to_resource_type],
                                                       self.mapper.getResourcePropertyPair)
            to_resource[self.to_meta["resource"]["type"]] = to_resource_type
            to_resource = self.translateSpecial[from_resource_type](from_resource, to_resource) if self.translateSpecial.get(from_resource_type, None) is not None else to_resource
            to_resource = self.translateResourceTags(from_resource, to_resource)
        else:
            to_resource = None
        return to_resource

    def translateKeys(self, ref, value):
        """
        Method to translate references and special functions in a template.
        :param ref: The key to be translated
        :param value: The value assigne to the key.
        :return: Returns translated reference.
        """
        return { ref: value }

    def translateTemplate(self, from_template):
        """
        Method to translate the template.
        :param from_template: Dict containing the template to be translated
        :return: Dict containing the translated template
        """
        self.to_template = self.to_schema["template_structure"]
        if self.to_meta["template_version"] in self.to_template and self.to_template[self.to_meta["template_version"]] is None and from_template.get(self.from_meta["template_version"], None) is not None:
            self.to_template[self.to_meta["template_version"]] = from_template[self.from_meta["template_version"]]
        try:
            self.to_template[self.to_meta["description"]] = from_template[self.from_meta["description"]].rstrip()
        except (KeyError, AttributeError):
            pass
        # todo translateParameters method
        # In case of of different parameter configuration in template, create method translateParameters
        for parameter in from_template[self.from_meta["parameters"]]:
            self.to_template[self.to_meta["parameters"]][parameter] = self.translateParameter(from_template[self.from_meta["parameters"]][parameter])
        if isinstance(from_template[self.from_meta["resources"]], dict): #if resources are a dictionary
            for resource in from_template[self.from_meta["resources"]]:
                from_resource = from_template[self.from_meta["resources"]][resource]
                to_resource = self.translateResource(from_resource)
                if to_resource is not None:
                    if self.to_platform != "Azure":
                        self.to_template[self.to_meta["resources"]][resource] = to_resource
                    else:
                        self.to_template[self.to_meta["resources"]].append(to_resource)
                else:
                    "Not Implemented - {0}".format(from_resource[self.from_meta["resource"]["type"]])
        elif isinstance(from_template[self.from_meta["resources"]], list): #if resources are a dictionary
            for index, resource in enumerate(from_template[self.from_meta["resources"]]):
                to_resource = self.translateResource(resource)
                if to_resource is not None:
                    if self.from_platform == "Azure":
                        self.to_template[self.to_meta["resources"]]['Resource'+str(index)] = to_resource
                    else:
                        self.to_template[self.to_meta["resources"]].append(to_resource)
                else:
                    "Not Implemented - {0}".format(resource[self.from_meta["resource"]["type"]])
        #self.to_template = self.changeKeys(self.to_template, self.translateKeys)
        return self.to_template

    def set_nested(self,path, obj, value):
        *path, last = path.split(".")
        for bit in path:
            obj = obj.setdefault(bit, {})
        obj[last] = value

    def get_nested(self, path, obj):
        *path, last = path.split(".")
        for bit in path:
            obj = obj.setdefault(bit, {})
        return obj[last]

    def key_exists(self, path, obj):
        if path is None:
            return False
        path_parts = path.split(".")
        for part in path_parts:
            if part in obj:
                obj = obj[part]
            else:
                return False
        return True

    def print_path_to_key(self, value, d):
        queue = [(k, v, k) for k, v in d.items()]
        while queue:
            key, val, path = queue.pop(0)
            if key == value:
                return path
            if isinstance(val, dict):
                for k, v in val.items():
                    queue.append((k, v, f"{path}.{k}"))
        return value

    def update(self, d, u):
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = self.update(d.get(k, {}), v)
            else:
                d[k] = v
        return d