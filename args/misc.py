def name():
    return "Misc."

def parse(parser):
    misc = parser.add_argument_group("Misc.")
    misc.add_argument("-as", "--auto-sprint", action = "store_true",
                      help = "Player always sprints. Sprint Shoes have no effect")
    misc.add_argument("-ond", "--original-name-display", action = "store_true",
                      help = "Display original character names in party and party select menus")
    misc.add_argument("-rr", "--random-rng", action = "store_true",
                      help = "Randomize in-game RNG table. Affects Setzer's Slots, Auction House, Ebot's Rock, ...")
    misc.add_argument("-rc", "--random-clock", action = "store_true",
                      help = "Randomize clock's correct time and NPC clues in Zozo")
    misc.add_argument("-scan", "--scan-all", action = "store_true",
                      help = "All enemies scannable. All characters start with scan learned. Scan costs 0 MP. Useful for testing/debugging")

    event_timers = misc.add_mutually_exclusive_group()
    event_timers.add_argument("-etr", "--event-timers-random", action = "store_true",
                              help = "Collapsing House, Opera House, and Floating Continent timers randomized")
    event_timers.add_argument("-etn", "--event-timers-none", action = "store_true",
                              help = "Collapsing House, Opera House, and Floating Continent timers removed")

    y_npc = misc.add_mutually_exclusive_group()
    y_npc.add_argument("-ymascot", "--y-npc-mascot", action = "store_true",
                       help = "Transform NPC into random mascot")
    y_npc.add_argument("-ycreature", "--y-npc-creature", action = "store_true",
                       help = "Transform NPC into random creature")
    y_npc.add_argument("-yimperial", "--y-npc-imperial", action = "store_true",
                       help = "Transform NPC into random imperial unit")
    y_npc.add_argument("-ymain", "--y-npc-main", action = "store_true",
                       help = "Transform NPC into random main character")
    y_npc.add_argument("-yreflect", "--y-npc-reflect", action = "store_true",
                       help = "Transform NPC into current character")
    y_npc.add_argument("-ystone", "--y-npc-stone", action = "store_true",
                       help = "Turn NPC to stone")
    y_npc.add_argument("-yvxz", "--y-npc-vanish-xzone", action = "store_true",
                       help = "Cast vanish and x-zone on NPC")
    y_npc.add_argument("-ysketch", "--y-npc-sketch", action = "store_true",
                       help = "Sketch NPC")
    y_npc.add_argument("-yrandom", "--y-npc-random", action = "store_true",
                       help = "Transform NPC randomly")
    y_npc.add_argument("-yremove", "--y-npc-remove", action = "store_true",
                       help = "Remove NPC")
    parser.y_npc_group = y_npc

    remove_flashes = misc.add_mutually_exclusive_group()
    remove_flashes.add_argument("-frw", "--flashes-remove-worst", action = "store_true",
                              help = "Removes only the worst flashes from animations. Ex: Learning Bum Rush, Bum Rush, Quadra Slam/Slice, Flash, etc.")
    remove_flashes.add_argument("-frm", "--flashes-remove-most", action = "store_true",
                              help = "Removes most flashes from animations. Includes Kefka Death.")

def process(args):
    args.y_npc = False # are any y_npc flags enabled?

    group = args.parser.y_npc_group
    for action in group._group_actions:
        if getattr(args, action.dest):
            args.y_npc = True
            break

def flags(args):
    flags = ""

    if args.auto_sprint:
        flags += " -as"
    if args.original_name_display:
        flags += " -ond"
    if args.random_rng:
        flags += " -rr"
    if args.random_clock:
        flags += " -rc"
    if args.scan_all:
        flags += " -scan"

    if args.event_timers_random:
        flags += " -etr"
    elif args.event_timers_none:
        flags += " -etn"

    if args.y_npc_mascot:
        flags += " -ymascot"
    elif args.y_npc_creature:
        flags += " -ycreature"
    elif args.y_npc_imperial:
        flags += " -yimperial"
    elif args.y_npc_main:
        flags += " -ymain"
    elif args.y_npc_reflect:
        flags += " -yreflect"
    elif args.y_npc_stone:
        flags += " -ystone"
    elif args.y_npc_vanish_xzone:
        flags += " -yvxz"
    elif args.y_npc_sketch:
        flags += " -ysketch"
    elif args.y_npc_random:
        flags += " -yrandom"
    elif args.y_npc_remove:
        flags += " -yremove"

    if args.flashes_remove_worst:
        flags += " -frw"
    if args.flashes_remove_most:
        flags += " -frm"

    return flags

def options(args):
    event_timers = "Original"
    if args.event_timers_random:
        event_timers = "Random"
    elif args.event_timers_none:
        event_timers = "None"

    y_npc = "None"
    if args.y_npc_mascot:
        y_npc = "Mascot"
    elif args.y_npc_creature:
        y_npc = "Creature"
    elif args.y_npc_imperial:
        y_npc = "Imperial"
    elif args.y_npc_main:
        y_npc = "Main Character"
    elif args.y_npc_reflect:
        y_npc = "Reflect"
    elif args.y_npc_stone:
        y_npc = "Stone"
    elif args.y_npc_vanish_xzone:
        y_npc = "Vanish/X-Zone"
    elif args.y_npc_sketch:
        y_npc = "Sketch"
    elif args.y_npc_random:
        y_npc = "Random"
    elif args.y_npc_remove:
        y_npc = "Remove"

    remove_flashes = "Original"
    if args.flashes_remove_worst:
        remove_flashes = "Worst"
    elif args.flashes_remove_most:
        remove_flashes = "Most"

    return [
        ("Auto Sprint", args.auto_sprint),
        ("Original Name Display", args.original_name_display),
        ("Random RNG", args.random_rng),
        ("Random Clock", args.random_clock),
        ("Scan All", args.scan_all),
        ("Event Timers", event_timers),
        ("Y NPC", y_npc),
        ("Remove Flashes", remove_flashes)
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
