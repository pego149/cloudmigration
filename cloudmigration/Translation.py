from copy import deepcopy
from cloudmigration.Loader import Loader
from cloudmigration.Template import Template


class Translation:
    def __init__(self, from_platform, from_template, to_platform, loader):
        """
        Constructor of the Translation class.
        :param from_platform: Platform from which the template should be translated
        :param from_template: Template to be translated
        :param to_platform: Platform to which the template should be translated
        :param loader: Instance of Loader containing the necessary schemas, instance of Mapper, and classes of Translation modules
        """
        self.loader = loader if loader is not None else getattr(__import__("Loader", fromlist=["Loader"]), "Loader")
        self.from_platform = from_platform
        self.from_template = from_template
        self.to_platform = to_platform
        self.to_template = None

    def translate(self):
        """
        Method to translate the template with the use of translation modules.
        :return: Translated template
        """
        if self.from_platform in self.loader.enabled_platforms and self.to_platform in self.loader.enabled_platforms:
            if self.from_platform == self.to_platform:
                self.to_template = self.from_template
            if self.from_platform != "Generic":
                from_module = self.loader.translation_modules[self.from_platform](self.from_platform, "Generic", self.loader.schemas[self.from_platform], self.loader.schemas["Generic"], self.loader.mapper)
                self.to_template = from_module.translateTemplate(self.from_template)
            if self.to_platform != "Generic":
                to_module = self.loader.translation_modules[self.to_platform]("Generic", self.to_platform, self.loader.schemas["Generic"], self.loader.schemas[self.to_platform], self.loader.mapper)
                self.to_template = to_module.translateTemplate(self.to_template)
            return self.to_template
        else:
            return None

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

