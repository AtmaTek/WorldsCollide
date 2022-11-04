
def name():
    return "Check Rewards"

def parse(parser):
    advanced_checks = parser.add_argument_group("Check Rewards")

    advanced_checks.add_argument("-nfce", "--no-free-characters-espers", action = "store_true",
                help = "Remove character/esper rewards from: Auction House, Collapsing House, Figaro Castle Throne, Gau's Father's House, Kohlingen Inn, Mt. Zozo, Narshe Weapon Shop, Sealed Gate, South Figaro Basement, Tzen Thief, Zone Eater")

    advanced_checks.add_argument("-fcrr", "--force-character-rewards", type = str,
                help = "Forces list of checks to give an CHARACTER reward")

    advanced_checks.add_argument("-firr", "--force-item-rewards", type = str,
                help = "Forces list of checks to give an ITEM reward")

    advanced_checks.add_argument("-ferr", "--force-esper-rewards", type = str,
                help = "Forces list of checks to give an ESPER reward")

    advanced_checks.add_argument("-feirr", "--force-esper-item-rewards", type = str,
                help = "Forces list of checks to give an (ESPER | ITEM) reward")

    advanced_checks.add_argument("-dchar", "--dragons-as-characters", default = [0, 0], type = int,
                nargs = 2, metavar = ("MIN", "MAX"), choices = range(6),
                help = "Up to 5 dragons will reward characters. The dragon will have the recruited character's sprite. Kefka's Tower and Phoenix Cave dragons cannot be characters.")

character_title = "Character Checks"
esper_item_title = "Esper+Item Checks"
esper_title = "Esper Checks"
item_title = "Item Checks"

def process(args):
    from constants.checks import (
        AUCTION1, AUCTION2, COLLAPSING_HOUSE, FIGARO_CASTLE_THRONE,
        GAUS_FATHERS_HOUSE,KOHLINGEN_CAFE, MT_ZOZO, NARSHE_WEAPON_SHOP,
        SEALED_GATE, SOUTH_FIGARO_PRISONER, TZEN_THIEF, ZONE_EATER
    )
    args.character_rewards = []
    args.esper_item_rewards = []
    args.esper_rewards = []
    args.item_rewards = []

    args._process_min_max("dragons_as_characters")

    if args.force_character_rewards:
        args.character_rewards =  [int(check) for check in args.force_character_rewards.split(',')]

    if args.force_esper_item_rewards:
        args.esper_item_rewards =  [int(check) for check in args.force_esper_item_rewards.split(',')]

    if args.force_esper_rewards:
        args.esper_rewards =  [int(check) for check in args.force_esper_rewards.split(',')]

    if args.force_item_rewards:
        args.item_rewards =  [int(check) for check in args.force_item_rewards.split(',')]
    elif args.no_free_characters_espers:
        args.item_rewards = [
            AUCTION1.bit,
            AUCTION2.bit,
            COLLAPSING_HOUSE.bit,
            FIGARO_CASTLE_THRONE.bit,
            GAUS_FATHERS_HOUSE.bit,
            KOHLINGEN_CAFE.bit,
            MT_ZOZO.bit,
            NARSHE_WEAPON_SHOP.bit,
            SEALED_GATE.bit,
            SOUTH_FIGARO_PRISONER.bit,
            TZEN_THIEF.bit,
            ZONE_EATER.bit,
        ]

def flags(args):
    flags = ""

    if args.force_character_rewards:
        flags += f" -fcrr {args.force_character_rewards}"

    if args.force_esper_item_rewards:
        flags += f" -feirr {args.force_esper_item_rewards}"

    if args.force_esper_rewards:
        flags += f" -ferr {args.force_esper_rewards}"

    if args.force_item_rewards:
        flags += f" -firr {args.force_item_rewards}"

    if args.dragons_as_characters_min != 0 or args.dragons_as_characters_max != 0:
        flags += f" -dchar {args.dragons_as_characters_min} {args.dragons_as_characters_max}"

    return flags

def options(args):
    options = []
    if args.dragons_as_characters:
        options.append(('Dragon Characters', f"{args.dragons_as_characters_min}-${args.dragons_as_characters_max}"))
    if args.character_rewards:
        options.append((character_title, args.character_rewards))
    if args.esper_item_rewards:
        options.append((esper_item_title, args.esper_item_rewards))
    if args.esper_rewards:
        options.append((esper_title, args.esper_rewards))
    if args.item_rewards:
        options.append((item_title, args.item_rewards))
    return options

def _format_check_log_entries(check_ids):
    from constants.checks import check_name
    check_entries = []
    for check_id in check_ids:
        check_entries.append(("", check_name[check_id]))
    return check_entries

def menu(args):
    from menus.submenu_force_item_reward_checks import FlagsForceCharacterRewardChecks, FlagsForceEsperItemRewardChecks, FlagsForceEsperRewardChecks, FlagsForceItemRewardChecks

    entries = options(args)
    for index, entry in enumerate(entries):
        key, value = entry
        if key == character_title:
            if value:
                entries[index] = (character_title, FlagsForceCharacterRewardChecks(character_title, value, False)) # flags sub-menu
            else:
                 entries[index] = (character_title, "None")

        if key == esper_item_title:
            if value:
                entries[index] = (esper_item_title, FlagsForceEsperItemRewardChecks(esper_item_title, value, False)) # flags sub-menu
            else:
                 entries[index] = (esper_item_title, "None")

        if key == esper_title:
            if value:
                entries[index] = (esper_title, FlagsForceEsperRewardChecks(esper_title, value, False)) # flags sub-menu
            else:
                 entries[index] = (esper_title, "None")

        if key == item_title:
            if value:
                entries[index] = (item_title, FlagsForceItemRewardChecks(item_title, value, args.no_free_characters_espers)) # flags sub-menu
            else:
                 entries[index] = (item_title, "None")

    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        key, value = entry
        if key == esper_item_title or key == esper_title or key == item_title:
            if len(value) == 0:
                entry = (key, "None")
            else:
                entry = (key, "") # The entries will show up on subsequent lines
            log.append(format_option(*entry))
            for check_entry in _format_check_log_entries(value):
                log.append(format_option(*check_entry))
        else:
            log.append(format_option(*entry))

    return log
