
import menus.pregame_track_scroll_area as scroll_area
from data.text.text2 import text_value
import instruction.f0 as f0
from constants.gates import character_checks

class FlagsForceRewardChecks(scroll_area.ScrollArea):

    def __init__(self, title, item_checks, check_preset):
        self.number_items = len(item_checks)
        self.lines = []

        self.lines.append(scroll_area.Line(title, f0.set_blue_text_color))

        if check_preset:
            from constants.check_presets import key_preset
            preset_title = key_preset[check_preset].name

            self.lines.append(scroll_area.Line("-------------------------", f0.set_user_text_color))
            self.lines.append(scroll_area.Line(f"{preset_title}", f0.set_user_text_color))
            self.lines.append(scroll_area.Line("-------------------------", f0.set_user_text_color))

            self.lines.append(scroll_area.Line("", f0.set_user_text_color))

        check_lines = FlagsForceRewardChecks._format_check_list_menu(item_checks)
        for check in check_lines:
            self.lines.append(scroll_area.Line(f"{check}", f0.set_user_text_color))

        super().__init__()

    def _format_check_list_menu(check_ids):
        from constants.checks import check_name
        check_lines = []

        for (group_name, checks) in [(group, checks) for (group, checks) in character_checks.items()]:
            group_check_ids = [check.bit for check in checks]
            group_checks = [check for check in check_ids if check in group_check_ids]
            if len(group_checks) > 0:
                check_lines.append(group_name)
                for bit in group_checks:
                    check_lines.append(f"{' '}{check_name.get(bit)}")
                check_lines.append("")

        return check_lines


class FlagsForceEsperRewardChecks(FlagsForceRewardChecks):
    MENU_NUMBER = 16

class FlagsForceEsperItemRewardChecks(FlagsForceRewardChecks):
    MENU_NUMBER = 17

class FlagsForceItemRewardChecks(FlagsForceRewardChecks):
    MENU_NUMBER = 18

class FlagsForceCharacterRewardChecks(FlagsForceRewardChecks):
    MENU_NUMBER = 19
