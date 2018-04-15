import json
import os
from collections import defaultdict

# modules = ["OS","AWS"]
# bla = {}
# for module in modules:
#     bla[module] = __import__(module, fromlist=[module])
#

# print os.path.dirname(__file__)

class Mapper:
    def __init__(self, mapping_file = 'mapping.json'):
        self.path = os.path.dirname(__file__)
        if mapping_file is None:
            mapping_file = 'mapping.json'
        try:
            with open(os.path.join(self.path, mapping_file), 'r') as read_file:
                self.mapping = json.load(read_file)
        except json.decoder.JSONDecodeError:
            self.updateMapping()

    def loadMapping(self, mapping_file):
        """
        Method to load mapping from a file.
        :param mapping_file: Name of the file containing the mapping in JSON format
        """
        with open(mapping_file, 'r') as read_file:
            self.mapping = json.load(read_file)

    def updateMapping(self, mapping_file='mapping.json'):
        """
        Method to create a JSON file containing the mapping of resources and properties.
        :param mapping_file: Name of the file which will contain the updated mapping.
        """
        mapping = {
            "resource_types": defaultdict(list),
            "resource_properties": defaultdict(list),
            "parameter_properties": defaultdict(list)
        }
        for file_name in os.listdir(self.path):
            added_platforms = []
            if file_name.endswith(".txt"):
                with open(os.path.join(self.path, file_name), 'r') as read_file:
                    for line in read_file.readlines():
                        split_line = line.split("\t")
                        if file_name == "Parameter.txt":
                            mapping["parameter_properties"][split_line[0]] = [parameter_property.rstrip() if parameter_property.rstrip() != "-" else None for parameter_property in split_line[1:]]
                        else:
                            mapping["resource_types"][split_line[0]].append(split_line[1] if split_line[1] != "-" else None)
                            if split_line[0] in added_platforms:
                                with open(os.path.join(self.path, file_name), 'r') as read_file_2:
                                    for special_line in read_file_2.readlines():
                                        special_line = special_line.split("\t")
                                        if special_line[0] != split_line[0]:
                                            mapping["resource_types"][special_line[0]].append(special_line[1] if special_line[1] != "-" else None)
                            added_platforms.append(split_line[0])
                            if split_line[1] != '-':
                                mapping["resource_properties"][split_line[1]] = [resource_property.rstrip() if resource_property.rstrip() != "-" else None for resource_property in split_line[2:]]
        with open(os.path.join(self.path, mapping_file), "w") as write_file:
            json.dump(mapping, write_file, indent=2)
        self.mapping = mapping

    def getParameterPropertyPair(self, from_platform, from_parameter_property, to_platform):
        """
        Method to find the equivalent of a parameter property in the mapping
        :param from_platform: Ingoing platform
        :param from_parameter_property: Parameter property name
        :param to_platform: Outgoing platform
        :return: Equivalent of the parameter property if it exists, else None
        """
        if from_parameter_property in self.mapping["parameter_properties"][from_platform]:
            return self.mapping["parameter_properties"][to_platform][self.mapping["parameter_properties"][from_platform].index(from_parameter_property)]
        else:
            return None

    def getResourceTypePair(self, from_platform, from_resource, to_platform):
        """
        Method to find the equivalent of a resource in the mapping
        :param from_platform: Ingoing platform
        :param ffrom_resource: Name of the resource
        :param to_platform: Outgoing platform
        :return: Equivalent of the resource if it exists, else None
        """
        if from_resource in self.mapping["resource_types"][from_platform]:
            return self.mapping["resource_types"][to_platform][self.mapping["resource_types"][from_platform].index(from_resource)]
        else:
            return None

    def getResourcePropertyPair(self, from_resource, from_property, to_resource):
        """
        Method to find the equivalent of a parameter property in the mapping
        :param from_resource: Ingoing resource
        :param from_property: Resource property name
        :param to_resource: Outgoing resource
        :return: Equivalent of the resource property if it exists, else None
        """
        if from_property in self.mapping["resource_properties"][from_resource]:
            return self.mapping["resource_properties"][to_resource][self.mapping["resource_properties"][from_resource].index(from_property)]
        else:
            return None