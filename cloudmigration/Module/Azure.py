import ast
import re

from cloudmigration.Module.Generic import Generic


class Azure(Generic):
    def __init__(self, from_platform, to_platform, from_schema, to_schema, mapper, from_schema_file_path=None, to_schema_file_path=None):
        """
        Constructor of class Azure Resource Manager. Sets attributes of the translation module
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
            # "Generic::VM::SecurityGroupRule": self.translateSecurityGroupRule,
            # "Generic::VM::Server": self.translateInstance,
            # "AWS::EC2::Instance": self.translateInstance,
            # "Generic::VM::SecurityGroup": self.translateSecurityGroup,
            # "AWS::EC2::SecurityGroup": self.translateSecurityGroup
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
            if from_resource[self.from_meta["properties"]]["direction"] == "ingress":
                to_resource_type = "AWS::EC2::SecurityGroupIngress"
            elif from_resource[self.from_meta["properties"]]["direction"] == "egress":
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
        if from_resource[self.from_meta["resource"]["type"]] == "AWS::EC2::Instance":
            ######## TODO check this!!!
            from_tags = from_resource[self.from_meta["resource"]["properties"]].get("Tags", [])
            if from_tags:
                names = [tag for tag in from_tags if "Name" in tag.get("Key", None)]
                to_resource[self.to_meta["resource"]["properties"]]["name"] = names[0]["Value"] if names else None
                from_tags.remove(names[0])
        #UserData
            from_property = "UserData"
            from_user_data = from_resource[self.from_meta["resource"]["properties"]].get(from_property, None)
            if from_user_data is not None:
                if "Fn::Base64" in from_user_data:
                    bare_data = self.listJoin(from_user_data["Fn::Base64"]["Fn::Join"][0], from_user_data["Fn::Base64"]["Fn::Join"][1:]) if "Fn::Join" in from_user_data["Fn::Base64"] else from_user_data["Fn::Base64"]
                    user_data_params = {}
                    pattern = "\{'Ref'.+?\}"
                    p = re.compile(pattern)
                    found_references = p.findall(bare_data)
                    if found_references:
                        for from_reference in found_references:
                            dict_reference = ast.literal_eval(from_reference)
                            to_reference = "${0}".format(dict_reference["Ref"])
                            user_data_params[to_reference] = dict_reference #Ref to ref will be handled by reference replacement method
                            bare_data = bare_data.replace(from_reference, to_reference)
                    to_property = self.mapper.getResourcePropertyPair(from_resource[self.from_meta["resource"]["type"]], from_property, to_resource[self.to_meta["resource"]["type"]])
                    to_resource[self.to_meta["resource"]["properties"]].setdefault(to_property, {})["bare_data"] = bare_data
                    if user_data_params:
                        to_resource[self.to_meta["resource"]["properties"]].setdefault(to_property, {})["params"] = user_data_params

        elif from_resource[self.from_meta["resource"]["type"]] == "Generic::VM::Server":
            if from_resource[self.from_meta["resource"]["properties"]]["name"] is not None:
                to_resource[self.to_meta["resource"]["properties"]].setdefault("Tags", []).append(
                    {"Key": "Name", "Value": from_resource[self.from_meta["resource"]["properties"]]["name"]})
            from_property = "user_data"
            from_user_data = from_resource[self.from_meta["resource"]["properties"]].get(from_property, None)
            if from_user_data is not None and "bare_data" in from_user_data:
                to_user_data = from_user_data["bare_data"]
                if "params" in from_user_data:
                    from_params = from_user_data["params"]

                    join_list = re.split("({0})".format(re.escape('|'.join(list(from_params)))), to_user_data)
                    print(join_list)
                    join_list = [{'Ref': from_params[element]['ref']} if element in from_params else element for element in join_list]
                    to_user_data = {"Fn::Join": ["", join_list]}
                to_property = self.mapper.getResourcePropertyPair(from_resource[self.from_meta["resource"]["type"]],
                                                                  from_property,
                                                                  to_resource[self.to_meta["resource"]["type"]])
                to_resource[self.to_meta["resource"]["properties"]].setdefault(to_property, {})["Fn::Base64"] = to_user_data

        return to_resource

    def translateResourceTags(self, from_resource, to_resource):
        """
        Method to translate resource tags if the ingoing or outgoing resource contains them.
        :param from_resource: Ingoing resource
        :param to_resource: Outgoing resource which will be updated.
        :return: Updated to_resource
        """
        if self.to_platform == "Generic":
            if self.mapper.getResourcePropertyPair(from_resource[self.from_meta["resource"]["type"]], "Tags", to_resource[self.to_meta["resource"]["type"]]) is not None:
                from_tags = from_resource.get("Tags", [])
                if from_tags is not None and from_tags:
                    for from_tag in from_tags:
                        to_resource[self.to_meta["resource"]["properties"]].setdefault("tags", []).append({"key": from_tag["Key"], "value": from_tag["Value"]})
        elif self.from_platform == "Generic":
            if self.mapper.getResourcePropertyPair(from_resource[self.from_meta["resource"]["type"]], "tags", to_resource[self.to_meta["resource"]["type"]]) is not None:
                from_tags = from_resource.get("tags", [])
                if from_tags is not None and from_tags:
                    for from_tag in from_tags:
                        to_resource.setdefault("tags", {})[from_tag["key"]] = from_tag["value"]
        return to_resource

    # def translateResource(self, from_resource):
    #     """
    #     Method to translate the ingoing resource. Uses and overrides perent method.
    #     :param from_resource: Resource to be translated
    #     :return: Translated resource (dict)
    #     """
    #     to_resource = super(self.__class__, self).translateResource(from_resource)
    #     if to_resource is not None:
    #         to_resource = self.translateResourceTags(from_resource, to_resource)
    #         # from_resource_type = from_resource[self.from_meta["resource"]["type"]]
    #         # to_resource = self.translateSpecial[from_resource_type](from_resource, to_resource) if self.translateSpecial.get(from_resource_type, None) is not None else to_resource
    #     return to_resource

    def translateKeys(self, ref, value, nonjson=False):
        """
        Recursivly goes through the dictionary obj and replaces keys with the convert function.
        :param ref: Dict in which the keys should be replaced
        :param value: Value of key
        :return: Object with translated keys
        """
        if self.from_platform == "Generic":
            if ref in ["get_param", "get_resource"]:
                return "[parameters('" + value + "')]"
            elif ref == "list_join":
                ref = "[concat("+ (", '"+value[0]+"', ")
        elif self.to_platform == "Generic":
            list = re.split('\[|\(\'|\'\)', value)
            if "parameters" in list[1]:
                ref = {"get_param" : list[2]}
            elif ref == "Fn::Join":
                ref = "list_join"
        return ref