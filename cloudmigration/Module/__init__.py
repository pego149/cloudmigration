import os


class Module:
    def getModule(platform: str):
        """
        Function to load the schema for the given platform.
        :param platform: Platform name
        :return: Object containing the module
        """
        module = getattr(__import__("cloudmigration.Module." + platform, fromlist=[platform]), platform)
        return module
