from cloudmigration.Schemas import getSchema


class Loader:
    def __init__(self):
        """
        Constructor of class Loader. Loads schemas, mapper, and translation modules.
        """
        self.mapper = getattr(__import__("cloudmigration.Mapper", fromlist=["Mapper"]), "Mapper")()
        self.translation_modules = {}
        self.schemas = {}
        with open('available_platforms.conf', 'r') as read_file:
            for platform in read_file.readlines():
                # new_platform = __import__(platform.rstrip(), fromlist=[platform.rstrip()])
                self.translation_modules[platform.rstrip()] = getattr(
                    __import__("cloudmigration.Modules", fromlist=["{0}".format(platform.rstrip())]), platform.rstrip())
                self.schemas[platform.rstrip()] = getSchema(platform.rstrip())


if __name__ == "__main__":
    l = Loader()
    print(l.mapper)
    print(l.translation_modules)
    print(l.schemas)
