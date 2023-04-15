from cloudmigration.Module.Generic import Generic


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
            "OS::Neutron::SecurityGroup": self.translateSecurityGroup,
            "OS::Nova::Server": self.translateInstance,
            "Generic::VM::Server": self.translateInstance
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
                        self.translateProperties(self.from_platform,
                                                 constraint,
                                                 self.from_schema["parameters"],
                                                 self.to_platform,
                                                 self.to_schema["parameters"],
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
                if self.to_schema["parameters"][to_property].get("in_constraints", False):
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
            if self.mapper.getResourcePropertyPair(from_resource[self.from_meta["resource"]["type"]], "tags", to_resource[self.to_meta["resource"]["type"]]) is not None:
                from_tags = from_resource[self.from_meta["resource"]["properties"]].get("tags", [])
                if from_tags:
                    i = 1
                    for from_tag in from_tags:
                        to_resource.setdefault("tags", []).append({"key": "Key{0}".format(i), "value": from_tag})
                        i += 1
        elif self.from_platform == "Generic":
            if self.mapper.getResourcePropertyPair(from_resource[self.from_meta["resource"]["type"]], "tags", to_resource[self.to_meta["resource"]["type"]]) is not None:
                from_tags = from_resource[self.from_meta["resource"]["properties"]].get("tags", [])
                if from_tags:
                    for from_tag in from_tags:
                        to_resource[self.to_meta["resource"]["properties"]].setdefault("tags", []).append(from_tag["value"])
        return to_resource

    def translateInstance(self, from_resource, to_resource):
        """
        Method to translate special properties of an instance.
        :param from_resource: Ingoing resource
        :param to_resource: Outgoing resource which will be updated.
        :return: Updated to_resource
        """
        if from_resource[self.from_meta["resource"]["type"]] == "OS::Nova::Server":
            from_property = "user_data"
            from_user_data = from_resource[self.from_meta["resource"]["properties"]].get(from_property, None)
            if from_user_data is not None:
                to_user_data = from_user_data["str_replace"]["template"] if "str_replace" in from_user_data else from_user_data
                to_params = from_user_data["str_replace"]["params"] if "str_replace" in from_user_data else None
                to_property = self.mapper.getResourcePropertyPair(from_resource[self.from_meta["resource"]["type"]],
                                                                  from_property, to_resource[self.to_meta["resource"]["type"]])
                to_resource[self.to_meta["resource"]["properties"]].setdefault(to_property, {})["bare_data"] = to_user_data
                if to_params is not None:
                    to_resource[self.to_meta["resource"]["properties"]].setdefault(to_property, {})["params"] = to_params

        elif from_resource[self.from_meta["resource"]["type"]] == "Generic::VM::Server":
            from_property = "user_data"
            from_user_data = from_resource[self.from_meta["resource"]["properties"]].get(from_property, None)
            if from_user_data is not None:
                to_user_data = from_user_data.get("bare_data", None)
                to_params = from_user_data.get("params", None)
                if to_user_data is not None:
                    to_property = self.mapper.getResourcePropertyPair(from_resource[self.from_meta["resource"]["type"]],
                                                                      from_property,
                                                                      to_resource[self.to_meta["resource"]["type"]])
                    to_resource[self.to_meta["resource"]["properties"]][to_property] = {}
                    if to_params is not None:
                        to_resource[self.to_meta["resource"]["properties"]][to_property]["str_replace"] = {"template": to_user_data, "params": to_params}
                    else:
                        to_resource[self.to_meta["resource"]["properties"]][to_property] = to_user_data
        return to_resource

    def translateSecurityGroup(self, from_resource, to_resource):
        """
        Method to translate special properties of a security group.
        :param from_resource: Ingoing resource
        :param to_resource: Outgoing resource which will be updated.
        :return: Updated to_resource
        """
        from_resource_type = from_resource[self.from_meta["resource"]["type"]]
        if from_resource_type == "Generic::VM::SecurityGroup" or from_resource_type == "OS::Neutron::SecurityGroup": #"rules" have the same name
            from_rule_type = self.from_schema[self.from_meta["resource"]["properties"]]["rules"]["type"]
            to_rule_type = self.translateResourceType(from_rule_type)
            to_resource[self.to_meta["resource"]["properties"]]["rules"] = [self.translateProperties(from_rule_type, from_rule,
                                                                                                     self.from_schema[self.from_meta["resources"]][from_rule_type], to_rule_type,
                                                                                                     self.to_schema[self.to_meta["resources"]][to_rule_type],
                                                                                                     self.mapper.getResourcePropertyPair) for from_rule in from_resource[self.from_meta["resource"]["properties"]]["rules"]]

        return to_resource

    # def translateResource(self, from_resource):
    #     """
    #     Method to translate the ingoing resource. Uses and overrides perent method.
    #     :param from_resource: Resource to be translated
    #     :return: Translated resource (dict)
    #     """
    #     to_resource = super(self.__class__, self).translateResource(from_resource)
    #     if to_resource is not None:
    #         from_resource_type = from_resource[self.from_meta["resource"]["type"]]
    #         to_resource = self.translateResourceTags(from_resource, to_resource)
    #         # to_resource = self.translateSpecial[from_resource_type](from_resource, to_resource) if self.translateSpecial.get(from_resource_type, None) is not None else to_resource
    #
    #     return to_resource

    def translateKeys(self, ref, value):
        """
        Method to translate references and special functions in a template.
        :param ref: The key to be translated
        :param value: The value assigne to the key.
        :return: Returns translated reference.
        """
        return { ref: value }

#todo network/subnet
#in Openstack tags are only string values, in AWS {"Key": bla, "Value": bla}
# https://docs.openstack.org/heat/pike/api/heat.engine.cfn.functions.html#heat.engine.cfn.functions.Ref
