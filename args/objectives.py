from constants.objectives import MAX_OBJECTIVES, MAX_CONDITIONS

def parse(parser):
    objectives = parser.add_argument_group("Objectives")
    for oi in range(MAX_OBJECTIVES):
        objectives.add_argument("-o" + chr(ord('a') + oi), "--objective_" + chr(ord('a') + oi),
                                type = str, help = "Objective " + chr(ord('A') + oi))

def process(args):
    from constants.objectives.results import types as result_types
    from constants.objectives.results import id_type as result_id_type
    from constants.objectives.conditions import types as condition_types

    class Result:
        def __init__(self, _id, name, format_string, value_range, args):
            self.id = _id
            self.name = name
            self.format_string = format_string
            self.value_range = value_range
            self.args = args

    class Condition:
        def __init__(self, name, string_function, value_range, min_max, args):
            self.name = name
            self.string_function = string_function
            self.value_range = value_range
            self.min_max = min_max
            self.args = args

    class Objective:
        def __init__(self, letter, result, conditions, conditions_required_min, conditions_required_max):
            self.letter = letter
            self.result = result
            self.conditions = conditions
            self.conditions_required_min = conditions_required_min
            self.conditions_required_max = conditions_required_max

    args.objectives = []
    args.final_kefka_objective = False
    for oi in range(MAX_OBJECTIVES):
        lower_letter = chr(ord('a') + oi)
        upper_letter = chr(ord('A') + oi)

        values = getattr(args, "objective_" + lower_letter)
        if values is not None:
            values = values.split('.')
            for vi in range(len(values)):
                try:
                    values[vi] = int(values[vi])
                except ValueError:
                    pass
            value_index = 0

            result_type = result_id_type[values[value_index]]
            value_index += 1

            if result_type.value_range is not None:
                result_arg_count = 2
            else:
                result_arg_count = 0
            result_args = values[value_index : value_index + result_arg_count]
            value_index += result_arg_count

            for arg in result_args:
                if arg not in result_type.value_range:
                    import sys
                    args.parser.print_usage()
                    print(f"{sys.argv[0]}: error: {result_type.name}: invalid argument {arg}")
                    sys.exit(1)

            result = Result(*result_type, result_args)

            conditions_required_min = values[value_index]
            value_index += 1
            conditions_required_max = values[value_index]
            value_index += 1

            conditions = []
            while value_index < len(values) and len(conditions) < MAX_CONDITIONS:
                condition_type = condition_types[values[value_index]]
                value_index += 1

                if condition_type.name == "None":
                    continue

                if condition_type.min_max:
                    condition_arg_count = 2
                else:
                    condition_arg_count = 1
                condition_args = values[value_index : value_index + condition_arg_count]
                value_index += condition_arg_count

                for arg in condition_args:
                    if arg not in condition_type.value_range:
                        import sys
                        args.parser.print_usage()
                        print(f"{sys.argv[0]}: error: {condition_type.name}: invalid argument {arg}")
                        sys.exit(1)

                condition = Condition(*condition_type, condition_args)
                conditions.append(condition)

            conditions_required_min = max(min(conditions_required_min, len(conditions)), 0)
            conditions_required_max = max(min(conditions_required_max, len(conditions)), 0)

            objective = Objective(upper_letter, result, conditions, conditions_required_min, conditions_required_max)
            args.objectives.append(objective)

def flags(args):
    flags = ""

    for oi in range(MAX_OBJECTIVES):
        lower_letter = chr(ord('a') + oi)

        values = getattr(args, "objective_" + lower_letter)
        if values is not None:
            flags += " -o" + lower_letter + " " + values

    return flags

def log(args):
    from log import format_option

    lentries = [[]]
    rentries = [[]]
    for oi, objective in enumerate(args.objectives):
        entry = []

        result = objective.letter + " " + objective.result.name
        if objective.result.name != "Random" and objective.result.format_string == "Random":
            result_args = "Random"
        else:
            result_args = '-'.join([str(arg) for arg in objective.result.args])
        entry.append(format_option(result, result_args))

        for condition in objective.conditions:
            if condition.min_max:
                condition_args = '-'.join([str(arg) for arg in condition.args])
            elif condition.name == "Random":
                condition_args = ""
            else:
                if condition.args[0] == 'r':
                    condition_args = "Random"
                else:
                    condition_args = condition.string_function(*condition.args)
            entry.append(format_option("  " + condition.name, condition_args))

        conditions_required_args = f"{objective.conditions_required_min}-{objective.conditions_required_max}"
        entry.append(format_option("Conditions Required", conditions_required_args))

        if oi % 2:
            rentries.append(entry)
        else:
            lentries.append(entry)

    from log import section_entries
    section_entries("Objectives", lentries, rentries)
