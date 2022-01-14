import args

from objectives.results import results
from objectives.conditions import conditions
from objectives.objective import Objective

from objectives.result_dict import ResultDict

class Objectives:
    results = ResultDict()

    def __init__(self):
        self.objectives = []
        for index in range(len(args.objectives)):
            objective = Objective(index)
            self.objectives.append(objective)

            if objective.result.NAME in Objectives.results:
                Objectives.results[objective.result.NAME].append(objective)
            else:
                Objectives.results[objective.result.NAME] = [objective]

    def __len__(self):
        return len(self.objectives)

    def __getitem__(self, index):
        return self.objectives[index]
