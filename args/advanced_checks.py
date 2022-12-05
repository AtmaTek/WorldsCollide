
from event.event_reward import RewardType


def name():
    return "Check Rewards"

def parse(parser):
    from constants.check_presets import preset_keys
    advanced_checks = parser.add_argument_group("Check Rewards")

    presets = advanced_checks.add_mutually_exclusive_group()
    presets.name = "Check Presets"

    presets.add_argument('-checks', "--check-preset", type = str,
                choices = preset_keys, help = "A preset used to modify certain checks to rewards characters, espers, or items.")

    presets.add_argument("-nfce", "--no-free-characters-espers", action = "store_true",
                help = "Remove character/esper rewards from: Auction House, Collapsing House, Figaro Castle Throne, Gau's Father's House, Kohlingen Inn, Mt. Zozo, Narshe Weapon Shop, Sealed Gate, South Figaro Basement, Tzen Thief, Zone Eater")

    advanced_checks.add_argument("-firr", "--force-item-rewards", type = str,
                help = "Forces list of checks to give an ITEM reward")

    advanced_checks.add_argument("-ferr", "--force-esper-rewards", type = str,
                help = "Forces list of checks to give an ESPER reward")

    advanced_checks.add_argument("-feirr", "--force-esper-item-rewards", type = str,
                help = "Forces list of checks to give an (ESPER | ITEM) reward")

    advanced_checks.add_argument("-fcrr", "--force-character-rewards", type = str,
                help = "Forces list of checks to give an CHARACTER reward")

    advanced_checks.add_argument("-dchar", "--dragons-as-characters", default = [0, 0], type = int,
                nargs = 2, metavar = ("MIN", "MAX"), choices = range(6),
                help = "Up to 5 dragons are guranteed to reward characters. The dragon will have the recruited character's sprite. Kefka's Tower and Phoenix Cave dragons cannot be characters.")

character_title = "Character Checks"
esper_item_title = "Esper+Item Checks"
esper_title = "Esper Checks"
item_title = "Item Checks"

def process(args):
    from constants.check_presets import key_preset, NO_FREE_CHARACTERS_ESPERS
    args.character_rewards = []
    args.esper_item_rewards = []
    args.esper_rewards = []
    args.item_rewards = []
    args._process_min_max("dragons_as_characters")

    if args.no_free_characters_espers:
        args.check_preset = NO_FREE_CHARACTERS_ESPERS.key

    if args.check_preset:
        check_preset = key_preset[args.check_preset]
        bits = [int(check.bit) for check in check_preset.locations]
        if check_preset.reward == RewardType.CHARACTER:
            args.character_rewards = bits
        if check_preset.reward == (RewardType.ESPER | RewardType.ITEM):
            args.esper_item_rewards = bits
        if check_preset.reward == RewardType.ESPER:
            args.esper_rewards = bits
        if check_preset.reward == RewardType.ITEM:
            args.item_rewards = bits
    else:
        if args.force_character_rewards:
            args.character_rewards =  [int(check) for check in args.force_character_rewards.split(',')]

        if args.force_esper_item_rewards:
            args.esper_item_rewards =  [int(check) for check in args.force_esper_item_rewards.split(',')]

        if args.force_esper_rewards:
            args.esper_rewards =  [int(check) for check in args.force_esper_rewards.split(',')]

        if args.force_item_rewards:
            args.item_rewards =  [int(check) for check in args.force_item_rewards.split(',')]


def flags(args):
    flags = ""

    if args.check_preset:
        flags += f" -checks {args.check_preset}"

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
    opts = {}
    if args.character_rewards:
        opts[character_title] = args.character_rewards
    if args.esper_item_rewards:
        opts[esper_item_title] = args.esper_item_rewards
    if args.esper_rewards:
        opts[esper_title] = args.esper_rewards
    if args.item_rewards:
        opts[item_title] = args.item_rewards

    if args.dragons_as_characters:
        opts['Dragon Characters'] = f"{args.dragons_as_characters_min}-{args.dragons_as_characters_max}"

    return [(key, value) for (key, value) in opts.items()]

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
                entries[index] = (character_title, FlagsForceCharacterRewardChecks(character_title, value, args.check_preset)) # flags sub-menu
            else:
                 entries[index] = (character_title, "None")

        if key == esper_item_title:
            if value:
                entries[index] = (esper_item_title, FlagsForceEsperItemRewardChecks(esper_item_title, value, args.check_preset)) # flags sub-menu
            else:
                 entries[index] = (esper_item_title, "None")

        if key == esper_title:
            if value:
                entries[index] = (esper_title, FlagsForceEsperRewardChecks(esper_title, value, args.check_preset)) # flags sub-menu
            else:
                 entries[index] = (esper_title, "None")

        if key == item_title:
            if value:
                entries[index] = (item_title, FlagsForceItemRewardChecks(item_title, value, args.check_preset)) # flags sub-menu
            else:
                 entries[index] = (item_title, "None")

    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        key, value = entry
        if key == character_title or key == esper_item_title or key == esper_title or key == item_title:
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
