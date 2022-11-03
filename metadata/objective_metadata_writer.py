from metadata.objective_condition_metadata import ObjectiveConditionMetadata
from metadata.objective_metadata import ObjectiveMetadata

OBJECTIVE_BANK = "FF"
NAME_BANK = "FE"
HEADER_BANK = "FF"
OBJECTIVE_BANK_INT = (int(OBJECTIVE_BANK, 16) << 16) - 0xC00000
NAME_BANK_INT = (int(NAME_BANK, 16) << 16) - 0xC00000
HEADER_BANK_INT = (int(HEADER_BANK, 16) << 16) - 0xC00000

OBJECTIVE_HEADER_LENGTH = 31
OBJECTIVE_NAME_LENGTH = 31
CONDITION_NAME_LENGTH = 31

class ObjectiveMetadataWriter:
    def __init__(self):
        from constants.objectives.conditions import types as condition_types
        from constants.objectives.results import types as result_types, category_types

        self.objectives = [ObjectiveMetadata(result_type) for result_type in result_types]
        self.conditions = [ObjectiveConditionMetadata(condition_type) for condition_type in condition_types]

    def write(self):
        import args
        import json
        meta = {
            'conditions': [],
            'objectives': [],
        }
        for index in range(0, len(self.objectives)):
            objective = self.objectives[index]
            meta['objectives'].append(objective.to_json())

        for index in range(0, len(self.conditions)):
            condition = self.conditions[index]
            meta['conditions'].append(condition.to_json())

        file_name = f"{args.output_file}-objective.json"
        with open(file_name, "w") as out_file:
            out_file.write(json.dumps(meta, indent = 4))

    def __len__(self):
        return len(self.objectives)

    def __getitem__(self, index):
        return self.objectives[index]

