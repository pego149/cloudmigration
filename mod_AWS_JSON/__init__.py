from globalMethods import GlobalMethods
import MainWindow as MainWindow
import json
import yaml
import gc


class AWS_JSON(GlobalMethods):
    def __init__(self):
        self.name = "AWS JSON class"

    def printName(self):
        print(self.name)

    ##########################################
    # Attribute functions
    ##########################################

    @staticmethod
    def instance(paAttribute):
        """
        Method that transforms AWS JSON instance into Generic format in YAML.
        :param paAttribute: properties of AWS instance (AWS::EC2::Instance) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Image property (in AWS called AMI).
            if i == "ImageId":
                print(" " * 6 + "image: " + str(paAttribute[i]).replace("'", ""))
                string += " " * 6 + "image: " + str(paAttribute[i]).replace("'", "") + "\n"

            # SSH key property.
            elif i == "KeyName":
                print(" " * 6 + "key: " + str(paAttribute[i]).replace("'", ""))
                string += " " * 6 + "key: " + str(paAttribute[i]).replace("'", "") + "\n"

            # Instance type property. Defines CPU, RAM, HDD, ...
            elif i == "InstanceType":
                print(" " * 6 + "instance_type: " + str(paAttribute[i]).replace("'", ""))
                string += " " * 6 + "instance_type: " + str(paAttribute[i]).replace("'", "") + "\n"

            # Availability zone property.
            elif i == "AvailabilityZone":
                print(" " * 6 + "availability_zone: " + str(paAttribute[i]).replace("'", ""))
                string += " " * 6 + "availability_zone: " + str(paAttribute[i]).replace("'", "") + "\n"

            # User data. It gets and parses user data. Data itself are in "bare_data". If there are any
            # parameters/references, they are changed for key word  "parameter#", where # is subtracted for
            # sequence number of parameter. Parameters are referenced in next section: parameters.
            elif i == "UserData":
                array = []
                paramCount = 0

                print(" " * 6 + "user_data:")
                print(" " * 8 + "bare_data:")
                string += " " * 6 + "user_data:\n"
                string += " " * 8 + "bare_data:\n"

                # Get all data from UserData.
                for j in paAttribute[i]["Fn::Base64"]["Fn::Join"][1]:
                    try:
                        string += " " * 10 + j
                        print(j, end='')

                    # If there is any reference, increment parameters count and add reference to array.
                    except TypeError:
                        array.append(j["Ref"])
                        paramCount += 1
                        string += " " * 10 + "$parameter" + str(paramCount) + " "
                        print(" " * 10 + "$parameter" + str(paramCount) + " ")

                # If are there any parameters, print a section with them.
                if paramCount > 0:
                    string += " " * 8 + "parameters:\n"
                    print(" " * 8 + "parameters:")
                    for j in range(1, paramCount + 1):
                        string += " " * 10 + "$parameter" + str(j) + ": " + array[j - 1] + "\n"
                        print(" " * 10 + "$parameter" + str(j) + ": " + array[j - 1])

            # Tags properties. They are written in form Key: Value.
            elif i == "Tags":
                print(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute["Tags"]:
                    print(" " * 8 + "" + j["Key"] + ": " + j["Value"])
                    string += " " * 8 + j["Key"] + ": " + j["Value"] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                print(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def subnet(paAttribute):
        """
        Method that transforms AWS JSON subnet into Generic format in YAML.
        :param paAttribute: properties of AWS subnet (AWS::EC2::Subnet) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Network, that Subnet is par of.
            if i == "VpcId":
                print(" " * 6 + "network: " + str(paAttribute[i]).replace("'", ""))
                string += " " * 6 + "network: " + str(paAttribute[i]).replace("'", "") + "\n"

            # IP subnet in CIDR format (192.168.1.0/24).
            elif i == "CidrBlock":
                print(" " * 6 + "cidr: " + str(paAttribute[i]).replace("'", ""))
                string += " " * 6 + "cidr: " + str(paAttribute[i]).replace("'", "") + "\n"

            # Availability zone property.
            elif i == "AvailabilityZone":
                print(" " * 6 + "availability_zone: " + str(paAttribute[i]).replace("'", ""))
                string += " " * 6 + "availability_zone: " + str(paAttribute[i]).replace("'", "") + "\n"

            # Tags properties. They are written in form Key: Value.
            elif i == "Tags":
                print(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute["Tags"]:
                    print(" " * 8 + "" + j["Key"] + ": " + j["Value"])
                    string += " " * 8 + j["Key"] + ": " + j["Value"] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                print(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def network(paAttribute):
        """
        Method that transforms AWS JSON network into Generic format in YAML.
        :param paAttribute: properties of AWS network (AWS::EC2::VPC) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # IP subnet in CIDR format (192.168.1.0/24).
            if i == "CidrBlock":
                print(" " * 6 + "cidr: " + str(paAttribute[i]).replace("'", ""))
                string += " " * 6 + "cidr: " + str(paAttribute[i]).replace("'", "") + "\n"

            # Tags properties. They are written in form Key: Value.
            elif i == "Tags":
                print(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute["Tags"]:
                    print(" " * 8 + "" + j["Key"] + ": " + j["Value"])
                    string += " " * 8 + j["Key"] + ": " + j["Value"] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                print(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def securityGroup(paAttribute):
        """
        Method that transforms AWS JSON security groups into Generic format in YAML.
        :param paAttribute: properties of AWS network (AWS::EC2::SecurityGroup) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Writes description of Security group.
            if i == "GroupDescription":
                print(" "*6 + "description: " + paAttribute[i])
                string += " "*6 + "description: " + paAttribute[i] + "\n"

            # Security group rules in both: inbound and outbound directions.
            elif i == "SecurityGroupIngress" or i == "SecurityGroupEgress":
                if i == "SecurityGroupIngress":
                    print(" " * 6 + "ingres_rules:")
                    string += " " * 6 + "ingres_rules:\n"
                else:
                    print(" " * 6 + "egress_rules:")
                    string += " " * 6 + "egress_rules:\n"

                for j in paAttribute[i]:
                    first = 1
                    for k in j:
                        # Transport protocol carried in IP packet.
                        if k == "IpProtocol":
                            # If it is not first in list, just print it.
                            if not first:
                                print(" " * 10 + "protocol: " + j["IpProtocol"])
                                string += " " * 10 + "protocol: " + j["IpProtocol"] + "\n"

                            # If it is first in the list, write dash before it.
                            else:
                                first = 0
                                print(" " * 8 + "- protocol: " + j["IpProtocol"])
                                string += " " * 8 + "- protocol: " + j["IpProtocol"] + "\n"

                        # First port to start list with.
                        elif k == "FromPort":
                            # If it is not first in list, just print it.
                            if not first:
                                print(" " * 10 + "from_port: " + j["FromPort"])
                                string += " " * 10 + "from_port: " + j["FromPort"] + "\n"

                            # If it is first in the list, write dash before it.
                            else:
                                first = 0
                                print(" " * 8 + "- from_port: " + j["FromPort"])
                                string += " " * 8 + "- from_port: " + j["FromPort"] + "\n"

                        # Last port in the list.
                        elif k == "ToPort":
                            # If it is not first in list, just print it.
                            if not first:
                                print(" " * 10 + "to_port: " + j["ToPort"])
                                string += " " * 10 + "to_port: " + j["ToPort"] + "\n"

                            # If it is first in the list, write dash before it.
                            else:
                                first = 0
                                print(" " * 8 + "- to_port: " + j["ToPort"])
                                string += " " * 8 + "- to_port: " + j["ToPort"] + "\n"

                        # Network addres to bind rule to. In CIDR format (192.168.10.0/24).
                        elif k == "CidrIp":
                            # If it is not first in list, just print it.
                            if not first:
                                print(" " * 10 + "cidr: " + str(j[k]).replace("'", ""))
                                string += " " * 10 + "cidr: " + str(j[k]).replace("'", "") + "\n"

                            # If it is first in the list, write dash before it.
                            else:
                                first = 0
                                print(" " * 8 + "- cidr: " + str(j[k]).replace("'", ""))
                                string += " " * 8 + "- cidr: " + str(j[k]).replace("'", "") + "\n"

                        # Otherwise write, that it is not implemented yet.
                        else:
                            # If it is not first in list, just print it.
                            if not first:
                                print(" " * 10 + k + ": Not Implemented")
                                string += " " * 10 + k + ": Not Implemented\n"

                            # If it is first in the list, write dash before it.
                            else:
                                first = 0
                                print(" " * 8 + "- " + k + ": Not Implemented")
                                string += " " * 8 + "- " + k + ": Not Implemented\n"

            # Tags properties. They are written in form Key: Value.
            elif i == "Tags":
                print(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute["Tags"]:
                    print(" " * 8 + "" + j["Key"] + ": " + j["Value"])
                    string += " " * 8 + j["Key"] + ": " + j["Value"] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                print(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def dnsRecord(paAttribute):
        string = ""

        for i in paAttribute:
            # Name of the RR
            if i == "Name":
                print(" " * 6 + "name: " + paAttribute[i])
                string += " " * 6 + "name: " + paAttribute[i] + "\n"

            # Type of the RR
            elif i == "Type":
                print(" " * 6 + "type: " + paAttribute[i])
                string += " " * 6 + "type: " + paAttribute[i] + "\n"

            # Value of the RR
            elif i == "ResourceRecords":
                print(" " * 6 + "record: " + str(paAttribute[i]).replace("'", ""))
                string += " " * 6 + "record: " + str(paAttribute[i]).replace("'", "") + "\n"

            # TTL of the RR
            elif i == "TTL":
                print(" " * 6 + "ttl: " + paAttribute[i])
                string += " " * 6 + "ttl: " + paAttribute[i] + "\n"

            # Comment
            elif i == "Comment":
                print(" " * 6 + "comment: " + paAttribute[i])
                string += " " * 6 + "comment: " + paAttribute[i] + "\n"

            # Zone in which is RR
            elif i == "HostedZoneId":
                print(" " * 6 + "zone: " + str(paAttribute[i]).replace("'", ""))
                string += " " * 6 + "zone: " + str(paAttribute[i]).replace("'", "") + "\n"

            # Tags properties. They are written in form Key: Value.
            elif i == "Tags":
                print(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute["Tags"]:
                    print(" " * 8 + "" + j["Key"] + ": " + j["Value"])
                    string += " " * 8 + j["Key"] + ": " + j["Value"] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                print(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def autocsaling(paAttribute):
        # TODO dorobit
        pass

    @staticmethod
    def loadBallancer(paAttribute):
        # TODO dorobit
        pass

    # @staticmethod
    # def instance(paAttribute):
    #     string = ""
    #
    #     for i in paAttribute:
    #         if i == " ":
    #             print()
    #         elif i == "":
    #             print()
    #
    #         # Tags properties. They are written in form Key: Value.
    #         elif i == "Tags":
    #             print(" " * 6 + "tags:")
    #             string += " " * 6 + "tags: " + "\n"
    #             for j in paAttribute["Tags"]:
    #                 print(" " * 8 + "" + j["Key"] + ": " + j["Value"])
    #                 string += " " * 8 + j["Key"] + ": " + j["Value"] + "\n"
    #
    #         # Else write, that this property is not implemented yet.
    #         else:
    #             print(" " * 6 + i + ": Not implemented")
    #             string += " " * 6 + i + ": Not implemented" + "\n"
    #
    #     return string

    ##########################################
    # Main function
    ##########################################


    def readFromFile(self, paFile):

        finalString = ""

        # Reads JSON from file
        with open(paFile) as data_file:
            string = json.load(data_file)

        # Prints format of this template.
        print("AWS Template Format: " + string["AWSTemplateFormatVersion"])

        # Because of issues of date in JSON, it is printed with dots. Therefore it is recommended to check ity manually.
        finalString += "Template_version: " + string["AWSTemplateFormatVersion"].replace("-", ".") + \
                       " - Please check and update manually\n"

        # Prints description of whole template.
        print("Description: " + string["Description"] + "\n")
        finalString += "Description: " + string["Description"] + "\n"

        ###########################################################################################
        # PARAMETERS
        ###########################################################################################

        print("Parameters:\n")
        parameter = string["Parameters"]
        finalString += "Parameters:\n"

        # Iterates all parameters and prints them
        for i in parameter:
            # Prints name of parameter.
            print(i + ":")
            finalString += "  " + i + ":\n"

            for attribute in parameter[i]:
                # prints name of attribute
                print("  " + attribute + ": ", end='')
                finalString += "    " + attribute + ": "

                # In these types of attributes, there is just simple print of original value.
                if attribute == "Type" or attribute == "Description" or attribute == "Default" or \
                                attribute == "MinLength" or attribute == "MaxLength" or \
                                attribute == "ConstraintDescription":
                    print(parameter[i][attribute])
                    finalString += parameter[i][attribute] + "\n"

                # In Allowed pattern, there is Regex, which is printed with warning, that it should be checked manually.
                elif attribute == "AllowedPattern":
                    print(str(parameter[i][attribute]))
                    finalString += "Check manually " + parameter[i][attribute] + "\n"

                # Allowed values are printed as a list.
                elif attribute == "AllowedValues":
                    print()
                    for k in parameter[i][attribute]:
                        print(" " * 4 + "- " + k)
                        finalString += "\n" + " " * 4 + "- " + k + "\n"

                # Else write, that it is not implemented yet.
                else:
                    print("Not implemented")
                    finalString += "Not Implemented\n"

        ###########################################################################################
        # RESOURCES
        ###########################################################################################

        print("\nResources:\n")
        resource = string["Resources"]
        finalString += "Resources:\n"

        for i in resource:
            # prints name of resource
            print("  " + i + ": ")
            finalString += "  " + i + ":\n"

            # Based on resource name, calls method which will transform property data.
            if resource[i]["Type"] == "AWS::EC2::Instance":
                print(" " * 4 + "Type: Generic::VirtualMachine")
                finalString += " " * 4 + "Type: Generic::VirtualMachine\n"
                print(" " * 4 + "Properties:")
                finalString += " " * 4 + "Properties:\n" + self.instance(resource[i]["Properties"])
            elif resource[i]["Type"] == "AWS::EC2::VPC":
                print(" " * 4 + "Type: Generic::Network")
                finalString += " " * 4 + "Type: Generic::Network\n"
                print(" " * 4 + "Properties:")
                finalString += " " * 4 + "Properties:\n" + self.network(resource[i]["Properties"])
            elif resource[i]["Type"] == "AWS::EC2::Subnet":
                print(" " * 4 + "Type: Generic::Subnet")
                finalString += " " * 4 + "Type: Generic::Subnet\n"
                print(" " * 4 + "Properties:")
                finalString += " " * 4 + "Properties:\n" + self.subnet(resource[i]["Properties"])
            elif resource[i]["Type"] == "AWS::EC2::SecurityGroup":
                print(" " * 4 + "Type: Generic::SecurityGroup")
                finalString += " " * 4 + "Type: Generic::SecurityGroup\n"
                print(" " * 4 + "Properties:")
                finalString += " " * 4 + "Properties:\n" + self.securityGroup(resource[i]["Properties"])
            elif resource[i]["Type"] == "AWS::Route53::RecordSet":
                print(" " * 4 + "Type: Generic::DNSRecord")
                finalString += " " * 4 + "Type: Generic::DNSRecord\n"
                print(" " * 4 + "Properties:")
                finalString += " " * 4 + "Properties:\n" + self.dnsRecord(resource[i]["Properties"])
            else:
                print(" " * 4 + "Type: Generic::Unknown")
                finalString += " " * 4 + "Type: Generic::Unknown\n"
                print(" " * 4 + "Properties: Not Implemented")
                finalString += " " * 4 + "Properties: Not implemented\n"

        # Converts YAML int JSON
        finalString = json.dumps(yaml.load(finalString), sort_keys=False, indent=2)
        MainWindow.infoWindow("info", finalString)

        #exit(0)

        return finalString
