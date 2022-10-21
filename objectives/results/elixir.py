from objectives.results._objective_result import *
from data.item_names import name_id as item_name_id

class Field(field_result.Result):
    def src(self):
        return [
            field.AddItem(item_name_id["Elixir"]),
        ]

class Battle(battle_result.Result):
    def src(self):
        return [
            battle_result.AddItem(item_name_id["Elixir"]),
        ]

class Result(ObjectiveResult):
    NAME = "Elixir"
    def __init__(self):
        super().__init__(Field, Battle)
