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
    CELES,
    CYAN,
    EDGAR,
    GAU,
    GOGO,
    LOCKE,
    MOG,
    RELM,
    SABIN,
    SETZER,
    SHADOW,
    STRAGO,
    TERRA,
    UMARO,
    UNGATED,
)
import menus.pregame_track_scroll_area as scroll_area
from data.text.text2 import text_value
import instruction.f0 as f0

groups = [
    ("Celes", CELES),
    ("Cyan", CYAN),
    ("Edgar", EDGAR),
    ("Gau", GAU),
    ("Gogo", GOGO),
    ("Locke", LOCKE),
    ("Mog", MOG),
    ("Relm", RELM),
    ("Sabin", SABIN),
    ("Setzer", SETZER),
    ("Shadow", SHADOW),
    ("Strago", STRAGO),
    ("Terra", TERRA),
    ("Umaro", UMARO),
    ("Ungated", UNGATED),
]

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
class FlagsForceRewardChecks(scroll_area.ScrollArea):

    def __init__(self, title, item_checks, is_nfce):
        self.number_items = len(item_checks)
        self.lines = []

        self.lines.append(scroll_area.Line(title, f0.set_blue_text_color))

        if is_nfce:
            self.lines.append(scroll_area.Line("-------------------------", f0.set_user_text_color))
            self.lines.append(scroll_area.Line("No Free Characters Espers", f0.set_user_text_color))
            self.lines.append(scroll_area.Line("-------------------------", f0.set_user_text_color))
            for check in nfce:
                self.lines.append(scroll_area.Line(f"{check.name}", f0.set_user_text_color))

            self.lines.append(scroll_area.Line("", f0.set_user_text_color))

        # Someone set the check rewards
        if not (is_nfce):
            check_lines = FlagsForceRewardChecks._format_check_list_menu(item_checks)
            for check in check_lines:
                self.lines.append(scroll_area.Line(f"{check}", f0.set_user_text_color))

        super().__init__()

    def _format_check_list_menu(check_ids):
        from constants.checks import check_name
        check_lines = []

        for (group_name, checks) in groups:
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
