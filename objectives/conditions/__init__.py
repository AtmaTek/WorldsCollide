conditions = {}
def __init__():
    import os, importlib
    for module_file in os.listdir(os.path.dirname(__file__)):
        if module_file[0] == '_' or module_file[-3:] != ".py":
            continue

        module_name = module_file[:-3]
        module = importlib.import_module("objectives.conditions." + module_name)

        conditions[module.Condition.NAME] = module.Condition
__init__()
