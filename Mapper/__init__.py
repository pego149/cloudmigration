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
        with open(os.path.join(self.path, mapping_file), 'r') as read_file:
            self.mapping = json.load(read_file)

    def loadMapping(self, mapping_file):
        with open(mapping_file, 'r') as read_file:
            self.mapping = json.load(read_file)

    def updateMapping(self, mapping_file='mapping.json'):
        mapping = {
            "platforms": defaultdict(list),
            "resources": defaultdict(list)
        }
        for file_name in os.listdir(self.path):
        # for file_name in os.listdir(os.path.dirname(__file__)):
        # for file_name in os.listdir('.'):
            added_platforms = []
            if file_name.endswith(".txt"):
                with open(os.path.join(self.path, file_name), 'r') as read_file:
                    for line in read_file.readlines():
                        split_line = line.split("\t")
                        mapping["platforms"][split_line[0]].append(split_line[1])
                        if split_line[0] in added_platforms:
                            with open(os.path.join(self.path, file_name), 'r') as read_file_2:
                                for special_line in read_file_2.readlines():
                                    special_line = special_line.split("\t")
                                    if special_line[0] != split_line[0]:
                                        mapping["platforms"][special_line[0]].append(special_line[1])
                        added_platforms.append(split_line[0])
                        if split_line[1] != '-':
                            mapping["resources"][split_line[1]].append(
                                [resource_property.rstrip() for resource_property in split_line[2:]])
        with open(os.path.join(self.path, mapping_file), "w") as write_file:
            json.dump(mapping, write_file, indent=2)
        self.mapping = mapping

    def getResourcePair(self, paFromPlatform, paFromResource, paToPlatform):
        if paFromResource in self.mapping["platforms"][paFromPlatform]:
            return self.mapping["platforms"][paToPlatform][self.mapping["platforms"][paFromPlatform].index(paFromResource)]
        else:
            return None

    def getPropertyPair(self, paFromResource, paFromProperty, paToResource):
        if paFromProperty in self.mapping["resources"][paFromResource]:
            return self.mapping["resources"][paToResource][self.mapping["resources"][paFromResource].index(paFromProperty)]
        else:
            return None
# # print bla.path
# # print bla.mapping
# # bla.updateMapping('mapping_2.json')