def name():
    return "Enemies"

def parse(parser):
    enemies = parser.add_argument_group("Enemies")
    enemies.add_argument("-eosrp", "--enemy-offense-stat-random-percent", default = [100, 100], type = int,
                            nargs = 2, metavar = ("MIN", "MAX"), choices = range(401),
                            help = "Each enemy MPwr & BPwr set to random percent of original (or normalized/distorted) within given range ")
    enemies.add_argument("-edsrp", "--enemy-defense-stat-random-percent", default = [100, 100], type = int,
                            nargs = 2, metavar = ("MIN", "MAX"), choices = range(201),
                            help = "Each enemy's MDef and Def stat set to random percent of original (or normalized/distorted) within given range ")
    enemies.add_argument("-essrp", "--enemy-speed-stat-random-percent", default = [100, 100], type = int,
                            nargs = 2, metavar = ("MIN", "MAX"), choices = range(201),
                            help = "Each enemy's Speed stat set to random percent of original (or normalized/distorted) within given range ")


def process(args):
    args._process_min_max("enemy_offense_stat_random_percent")
    args._process_min_max("enemy_defense_stat_random_percent")
    args._process_min_max("enemy_speed_stat_random_percent")

def flags(args):
    flags = ""

    if args.enemy_offense_stat_random_percent_min != 100 or args.enemy_offense_stat_random_percent_max != 100:
        flags += f" -eosrp {args.enemy_offense_stat_random_percent_min} {args.enemy_offense_stat_random_percent_max}"
    if args.enemy_defense_stat_random_percent_min != 100 or args.enemy_defense_stat_random_percent_max != 100:
        flags += f" -edsrp {args.enemy_defense_stat_random_percent_min} {args.enemy_defense_stat_random_percent_max}"
    if args.enemy_speed_stat_random_percent_min != 100 or args.enemy_speed_stat_random_percent_max != 100:
        flags += f" -essrp {args.enemy_speed_stat_random_percent_min} {args.enemy_speed_stat_random_percent_max}"

    return flags

def options(args):
    enemy_offense_stats = f"{args.enemy_offense_stat_random_percent_min}-{args.enemy_offense_stat_random_percent_max}%"
    enemy_defense_stats = f"{args.enemy_defense_stat_random_percent_min}-{args.enemy_defense_stat_random_percent_max}%"
    enemy_speed_stats = f"{args.enemy_speed_stat_random_percent_min}-{args.enemy_speed_stat_random_percent_max}%"

    return [
        ("Enemy Offense", enemy_offense_stats),
        ("Enemy Defense", enemy_defense_stats),
        ("Enemy Speed", enemy_speed_stats),
    ]

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
