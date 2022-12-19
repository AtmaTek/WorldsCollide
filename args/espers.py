from data.espers import Espers
from event.event_reward import CHARACTER_ESPER_ONLY_REWARDS

# If all 27 espers are allocated at start, there will be logic errors when it comes to
# assigning characters to character/esper only checks.
# We would have to ensure that a character is assigned to the {6} char/esper only rewards.
# We could account for this in the logic, but it would gentrify the routing logic a bit much.
MAX_STARTING_ESPERS = Espers.ESPER_COUNT - CHARACTER_ESPER_ONLY_REWARDS

def name():
    return "Espers"

def parse(parser):
    from data.esper import Esper
    from data.characters import Characters
    espers = parser.add_argument_group("Espers")

    esper_start = espers.add_mutually_exclusive_group()
    esper_start.add_argument("-stesp", "--starting-espers", default = [0, 0], type = int,
                                nargs = 2, metavar = ("MIN", "MAX"), choices = range(MAX_STARTING_ESPERS + 1),
                                help = "Party starts with %(metavar) random espers")

    esper_spells = espers.add_mutually_exclusive_group()

    esper_spells.add_argument("-esrr", "--esper-spells-random-rates", action = "store_true",
                              help = "Original esper spells with random learn rates")
    esper_spells.add_argument("-ess", "--esper-spells-shuffle", action = "store_true",
                              help = "Esper spells shuffled with original learn rates")
    esper_spells.add_argument("-essrr", "--esper-spells-shuffle-random-rates", action = "store_true",
                              help = "Esper spells shuffled with random learn rates")
    esper_spells.add_argument("-esr", "--esper-spells-random", default = None, type = int,
                              nargs = 2, metavar = ("MIN", "MAX"), choices = range(Esper.SPELL_COUNT + 1),
                              help = "Esper spells and learn rates randomized")
    esper_spells.add_argument("-esrt", "--esper-spells-random-tiered", action = "store_true",
                              help = "Esper spells and learn rates randomized by tier")

    esper_bonuses = espers.add_mutually_exclusive_group()
    esper_bonuses.add_argument("-ebs", "--esper-bonuses-shuffle", action = "store_true",
                               help = "Esper bonuses shuffled")
    esper_bonuses.add_argument("-ebr", "--esper-bonuses-random",
                               default = None, type = int, metavar = "PERCENT", choices = range(101),
                               help = "Esper bonuses randomized")

    esper_mp = espers.add_mutually_exclusive_group()
    esper_mp.add_argument("-emps", "--esper-mp-shuffle", action = "store_true",
                          help = "Esper MP costs shuffled")
    esper_mp.add_argument("-emprv", "--esper-mp-random-value", default = None, type = int,
                          nargs = 2, metavar = ("MIN", "MAX"), choices = range(255),
                          help = "Each esper's MP cost set to random value within given range")
    esper_mp.add_argument("-emprp", "--esper-mp-random-percent", default = None, type = int,
                          nargs = 2, metavar = ("MIN", "MAX"), choices = range(201),
                          help = "Each esper's MP cost set to random percent of original within given range")

    esper_equipable = espers.add_mutually_exclusive_group()
    esper_equipable.add_argument("-eer", "--esper-equipable-random",
                                 default = None, type = int, nargs = 2, metavar = ("MIN", "MAX"),
                                 choices = range(Characters.CHARACTER_COUNT - 1), # exclude gogo/umaro
                                 help = "Each esper equipable by between %(metavar)s random characters")
    esper_equipable.add_argument("-eebr", "--esper-equipable-balanced-random",
                                 default = None, type = int, metavar = "VALUE",
                                 choices = range(Characters.CHARACTER_COUNT - 1), # exclude gogo/umaro
                                 help = "Each esper equipable by %(metavar)s random characters. Total number of espers equipable by each character is balanced")

    espers.add_argument("-ems", "--esper-multi-summon", action = "store_true",
                        help = "Espers can be summoned multiple times in battle")

