from objectives.results._objective_result import *
from data.item_names import name_id as item_name_id

RODS = ["Heal Rod", "Fire Rod", "Ice Rod", "Thunder Rod", "Poison Rod", "Pearl Rod", "Gravity Rod"]
ROD_IDS = [item_name_id[item_name] for item_name in RODS]

class Field(field_result.Result):
    def src(self):
        src = []
        for item_id in ROD_IDS:
            src += [
                field.AddItem(item_id),
            ]
        return src

class Battle(battle_result.Result):
    def src(self):
        src = []
        for item_id in ROD_IDS:
            src += [
                battle_result.AddItem(item_id),
            ]
        return src

class Result(ObjectiveResult):
    NAME = "Breakable Rods"
    def __init__(self):
        super().__init__(Field, Battle)
