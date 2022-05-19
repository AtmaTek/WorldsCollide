
def name():
    return "Checks"

def parse(parser):
    advanced_checks = parser.add_argument_group("Checks")
    check_rewards = advanced_checks.add_mutually_exclusive_group()
    check_rewards.name = "Check Rewards"
    check_rewards.add_argument("-nfce", "--no-free-characters-espers", action = "store_true",
                help = "Remove character/esper rewards from: Auction House, Collapsing House, Figaro Castle Throne, Gau's Father's House, Kohlingen Inn, Mt. Zozo, Narshe Weapon Shop, Sealed Gate, South Figaro Basement, Tzen Thief, Zone Eater")

    check_rewards.add_argument("-fir", "--force-item-reward-checks", type = str,
                help = "Forces list of checks to give an item reward. Maximum of 12 checks.")

    check_rewards.add_argument("-fir", "--force-esper-reward-checks", type = str,
                help = "Forces list of checks to give an esper reward. Maximum of 27 checks")

def process(args):
    from constants.checks import (
        AUCTION1, AUCTION2, COLLAPSING_HOUSE, FIGARO_CASTLE_THRONE,
        GAUS_FATHERS_HOUSE,KOHLINGEN_CAFE, MT_ZOZO, NARSHE_WEAPON_SHOP,
        SEALED_GATE, SOUTH_FIGARO_PRISONER, TZEN_THIEF, ZONE_EATER
    )

    if args.force_item_reward_checks == 'none':
        args.item_reward_checks = []
    elif args.force_item_reward_checks:
        args.item_reward_checks =  [int(check) for check in args.force_item_reward_checks.split(',')]
    elif args.no_free_characters_espers:
        args.item_reward_checks = [
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

    # assert that no items in item_reward_checks is CHAR | ESPER only reward
    assert len(args.item_reward_checks) < 13

def flags(args):
    flags = ""

    if args.force_item_reward_checks:
        flags += f" -fir {args.force_item_reward_checks}"

    return flags

def options(args):
    return [
        ("Forced Item Checks", args.item_reward_checks),
    ]

def _format_check_log_entries(check_ids):
    from constants.checks import check_name
    check_entries = []
    for check_id in check_ids:
        check_entries.append(("", check_name[check_id]))
    return check_entries

def menu(args):
    from menus.submenu_force_item_reward_checks import FlagsForceItemRewardChecks

    entries = options(args)
    for index, entry in enumerate(entries):
        key, value = entry
        if key == "Forced Item Checks":
            if value:
                entries[index] = ("Forced Item Checks", FlagsForceItemRewardChecks(value, args.no_free_characters_espers)) # flags sub-menu
            else:
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