def process(args):
    args._process_min_max("starting_espers")
    args._process_min_max("esper_spells_random")
    args._process_min_max("esper_mp_random_value")
    args._process_min_max("esper_mp_random_percent")
    args._process_min_max("esper_equipable_random")

    if args.esper_bonuses_random is not None:
        args.esper_bonuses_random_percent = args.esper_bonuses_random
        args.esper_bonuses_random = True

    if args.esper_equipable_balanced_random is not None:
        args.esper_equipable_balanced_random_value = args.esper_equipable_balanced_random
        args.esper_equipable_balanced_random = True

def flags(args):
    flags = ""

    if args.starting_espers_min or args.starting_espers_max:
        flags += f" -stesp {args.starting_espers_min} {args.starting_espers_max}"

    if args.esper_spells_random_rates:
        flags += " -esrr"
    elif args.esper_spells_shuffle:
        flags += " -ess"
    elif args.esper_spells_shuffle_random_rates:
        flags += " -essrr"
    elif args.esper_spells_random:
        flags += f" -esr {args.esper_spells_random_min} {args.esper_spells_random_max}"
    elif args.esper_spells_random_tiered:
        flags += " -esrt"

    if args.esper_bonuses_shuffle:
        flags += " -ebs"
    elif args.esper_bonuses_random:
        flags += f" -ebr {args.esper_bonuses_random_percent}"

    if args.esper_mp_shuffle:
        flags += " -emps"
    elif args.esper_mp_random_value:
        flags += f" -emprv {args.esper_mp_random_value_min} {args.esper_mp_random_value_max}"
    elif args.esper_mp_random_percent:
        flags += f" -emprp {args.esper_mp_random_percent_min} {args.esper_mp_random_percent_max}"

    if args.esper_equipable_random:
        flags += f" -eer {args.esper_equipable_random_min} {args.esper_equipable_random_max}"
    elif args.esper_equipable_balanced_random:
        flags += f" -eebr {args.esper_equipable_balanced_random_value}"

    if args.esper_multi_summon:
        flags += " -ems"

    return flags

def options(args):
    spells = "Original"
    if args.esper_spells_random_rates:
        spells = "Original (Random Rates)"
    elif args.esper_spells_shuffle:
        spells = "Shuffle"
    elif args.esper_spells_shuffle_random_rates:
        spells = "Shuffle (Random Rates)"
    elif args.esper_spells_random:
        spells = f"Random {args.esper_spells_random_min}-{args.esper_spells_random_max}"
    elif args.esper_spells_random_tiered:
        spells = "Random Tiered"

    bonuses = "Original"
    if args.esper_bonuses_shuffle:
        bonuses = "Shuffle"
    elif args.esper_bonuses_random:
        bonuses = "Random"

    mp = "Original"
    if args.esper_mp_shuffle:
        mp = "Shuffle"
    elif args.esper_mp_random_value:
        mp = f"Random Value {args.esper_mp_random_value_min}-{args.esper_mp_random_value_max}"
    elif args.esper_mp_random_percent:
        mp = f"Random Percent {args.esper_mp_random_percent_min}-{args.esper_mp_random_percent_max}%"

    equipable = "All"
    if args.esper_equipable_random:
        equipable = f"Random {args.esper_equipable_random_min}-{args.esper_equipable_random_max}"
    elif args.esper_equipable_balanced_random:
        equipable = f"Balanced Random {args.esper_equipable_balanced_random_value}"

    result = []
    result.append(("Starting Espers", f"{args.starting_espers_min}-{args.starting_espers_max}"))
    result.append(("Spells", spells))
    result.append(("Bonuses", bonuses))
    if args.esper_bonuses_random:
        result.append(("Bonus Chance", f"{args.esper_bonuses_random_percent}%"))
    result.append(("MP", mp))
    result.append(("Equipable", equipable))
    result.append(("Multi Summon", args.esper_multi_summon))
    return result

def menu(args):
    entries = options(args)
    for index, entry in enumerate(entries):
        key, value = entry
        try:
            value = value.replace("Original (Random Rates)", "Random Rates")
            value = value.replace("Shuffle (Random Rates)", "Shuffle R Rates")
            value = value.replace("Random Value", "")
            value = value.replace("Random Percent", "")
            value = value.replace("Balanced Random", "Balanced")
            if key == "Equipable":
                value = value.replace("Random", "")
            entries[index] = (key, value)
        except:
            pass
    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
