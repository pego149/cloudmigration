import json

from cloudmigration.MainWindow import MainWindow
from cloudmigration.Loader import Loader
from cloudmigration.Translation import Translation, Template
import tkinter as tk


class CloudMigration:
    def __init__(self):
        self.loader = Loader()
        self.loader.mapper.updateMapping()
        print(self.loader.enabled_platforms)
        self.root = tk.Tk()
        self.mainWindow = MainWindow(self.root, self.loader.enabled_platforms, self.doTransformation)
        if not self.mainWindow:
            MainWindow.infoWindow("error", "Error in creating main window.")
            exit(1)

        self.root.mainloop()

    def doTransformation(self, from_format, from_file, from_platform, to_format, to_file, to_platform):
        print(from_format, from_file, from_platform, to_format, to_file, to_platform)
        from_template = Template()  # create empty template class
        from_template.dictFromFile(from_file, from_format)  # load template in yaml format to template
        translation = Translation(from_platform, from_template.template, to_platform, self.loader)  # creata instance of translation
        to_template = Template(translation.translate())  # translate the template
        dump = json.dumps(to_template.template, sort_keys=True, indent=2)
        self.mainWindow.getLogger().debug(dump)
        to_template.dictToFile(to_file, to_format)  # save to JSON
        # to_template.dictToFile("to_orbis.yaml", "YAML")  # save to Zaml


if __name__ == '__main__':
    cloudmigration = CloudMigration()
