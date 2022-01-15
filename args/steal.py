def name():
    return "Steal"

def parse(parser):
    steal = parser.add_argument_group("Steal")

    steal.add_argument("-bs", "--better-steal", action = "store_true",
                         help = "Steal Rate is improved and rare steals are more likely")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.better_steal:
        flags += " -bs"

    return flags

def options(args):
    return [
        ("Better Steal", args.better_steal),
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
