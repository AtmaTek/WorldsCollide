def name():
    return "Sketch/Control"

def parse(parser):
    sketch_control = parser.add_argument_group("Sketch/Control")

    sketch_control.add_argument("-isc", "--improve-sketch-control", action = "store_true",
                         help = "Sketch & Control 100%% accurate, Sketch uses caster's stats, and both have more useful commands")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.improve_sketch_control:
        flags += " -isc"

    return flags

def options(args):

    return [
        ("Improve", args.improve_sketch_control),
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
