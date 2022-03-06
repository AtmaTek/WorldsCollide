def name():
    return "Sketch/Control"

def parse(parser):
    sketch_control = parser.add_argument_group("Sketch/Control")

    sketch_control.add_argument("-scis", "--sketch-control-improved-stats", action = "store_true",
                         help = "Sketch & Control 100%% accurate and Sketch uses caster's stats")
    sketch_control.add_argument("-sia", "--sketch-improved-abilities", action = "store_true",
                         help = "Improves Sketch abilities by removing Battle. Adds Rage as a Sketch possibility for most monsters. Gives Sketch abilities to most bosses.")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.sketch_control_improved_stats:
        flags += " -scis"
    if args.sketch_improved_abilities:
        flags += " -sia"

    return flags

def options(args):

    return [
        ("Improved Stats", args.sketch_control_improved_stats),
        ("Buff Sketch Abilities", args.sketch_improved_abilities),
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
