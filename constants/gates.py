import constants.checks as c
from constants.checks import all_checks
from constants.entities import (
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
)

character_checks = {
    "Celes"  : [c for c in [check for check in all_checks if check.gate_character == CELES]],
    "Cyan"   : [c for c in [check for check in all_checks if check.gate_character == CYAN]],
    "Edgar"  : [c for c in [check for check in all_checks if check.gate_character == EDGAR]],
    "Gau"    : [c for c in [check for check in all_checks if check.gate_character == GAU]],
    "Gogo"   : [c for c in [check for check in all_checks if check.gate_character == GOGO]],
    "Locke"  : [c for c in [check for check in all_checks if check.gate_character == LOCKE]],
    "Mog"    : [c for c in [check for check in all_checks if check.gate_character == MOG]],
    "Relm"   : [c for c in [check for check in all_checks if check.gate_character == RELM]],
    "Sabin"  : [c for c in [check for check in all_checks if check.gate_character == SABIN]],
    "Setzer" : [c for c in [check for check in all_checks if check.gate_character == SETZER]],
    "Shadow" : [c for c in [check for check in all_checks if check.gate_character == SHADOW]],
    "Strago" : [c for c in [check for check in all_checks if check.gate_character == STRAGO]],
    "Terra"  : [c for c in [check for check in all_checks if check.gate_character == TERRA]],
    "Umaro"  : [c for c in [check for check in all_checks if check.gate_character == UMARO]],
    ""       : [c for c in [check for check in all_checks if check.gate_character is None]],
}

character_check_names = {
    "Celes"  : [c.name for c in [check for check in all_checks if check.gate_character == CELES]],
    "Cyan"   : [c.name for c in [check for check in all_checks if check.gate_character == CYAN]],
    "Edgar"  : [c.name for c in [check for check in all_checks if check.gate_character == EDGAR]],
    "Gau"    : [c.name for c in [check for check in all_checks if check.gate_character == GAU]],
    "Gogo"   : [c.name for c in [check for check in all_checks if check.gate_character == GOGO]],
    "Locke"  : [c.name for c in [check for check in all_checks if check.gate_character == LOCKE]],
    "Mog"    : [c.name for c in [check for check in all_checks if check.gate_character == MOG]],
    "Relm"   : [c.name for c in [check for check in all_checks if check.gate_character == RELM]],
    "Sabin"  : [c.name for c in [check for check in all_checks if check.gate_character == SABIN]],
    "Setzer" : [c.name for c in [check for check in all_checks if check.gate_character == SETZER]],
    "Shadow" : [c.name for c in [check for check in all_checks if check.gate_character == SHADOW]],
    "Strago" : [c.name for c in [check for check in all_checks if check.gate_character == STRAGO]],
    "Terra"  : [c.name for c in [check for check in all_checks if check.gate_character == TERRA]],
    "Umaro"  : [c.name for c in [check for check in all_checks if check.gate_character == UMARO]],
    ""       : [c.name for c in [check for check in all_checks if check.gate_character is None]],
}
