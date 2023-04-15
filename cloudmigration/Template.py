import json
import yaml


class Template:
    def __init__(self, template=None):
        """
        Constructor of class Template.
        :param template: The template in dict format
        """
        self.template = template

    def dictFromFile(self, file_name, template_format):
        """
        Method to load template from a file.
        :param file_name: Name of the file containing the template
        :param template_format: "JSON" or "YAML"
        :return: Dict containing the template
        """
        with open(file_name, 'r') as read_file:
            if template_format == "JSON":
                self.template = json.load(read_file)
            elif template_format == "YAML":
                self.template = yaml.load(read_file, Loader=yaml.Loader)
        return self.template

    def dictFromString(self, template, template_format):
        """
        Method to load template from a string.
        :param template: String containing the template
        :param template_format: "JSON" or "YAML"
        :return: Dict containing the template
        """
        if template_format == "JSON":
            self.template = json.loads(template)
        elif template_format == "YAML":
            self.template = yaml.load(template, Loader=yaml.Loader)
        return self.template

    def dictToFile(self, file_name, template_format, template=None):
        """
        Method to save template to a file in the specified format
        :param file_name: Name of the file where the template is to be saved
        :param template_format: "JSON" or "YAML"
        :param template: Template to be saved. If None, uses class attribute.
        """
        template = template if template is not None else self.template
        with open(file_name, 'w') as write_file:
            if template_format == "JSON":
                json.dump(template, write_file, indent=2, sort_keys=True)
            elif template_format == "YAML":
                yaml.dump(template, write_file, indent=2, sort_keys=True)

    def dictToString(self, template_format, template=None):
        """
        Method to save template to a string in the specified format
        :param template_format: "JSON" or "YAML"
        :param template: Template to be saved. If None, uses class attribute.
        """
        template = template if template is not None else self.template
        if template_format == "JSON":
            return json.dumps(template, indent=2)
        elif template_format == "YAML":
            return yaml.dump(template, indent=2)
