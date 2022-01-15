def name():
    return "Steal"

def parse(parser):
    steal = parser.add_argument_group("Steal")

    steal.add_argument("-hsr", "--higher-steal-rate", action = "store_true",
                         help = "Steal Rate is improved")

    steal.add_argument("-mrs", "--more-rare-steals", action = "store_true",
                         help = "Steals of rare items are more likely")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.higher_steal_rate:
        flags += " -hsr"
    if args.more_rare_steals:
        flags += " -mrs"

    return flags

def options(args):
    return [
        ("Higher Steal Rate", args.higher_steal_rate),
        ("More Rare Steals", args.more_rare_steals),
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
