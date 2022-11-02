import constants.checks as c
from constants.checks import (
    CELES, CYAN, EDGAR, GAU,
    GOGO, LOCKE, MOG, RELM,
    SABIN, SETZER, STRAGO, SHADOW,
    TERRA,  UMARO, UNGATED, UNGATED_DRAGONS
)

character_checks = {
    "Celes"  : [c.name for c in CELES],
    "Cyan"   : [c.name for c in CYAN],
    "Edgar"  : [c.name for c in EDGAR],
    "Gau"    : [c.name for c in GAU],
    "Gogo"   : [c.name for c in GOGO],
    "Locke"  : [c.name for c in LOCKE],
    "Mog"    : [c.name for c in MOG],
    "Relm"   : [c.name for c in RELM],
    "Sabin"  : [c.name for c in SABIN],
    "Setzer" : [c.name for c in SETZER],
    "Shadow" : [c.name for c in SHADOW],
    "Strago" : [c.name for c in STRAGO],
    "Terra"  : [c.name for c in TERRA],
    "Umaro"  : [c.name for c in UMARO],
    ""       : [c.name for c in UNGATED_DRAGONS] + [c.name for c in UNGATED],
}
