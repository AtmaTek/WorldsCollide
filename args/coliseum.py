def name():
    return "Coliseum"

def parse(parser):
    from constants.items import ITEM_COUNT

    coliseum = parser.add_argument_group("Coliseum")

    coliseum_opponents = coliseum.add_mutually_exclusive_group()
    coliseum_opponents.add_argument("-cos", "--coliseum-opponents-shuffle", action = "store_true",
                                     help = "Coliseum opponents shuffled")
    coliseum_opponents.add_argument("-cor", "--coliseum-opponents-random", action = "store_true",
                                     help = "Coliseum opponents randomized")

    coliseum_rewards = coliseum.add_mutually_exclusive_group()
    coliseum_rewards.add_argument("-crs", "--coliseum-rewards-shuffle", action = "store_true",
                                   help = "Coliseum rewards shuffled")
    coliseum_rewards.add_argument("-crr", "--coliseum-rewards-random", action = "store_true",
                                   help = "Coliseum rewards randomized")

    coliseum.add_argument("-crvr", "--coliseum-rewards-visible-random", default = None, type = int,
                          nargs = 2, metavar = ("MIN", "MAX"), choices = range(ITEM_COUNT),
                          help = "Random number of rewards within given range visible before beginning the match. Remaining rewards will display as question marks")
    coliseum.add_argument("-crm", "--coliseum-rewards-menu", action = "store_true",
                          help = "Display rewards in item selection menu. Hidden rewards will display as question marks")

    coliseum.add_argument("-cnee", "--coliseum-no-exp-eggs", action = "store_true",
                       help = "Exp. Eggs will not appear in coliseum")
    coliseum.add_argument("-cnil", "--coliseum-no-illuminas", action = "store_true",
                       help = "Illuminas will not appear in coliseum")

def process(args):
    args._process_min_max("coliseum_rewards_visible_random")

def flags(args):
    flags = ""

    if args.coliseum_opponents_shuffle:
        flags += " -cos"
    elif args.coliseum_opponents_random:
        flags += " -cor"

    if args.coliseum_rewards_shuffle:
        flags += " -crs"
    elif args.coliseum_rewards_random:
        flags += " -crr"

    if args.coliseum_rewards_visible_random:
        flags += f" -crvr {args.coliseum_rewards_visible_random_min} {args.coliseum_rewards_visible_random_max}"

    if args.coliseum_rewards_menu:
        flags += " -crm"

    if args.coliseum_no_exp_eggs:
        flags += " -cnee"
    if args.coliseum_no_illuminas:
        flags += " -cnil"

    return flags

def options(args):
    result = []

    opponents = "Original"
    if args.coliseum_opponents_shuffle:
        opponents = "Shuffle"
    elif args.coliseum_opponents_random:
        opponents = "Random"

    rewards = "Original"
    if args.coliseum_rewards_shuffle:
        rewards = "Shuffle"
    elif args.coliseum_rewards_random:
        rewards = "Random"

    rewards_visible = "Original"
    if args.coliseum_rewards_visible_random:
        rewards_visible = f"{args.coliseum_rewards_visible_random_min}-{args.coliseum_rewards_visible_random_max}"

    return [
        ("Opponents", opponents),
        ("Rewards", rewards),
        ("Rewards Visible", rewards_visible),
        ("Rewards Menu", args.coliseum_rewards_menu),
        ("No Exp. Eggs", args.coliseum_no_exp_eggs),
        ("No Illuminas", args.coliseum_no_illuminas),
    ]

def menu(args):
    return (name(), options(args))

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
