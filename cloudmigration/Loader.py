from cloudmigration.Module import Module
from cloudmigration.Schema import Schema


class Loader:
    def __init__(self):
        """
        Constructor of class Loader. Loads schemas, mapper, and translation modules.
        """
        self.mapper = __import__("cloudmigration.Mapper", fromlist=["Mapper"]).Mapper()
        self.translation_modules = {}
        self.schemas = {}
        self.enabled_platforms = []
        with open('cloudmigration/enabled_platforms.conf', 'r') as read_file:
            for platform in read_file.readlines():
                platform = platform.rstrip()
                # new_platform = __import__(platform.rstrip(), fromlist=[platform.rstrip()])
                self.translation_modules[platform] = Module.getModule(platform)
                self.schemas[platform] = Schema.getSchema(platform)
                self.enabled_platforms.append(platform)
