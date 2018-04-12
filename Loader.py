from cloudmigration.Schemas import Schema


class Loader:
    def __init__(self):
        """
        Constructor of class Loader. Loads schemas, mapper, and translation modules.
        """
        self.mapper = getattr(__import__("cloudmigration.Mapper", fromlist=["Mapper"]), "Mapper")()
        self.translation_modules = {}
        self.schemas = {}
        self.enabled_platforms = []
        with open('enabled_platforms.conf', 'r') as read_file:
            for platform in read_file.readlines():
                platform = platform.rstrip()
                # new_platform = __import__(platform.rstrip(), fromlist=[platform.rstrip()])
                self.translation_modules[platform] = getattr(
                    __import__("cloudmigration.Modules", fromlist=["{0}".format(platform)]), platform)
                self.schemas[platform.rstrip()] = Schema.getSchema(platform)
                self.enabled_platforms.append(platform)

if __name__ == "__main__":
    l = Loader()
    print(l.mapper)
    print(l.translation_modules)
    print(l.schemas)
