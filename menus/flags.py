from memory.space import START_ADDRESS_SNES, Bank, Reserve, Allocate, Write
import instruction.asm as asm
import instruction.f0 as f0
import args

import menus.pregame_track_scroll_area as scroll_area

class Flags(scroll_area.ScrollArea):
    MENU_NUMBER = 12

    def __init__(self):
        self.lines = []
        for _, group in args.group_modules.items():
            if hasattr(group, "menu"):
                name, options = group.menu(args)

                self.lines.append(scroll_area.Line(name, f0.set_blue_text_color))
                for option in options:
                    key, value = option

                    key = "  " + key.replace("&", "+")
                    value = str(value)
                    if value == "True":
                        value = "T"
                    elif value == "False":
                        value = "F"

                    padding = scroll_area.WIDTH - (len(key) + len(value))
                    self.lines.append(scroll_area.Line(f"{key}{' ' * padding}{value}", f0.set_user_text_color))

                self.lines.append(scroll_area.Line("", f0.set_user_text_color))
        del self.lines[-1] # exclude final empty line

        super().__init__()
