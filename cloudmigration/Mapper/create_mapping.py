import os
from collections import defaultdict
import json
mapping = {
    "platforms": defaultdict(list),
    "resources": defaultdict(list)
}


for file_name in os.listdir('../../Mapper'):
    added_platforms = []
    if file_name.endswith(".csv"):
        with open(file_name, 'r') as read_file:
            for line in read_file.readlines():
                split_line = line.split(",")
                mapping["platforms"][split_line[0]].append(split_line[1])
                if split_line[0] in added_platforms:
                    with open(file_name, 'r') as read_file_2:
                        for special_line in read_file_2.readlines():
                            special_line = special_line.split("\t")
                            if special_line[0] != split_line[0]:
                                mapping["platforms"][special_line[0]].append(special_line[1])
                added_platforms.append(split_line[0])

                if split_line[1] != '-':
                    mapping["resources"][split_line[1]].append([resource_property.rstrip() for resource_property in split_line[2:]])

with open("mapping.json", "w") as write_file:
    json.dump(mapping, write_file, indent=2)