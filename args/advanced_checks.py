
def name():
    return "Advanced Checks"

def parse(parser):
    advanced_checks = parser.add_argument_group("Checks")
    nfce = advanced_checks.add_mutually_exclusive_group()
    nfce.name = "Advanced Checks"
    nfce.name = "No Free Character/Esper Checks"
    nfce.add_argument("-nfce", "--no-free-characters-espers", action = "store_true",
                help = "Remove character/esper rewards from: Auction House, Collapsing House, Figaro Castle Throne, Gau's Father's House, Kohlingen Inn, Narshe Weapon Shop, Sealed Gate, South Figaro Basement")

    nfce.add_argument("-fir", "--force-item-reward-checks", type = str,
                help = "Forces list of checks to give an item reward. Maximum of 9 checks.")

def process(args):
    from constants.checks import (
        character_esper_check_name,
        AUCTION1, AUCTION2, COLLAPSING_HOUSE, FIGARO_CASTLE_THRONE, GAUS_FATHERS_HOUSE,
        KOHLINGEN_CAFE, NARSHE_WEAPON_SHOP, SEALED_GATE, SOUTH_FIGARO_PRISONER,

        LONE_WOLF_MOOGLE_ROOM,
        FANATICS_TOWER_LEADER,
        NARSHE_WEAPON_SHOP_MINES
    )

    if args.force_item_reward_checks:
        args.item_reward_checks =  [int(check) for check in args.force_item_reward_checks.split(',')]
    elif args.no_free_characters_espers:
        args.item_reward_checks = [
            AUCTION1.bit,
            AUCTION2.bit,
            COLLAPSING_HOUSE.bit,
            FIGARO_CASTLE_THRONE.bit,
            GAUS_FATHERS_HOUSE.bit,
            KOHLINGEN_CAFE.bit,
            NARSHE_WEAPON_SHOP.bit,
            SEALED_GATE.bit,
            SOUTH_FIGARO_PRISONER.bit,
        ]
    else:
        # legacy behavior
        args.item_reward_checks = [
            FANATICS_TOWER_LEADER,
            LONE_WOLF_MOOGLE_ROOM,
            NARSHE_WEAPON_SHOP_MINES,
        ]
    # max amount (can probably calculate this somehow)
    assert len(args.item_reward_checks) < 10

def flags(args):
    flags = ""

    if args.force_item_reward_checks:
        flags += f" -fir {args.force_item_reward_checks}"

    return flags

def options(args):
    return [
        ("Forced Item Checks", args.item_reward_checks),
    ]

def _format_check_log_entries(spell_ids):
    from constants.checks import all_checks_check_name
    spell_entries = []
    for spell_id in spell_ids:
        spell_entries.append(("", all_checks_check_name[spell_id]))
    return spell_entries

def menu(args):
    from menus.submenu_force_item_reward_checks import FlagsForceItemRewardChecks

    entries = options(args)
    for index, entry in enumerate(entries):
        key, value = entry

        if key == "Forced Item Checks" and value:
            entries[index] = ("Forced Item Checks", FlagsForceItemRewardChecks(value)) # flags sub-menu
        elif key == "Forced Item Checks":
            entries[index] = ("Forced Item Checks", "None") # flags sub-menu

    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        key, value = entry
        if key == "Forced Item Checks":
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
