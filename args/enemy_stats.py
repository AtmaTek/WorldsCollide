class EnemyStatArg:
    def __init__(self, name, short_arg, arg_min, arg_max, value_min, value_max, percent=True):
        # Name of the attribute -- should match the attr in data/enemy.py
        self.name = name

        # Short argument name
        self.short_arg = short_arg

        # Min/Max percent/delta for the argument
        self.arg_min = arg_min
        self.arg_max = arg_max

        # The hard min/max for the stat
        self.value_min = value_min 
        self.value_max = value_max

        # Whether the arg is a percent. If false, arg is treated as a value delta
        self.percent = percent

    def get_default(self):
        # Default is just a function of whether it's a percent or delta
        return 100 if self.percent else 0

    def _get_arg_value_type(self):
        return "percent" if self.percent else "delta"

    def get_dest_str(self):
        return f"enemy_{self.name}_random_{self._get_arg_value_type()}"

    def get_dest_attr(self, args):
        return getattr(args, self.get_dest_str())

    # helper method to get the long argument name associated with the arg_attr
    def get_long_arg(self):
        return self.get_dest_str().replace("_", "-")

    # helper methods to get the min/max attributes set by arguments._process_min_max
    def get_min_attr(self, args):
        return getattr(args, f"{self.get_dest_str()}_min")
    def get_max_attr(self, args):
        return getattr(args, f"{self.get_dest_str()}_max")

    def get_pretty_name(self):
        import string
        return string.capwords(self.name.replace("_", " "))

    def get_description(self):
        return f"Each enemy {self.get_pretty_name()} set to random {self._get_arg_value_type()} of original (or normalized/distorted) within given range."


#Enemy stat arguments
ENEMY_SPEED_ARG = EnemyStatArg("speed", "-esrp", 25, 201, 1, 128)
ENEMY_VIGOR_ARG = EnemyStatArg("vigor", "-evrp", 25, 401, 1, 255)
ENEMY_MPWR_ARG = EnemyStatArg("magic", "-emrp", 25, 201, 1, 128)
ENEMY_MDEF_ARG = EnemyStatArg("magic_defense", "-emdrp", 0, 151, 0, 255)
ENEMY_DEF_STAT_ARG = EnemyStatArg("defense", "-edrp", 0, 151, 0, 255)
ENEMY_ACC_STAT_ARG = EnemyStatArg("accuracy", "-eard", -100, 101, 1, 200, percent=False)
ENEMY_EVADE_STAT_ARG = EnemyStatArg("evasion", "-eerd", -250, 101, 0, 250, percent=False)
ENEMY_MEVADE_STAT_ARG = EnemyStatArg("magic_evasion", "-emerd", -250, 101, 0, 250, percent=False)
ENEMY_STAT_ARGS = [ENEMY_SPEED_ARG, ENEMY_VIGOR_ARG, ENEMY_MPWR_ARG, ENEMY_MDEF_ARG, ENEMY_DEF_STAT_ARG, ENEMY_ACC_STAT_ARG, ENEMY_EVADE_STAT_ARG, ENEMY_MEVADE_STAT_ARG]

def name():
    return "Enemy Stats"

def parse(parser):
    enemy_stats = parser.add_argument_group("Enemy Stats")

    for stat_arg in ENEMY_STAT_ARGS:
        enemy_stats.add_argument(stat_arg.short_arg, f"--{stat_arg.get_long_arg()}", default = [stat_arg.get_default(), stat_arg.get_default()], type = int,
                                nargs = 2, metavar = ("MIN", "MAX"), choices = range(stat_arg.arg_min, stat_arg.arg_max),
                                help = stat_arg.get_description())

def process(args):
    for stat_arg in ENEMY_STAT_ARGS:
        args._process_min_max(stat_arg.get_dest_str())

def flags(args):
    flags = ""

    for stat_arg in ENEMY_STAT_ARGS:
        if stat_arg.get_min_attr(args) != stat_arg.get_default() or stat_arg.get_max_attr(args) != stat_arg.get_default():
            flags += f" {stat_arg.short_arg} {stat_arg.get_min_attr(args)} {stat_arg.get_max_attr(args)}"

    return flags

def options(args):
    options = []
    for stat_arg in ENEMY_STAT_ARGS:
        options.append(
            (f"Enemy {stat_arg.get_pretty_name()}", f"{stat_arg.get_min_attr(args)}-{stat_arg.get_max_attr(args)}")
        )
    return options

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
