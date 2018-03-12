from cloudmigration.Loader import Loader
import json
import yaml
from copy import deepcopy


class Template:
    def __init__(self, template=None):
        self.template = template

    def dictFromFile(self, file_name, template_format):
        with open(file_name, 'r') as read_file:
            if template_format == "JSON":
                self.template = json.load(read_file)
            elif template_format == "YAML":
                self.template = yaml.load(read_file)
        return self.template

    def dictFromString(self, template, template_format):
        if template_format == "JSON":
            self.template = json.loads(template)
        elif template_format == "YAML":
            self.template = yaml.load(template)
        return self.template

    def dictToFile(self, file_name, template_format, template=None):
        template = template if template is not None else self.template
        with open(file_name, 'w') as write_file:
            if template_format == "JSON":
                json.dump(template, write_file, indent=2)
            elif template_format == "YAML":
                yaml.dump(template, write_file, indent=2)

    def dictToString(self, template_format, template=None):
        template = template if template is not None else self.template
        if template_format == "JSON":
            return json.dumps(template, indent=2)
        elif template_format == "YAML":
            return yaml.dump(template, indent=2)

class Translation:
    def __init__(self, from_platform, from_template, to_platform, loader):
        self.loader = deepcopy(loader if loader is not None else getattr(__import__("Loader", fromlist=["Loader"]), "Loader")) #copies
        self.from_platform = from_platform
        self.from_template = from_template
        self.to_platform = to_platform
        self.to_template = None

    def translate(self):
        if self.from_platform == self.to_platform:
            self.to_template = self.from_template
        if self.from_platform != "Generic":
            from_module = self.loader.translation_modules[self.from_platform](self.from_platform, "Generic", self.loader.schemas[self.from_platform], self.loader.schemas["Generic"], self.loader.mapper)
            self.to_template = from_module.translateTemplate(self.from_template)
        if self.to_platform != "Generic":
            to_module = self.loader.translation_modules[self.to_platform]("Generic", self.to_platform, self.loader.schemas["Generic"], self.loader.schemas[self.to_platform], self.loader.mapper)
            self.to_template = to_module.translateTemplate(self.to_template)
        return self.to_template

    # def translate(self, paFromPlatform=None, paFromTemplate=None, paToPlatform=None, paLoader=None):
    #     paFromPlatform = paFromPlatform if paFromPlatform is not None else self.from_platform
    #     paFromTemplate = paFromTemplate if paFromTemplate is not None else self.from_template
    #     paToPlatform = paToPlatform if paToPlatform is not None else self.to_platform
    #     paLoader = paLoader if paLoader is not None else self.loader
    #     if paFromPlatform == paToPlatform:
    #         self.to_template = paFromTemplate
    #     else:
    #         from_module = paLoader.translation_modules[paFromPlatform]
    #         to_module = paLoader.translation_modules[paToPlatform]
    #
    #     return self.to_template


if __name__ == "__main__":
    t = Template()
    print(t.dictFromFile("bla.yaml", "YAML"))
    loader = Loader()
    template = {}
    translation = Translation("AWS", template, "AWS", loader)
    print(translation.loader.schemas)
    # print(translation.from_platform)
    # print(translation.to_platform)
    # print(translation.translate())

