results = {}
def __init__():
    import os, importlib
    for module_file in os.listdir(os.path.dirname(__file__)):
        if module_file[0] == '_' or module_file[-3:] != ".py":
            continue

        module_name = module_file[:-3]
        module = importlib.import_module("objectives.results." + module_name)

        results[module.Result.NAME] = module.Result
__init__()
