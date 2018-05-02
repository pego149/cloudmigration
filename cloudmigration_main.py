from cloudmigration.Loader import Loader
from cloudmigration.Translation import Translation, Template

class CloudMigration:
    def __init__(self):
        self.loader = Loader()

    def main(self, from_format, from_file, from_platform, to_format, to_file, to_platform):
    #     self.loader = Loader()
        self.loader.mapper.updateMapping()
        print(self.loader.enabled_platforms)
        from_template = Template()  # create empty template class
        from_template.dictFromFile(from_file, from_format)  # load template in yaml format to template
        translation = Translation(from_platform, from_template.template, to_platform, self.loader)  # creata instance of translation
        to_template = Template(translation.translate())  # translate the template
        print(to_template.template)
        to_template.dictToFile(to_file, to_format)  # save to JSON
        # to_template.dictToFile("to_orbis.yaml", "YAML")  # save to Zaml

if __name__ == '__main__':
    cloudmigration = CloudMigration()
    cloudmigration.main("YAML", "openstack_test.yaml", "OpenStack", "JSON", "aws_test.json", "AWS")
    cloudmigration.main("YAML", "openstack_test.yaml", "OpenStack", "JSON", "generic_test.json", "Generic")
    cloudmigration.main("JSON", "aws_test.json", "AWS", "YAML", "openstack_test2.yaml", "OpenStack")
    cloudmigration.main("JSON", "aws_test.json", "AWS", "JSON", "generic_test2.json", "Generic")

