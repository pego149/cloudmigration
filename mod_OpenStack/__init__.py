from globalMethods import GlobalMethods, pprint
import MainWindow as MainWindow
import json


class OpenStack(GlobalMethods):

    def __init__(self):
        self.aName = "OpenStack class"

        # List of parameters given in file
        self.aParameters = []

    def printName(self):
        print(self.aName)

    def isInParameters(self, paValue):
        """
        Checks, if is given keyword in list (parameter section)
        :param paValue: value to search
        :return: boolean value of success
        """

        for i in self.aParameters:
            if i == paValue:
                return True

        return False

    ##########################################
    # Attribute functions
    ##########################################

    def instanceFromGeneric(self, paAttribute):
        """
        Method that transforms Generic instance into OpenStack format in YAML.
        :param paAttribute: properties of Generic instance (Generic::VirtualMachine) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Image property (in AWS called AMI).
            if i == "image":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    if self.isInParameters(paAttribute[i]["ref"]):
                        pprint(" " * 6 + "image: { get_param: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "image: { get_param: " + paAttribute[i]["ref"] + " }\n"
                    else:
                        pprint(" " * 6 + "image: { get_resource: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "image: { get_resource: " + paAttribute[i]["ref"] + " }\n"
                else:
                    pprint(" " * 6 + "image: " + paAttribute[i])
                    string += " " * 6 + "image: " + paAttribute[i] + "\n"

            # SSH key property.
            elif i == "key":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    if self.isInParameters(paAttribute[i]["ref"]):
                        pprint(" " * 6 + "key_name: { get_param: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "key_name: { get_param: " + paAttribute[i]["ref"] + " }\n"
                    else:
                        pprint(" " * 6 + "key_name: { get_resource: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "key_name: { get_resource: " + paAttribute[i]["ref"] + " }\n"
                else:
                    pprint(" " * 6 + "key_name: " + paAttribute[i])
                    string += " " * 6 + "key_name: " + paAttribute[i] + "\n"

            # Instance type property. Defines CPU, RAM, HDD, ...
            elif i == "instance_type":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    if self.isInParameters(paAttribute[i]["ref"]):
                        pprint(" " * 6 + "flavor: { get_param: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "flavor: { get_param: " + paAttribute[i]["ref"] + " }\n"
                    else:
                        pprint(" " * 6 + "flavor: { get_resource: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "flavor: { get_resource: " + paAttribute[i]["ref"] + " }\n"
                else:
                    pprint(" " * 6 + "flavor: " + paAttribute[i])
                    string += " " * 6 + "flavor: " + paAttribute[i] + "\n"

            # Availability zone property.
            elif i == "availability_zone":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    if self.isInParameters(paAttribute[i]["ref"]):
                        pprint(" " * 6 + "availability_zone: { get_param: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "availability_zone: { get_param: " + paAttribute[i]["ref"] + " }\n"
                    else:
                        pprint(" " * 6 + "availability_zone: { get_resource: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "availability_zone: { get_resource: " + paAttribute[i]["ref"] + " }\n"
                else:
                    pprint(" " * 6 + "availability_zone: " + paAttribute[i])
                    string += " " * 6 + "availability_zone: " + paAttribute[i] + "\n"

            # User data. It gets and parses user data. Data itself are in "bare_data". Parameters are referenced in
            # section: parameters.
            elif i == "user_data":

                pprint(" " * 6 + "user_data:\n" + " " * 8 + "str_replace:\n" + " " * 10 + "template: |")
                string += " " * 6 + "user_data:\n" + " " * 8 + "str_replace:\n" + " " * 10 + "template: |\n"

                # Get all data from UserData.
                string += " " * 12 + j
                pprint(" " * 12 + str(paAttribute[i]["bare_data"]))

                # Print a section with parameters.
                string += " " * 10 + "params:\n"
                pprint(" " * 10 + "params:")
                # for j in range(1, paramCount + 1):
                for j in paAttribute[i]["parameters"]:
                    # If is parameter in Parameters global section, write reference. else write just value
                    if self.isInParameters(paAttribute[i]["parameters"][j]):
                        pprint(" " * 12 + j + ": { get_param: " + paAttribute[i]["parameters"][j] + " }")
                        string += " " * 12 + j + ": { get_param: " + paAttribute[i]["parameters"][j] + " }\n"
                    else:
                        pprint(" " * 12 + j + ": " + paAttribute[i]["parameters"][j] + " }")
                        string += " " * 12 + j + ": " + paAttribute[i]["parameters"][j] + " }\n"

            # Tags properties. They are written in form Key: Value.
            elif i == "tags":
                pprint(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute[i]:
                    pprint(" " * 8 + "- " + paAttribute[i][j])
                    string += " " * 8 + "- " + paAttribute[i][j] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    def subnetFromGeneric(self, paAttribute):
        """
        Method that transforms Generic subnet into OpenStack format in YAML.
        :param paAttribute: properties of Generic subnet (Generic::Subnet) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Network, that Subnet is par of.
            if i == "network":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    if self.isInParameters(paAttribute[i]["ref"]):
                        pprint(" " * 6 + "network: { get_param: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "network: { get_param: " + paAttribute[i]["ref"] + " }\n"
                    else:
                        pprint(" " * 6 + "network: { get_resource: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "network: { get_resource: " + paAttribute[i]["ref"] + " }\n"
                else:
                    pprint(" " * 6 + "network: " + paAttribute[i])
                    string += " " * 6 + "network: " + paAttribute[i] + "\n"

            # IP subnet in CIDR format (192.168.1.0/24).
            elif i == "cidr":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    if self.isInParameters(paAttribute[i]["ref"]):
                        pprint(" " * 6 + "cidr: { get_param: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "cidr: { get_param: " + paAttribute[i]["ref"] + " }\n"
                    else:
                        pprint(" " * 6 + "cidr: { get_resource: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "cidr: { get_resource: " + paAttribute[i]["ref"] + " }\n"
                else:
                    pprint(" " * 6 + "cidr: " + paAttribute[i])
                    string += " " * 6 + "cidr: " + paAttribute[i] + "\n"

            # Availability zone property. OpenStack does not have it.
            elif i == "availability_zone":
                pprint(" " * 6 + "# AvailabilityZone: does not have this property. Original: " + str(paAttribute[i]).replace("'", ""))
                string += " " * 6 + "# AvailabilityZone: does not have this property. Original: " + str(paAttribute[i]).replace("'", "") + "\n"

            # Tags properties. They are just list of values.
            elif i == "tags":
                pprint(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute[i]:
                    pprint(" " * 8 + "- " + paAttribute[i][j])
                    string += " " * 8 + "- " + paAttribute[i][j] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def networkFromGeneric(paAttribute):
        """
        Method that transforms Generic network into OpenStack format in YAML.
        :param paAttribute: properties of Generic network (Generic::Network) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # IP subnet in CIDR format (192.168.1.0/24). OpenStack does not have it.
            if i == "cidr":
                pprint(" " * 6 + "# cidr: does not have this property. Original: " + str(paAttribute[i]).replace("'", ""))
                string += " " * 6 + "# cidr: does not have this property. Original: " + str(paAttribute[i]).replace("'", "") + "\n"

            # Tags properties. They are just list of values.
            elif i == "tags":
                pprint(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute[i]:
                    pprint(" " * 8 + "- " + paAttribute[i][j])
                    string += " " * 8 + "- " + paAttribute[i][j] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    def securityGroupFromGeneric(self, paAttribute):
        """
        Method that transforms AWS JSON security groups into Generic format in YAML.
        :param paAttribute: properties of AWS network (AWS::EC2::SecurityGroup) in JSON format
        :return: string in YAML format
        """

        string = ""
        # Checks, if there are any rule
        rules = 0

        for i in paAttribute:
            # Writes description of Security group.
            if i == "description":
                pprint(" " * 6 + "description: " + paAttribute[i])
                string += " " * 6 + "description: " + paAttribute[i] + "\n"

            # Security group rules in both: inbound and outbound directions.
            elif i == "ingres_rules" or i == "egress_rules":

                if not rules:
                    rules = 1
                    pprint(" " * 6 + "rules:")
                    string += " " * 6 + "rules:\n"

                for j in paAttribute[i]:
                    if i == "ingres_rules":
                        pprint(" " * 8 + "- direction: ingress")
                        string += " " * 8 + "- direction: ingress\n"
                    else:
                        pprint(" " * 8 + "- direction: egress")
                        string += " " * 8 + "- direction: egress\n"

                    for k in j:
                        # Transport protocol carried in IP packet.
                        if k == "protocol":
                            pprint(" " * 10 + "protocol: " + j["protocol"])
                            string += " " * 10 + "protocol: " + j["protocol"] + "\n"

                        # First port to start list with.
                        elif k == "from_port":
                            pprint(" " * 10 + "port_range_min: " + str(j["from_port"]))
                            string += " " * 10 + "port_range_min: " + str(j["from_port"]) + "\n"

                        # Last port in the list.
                        elif k == "to_port":
                            pprint(" " * 10 + "port_range_max: " + str(j["to_port"]))
                            string += " " * 10 + "port_range_max: " + str(j["to_port"]) + "\n"

                        # Network addres to bind rule to. In CIDR format (192.168.10.0/24).
                        elif k == "cidr":
                            if isinstance(j[k], dict):
                                if self.isInParameters(j[k]["ref"]):
                                    pprint(" " * 10 + "remote_ip_prefix: { get_param: " + j[k]["ref"] + " }")
                                    string += " " * 10 + "remote_ip_prefix: { get_param: " + j[k]["ref"] + " }\n"
                                else:
                                    pprint(" " * 10 + "remote_ip_prefix: { get_resource: " + j[k]["ref"] + " }")
                                    string += " " * 10 + "remote_ip_prefix: { get_resource: " + j[k]["ref"] + " }\n"

                            else:
                                pprint(" " * 10 + "remote_ip_prefix: " + j[k])
                                string += " " * 10 + "remote_ip_prefix: " + j[k] + "\n"

                        # Version of IP protocol.
                        elif k == "ethertype":
                            pprint(" " * 10 + "ethertype: " + j["ethertype"])
                            string += " " * 10 + "ethertype: " + j["ethertype"] + "\n"

                        # Otherwise write, that it is not implemented yet.
                        else:
                            pprint(" " * 10 + k + ": Not Implemented")
                            string += " " * 10 + k + ": Not Implemented\n"

            # Tags properties. They are just list of values.
            elif i == "tags":
                pprint(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute[i]:
                    pprint(" " * 8 + "- " + paAttribute[i][j])
                    string += " " * 8 + "- " + paAttribute[i][j] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    ##########################################
    # Main functions
    ##########################################

    def readFromFile(self, paFile):
        try:
            file = open(paFile, 'r')
        except IOError:
            MainWindow.infoWindow("error", "Error in parsing YAML file - " + self.name)
            return False

        return file.read()

    def saveToFile(self, paFile, paString):

        # Loads JSON string.
        string = json.loads(paString)

        # This string is being filled with data and finally is returned from this function.
        finalString = ""

        # Prints format of this template.
        pprint("heat_template_version: " + string["Template_version"])

        # Because of issues of date in JSON, it is printed with dots. Therefore it is recommended to check ity manually.
        finalString += "heat_template_version: " + string["Template_version"].replace("-", ".") + \
                       " - Please check and update manually\n"

        # Prints description of whole template.
        pprint("description: " + string["Description"] + "\n")
        finalString += "description: " + string["Description"] + "\n"

        ###########################################################################################
        # PARAMETERS
        ###########################################################################################

        pprint("parameters:")
        parameter = string["Parameters"]
        finalString += "parameters:\n"

        # Iterates all parameters and prints them
        for i in parameter:
            # Add parameter to list
            self.aParameters.append(i)

            # Prints name of parameter.
            pprint(" "*2 + i + ":")
            finalString += " "*2 + i + ":\n"

            for attribute in parameter[i]:
                # prints name of attribute
                pprint(" "*4 + attribute + ": ", end='')
                finalString += " "*4 + attribute + ": "

                if parameter[i][attribute] is None:
                    pprint()
                    finalString += "\n"

                # In these types of attributes, there is just simple pprint() of original value.
                elif attribute == "Type" or attribute == "Description" or attribute == "Default" or \
                                attribute == "MinLength" or attribute == "MaxLength" or \
                                attribute == "ConstraintDescription":
                    pprint(parameter[i][attribute])
                    finalString += str(parameter[i][attribute]) + "\n"

                # In Allowed pattern, there is Regex, which is printed with warning, that it should be checked manually.
                elif attribute == "AllowedPattern":
                    pprint(str(parameter[i][attribute]))
                    finalString += "Check manually " + parameter[i][attribute] + "\n"

                # Allowed values are printed as a list.
                elif attribute == "AllowedValues":
                    pprint()
                    for k in parameter[i][attribute]:
                        pprint(" " * 6 + "- " + k)
                        finalString += "\n" + " " * 6 + "- " + k + "\n"

                # Else write, that it is not implemented yet.
                else:
                    pprint("Not implemented")
                    finalString += "Not Implemented\n"

        ###########################################################################################
        # RESOURCES
        ###########################################################################################

        pprint("\nresources:\n")
        resource = string["Resources"]
        finalString += "resources:\n"

        for i in resource:
            # prints name of resource
            pprint(" "*2 + i + ": ")
            finalString += " "*2 + i + ":\n"

            # Based on resource name, calls method which will transform property data.
            if resource[i]["Type"] == "Generic::VirtualMachine":
                pprint(" " * 4 + "Type: OS::Nova::Server")
                finalString += " " * 4 + "Type: OS::Nova::Server\n"
                pprint(" " * 4 + "Properties:")
                finalString += " " * 4 + "Properties:\n" + self.instanceFromGeneric(resource[i]["Properties"])
            elif resource[i]["Type"] == "Generic::Network":
                pprint(" " * 4 + "Type: OS::Neutron::Net")
                finalString += " " * 4 + "Type: OS::Neutron::Net\n"
                pprint(" " * 4 + "Properties:")
                finalString += " " * 4 + "Properties:\n" + self.networkFromGeneric(resource[i]["Properties"])
            elif resource[i]["Type"] == "Generic::Subnet":
                pprint(" " * 4 + "Type: OS::Neutron::Subnet")
                finalString += " " * 4 + "Type: OS::Neutron::Subnet\n"
                pprint(" " * 4 + "Properties:")
                finalString += " " * 4 + "Properties:\n" + self.subnetFromGeneric(resource[i]["Properties"])
            elif resource[i]["Type"] == "Generic::SecurityGroup":
                pprint(" " * 4 + "Type: OS::Neutron::SecurityGroup")
                finalString += " " * 4 + "Type: OS::Neutron::SecurityGroup\n"
                pprint(" " * 4 + "Properties:")
                finalString += " " * 4 + "Properties:\n" + self.securityGroupFromGeneric(resource[i]["Properties"])
            # elif resource[i]["Type"] == "AWS::Route53::RecordSet":
            #     pprint()(" " * 4 + "Type: Generic::DNSRecord")
            #     finalString += " " * 4 + "Type: Generic::DNSRecord\n"
            #     pprint()(" " * 4 + "Properties:")
            #     finalString += " " * 4 + "Properties:\n" + self.dnsRecord(resource[i]["Properties"])
            else:
                pprint(" " * 4 + "Type: " + resource[i]["Type"])
                finalString += " " * 4 + "Type: " + resource[i]["Type"] + "\n"
                pprint(" " * 4 + "Properties: Not Implemented")
                finalString += " " * 4 + "Properties: Not implemented\n"

        # Saving to file
        try:
            file = open(paFile, 'w')
            file.write(finalString)
        except IOError:
            MainWindow.infoWindow("error", "Error in saving file " + paFile)

        return finalString

