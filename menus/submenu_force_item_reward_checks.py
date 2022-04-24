import menus.pregame_track_scroll_area as scroll_area
from data.text.text2 import text_value
import instruction.f0 as f0

class FlagsForceItemRewardChecks(scroll_area.ScrollArea):
    MENU_NUMBER = 16

    def __init__(self, item_checks):
        self.number_items = len(item_checks)
        self.lines = []

        self.lines.append(scroll_area.Line(f"Forced Item Reward Checks", f0.set_blue_text_color))

        check_lines = FlagsForceItemRewardChecks._format_check_list_menu(item_checks)

        for list_value in check_lines:
            self.lines.append(scroll_area.Line(f"{list_value}", f0.set_user_text_color))

        super().__init__()

    def _format_check_list_menu(check_ids):
        from constants.checks import all_checks_check_name
        check_lines = []

        # Step through each check
        for a_check_bit in check_ids:
            check_str = f"{all_checks_check_name.get(a_check_bit)}"
            current_line = f"{'  '}{check_str}"
            # Write the line
            check_lines.append(current_line)
        return check_lines
