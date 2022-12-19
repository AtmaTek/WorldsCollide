from objectives.results._objective_result import *

class Field(field_result.Result):
    def src(self):
        return []

class Battle(battle_result.Result):
    def src(self):
        return []

class Result(ObjectiveResult):
    NAME = "Magitek Upgrade"
    def __init__(self):
        super().__init__(Field, Battle)
