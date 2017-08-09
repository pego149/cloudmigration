from globalMethods import GlobalMethods, pprint
import MainWindow as MainWindow
import json
import yaml
from io import StringIO


class AWS(GlobalMethods):
    def __init__(self):
        self.name = "AWS JSON class"

    def printName(self):
        print(self.name)

    ##########################################
    # Attribute functions to generic
    ##########################################

    @staticmethod
    def instanceToGeneric(paAttribute):
        """
        Method that transforms AWS JSON instance into Generic format in YAML.
        :param paAttribute: properties of AWS instance (AWS::EC2::Instance) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Image property (in AWS called AMI).
            if i == "ImageId":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    pprint(" " * 6 + "image: { ref: " + paAttribute[i]["Ref"] + " }")
                    string += " " * 6 + "image: { ref: " + paAttribute[i]["Ref"] + " }\n"
                else:
                    pprint(" " * 6 + "image: " + paAttribute[i])
                    string += " " * 6 + "image: " + paAttribute[i] + "\n"

            # SSH key property.
            elif i == "KeyName":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    pprint(" " * 6 + "key: { ref: " + paAttribute[i]["Ref"] + " }")
                    string += " " * 6 + "key: { ref: " + paAttribute[i]["Ref"] + " }\n"
                else:
                    pprint(" " * 6 + "key: " + paAttribute[i])
                    string += " " * 6 + "key: " + paAttribute[i] + "\n"

            # Instance type property. Defines CPU, RAM, HDD, ...
            elif i == "InstanceType":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    pprint(" " * 6 + "instance_type: { ref: " + paAttribute[i]["Ref"] + " }")
                    string += " " * 6 + "instance_type: { ref: " + paAttribute[i]["Ref"] + " }\n"
                else:
                    pprint(" " * 6 + "instance_type: " + paAttribute[i])
                    string += " " * 6 + "instance_type: " + paAttribute[i] + "\n"

            # Availability zone property.
            elif i == "AvailabilityZone":
                if isinstance(paAttribute[i], dict):
                    pprint(" " * 6 + "availability_zone: { ref: " + paAttribute[i]["Ref"] + " }")
                    string += " " * 6 + "availability_zone: { ref: " + paAttribute[i]["Ref"] + " }\n"
                else:
                    pprint(" " * 6 + "availability_zone: " + paAttribute[i])
                    string += " " * 6 + "availability_zone: " + paAttribute[i] + "\n"

            # User data. It gets and parses user data. Data itself are in "bare_data". If there are any
            # parameters/references, they are changed for key word  "parameter#", where # is subtracted for
            # sequence number of parameter. Parameters are referenced in next section: parameters.
            elif i == "UserData":
                array = []
                paramCount = 0

                pprint(" " * 6 + "user_data:")
                pprint(" " * 8 + "bare_data:")
                string += " " * 6 + "user_data:\n"
                string += " " * 8 + "bare_data:\n"

                # Get all data from UserData.
                for j in paAttribute[i]["Fn::Base64"]["Fn::Join"][1]:
                    try:
                        string += " " * 10 + j
                        pprint(" " * 10 + j, end='')

                    # If there is any reference, increment parameters count and add reference to array.
                    except TypeError:
                        array.append(j["Ref"])
                        paramCount += 1
                        string += "$parameter" + str(paramCount) + " "
                        pprint("$parameter" + str(paramCount) + " ", end='')

                # If are there any parameters, pprint a section with them.
                if paramCount > 0:
                    string += " " * 8 + "parameters:\n"
                    pprint(" " * 8 + "parameters:")
                    for j in range(1, paramCount + 1):
                        string += " " * 10 + "$parameter" + str(j) + ": " + array[j - 1] + "\n"
                        pprint(" " * 10 + "$parameter" + str(j) + ": " + array[j - 1])

            # Tags properties. They are written in form Key: Value.
            elif i == "Tags":
                pprint(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute["Tags"]:
                    pprint(" " * 8 + "" + j["Key"] + ": " + j["Value"])
                    string += " " * 8 + j["Key"] + ": " + j["Value"] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def subnetToGeneric(paAttribute):
        """
        Method that transforms AWS JSON subnet into Generic format in YAML.
        :param paAttribute: properties of AWS subnet (AWS::EC2::Subnet) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Network, that Subnet is par of.
            if i == "VpcId":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    pprint(" " * 6 + "network: { ref: " + paAttribute[i]["Ref"] + " }")
                    string += " " * 6 + "network: { ref: " + paAttribute[i]["Ref"] + " }\n"
                else:
                    pprint(" " * 6 + "network: " + paAttribute[i])
                    string += " " * 6 + "network: " + paAttribute[i] + "\n"

            # IP subnet in CIDR format (192.168.1.0/24).
            elif i == "CidrBlock":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    pprint(" " * 6 + "cidr: { ref: " + paAttribute[i]["Ref"] + " }")
                    string += " " * 6 + "cidr: { ref: " + paAttribute[i]["Ref"] + " }\n"
                else:
                    pprint(" " * 6 + "cidr: " + paAttribute[i])
                    string += " " * 6 + "cidr: " + paAttribute[i] + "\n"

            # Availability zone property.
            elif i == "AvailabilityZone":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    pprint(" " * 6 + "availability_zone: { ref: " + paAttribute[i]["Ref"] + " }")
                    string += " " * 6 + "availability_zone: { ref: " + paAttribute[i]["Ref"] + " }\n"
                else:
                    pprint(" " * 6 + "availability_zone: " + paAttribute[i])
                    string += " " * 6 + "availability_zone: " + paAttribute[i] + "\n"

            # Tags properties. They are written in form Key: Value.
            elif i == "Tags":
                pprint(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute["Tags"]:
                    pprint(" " * 8 + "" + j["Key"] + ": " + j["Value"])
                    string += " " * 8 + j["Key"] + ": " + j["Value"] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def networkToGeneric(paAttribute):
        """
        Method that transforms AWS JSON network into Generic format in YAML.
        :param paAttribute: properties of AWS network (AWS::EC2::VPC) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # IP subnet in CIDR format (192.168.1.0/24).
            if i == "CidrBlock":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    pprint(" " * 6 + "cidr: { ref: " + paAttribute[i]["Ref"] + " }")
                    string += " " * 6 + "cidr: { ref: " + paAttribute[i]["Ref"] + " }\n"
                else:
                    pprint(" " * 6 + "cidr: " + paAttribute[i])
                    string += " " * 6 + "cidr: " + paAttribute[i] + "\n"

            # Tags properties. They are written in form Key: Value.
            elif i == "Tags":
                pprint(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute["Tags"]:
                    pprint(" " * 8 + "" + j["Key"] + ": " + j["Value"])
                    string += " " * 8 + j["Key"] + ": " + j["Value"] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def securityGroupToGeneric(paAttribute):
        """
        Method that transforms AWS JSON security groups into Generic format in YAML.
        :param paAttribute: properties of AWS network (AWS::EC2::SecurityGroup) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Writes description of Security group.
            if i == "GroupDescription":
                pprint(" "*6 + "description: " + paAttribute[i])
                string += " "*6 + "description: " + paAttribute[i] + "\n"

            # Security group rules in both: inbound and outbound directions.
            elif i == "SecurityGroupIngress" or i == "SecurityGroupEgress":
                if i == "SecurityGroupIngress":
                    pprint(" " * 6 + "ingress_rules:")
                    string += " " * 6 + "ingress_rules:\n"
                else:
                    pprint(" " * 6 + "egress_rules:")
                    string += " " * 6 + "egress_rules:\n"

                for j in paAttribute[i]:
                    first = 1
                    for k in j:
                        # Transport protocol carried in IP packet.
                        if k == "IpProtocol":
                            # If it is not first in list, just pprint it.
                            if not first:
                                pprint(" " * 10 + "protocol: " + j["IpProtocol"])
                                string += " " * 10 + "protocol: " + j["IpProtocol"] + "\n"

                            # If it is first in the list, write dash before it.
                            else:
                                first = 0
                                pprint(" " * 8 + "- protocol: " + j["IpProtocol"])
                                string += " " * 8 + "- protocol: " + j["IpProtocol"] + "\n"

                        # First port to start list with.
                        elif k == "FromPort":
                            # If it is not first in list, just pprint it.
                            if not first:
                                pprint(" " * 10 + "from_port: " + j["FromPort"])
                                string += " " * 10 + "from_port: " + j["FromPort"] + "\n"

                            # If it is first in the list, write dash before it.
                            else:
                                first = 0
                                pprint(" " * 8 + "- from_port: " + j["FromPort"])
                                string += " " * 8 + "- from_port: " + j["FromPort"] + "\n"

                        # Last port in the list.
                        elif k == "ToPort":
                            # If it is not first in list, just pprint it.
                            if not first:
                                pprint(" " * 10 + "to_port: " + j["ToPort"])
                                string += " " * 10 + "to_port: " + j["ToPort"] + "\n"

                            # If it is first in the list, write dash before it.
                            else:
                                first = 0
                                pprint(" " * 8 + "- to_port: " + j["ToPort"])
                                string += " " * 8 + "- to_port: " + j["ToPort"] + "\n"

                        # Network addres to bind rule to. In CIDR format (192.168.10.0/24).
                        elif k == "CidrIp":
                            # If it is not first in list, just pprint it.
                            if not first:
                                # Checks, if it is reference
                                if isinstance(j[k], dict):
                                    pprint(" " * 10 + "cidr: { ref: " + j[k]["Ref"] + " }")
                                    string += " " * 10 + "cidr: { ref: " + j[k]["Ref"] + " }\n"
                                else:
                                    pprint(" " * 10 + "cidr: " + j[k])
                                    string += " " * 10 + "cidr: " + j[k] + "\n"

                            # If it is first in the list, write dash before it.
                            else:
                                first = 0
                                # Checks, if it is reference
                                if isinstance(j[k], dict):
                                    pprint(" " * 8 + "- cidr: { ref: " + j[k] + " }")
                                    string += " " * 8 + "- cidr: { ref: " + j[k] + " }\n"
                                else:
                                    pprint(" " * 8 + "- cidr: " + j[k])
                                    string += " " * 8 + "- cidr: " + j[k] + "\n"

                        # Otherwise write, that it is not implemented yet.
                        else:
                            # If it is not first in list, just pprint it.
                            if not first:
                                pprint(" " * 10 + k + ": Not Implemented")
                                string += " " * 10 + k + ": Not Implemented\n"

                            # If it is first in the list, write dash before it.
                            else:
                                first = 0
                                pprint(" " * 8 + "- " + k + ": Not Implemented")
                                string += " " * 8 + "- " + k + ": Not Implemented\n"

            # Tags properties. They are written in form Key: Value.
            elif i == "Tags":
                pprint(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute["Tags"]:
                    pprint(" " * 8 + "" + j["Key"] + ": " + j["Value"])
                    string += " " * 8 + j["Key"] + ": " + j["Value"] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def dnsRecordToGeneric(paAttribute):
        """
        Method that transforms AWS JSON DNS resource record into Generic format in YAML.
        :param paAttribute: properties of AWS DNS RR (AWS::Route53::RecordSet) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Name of the RR
            if i == "Name":
                pprint(" " * 6 + "name: " + paAttribute[i])
                string += " " * 6 + "name: " + paAttribute[i] + "\n"

            # Type of the RR
            elif i == "Type":
                pprint(" " * 6 + "type: " + paAttribute[i])
                string += " " * 6 + "type: " + paAttribute[i] + "\n"

            # Value of the RR
            elif i == "ResourceRecords":
                # pprint(" " * 6 + "record: " + str(paAttribute[i]).replace("'", ""))
                # string += " " * 6 + "record: " + str(paAttribute[i]).replace("'", "") + "\n"

                pprint(" " * 6 + "records:")
                string += " " * 6 + "records:\n"

                for j in paAttribute[i]:
                    pprint(" " * 8 + "- attribute")
                    string += " " * 8 + "- attribute\n"

                    pprint(" " * 10 + "- " + j["Fn::GetAtt"][0])
                    string += " " * 10 + "- " + j["Fn::GetAtt"][0] + "\n"
                    pprint(" " * 12 + j["Fn::GetAtt"][1])
                    string += " " * 12 + j["Fn::GetAtt"][1] + "\n"

            # TTL of the RR
            elif i == "TTL":
                pprint(" " * 6 + "ttl: " + paAttribute[i])
                string += " " * 6 + "ttl: " + paAttribute[i] + "\n"

            # Comment
            elif i == "Comment":
                pprint(" " * 6 + "comment: " + paAttribute[i])
                string += " " * 6 + "comment: " + paAttribute[i] + "\n"

            # Zone in which is RR
            elif i == "HostedZoneId":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    pprint(" " * 6 + "zone: { ref: " + paAttribute[i]["Ref"] + " }")
                    string += " " * 6 + "zone: { ref: " + paAttribute[i]["Ref"] + " }\n"
                else:
                    pprint(" " * 6 + "zone: " + paAttribute[i])
                    string += " " * 6 + "zone: " + paAttribute[i] + "\n"

            # Tags properties. They are written in form Key: Value.
            elif i == "Tags":
                pprint(" " * 6 + "tags:")
                string += " " * 6 + "tags: " + "\n"
                for j in paAttribute["Tags"]:
                    pprint(" " * 8 + "" + j["Key"] + ": " + j["Value"])
                    string += " " * 8 + j["Key"] + ": " + j["Value"] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def autocsalingGroupToGeneric(paAttribute):
        # TODO dorobit
        pass

    @staticmethod
    def autocsalingPolicyToGeneric(paAttribute):
        # TODO dorobit
        pass

    @staticmethod
    def loadBalancerToGeneric(paAttribute):
        # TODO dorobit
        pass

    ##########################################
    # Attribute functions from generic
    ##########################################

    @staticmethod
    def instanceFromGeneric(paAttribute):
        """
        Method that transforms Generic instance into AWS format in YAML.
        :param paAttribute: properties of Generic instance (Generic::VirtualMachine) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Image property (in AWS called AMI).
            if i == "image":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                        pprint(" " * 6 + "ImageId: { Ref: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "ImageId: { Ref: " + paAttribute[i]["ref"] + " }\n"
                else:
                    pprint(" " * 6 + "ImageId: " + paAttribute[i])
                    string += " " * 6 + "ImageId: " + paAttribute[i] + "\n"

            # SSH key property.
            elif i == "key":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                        pprint(" " * 6 + "KeyName: { Ref: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "KeyName: { Ref: " + paAttribute[i]["ref"] + " }\n"
                else:
                    pprint(" " * 6 + "KeyName: " + paAttribute[i])
                    string += " " * 6 + "KeyName: " + paAttribute[i] + "\n"

            # Instance type property. Defines CPU, RAM, HDD, ...
            elif i == "instance_type":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                        pprint(" " * 6 + "InstanceType: { Ref: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "InstanceType: { Ref: " + paAttribute[i]["ref"] + " }\n"
                else:
                    pprint(" " * 6 + "InstanceType: " + paAttribute[i])
                    string += " " * 6 + "InstanceType: " + paAttribute[i] + "\n"

            # Availability zone property.
            elif i == "availability_zone":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                        pprint(" " * 6 + "AvailabilityZone: { Ref: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "AvailabilityZone: { Ref: " + paAttribute[i]["ref"] + " }\n"
                else:
                    pprint(" " * 6 + "AvailabilityZone: " + paAttribute[i])
                    string += " " * 6 + "AvailabilityZone: " + paAttribute[i] + "\n"

            # Security groups.
            elif i == "security_groups":
                pprint(" " * 6 + "SecurityGroupIds:")
                string += " " * 6 + "SecurityGroupIds:\n"

                for j in paAttribute[i]:
                    try:
                        pprint(" " * 8 + "- " + j)
                        string += " " * 8 + "- " + j + "\n"
                    except TypeError:
                        for k in j:
                            # If it is parameter, write get_param
                                pprint(" " * 8 + "- { Ref: " + j[k] + " }")
                                string += " " * 8 + "- { Ref: " + j[k] + " }\n"

            # User data. It gets and parses user data.
            elif i == "user_data":

                pprint(" " * 6 + "UserData:\n" + " " * 8 + "Fn::Base64:\n" + " " * 10 + "Fn::Join:\n" + " " * 12 + "- \"\"\n" + " " * 12 + "- # data")
                string += " " * 6 + "UserData:\n" + " " * 8 + "Fn::Base64:\n" + " " * 10 + "Fn::Join:\n" + " " * 12 + "- \"\"\n" + " " * 12 + "- # data\n"

                temp = str(paAttribute[i]["bare_data"])

                if paAttribute[i]["parameters"] is not None:
                    for j in paAttribute[i]["parameters"]:
                        # Replace parameters for their values.
                        temp = temp.replace(j, "{ Ref: " + paAttribute[i]["parameters"][j] + " }")

                # Get all data from UserData.
                # string += " " * 14 + temp + "\n"
                # pprint(" " * 14 + temp)

                s = StringIO(temp)
                for line in s:
                    string += " " * 14 + line + "\n"
                    pprint(" " * 14 + line, end='')

            # Tags properties
            elif i == "tags":
                pprint(" " * 6 + "Tags:")
                string += " " * 6 + "Tags: " + "\n"
                for j in paAttribute[i]:
                    pprint(" " * 8 + "- Key: " + j + "\n" + " " * 10 + "Value: " + paAttribute[i][j])
                    string += " " * 8 + "- Key: " + j + "\n" + " " * 10 + "Value: " + paAttribute[i][j] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def subnetFromGeneric(paAttribute):
        """
        Method that transforms Generic subnet into AWS format in YAML.
        :param paAttribute: properties of Generic subnet (Generic::Subnet) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Network, that Subnet is par of.
            if i == "network":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                        pprint(" " * 6 + "VpcId: { Ref: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "VpcId: { Ref: " + paAttribute[i]["ref"] + " }\n"
                else:
                    pprint(" " * 6 + "VpcId: " + paAttribute[i])
                    string += " " * 6 + "VpcId: " + paAttribute[i] + "\n"

            # IP subnet in CIDR format (192.168.1.0/24).
            elif i == "cidr":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                        pprint(" " * 6 + "CidrBlock: { Ref: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "CidrBlock: { Ref: " + paAttribute[i]["ref"] + " }\n"
                else:
                    pprint(" " * 6 + "CidrBlock: " + paAttribute[i])
                    string += " " * 6 + "CidrBlock: " + paAttribute[i] + "\n"

            # Availability zone property. OpenStack does not have it.
            elif i == "availability_zone":
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                    pprint(" " * 6 + "AvailabilityZone: { Ref: " + paAttribute[i]["ref"] + " }")
                    string += " " * 6 + "AvailabilityZone: { Ref: " + paAttribute[i]["ref"] + " }\n"
                else:
                    pprint(" " * 6 + "AvailabilityZone: " + paAttribute[i])
                    string += " " * 6 + "AvailabilityZone: " + paAttribute[i] + "\n"

            # Tags properties
            elif i == "tags":
                pprint(" " * 6 + "Tags:")
                string += " " * 6 + "Tags: " + "\n"
                for j in paAttribute[i]:
                    pprint(" " * 8 + "- Key: " + j + "\n" + " " * 10 + "Value: " + paAttribute[i][j])
                    string += " " * 8 + "- Key: " + j + "\n" + " " * 10 + "Value: " + paAttribute[i][j] + "\n"

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
                # Checks, if it is reference
                if isinstance(paAttribute[i], dict):
                        pprint(" " * 6 + "CidrBlock: { Ref: " + paAttribute[i]["ref"] + " }")
                        string += " " * 6 + "CidrBlock: { Ref: " + paAttribute[i]["ref"] + " }\n"
                else:
                    pprint(" " * 6 + "CidrBlock: " + paAttribute[i])
                    string += " " * 6 + "CidrBlock: " + paAttribute[i] + "\n"

            # Tags properties
            elif i == "tags":
                pprint(" " * 6 + "Tags:")
                string += " " * 6 + "Tags: " + "\n"
                for j in paAttribute[i]:
                    pprint(" " * 8 + "- Key: " + j + "\n" + " " * 10 + "Value: " + paAttribute[i][j])
                    string += " " * 8 + "- Key: " + j + "\n" + " " * 10 + "Value: " + paAttribute[i][j] + "\n"

            # Else write, that this property is not implemented yet.
            else:
                pprint(" " * 6 + i + ": Not implemented")
                string += " " * 6 + i + ": Not implemented" + "\n"

        return string

    @staticmethod
    def securityGroupFromGeneric(paAttribute):
        """
        Method that transforms Generic security groups into AWS format in YAML.
        :param paAttribute: properties of Generic Security Group (Generic::SecurityGroup) in JSON format
        :return: string in YAML format
        """

        string = ""

        for i in paAttribute:
            # Writes description of Security group.
            if i == "description":
                pprint(" " * 6 + "description: " + paAttribute[i])
                string += " " * 6 + "description: " + paAttribute[i] + "\n"

            # Security group rules in inbound direction.
            elif i == "ingress_rules":

                pprint(" " * 6 + "SecurityGroupIngress: ")
                string += " " * 6 + "SecurityGroupIngress:\n"

                for j in paAttribute[i]:
                    for k in j:
                        # Transport protocol carried in IP packet.
                        if k == "protocol":
                            pprint(" " * 8 + "- IpProtocol: " + j["protocol"])
                            string += " " * 8 + "- IpProtocol: " + j["protocol"] + "\n"

                        # First port to start list with.
                        elif k == "from_port":
                            pprint(" " * 10 + "FromPort: " + str(j["from_port"]))
                            string += " " * 10 + "FromPort: " + str(j["from_port"]) + "\n"

                        # Last port in the list.
                        elif k == "to_port":
                            pprint(" " * 10 + "ToPort: " + str(j["to_port"]))
                            string += " " * 10 + "ToPort: " + str(j["to_port"]) + "\n"

                        # Network addres to bind rule to. In CIDR format (192.168.10.0/24).
                        elif k == "cidr":
                            if isinstance(j[k], dict):
                                    pprint(" " * 10 + "CidrIp: { Ref: " + j[k]["ref"] + " }")
                                    string += " " * 10 + "CidrIp: { Ref: " + j[k]["ref"] + " }\n"
                            else:
                                pprint(" " * 10 + "CidrIp: " + j[k])
                                string += " " * 10 + "CidrIp: " + j[k] + "\n"

                        # Version of IP protocol.
                        elif k == "ethertype":
                            pprint(" " * 10 + "ethertype: " + j["ethertype"])
                            string += " " * 10 + "ethertype: " + j["ethertype"] + "\n"

                        # Otherwise write, that it is not implemented yet.
                        else:
                            pprint(" " * 10 + k + ": Not Implemented")
                            string += " " * 10 + k + ": Not Implemented\n"

            # Security group rules in outbound direction.
            elif i == "egress_rules":

                pprint(" " * 6 + "SecurityGroupEgress: ")
                string += " " * 6 + "SecurityGroupEgress:\n"

                for j in paAttribute[i]:
                    for k in j:
                        # Transport protocol carried in IP packet.
                        if k == "protocol":
                            pprint(" " * 8 + "- IpProtocol: " + j["protocol"])
                            string += " " * 8 + "- IpProtocol: " + j["protocol"] + "\n"

                        # First port to start list with.
                        elif k == "from_port":
                            pprint(" " * 10 + "FromPort: " + str(j["from_port"]))
                            string += " " * 10 + "FromPort: " + str(j["from_port"]) + "\n"

                        # Last port in the list.
                        elif k == "to_port":
                            pprint(" " * 10 + "ToPort: " + str(j["to_port"]))
                            string += " " * 10 + "ToPort: " + str(j["to_port"]) + "\n"

                        # Network addres to bind rule to. In CIDR format (192.168.10.0/24).
                        elif k == "cidr":
                            if isinstance(j[k], dict):
                                    pprint(" " * 10 + "CidrIp: { Ref: " + j[k]["ref"] + " }")
                                    string += " " * 10 + "CidrIp: { Ref: " + j[k]["ref"] + " }\n"
                            else:
                                pprint(" " * 10 + "CidrIp: " + j[k])
                                string += " " * 10 + "CidrIp: " + j[k] + "\n"

                        # Version of IP protocol.
                        elif k == "ethertype":
                            pprint(" " * 10 + "ethertype: " + j["ethertype"])
                            string += " " * 10 + "ethertype: " + j["ethertype"] + "\n"

                        # Otherwise write, that it is not implemented yet.
                        else:
                            pprint(" " * 10 + k + ": Not Implemented")
                            string += " " * 10 + k + ": Not Implemented\n"

            # Tags properties.
            elif i == "tags":
                pprint(" " * 6 + "Tags:")
                string += " " * 6 + "Tags: " + "\n"
                for j in paAttribute[i]:
                    pprint(" " * 8 + "- Key: " + j + "\n" + " " * 10 + "Value: " + paAttribute[i][j])
                    string += " " * 8 + "- Key: " + j + "\n" + " " * 10 + "Value: " + paAttribute[i][j] + "\n"

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
        Method reads data from file passes as parameter. Data can be in two formats, JSON and YAML. It parses it, and
        calls other methods, which parses smaller parts of given data. Finally, it returns string in generic format.
        The string is formatted in JSON format.
        :param paFile: file to read data from
        :return: converted string in generic format, written in JSON
        """

        # This string is being filled with data and finally is returned from this function.
        finalString = ""

        # Reads data from file. It is smart, will read both: YAML and JSON.
        with open(paFile) as data_file:
            string = json.load(data_file)
            # string = json.dumps(yaml.load(data_file), sort_keys=False, indent=2)

        # Prints format of this template.
        pprint("template_version: " + string["AWSTemplateFormatVersion"])

        # Because of issues of date in JSON, it is printed with dots. Therefore it is recommended to check it manually.
        finalString += "template_version: " + string["AWSTemplateFormatVersion"].replace("-", ".") + \
                       " - Please check and update manually\n"

        # Prints description of whole template.
        pprint("description: " + string["Description"] + "\n")
        finalString += "description: " + string["Description"] + "\n"

        ###########################################################################################
        # PARAMETERS
        ###########################################################################################

        pprint("parameters:\n")
        finalString += "parameters:\n"

        parameter = string["Parameters"]

        # Iterates all parameters and prints them
        for i in parameter:
            # Prints name of parameter.
            pprint(" "*2 + i + ":")
            finalString += " "*2 + i + ":\n"

            for attribute in parameter[i]:
                # prints name of attribute
                # pprint(" "*4 + attribute + ": ", end='')
                # finalString += " "*4 + attribute + ": "

                # In these types of attributes, there is just simple print of original value.
                if attribute == "Type" or attribute == "Description" or attribute == "Default":
                    pprint(" "*4 + attribute.lower() + ": " + parameter[i][attribute])
                    finalString += " "*4 + attribute.lower() + ": " + parameter[i][attribute] + "\n"

                elif attribute == "MinLength":
                    pprint(" " * 4 + "min_length: " + parameter[i][attribute])
                    finalString += " " * 4 + "min_length: " + parameter[i][attribute] + "\n"

                elif attribute == "MaxLength":
                    pprint(" " * 4 + "max_length: " + parameter[i][attribute])
                    finalString += " " * 4 + "max_length: " + parameter[i][attribute] + "\n"

                elif attribute == "ConstraintDescription":
                    pprint(" " * 4 + "constraint_description: " + parameter[i][attribute])
                    finalString += " " * 4 + "constraint_description: " + parameter[i][attribute] + "\n"

                # In Allowed pattern, there is Regex, which is printed with warning, that it should be checked manually.
                elif attribute == "AllowedPattern":
                    pprint(" "*4 + "allowed_pattern: " + str(parameter[i][attribute]))
                    finalString += " "*4 + "allowed_pattern: " + "Check manually " + parameter[i][attribute] + "\n"

                # Allowed values are printed as a list.
                elif attribute == "AllowedValues":
                    pprint(" " * 4 + attribute.lower() + ":")
                    finalString += " "*4 + "allowed_values:\n"
                    for k in parameter[i][attribute]:
                        pprint(" " * 4 + "- " + k)
                        finalString += " " * 4 + "- " + k + "\n"

                # Else write, that it is not implemented yet.
                else:
                    pprint("Not implemented")
                    finalString += "Not Implemented\n"

        ###########################################################################################
        # RESOURCES
        ###########################################################################################

        pprint("\nresources:\n")
        finalString += "resources:\n"
        resource = string["Resources"]

        for i in resource:
            # prints name of resource
            pprint("  " + i + ": ")
            finalString += "  " + i + ":\n"

            # Based on resource name, calls method which will transform property data.
            if resource[i]["Type"] == "AWS::EC2::Instance":
                pprint(" " * 4 + "type: Generic::VirtualMachine")
                finalString += " " * 4 + "type: Generic::VirtualMachine\n"
                pprint(" " * 4 + "properties:")
                finalString += " " * 4 + "properties:\n" + self.instanceToGeneric(resource[i]["Properties"])
            elif resource[i]["Type"] == "AWS::EC2::VPC":
                pprint(" " * 4 + "type: Generic::Network")
                finalString += " " * 4 + "type: Generic::Network\n"
                pprint(" " * 4 + "properties:")
                finalString += " " * 4 + "properties:\n" + self.networkToGeneric(resource[i]["Properties"])
            elif resource[i]["Type"] == "AWS::EC2::Subnet":
                pprint(" " * 4 + "type: Generic::Subnet")
                finalString += " " * 4 + "type: Generic::Subnet\n"
                pprint(" " * 4 + "properties:")
                finalString += " " * 4 + "properties:\n" + self.subnetToGeneric(resource[i]["Properties"])
            elif resource[i]["Type"] == "AWS::EC2::SecurityGroup":
                pprint(" " * 4 + "type: Generic::SecurityGroup")
                finalString += " " * 4 + "type: Generic::SecurityGroup\n"
                pprint(" " * 4 + "properties:")
                finalString += " " * 4 + "properties:\n" + self.securityGroupToGeneric(resource[i]["Properties"])
            elif resource[i]["Type"] == "AWS::Route53::RecordSet":
                pprint(" " * 4 + "type: Generic::DNSRecord")
                finalString += " " * 4 + "type: Generic::DNSRecord\n"
                pprint(" " * 4 + "properties:")
                finalString += " " * 4 + "properties:\n" + self.dnsRecordToGeneric(resource[i]["Properties"])
            else:
                pprint(" " * 4 + "type: Generic::Unknown")
                finalString += " " * 4 + "type: Generic::Unknown\n"
                pprint(" " * 4 + "properties: Not Implemented")
                finalString += " " * 4 + "properties: Not implemented\n"

        # Converts YAML int JSON
        finalString = json.dumps(yaml.load(finalString), sort_keys=False, indent=2)

        return finalString

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
        pprint("AWSTemplateFormatVersion: " + string["template_version"])

        # Because of issues of date in JSON, it is printed with dots. Therefore it is recommended to check ity manually.
        finalString += "AWSTemplateFormatVersion: " + string["template_version"].replace("-", ".") + \
                       " - Please check and update manually\n"

        # Prints description of whole template.
        pprint("Description: " + string["description"] + "\n")
        finalString += "Description: " + string["description"] + "\n"

        ###########################################################################################
        # PARAMETERS
        ###########################################################################################

        pprint("Parameters:")
        finalString += "Parameters:\n"
        parameter = string["parameters"]

        # Iterates all parameters and prints them
        for i in parameter:

            # Prints name of parameter.
            pprint(" " * 2 + i + ":")
            finalString += " " * 2 + i + ":\n"

            for attribute in parameter[i]:
                # If there is empty parameter, skip it
                if parameter[i][attribute] is None:
                    continue

                # Type has to be lowercase
                elif attribute == "type":
                    pprint(" " * 4 + "Type: " + parameter[i][attribute].lower())
                    finalString += " " * 4 + "Type: " + parameter[i][attribute].lower() + "\n"

                # Description of parameter.
                elif attribute == "description":
                    pprint(" " * 4 + "Description: " + parameter[i][attribute])
                    finalString += " " * 4 + "Description: " + parameter[i][attribute] + "\n"

                # Default value of parameter.
                elif attribute == "default":
                    pprint(" " * 4 + "Default: " + parameter[i][attribute])
                    finalString += " " * 4 + "Default: " + parameter[i][attribute] + "\n"

                # Minimal length of parameter.
                elif attribute == "min_length":
                    pprint(" " * 4 + "MinLength: " + str(parameter[i][attribute]))
                    finalString += " " * 4 + "MinLength: " + str(parameter[i][attribute]) + "\n"

                # Maximal length of parameter.
                elif attribute == "max_length":
                    pprint(" " * 4 + "Maxength: " + str(parameter[i][attribute]))
                    finalString += " " * 4 + "MaxLength: " + str(parameter[i][attribute]) + "\n"

                # In Allowed pattern, there is Regex, which is printed with warning, that it should be checked manually.
                elif attribute == "allowed_pattern":
                    pprint(" " * 4 + "AllowedPattern: " + parameter[i][attribute] + " - Check manually")
                    finalString += " " * 4 + "AllowedPattern: " + parameter[i][attribute] + " - Check manually\n"

                # Allowed values are printed as a list.
                elif attribute == "allowed_values":
                    pprint(" " * 4 + "AllowedValues:")
                    finalString += " " * 4 + "AllowedValues:\n"

                    for j in parameter[i][attribute]:
                        pprint(" " * 6 + "- " + j)
                        finalString += " " * 6 + "- " + j + "\n"

                # Constraint description - OpenStack does not have this attribute
                elif attribute == "constraint_description":
                    pprint(" " * 4 + "ConstraintDescription: " + parameter[i][attribute])
                    finalString += " " * 4 + "ConstraintDescription: " + parameter[i][attribute] + "\n"

                # Else write, that it is not implemented yet.
                else:
                    pprint(" " * 4 + attribute.lower() + ": " + "Not implemented")
                    finalString += " " * 4 + attribute.lower() + ": " + "Not Implemented\n"

        ###########################################################################################
        # RESOURCES
        ###########################################################################################

        pprint("\nResources:\n")
        finalString += "Resources:\n"
        resource = string["resources"]

        for i in resource:
            # prints name of resource
            pprint(" " * 2 + i + ": ")
            finalString += " " * 2 + i + ":\n"

            # Based on resource name, calls method which will transform property data.
            if resource[i]["type"] == "Generic::VirtualMachine":
                pprint(" " * 4 + "Type: AWS::EC2::Instance")
                finalString += " " * 4 + "Type: AWS::EC2::Instance\n"
                pprint(" " * 4 + "Properties:")
                finalString += " " * 4 + "Properties:\n" + self.instanceFromGeneric(resource[i]["properties"])
            elif resource[i]["type"] == "Generic::Network":
                pprint(" " * 4 + "Type: AWS::EC2::VPC")
                finalString += " " * 4 + "Type: AWS::EC2::VPC\n"
                pprint(" " * 4 + "Properties:")
                finalString += " " * 4 + "Properties:\n" + self.networkFromGeneric(resource[i]["properties"])
            elif resource[i]["type"] == "Generic::Subnet":
                pprint(" " * 4 + "Type: AWS::EC2::Subnet")
                finalString += " " * 4 + "Type: AWS::EC2::Subnet\n"
                pprint(" " * 4 + "Properties:")
                finalString += " " * 4 + "Properties:\n" + self.subnetFromGeneric(resource[i]["properties"])
            elif resource[i]["type"] == "Generic::SecurityGroup":
                pprint(" " * 4 + "Type: AWS::EC2::SecurityGroup")
                finalString += " " * 4 + "Type: AWS::EC2::SecurityGroup\n"
                pprint(" " * 4 + "Properties:")
                finalString += " " * 4 + "Properties:\n" + self.securityGroupFromGeneric(resource[i]["properties"])
            else:
                pprint(" " * 4 + "Type: " + resource[i]["type"])
                finalString += " " * 4 + "Type: " + resource[i]["type"] + "\n"
                pprint(" " * 4 + "Properties: Not Implemented")
                finalString += " " * 4 + "Properties: Not implemented\n"

        # Converting YAML to JSON.
        finalString = json.dumps(yaml.load(finalString), sort_keys=False, indent=2)

        # Saving to file
        try:
            file = open(paFile, 'w')
            file.write(finalString)
        except IOError:
            MainWindow.infoWindow("error", "Error in saving file " + paFile)

        return finalString


