from constants.checks import (
    FANATICS_TOWER_LEADER,
    LONE_WOLF_MOOGLE_ROOM,
    NARSHE_WEAPON_SHOP_MINES,
    AUCTION1,
    AUCTION2,
    COLLAPSING_HOUSE,
    FIGARO_CASTLE_THRONE,
    GAUS_FATHERS_HOUSE,
    KOHLINGEN_CAFE,
    NARSHE_WEAPON_SHOP,
    SEALED_GATE,
    SOUTH_FIGARO_PRISONER,
)
import menus.pregame_track_scroll_area as scroll_area
from data.text.text2 import text_value
import instruction.f0 as f0

nfce = [
    AUCTION1,
    AUCTION2,
    COLLAPSING_HOUSE,
    FIGARO_CASTLE_THRONE,
    GAUS_FATHERS_HOUSE,
    KOHLINGEN_CAFE,
    NARSHE_WEAPON_SHOP,
    SEALED_GATE,
    SOUTH_FIGARO_PRISONER,
]

legacy = [
    FANATICS_TOWER_LEADER,
    LONE_WOLF_MOOGLE_ROOM,
    NARSHE_WEAPON_SHOP_MINES,
]
class FlagsForceItemRewardChecks(scroll_area.ScrollArea):
    MENU_NUMBER = 16

    def __init__(self, item_checks, is_nfce, is_legacy):
        self.number_items = len(item_checks)
        self.lines = []

        self.lines.append(scroll_area.Line(f"Forced Item Reward Checks", f0.set_blue_text_color))

        if is_nfce:
            self.lines.append(scroll_area.Line("-------------------------", f0.set_user_text_color))
            self.lines.append(scroll_area.Line("No Free Characters Espers", f0.set_user_text_color))
            self.lines.append(scroll_area.Line("-------------------------", f0.set_user_text_color))
            for check in nfce:
                self.lines.append(scroll_area.Line(f"{check.name}", f0.set_user_text_color))

            self.lines.append(scroll_area.Line("", f0.set_user_text_color))

        if is_legacy:
            self.lines.append(scroll_area.Line("-------------------------", f0.set_user_text_color))
            self.lines.append(scroll_area.Line("Classic Item Reward Checks", f0.set_user_text_color))
            self.lines.append(scroll_area.Line("-------------------------", f0.set_user_text_color))
            for check in legacy:
                self.lines.append(scroll_area.Line(f"{check.name}", f0.set_user_text_color))

            self.lines.append(scroll_area.Line("", f0.set_user_text_color))

        # Someone set the check rewards
        if not (is_nfce or is_legacy):
            check_lines = FlagsForceItemRewardChecks._format_check_list_menu(item_checks)
            for check in check_lines:
                self.lines.append(scroll_area.Line(f"{check}", f0.set_user_text_color))


        super().__init__()

    def _format_check_list_menu(check_ids):
        from constants.checks import check_name
        check_lines = []

        # Step through each check
        for a_check_bit in check_ids:
            check_str = f"{check_name.get(a_check_bit)}"
            current_line = f"{'  '}{check_str}"
            # Write the line
            check_lines.append(current_line)
        return check_lines
