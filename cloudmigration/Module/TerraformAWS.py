import json

from terraformpy import Provider, Resource, Terraform, Variable, Output
import hcl2

res = Resource(
    'aws_instance', 'example',
    ami='ami-2757f631',
    instance_type='t2.micro',
    tags=dict(
        Name="test"
    )
)


tf = dict()
with open('../../aws_test.tf', 'r') as file:
    loaded = hcl2.load(file)
    #for modules in dict.get("module", []):
    #    for module in modules.keys():
    #        print(modules.keys())
    #        print(f"terraform state mv -state {state} -state-out {state_out} module.{module} module.{module}")

    tf['variable'] = {}
    for variables in loaded.get("variable", []):
        for variable in variables:
            tf['variable'][variable] = Variable(variable, **variables[variable])

    tf['provider'] = {}
    for providers in loaded.get("provider", []):
        for provider in providers:
            tf['provider'][provider] = Provider(provider, **providers[provider])

    tf['resource'] = {}
    for resources in loaded.get("resource", []):
        for resourceK in resources:
            for resK in resources[resourceK]:
                tf['resource'][resK] = Resource(resourceK, resK, **resources[resourceK][resK])

    tf['output'] = {}
    for outputs in loaded.get("output", []):
        for output in outputs:
            tf['output'][output] = Output(output, **outputs[output])


def printhcl(mydict, param="", ident=False, depth=0):
    """
    Produces a multi-line string for use in terraform tfvars file from a dictionary
    :param mydict: Dict
    :param ident: Should the lines be idented or not
    :return s: Multi-line String in hcl format
    """

    s = ""
    for key, val in mydict.items():
        space = "  "
        if depth == 0:
            param = key
        if ident:
            if param == "resource":
                sp = depth - 1
            else:
                sp = depth
            for i in range(sp-1):
                s += space
        if isinstance(val, dict):
            if len(val) > 0:
                if depth == 1 and param == "resource":
                    s += '"{0}" {1}'.format(key, str(printhcl(val, param, ident=False, depth=depth + 1)))
                elif depth == 1:
                    s += '"{0}" {1}'.format(key, "{\n" + str(printhcl(val, param, ident=True, depth=depth + 1)))
                else:
                    if param == "resource" and depth == 2:
                        s += '"{0}" {1}'.format(key, "{\n" + str(printhcl(val, param, ident=True, depth=depth + 1)))
                    else:
                        s += '{0} {1}'.format(key, "= {\n" + str(printhcl(val, param, ident=True, depth=depth + 1)))
            if ident:
                if param == "resource":
                    sp = depth - 1
                else:
                    sp = depth
                for i in range(sp - 1):
                    s += space
            if param != "resource" or depth != 1:
                s += '}'
            s += '\n'
        elif isinstance(val, str):
            if "${" in val:
                s += '{0} = {1}\n'.format(key, val.replace("${", "").replace("}", "").replace(",", ", "))
            else:
                s += '{0} = {1}\n'.format(key, '"' + val + '"')
        elif isinstance(val, list):
            if depth == 0:
                if key == "terraform":
                    for i in val:
                        s += key + ' {\n'
                        s += space + str(printhcl(i, param, ident=True, depth=depth + 1)).strip() + '\n'
                        s += '}\n\n'
                else:
                    for i in val:
                        s += key + ' '
                        if isinstance(i, dict):
                            s += str(printhcl(i, param, ident=True, depth=depth + 1)).strip() + '\n'
                        else:
                            s += '"{}",\n'.format(i)
                        s += '\n'
            if depth == 3 and isinstance(val[0], dict):
                for i in val:
                    s += '\n'
                    if ident:
                        s += space
                    if key == "tags":
                        s += key + ' = {\n'
                    else:
                        s += key + ' {\n'
                    if ident:
                        s += space
                    if isinstance(i, dict):
                        s += space + str(printhcl(i, param, ident=True, depth=depth+1)).strip() + '\n'
                    else:
                        s += space + i
                    if ident:
                        if param == "resource":
                            sp = depth - 1
                        else:
                            sp = depth
                        for i in range(sp - 1):
                            s += space
                    s += '}\n'

            else:
                if depth == 0:
                    continue
                s += key + ' = [ '
                for i in val:
                    if isinstance(i, dict):
                        s += str(printhcl(i, param, ident=True, depth=depth + 1)).strip() + ',\n'
                    else:
                        if "${" in i:
                            s += i.replace("${", "").replace("}", "").replace(",", ", ")
                        else:
                            s += '"' + i + '"'
                    s += ' ]\n'
        elif val is None:
            if ident:
                s += '{0} = {1}\n'.format(key, '""')
            else:
                s += '{0} = {1}\n'.format(key, '""')
        else:
            s += '{0} = {1}\n'.format(key, str(val).lower())
    return s


print(printhcl(loaded))

