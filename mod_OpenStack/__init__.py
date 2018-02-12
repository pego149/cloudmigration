from builtins import staticmethod
from io import StringIO

from globalMethods import GlobalMethods, pprint
import MainWindow as MainWindow
import json
import yaml
# from ruamel.yaml import YAML as yaml

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
    # Attribute functions from generic
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

            # Networks.
            elif i == "network":
                pprint(" " * 6 + "networks:")
                string += " " * 6 + "networks:\n"

                for j in paAttribute[i]:
                    try:
                        pprint(" " * 8 + "- " + j)
                        string += " " * 8 + "- " + j + "\n"
                    except TypeError:
                        for k in j:
                            pprint(" " * 8 + "- " + j[k])
                            string += " " * 8 + "- " + j[k] + "\n"

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

            # Security groups
            elif i == "security_groups":
                pprint(" " * 6 + "security_groups:")
                string += " " * 6 + "security_groups:\n"

                for j in paAttribute[i]:
                    try:
                        pprint(" " * 8 + "- " + j)
                        string += " " * 8 + "- " + j + "\n"
                    except TypeError:
                        for k in j:
                            # If it is parameter, write get_param
                            if self.isInParameters(j[k]):
                                pprint(" " * 8 + "- { get_param: " + j[k] + " }")
                                string += " " * 8 + "- { get_param: " + j[k] + " }\n"
                            else:
                                pprint(" " * 8 + "- { get_resource: " + j[k] + " }")
                                string += " " * 8 + "- { get_resource: " + j[k] + " }\n"

            # User data. It gets and parses user data. Data itself are in "bare_data". Parameters are referenced in
            # section: parameters.
            elif i == "user_data":

                pprint(" " * 6 + "user_data:\n" + " " * 8 + "str_replace:\n" + " " * 10 + "template: |")
                string += " " * 6 + "user_data:\n" + " " * 8 + "str_replace:\n" + " " * 10 + "template: |\n"

                # Get all data from UserData.
                string += " " * 12 + str(paAttribute[i]["bare_data"]) + "\n"
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
                pprint(" " * 6 + "# AvailabilityZone: does not have this property. Original: " +
                       str(paAttribute[i]).replace("'", ""))
                string += " " * 6 + "# AvailabilityZone: does not have this property. Original: " +\
                          str(paAttribute[i]).replace("'", "") + "\n"

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
                pprint(" " * 6 + "# cidr: does not have this property. Original: " +
                       str(paAttribute[i]).replace("'", ""))
                string += " " * 6 + "# cidr: does not have this property. Original: " + \
                        str(paAttribute[i]).replace("'", "") + "\n"

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
        Method that transforms Generic security groups into OpenStack format in YAML.
        :param paAttribute: properties of Generic Security Group (Generic::SecurityGroup) in JSON format
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
            elif i == "ingress_rules" or i == "egress_rules":

                if not rules:
                    rules = 1
                    pprint(" " * 6 + "rules:")
                    string += " " * 6 + "rules:\n"

                for j in paAttribute[i]:
                    if i == "ingress_rules":
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
    # Attribute functions to generic
    ##########################################

    @staticmethod
    def instanceToGeneric(paAttribute):
        """
        Method that transforms OpenStack instance into Generic format in YAML.
        :param paAttribute: properties of OpenStack instance (OS::Nova::Server) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Name of network.
            if i == "name":
                pprint(" " * 6 + "name: " + paAttribute[i])
                string += " " * 6 + "name: " + paAttribute[i] + "\n"

            # Instance type (CPUs, RAM, HDD, ...).
            elif i == "flavor":
                # Check, if it is a reference
                if isinstance(paAttribute[i], dict):
                    # If it is not in parameters, it is in resources
                    try:
                        pprint(" " * 6 + "flavor: { ref: " + paAttribute[i]["get_param"] + " }")
                        string += " " * 6 + "flavor: { ref: " + paAttribute[i]["get_param"] + " }\n"
                    except KeyError:
                        pprint(" " * 6 + "flavor: { ref: " + paAttribute[i]["get_resource"] + " }")
                        string += " " * 6 + "flavor: { ref: " + paAttribute[i]["get_resource"] + " }\n"
                else:
                    pprint(" " * 6 + "flavor: " + paAttribute[i])
                    string += " " * 6 + "flavor: " + paAttribute[i] + "\n"

            # Image to build server from.
            elif i == "image":
                # Check, if it is a reference
                if isinstance(paAttribute[i], dict):
                    # If it is not in parameters, it is in resources
                    try:
                        pprint(" " * 6 + "image: { ref: " + paAttribute[i]["get_param"] + " }")
                        string += " " * 6 + "image: { ref: " + paAttribute[i]["get_param"] + " }\n"
                    except KeyError:
                        pprint(" " * 6 + "image: { ref: " + paAttribute[i]["get_resource"] + " }")
                        string += " " * 6 + "image: { ref: " + paAttribute[i]["get_resource"] + " }\n"
                else:
                    pprint(" " * 6 + "image: " + paAttribute[i])
                    string += " " * 6 + "image: " + paAttribute[i] + "\n"

            # SSH key.
            elif i == "key_name":
                # Check, if it is a reference
                if isinstance(paAttribute[i], dict):
                    # If it is not in parameters, it is in resources
                    try:
                        pprint(" " * 6 + "key: { ref: " + paAttribute[i]["get_param"] + " }")
                        string += " " * 6 + "key: { ref: " + paAttribute[i]["get_param"] + " }\n"
                    except KeyError:
                        pprint(" " * 6 + "key: { ref: " + paAttribute[i]["get_resource"] + " }")
                        string += " " * 6 + "key: { ref: " + paAttribute[i]["get_resource"] + " }\n"
                else:
                    pprint(" " * 6 + "key: " + paAttribute[i])
                    string += " " * 6 + "key: " + paAttribute[i] + "\n"

            # Availability zone.
            elif i == "availability_zone":
                # Check, if it is a reference
                if isinstance(paAttribute[i], dict):
                    # If it is not in parameters, it is in resources
                    try:
                        pprint(" " * 6 + "availability_zone: { ref: " + paAttribute[i]["get_param"] + " }")
                        string += " " * 6 + "availability_zone: { ref: " + paAttribute[i]["get_param"] + " }\n"
                    except KeyError:
                        pprint(" " * 6 + "availability_zone: { ref: " + paAttribute[i]["get_resource"] + " }")
                        string += " " * 6 + "availability_zone: { ref: " + paAttribute[i]["get_resource"] + " }\n"
                else:
                    pprint(" " * 6 + "availability_zone: " + paAttribute[i])
                    string += " " * 6 + "availability_zone: " + paAttribute[i] + "\n"

            # Networks.
            elif i == "networks":
                pprint(" " * 6 + "networks:")
                string += " " * 6 + "networks:\n"

                for j in paAttribute[i]:
                    try:
                        pprint(" " * 8 + "- " + j)
                        string += " " * 8 + "- " + j + "\n"
                    except TypeError:
                        for k in j:
                            pprint(" " * 8 + "- { ref: " + j[k] + " }")
                            string += " " * 8 + "- { ref: " + j[k] + " }\n"

            # Security group
            elif i == "security_groups":
                pprint(" " * 6 + "security_groups:")
                string += " " * 6 + "security_groups:\n"

                for j in paAttribute[i]:
                    try:
                        pprint(" " * 8 + "- " + j)
                        string += " " * 8 + "- " + j + "\n"
                    except TypeError:
                        for k in j:
                            pprint(" " * 8 + "- { ref: " + j[k] + " }")
                            string += " " * 8 + "- { ref: " + j[k] + " }\n"

            # User data.
            elif i == "user_data":

                pprint(" " * 6 + "user_data:\n" + " " * 8 + "bare_data:")
                string += " " * 6 + "user_data:\n" + " " * 8 + "bare_data:\n"

                s = StringIO(paAttribute[i]["str_replace"]["template"])
                for line in s:
                    string += " " * 10 + line
                    pprint(" " * 10 + line, end='')

                pprint(" " * 8 + "parameters:")
                string += " " * 8 + "parameters:\n"

                for param in paAttribute[i]["str_replace"]["params"]:
                    # If is reference.
                    if isinstance(paAttribute[i]["str_replace"]["params"], dict):
                        try:
                            pprint(" " * 10 + param + ": " + paAttribute[i]["str_replace"]["params"][param])
                        except TypeError:
                            pprint(" " * 10 + param + ": { ref: " +
                                   paAttribute[i]["str_replace"]["params"][param]["get_param"] + " }")

            # Tags properties. They are just list of values.
            elif i == "tags":
                tagCount = 1
                pprint(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute[i]:
                    pprint(" " * 8 + "key" + str(tagCount) + ": " + j)
                    string += " " * 8 + "key" + str(tagCount) + ": " + j + "\n"
                    tagCount += 1

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def networkToGeneric(paAttribute):
        """
        Method that transforms OpenStack network into Generic format in YAML.
        :param paAttribute: properties of OpenStack network (OS::Neutron::Net) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Name of network.
            if i == "name":
                pprint(" " * 6 + "name: " + paAttribute[i])
                string += " " * 6 + "name: " + paAttribute[i] + "\n"

            # Tags properties. They are just list of values.
            elif i == "tags":
                tagCount = 1
                pprint(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute[i]:
                    pprint(" " * 8 + "key" + str(tagCount) + ": " + j)
                    string += " " * 8 + "key" + str(tagCount) + ": " + j + "\n"
                    tagCount += 1

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def subnetToGeneric(paAttribute):
        """
        Method that transforms OpenStack subnet into Generic format in YAML.
        :param paAttribute: properties of OpenStack subnet (OS::Neutron::Subnet) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Network, that Subnet is par of.
            if i == "network":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    # If it is not in parameters, it is in resources
                    try:
                        pprint(" " * 6 + "network: { ref: " + paAttribute[i]["get_param"] + " }")
                        string += " " * 6 + "network: { ref: " + paAttribute[i]["get_param"] + " }\n"
                    except KeyError:
                        pprint(" " * 6 + "network: { ref: " + paAttribute[i]["get_resource"] + " }")
                        string += " " * 6 + "network: { ref: " + paAttribute[i]["get_resource"] + " }\n"
                else:
                    pprint(" " * 6 + "network: " + paAttribute[i])
                    string += " " * 6 + "network: " + paAttribute[i] + "\n"

            # IP subnet in CIDR format (192.168.1.0/24).
            elif i == "cidr":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    # If it is not in parameters, it is in resources
                    try:
                        pprint(" " * 6 + "cidr: { ref: " + paAttribute[i]["get_param"] + " }")
                        string += " " * 6 + "cidr: { ref: " + paAttribute[i]["get_param"] + " }\n"
                    except KeyError:
                        pprint(" " * 6 + "cidr: { ref: " + paAttribute[i]["get_resource"] + " }")
                        string += " " * 6 + "cidr: { ref: " + paAttribute[i]["get_resource"] + " }\n"
                else:
                    pprint(" " * 6 + "cidr: " + paAttribute[i])
                    string += " " * 6 + "cidr: " + paAttribute[i] + "\n"

            # Name of subnet.
            elif i == "name":
                pprint(" " * 6 + "name: " + paAttribute[i])
                string += " " * 6 + "name: " + paAttribute[i] + "\n"

            # Tags properties. They are just list of values.
            elif i == "tags":
                tagCount = 1
                pprint(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute[i]:
                    pprint(" " * 8 + "key" + str(tagCount) + ": " + j)
                    string += " " * 8 + "key" + str(tagCount) + ": " + j + "\n"
                    tagCount += 1

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def securityGroupToGeneric(paAttribute):
        """
        Method that transforms OpenStack SecurityGroup into Generic format in YAML.
        :param paAttribute: properties of OpenStack SecurityGroup (OS::Neutron::SecurityGroup) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Name of network.
            if i == "description":
                pprint(" " * 6 + "description: " + paAttribute[i])
                string += " " * 6 + "description: " + paAttribute[i] + "\n"

            # Rules in either ingress and egress direction.
            elif i == "rules":
                ingress = " " * 6 + "ingress_rules:\n"
                egress = " " * 6 + "egress_rules:\n"

                for j in paAttribute[i]:
                    # If it is in egress direction
                    if j["direction"] == "egress":
                        egress += " " * 8 + "- protocol: " + j["protocol"] + "\n"
                        egress += " " * 10 + "from_port: " + str(j["port_range_min"]) + "\n"
                        egress += " " * 10 + "to_port: " + str(j["port_range_max"]) + "\n"

                        # Checks, if it is reference
                        if isinstance(j["remote_ip_prefix"], dict):
                            # If it is not in parameters, it is in resources
                            try:
                                egress += " " * 10 + "cidr: { ref: " + j["remote_ip_prefix"]["get_param"] + " }\n"
                            except KeyError:
                                egress += " " * 10 + "cidr: { ref: " + j["remote_ip_prefix"]["get_resource"] + " }\n"
                        else:
                            egress += " " * 10 + "cidr: " + j["remote_ip_prefix"] + "\n"

                    # Else it is in ingress direction, either it is not written
                    else:
                        ingress += " " * 8 + "- protocol: " + j["protocol"] + "\n"
                        ingress += " " * 10 + "from_port: " + str(j["port_range_min"]) + "\n"
                        ingress += " " * 10 + "to_port: " + str(j["port_range_max"]) + "\n"

                        # Checks, if it is reference
                        if isinstance(j["remote_ip_prefix"], dict):
                            # If it is not in parameters, it is in resources
                            try:
                                ingress += " " * 10 + "cidr: { ref: " + j["remote_ip_prefix"]["get_param"] + " }\n"
                            except KeyError:
                                ingress += " " * 10 + "cidr: { ref: " + j["remote_ip_prefix"]["get_resource"] + " }\n"
                        else:
                            ingress += " " * 10 + "cidr: " + j["remote_ip_prefix"] + "\n"

                pprint(ingress, end='')
                string += ingress
                pprint(egress, end='')
                string += egress

            # Tags properties. They are just list of values.
            elif i == "tags":
                tagCount = 1
                pprint(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute[i]:
                    pprint(" " * 8 + "key" + str(tagCount) + ": " + j)
                    string += " " * 8 + "key" + str(tagCount) + ": " + j + "\n"
                    tagCount += 1

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    ##########################################
    # Main functions
    ##########################################

    def readFromFile(self, paFile):
        """
        Method reads data from file passes as parameter. Data can be in YAML format only. It parses it, and
        calls other methods, which parses smaller parts of given data. Finally, it returns string in generic format.
        The string is formatted in JSON format.
        :param paFile: file to read data from
        :return: converted string in generic format, written in JSON
        """

        # This string is being filled with data and finally is returned from this function.
        finalString = ""

        # Reads data from file. It is smart, will read both: YAML and JSON.
        with open(paFile) as data_file:
            # string = json.load(data_file)
            string = yaml.load(data_file)
            original_template = yaml.load(data_file)
        with open("Generic.json", "r") as generic_file:
            generic_template = json.load(generic_file)

        new_template = generic_template["template_structure"]
        new_template["template_version"] = original_template["heat_template_version"]
        new_template["description"] = original_template["description"]
        # Prints format of this template.
        # pprint("template_version: " + string["heat_template_version"])
        #
        # Because of issues of date in JSON, it is printed with dots. Therefore it is recommended to check ity manually.
        # finalString += "template_version: " + string["heat_template_version"].replace("-", ".") + \
        #                " - Please check and update manually\n"

        # Prints description of whole template.
        # pprint("description: " + string["description"] + "\n")
        # finalString += "description: " + string["description"] + "\n"

        ###########################################################################################
        # PARAMETERS
        ###########################################################################################

        # pprint("parameters:\n")
        # finalString += "parameters:\n"
        # parameter = string["parameters"]

        for parameter in original_template["parameters"]:
            new_template["parameters"][parameter] = dict(generic_template["parameter"])
            new_template["parameters"][parameter]["type"] = parameter.get("type", None)
            new_template["parameters"][parameter]["name"] = parameter.get("name", None)
            new_template["parameters"][parameter]["default"] = parameter.get("default", None)
            for constraint in parameter["constraints"]:
                if "allowed_pattern" in constraint:
                    new_template["parameters"][parameter]["allowed_pattern"] = constraint["allowed_pattern"]
                elif "allowed_values" in constraint:
                    new_template["parameters"][parameter]["allowed_values"] = constraint["allowed_values"]
                elif "length" in constraint:
                    new_template["parameters"][parameter]["min_length"] = constraint["length"].get("min", None)
                    new_template["parameters"][parameter]["max_length"] = constraint["length"].get("max", None)

        #todo check unimplemented parameters
        # # Iterates all parameters and prints them
        # for i in parameter:
        #     # Add parameter to list, in which are searched references (get_param)
        #     self.aParameters.append(i)
        #
        #     # Prints name of parameter.
        #     pprint(" " * 2 + i + ":")
        #     finalString += " " * 2 + i + ":\n"
        #
        #     for attribute in parameter[i]:
        #         # If there is empty parameter, skip it
        #         if parameter[i][attribute] is None:
        #             continue
        #
        #         # In these types of attributes, there is just simple print of original value.
        #         elif attribute == "type" or attribute == "description" or attribute == "default":
        #             pprint(" " * 4 + attribute + ": " + parameter[i][attribute])
        #             finalString += " " * 4 + attribute + ": " + parameter[i][attribute] + "\n"
        #
        #         # In these types of attributes, there is just simple print of original value.
        #         elif attribute == "constraints":
        #
        #             # Constraints is a list
        #             for j in parameter[i][attribute]:
        #                 for k in j:
        #                     if k == "allowed_pattern":
        #                         pprint(" " * 4 + "allowed_pattern: " + j[k])
        #                         finalString += " " * 4 + "allowed_pattern: " + j[k] + "\n"
        #
        #                     elif k == "allowed_values":
        #                         pprint(" " * 4 + "allowed_values:")
        #                         finalString += " " * 4 + "allowed_values:\n"
        #
        #                         # Write all values - it is a list
        #                         for l in j[k]:
        #                             pprint(" " * 6 + "- " + l)
        #                             finalString += " " * 6 + "- " + l + "\n"
        #
        #                     elif k == "length":
        #                         for l in j[k]:
        #
        #                             if l == "min":
        #                                 pprint(" " * 4 + "min_length: " + str(j[k][l]))
        #                                 finalString += " " * 4 + "min_length: " + str(j[k][l]) + "\n"
        #
        #                             else:
        #                                 pprint(" " * 4 + "max_length: " + str(j[k][l]))
        #                                 finalString += " " * 4 + "max_length: " + str(j[k][l]) + "\n"
        #
        #                     else:
        #                         pprint(" " * 4 + k + ": Not implemented")
        #                         finalString += " " * 4 + k + ": Not implemented\n"
        #
        #         # Else write, that it is not implemented yet.
        #         else:
        #             pprint(" " * 4 + attribute.lower() + ": " + "Not implemented")
        #             finalString += " " * 4 + attribute.lower() + ": " + "Not Implemented\n"

        ###########################################################################################
        # RESOURCES
        ###########################################################################################

        # pprint("\nresources:\n")
        # resource = string["resources"]
        # finalString += "resources:\n"

        to_generic_dict = {
            "OS::Nova::Server": "Generic::VM::Server",
            "OS::Neutron::Net": "Generic::Network::Net",
            "OS::Neutron::Subnet": "Generic::Network::Subnet",
            "OS::Neutron::SecurityGroup": "Generic::Network::Subnet"
        }
        for resource in original_template["resources"]:
            if resource["type"] == "OS::Nova::Server":
                new_template["resources"][resource] = self.instanceToGeneric("Generic::VM::Server") #todo aky parameter
            elif resource["type"] == "OS::Neutron::Net":
                new_template["resources"][resource] = self.networkToGeneric("Generic::Network::Net")
            elif resource["type"] == "OS::Neutron::Subnet":
                new_template["resources"][resource] = self.subnetToGeneric("Generic::Network::Subnet")
            elif resource["type"] == "OS::Neutron::SecurityGroup":
                new_template["resources"][resource] = self.securityGroupToGeneric("Generic::VM::SecurityGroup")
            else:
                new_template["resources"][resource] = "{0} Not Implemented".format(resource)




        # for i in resource:
        #     # prints name of resource
        #     pprint(" "*2 + i + ": ")
        #     finalString += " "*2 + i + ":\n"
        #
        #     # Based on resource name, calls method which will transform property data.
        #     if resource[i]["type"] == "OS::Nova::Server":
        #         pprint(" " * 4 + "type: Generic::VirtualMachine")
        #         finalString += " " * 4 + "type: Generic::VirtualMachine\n"
        #         pprint(" " * 4 + "properties:")
        #         finalString += " " * 4 + "properties:\n" + self.instanceToGeneric(resource[i]["properties"])
        #     elif resource[i]["type"] == "OS::Neutron::Net":
        #         pprint(" " * 4 + "type: Generic::Network")
        #         finalString += " " * 4 + "type: Generic::Network\n"
        #         pprint(" " * 4 + "properties:")
        #         finalString += " " * 4 + "properties:\n" + self.networkToGeneric(resource[i]["properties"])
        #     elif resource[i]["type"] == "OS::Neutron::Subnet":
        #         pprint(" " * 4 + "type: Generic::Subnet")
        #         finalString += " " * 4 + "type: Generic::Subnet\n"
        #         pprint(" " * 4 + "properties:")
        #         finalString += " " * 4 + "properties:\n" + self.subnetToGeneric(resource[i]["properties"])
        #     elif resource[i]["type"] == "OS::Neutron::SecurityGroup":
        #         pprint(" " * 4 + "type: Generic::SecurityGroup")
        #         finalString += " " * 4 + "type: Generic::SecurityGroup\n"
        #         pprint(" " * 4 + "properties:")
        #         finalString += " " * 4 + "properties:\n" + self.securityGroupToGeneric(resource[i]["properties"])
        #     # elif resource[i]["type"] == "AWS::Route53::RecordSet":
        #     #     pprint(" " * 4 + "type: Generic::DNSRecord")
        #     #     finalString += " " * 4 + "type: Generic::DNSRecord\n"
        #     #     pprint(" " * 4 + "properties:")
        #     #     finalString += " " * 4 + "properties:\n" + self.dnsRecordToGeneric(resource[i]["properties"])
        #     else:
        #         pprint(" " * 4 + "type: Generic::Unknown")
        #         finalString += " " * 4 + "type: Generic::Unknown\n"
        #         pprint(" " * 4 + "properties: Not Implemented")
        #         finalString += " " * 4 + "properties: Not implemented\n"

        # Converts YAML int JSON

        # finalString = json.dumps(yaml.load(finalString), sort_keys=False, indent=2)

        #exit(0)
        return new_template

    def saveToFile(self, paFile, paString):
        """
        Method reads data from string in generic format, parses it and calls other methods, which parses smaller parts
        of given data. Finally, it returns string in OpenStack format. The string is formatted in YAML format.
        :param paFile: File, to which will be saving performed
        :param paString: string, which will be saved to file
        :return: string formatted in YAML format in OpenStack notation
        """

        # Loads JSON string.
        string = json.loads(paString)

        # This string is being filled with data and finally is returned from this function.
        finalString = ""

        # Prints format of this template.
        pprint("heat_template_version: " + string["template_version"])

        # Because of issues of date in JSON, it is printed with dots. Therefore it is recommended to check ity manually.
        finalString += "heat_template_version: " + string["template_version"].replace("-", ".") + \
                       " - Please check and update manually\n"

        # Prints description of whole template.
        pprint("description: " + string["description"] + "\n")
        finalString += "description: " + string["description"] + "\n"

        ###########################################################################################
        # PARAMETERS
        ###########################################################################################

        pprint("parameters:")
        finalString += "parameters:\n"
        parameter = string["parameters"]

        # Iterates all parameters and prints them
        for i in parameter:
            # Add parameter to list, in which are searched references (get_param)
            self.aParameters.append(i)

            # Constraints section ######################
            isConstraints = False
            constraints = " "*4 + "constraints:\n"

            isLength = False
            lengthConstraint = " "*6 + "- length: {}\n"
            # Constraints section ######################

            # Prints name of parameter.
            pprint(" "*2 + i + ":")
            finalString += " "*2 + i + ":\n"

            for attribute in parameter[i]:
                # If there is empty parameter, skip it
                if parameter[i][attribute] is None:
                    continue

                # Type has to be lowercase
                elif attribute == "type":
                    pprint(" " * 4 + "type: " + parameter[i][attribute].lower())
                    finalString += " " * 4 + "type: " + parameter[i][attribute].lower() + "\n"

                # In these types of attributes, there is just simple print of original value.
                elif attribute == "description" or attribute == "default":
                    pprint(" " * 4 + attribute + ": " + parameter[i][attribute])
                    finalString += " " * 4 + attribute + ": " + parameter[i][attribute] + "\n"

                # In these types of attributes, there is just simple print of original value.
                elif attribute == "min_length" or attribute == "max_length":
                    isConstraints = True

                    if attribute == "min_length":
                        if isLength:
                            lengthConstraint = lengthConstraint[:-2] + ", min: " + str(parameter[i][attribute]) + "}\n"
                        else:
                            lengthConstraint = lengthConstraint[:-2] + " min: " + str(parameter[i][attribute]) + "}\n"

                        isLength = True

                    else:
                        if isLength:
                            lengthConstraint = lengthConstraint[:-2] + ", max: " + str(parameter[i][attribute]) + "}\n"
                        else:
                            lengthConstraint = lengthConstraint[:-2] + " max: " + str(parameter[i][attribute]) + "}\n"

                        isLength = True

                # In Allowed pattern, there is Regex, which is printed with warning, that it should be checked manually.
                elif attribute == "allowed_pattern":
                    isConstraints = True
                    constraints += " "*6 + "- allowed_pattern: " + parameter[i][attribute] + " - Check manually\n"

                # Allowed values are printed as a list.
                elif attribute == "allowed_values":
                    isConstraints = True
                    constraints += " " * 6 + "- allowed_values:\n"

                    for k in parameter[i][attribute]:
                        constraints += " " * 8 + "- " + k + "\n"

                # Constraint description - OpenStack does not have this attribute
                elif attribute == "constraint_description":
                    pprint(" " * 4 + "# ConstraintDescription: does not have this attribute. Original: " +
                           parameter[i][attribute])
                    finalString += " " * 4 + "# ConstraintDescription: does not have this attribute. Original: " +\
                                   parameter[i][attribute] + "\n"

                # Else write, that it is not implemented yet.
                else:
                    pprint(" " * 4 + attribute.lower() + ": " + "Not implemented")
                    finalString += " " * 4 + attribute.lower() + ": " + "Not Implemented\n"

            # Append constraints, if any
            if isConstraints:
                pprint(constraints, end='')
                finalString += constraints

                if isLength:
                    pprint(lengthConstraint)
                    finalString += lengthConstraint + "\n"
                else:
                    pprint()
                    finalString += "\n"

        ###########################################################################################
        # RESOURCES
        ###########################################################################################

        pprint("\nresources:\n")
        finalString += "resources:\n"
        resource = string["resources"]

        for i in resource:
            # prints name of resource
            pprint(" "*2 + i + ": ")
            finalString += " "*2 + i + ":\n"

            # Based on resource name, calls method which will transform property data.
            if resource[i]["type"] == "Generic::VirtualMachine":
                pprint(" " * 4 + "type: OS::Nova::Server")
                finalString += " " * 4 + "type: OS::Nova::Server\n"
                pprint(" " * 4 + "properties:")
                finalString += " " * 4 + "properties:\n" + self.instanceFromGeneric(resource[i]["properties"])
            elif resource[i]["type"] == "Generic::Network":
                pprint(" " * 4 + "type: OS::Neutron::Net")
                finalString += " " * 4 + "type: OS::Neutron::Net\n"
                pprint(" " * 4 + "properties:")
                finalString += " " * 4 + "properties:\n" + self.networkFromGeneric(resource[i]["properties"])
            elif resource[i]["type"] == "Generic::Subnet":
                pprint(" " * 4 + "type: OS::Neutron::Subnet")
                finalString += " " * 4 + "type: OS::Neutron::Subnet\n"
                pprint(" " * 4 + "properties:")
                finalString += " " * 4 + "properties:\n" + self.subnetFromGeneric(resource[i]["properties"])
            elif resource[i]["type"] == "Generic::SecurityGroup":
                pprint(" " * 4 + "type: OS::Neutron::SecurityGroup")
                finalString += " " * 4 + "type: OS::Neutron::SecurityGroup\n"
                pprint(" " * 4 + "properties:")
                finalString += " " * 4 + "properties:\n" + self.securityGroupFromGeneric(resource[i]["properties"])
            # elif resource[i]["type"] == "AWS::Route53::RecordSet":
            #     pprint()(" " * 4 + "type: Generic::DNSRecord")
            #     finalString += " " * 4 + "type: Generic::DNSRecord\n"
            #     pprint()(" " * 4 + "properties:")
            #     finalString += " " * 4 + "properties:\n" + self.dnsRecord(resource[i]["properties"])
            else:
                pprint(" " * 4 + "type: " + resource[i]["type"])
                finalString += " " * 4 + "type: " + resource[i]["type"] + "\n"
                pprint(" " * 4 + "properties: Not Implemented")
                finalString += " " * 4 + "properties: Not implemented\n"

        # Saving to file
        try:
            file = open(paFile, 'w')
            file.write(finalString)
        except IOError:
            MainWindow.infoWindow("error", "Error in saving file " + paFile)

        return finalString
