def name():
    return "Steal"

def parse(parser):
    steal = parser.add_argument_group("Steal")

    steal_chances = steal.add_mutually_exclusive_group()
    steal_chances.add_argument("-sch", "--steal-chances-higher", action = "store_true",
                         help = "Steal Rate is improved and rare steals are more likely")
    steal_chances.add_argument("-sca", "--steal-chances-always", action = "store_true",
                         help = "Steal will always succeed if enemy has an item")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.steal_chances_higher:
        flags += " -sch"
    if args.steal_chances_always:
        flags += " -sca"

    return flags

def options(args):
    steal_chances = "Original"
    if args.steal_chances_higher:
        steal_chances = "Higher"
    if args.steal_chances_always:
        steal_chances = "Always"

    return [
        ("Chances", steal_chances),
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
