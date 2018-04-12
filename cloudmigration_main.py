from cloudmigration.Loader import Loader
from cloudmigration.Translation import Translation, Template

loader = Loader()
print(loader.enabled_platforms)
from_template = Template() #create empty template class
from_template.dictFromFile("orbis-lab.yaml", "YAML") #load template in yaml format to template
translation = Translation("OpenStack", from_template.template, "AWS", loader) #creata instance of translation
to_template = Template(translation.translate()) #translate the template
print(to_template.template)
to_template.dictToFile("orbis.json", "JSON") #save to JSON
to_template.dictToFile("to_orbis.yaml", "YAML") #save to Zaml