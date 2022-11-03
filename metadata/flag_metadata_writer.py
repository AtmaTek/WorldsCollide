from argparse import _StoreTrueAction
import json

blacklisted_args = [
    'help',
    'input_file',
    'output_file',
    'seed_id',
    'debug',
    'no_rom_output',
    'stdout_log'
]

class Object:
    def toJSON(self):
        return self.__dict__

class FlagMetadataWriter:
    def __init__(self, args):
        self.groups = args.parser._action_groups
        self.mutually_exclusive_groups = args.parser._mutually_exclusive_groups
        self.metadata = {}

    def write(self):
        for group in self.groups:
            title = group.title
            description = group.description
            actions = group._group_actions
            group_title =  getattr(group, 'title', '')

            for action in actions:
                if action.dest in blacklisted_args:
                    continue
                for meg in self.mutually_exclusive_groups:
                    if action in (meg._group_actions or []):
                        action.mutually_exclusive_group_title = meg.title

                self.metadata[action.dest] = Object()
                self.metadata[action.dest].key = action.dest

                if isinstance(action, _StoreTrueAction):
                    self.metadata[action.dest].type = 'bool'
                else:
                    self.metadata[action.dest].type = action.type.__name__ if action.type else str.__name__

                self.metadata[action.dest].flag = action.option_strings[0]

                if action.default:
                    self.metadata[action.dest].default = action.default
                if action.help:
                    self.metadata[action.dest].description = action.help
                if action.nargs:
                    self.metadata[action.dest].nargs = action.nargs
                if action.metavar:
                    self.metadata[action.dest].args = action.metavar
                if action.choices is not None and isinstance(action.choices, list) and not isinstance(action.choices, range):
                    self.metadata[action.dest].allowed_values = list(action.choices)
                if type(group_title):
                    self.metadata[action.dest].group = group_title if type(group_title) == str else None if group_title == None else group_title()
                if getattr(action, 'mutually_exclusive_group_title', None) is not None:
                    self.metadata[action.dest].mutually_exclusive_group = action.mutually_exclusive_group_title
                if getattr(action, 'choices', None) is not None:
                    if isinstance(action.choices, range):
                        self.metadata[action.dest].options = {
                            'min_val': action.choices[0] if isinstance(action.choices, range) else None,
                            'max_val': action.choices[-1] if isinstance(action.choices, range) else None
                        }

            self.final_output = {key: value.toJSON() for key, value in self.metadata.items()}

            import args
            import json
            file_name = f"{args.output_file}-flag.json"
            with open(file_name, "w") as out_file:
                out_file.write(json.dumps(self.final_output, indent = 4))
