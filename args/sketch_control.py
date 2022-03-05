def name():
    return "Sketch/Control"

def parse(parser):
    sketch_control = parser.add_argument_group("Sketch/Control")

    sketch_control.add_argument("-scca", "--sketch-control-chances-always", action = "store_true",
                         help = "Sketch & Control will always succeed if target is valid")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.sketch_control_chances_always:
        flags += " -scca"

    return flags

def options(args):

    return [
        ("Chances Always", args.sketch_control_chances_always),
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
