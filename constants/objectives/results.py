from constants.blitzes import id_blitz
from constants.dances import id_dance
from constants.lores import id_lore
from constants.rages import id_rage
from constants.swdtechs import id_swdtech
from constants.spells import id_spell

from collections import namedtuple
ResultType = namedtuple("ResultType", ["name", "format_string", "value_range"])

category_types = {
    "Random" : [
        ResultType("Random", "Random", None),
    ],
    "Kefka's Tower" : [
        ResultType("Kefka's Tower", "Random", None),
        ResultType("Unlock Final Kefka", "Unlock Final Kefka", None),
        ResultType("Unlock KT Skip", "Unlock KT Skip", None),
    ],
    "Auto" : [
        ResultType("Auto", "Random", None),
        ResultType("Auto Berserk", "Auto Berserk", None),
        ResultType("Auto Condemned", "Auto Condemned", None),
        ResultType("Auto Float", "Auto Float", None),
        ResultType("Auto Haste", "Auto Haste", None),
        ResultType("Auto Image", "Auto Image", None),
        ResultType("Auto Muddle", "Auto Muddle", None),
        ResultType("Auto Mute", "Auto Mute", None),
        ResultType("Auto Reflect", "Auto Reflect", None),
        ResultType("Auto Regen", "Auto Regen", None),
        ResultType("Auto Safe", "Auto Safe", None),
        ResultType("Auto Seizure", "Auto Seizure", None),
        ResultType("Auto Shell", "Auto Shell", None),
        ResultType("Auto Sleep", "Auto Sleep", None),
        ResultType("Auto Slow", "Auto Slow", None),
        ResultType("Auto Stop", "Auto Stop", None),
    ],
    "Battle" : [
        ResultType("Battle", "Random", None),
        ResultType("Add Enemy Levels", "Enemy Levels {:+d}", list(range(1, 100))),
        ResultType("Add Boss Levels", "Boss Levels {:+d}", list(range(1, 100))),
        ResultType("Add Dragon Levels", "Dragon Levels {:+d}", list(range(1, 100))),
        ResultType("Add Final Levels", "Final Levels {:+d}", list(range(1, 100))),
    ],
    "Command" : [
        ResultType("Command", "Random", None),
        ResultType("Learn Blitzes", "Learn {} Blitzes", list(range(1, len(id_blitz) + 1))),
        ResultType("Learn Dances", "Learn {} Dances", list(range(1, len(id_dance) + 1))),
        ResultType("Learn Lores", "Learn {} Lores", list(range(1, len(id_lore) + 1))),
        ResultType("Learn Rages", "Learn {} Rages", list(range(1, len(id_rage) + 1))),
        ResultType("Learn SwdTechs", "Learn {} SwdTechs", list(range(1, len(id_swdtech) + 1))),
        ResultType("Learn Spells", "Learn {} Spells", list(range(1, len(id_spell) + 1))),
        ResultType("Forget Spells", "Forget {} Spells", list(range(1, len(id_spell) + 1))),
        ResultType("Max Morph Duration", "Max Morph Duration", None),
    ],
    "Item" : [
        ResultType("Item", "Random", None),
        ResultType("Breakable Rods", "Breakable Rods", None),
        ResultType("Dragoon", "Dragoon", None),
        ResultType("Dried Meat", "Dried Meat", None),
        ResultType("Exp. Egg", "Exp. Egg", None),
        ResultType("Imp Set", "Imp Set", None),
        ResultType("Illumina", "Illumina", None),
        ResultType("Rename Cards", "Rename Cards", None),
        ResultType("Ribbon", "Ribbon", None),
        ResultType("Tools", "Tools", None),
    ],
    "Stat" : [
        ResultType("Stat", "Random", None),
        ResultType("MagPwr All", "{:+d} Mag.Pwr All", list(range(-99, 100))),
        ResultType("Speed All", "{:+d} Speed All", list(range(-99, 100))),
        ResultType("Stamina All", "{:+d} Stamina All", list(range(-99, 100))),
        ResultType("Vigor All", "{:+d} Vigor All", list(range(-99, 100))),
        ResultType("MagPwr Random", "{:+d} Mag.Pwr {}", list(range(-99, 100))),
        ResultType("Speed Random", "{:+d} Speed {}", list(range(-99, 100))),
        ResultType("Stamina Random", "{:+d} Stamina {}", list(range(-99, 100))),
        ResultType("Vigor Random", "{:+d} Vigor {}", list(range(-99, 100))),
    ],
    "Status" : [
        ResultType("Status", "Random", None),
        ResultType("Fallen One", "Fallen One", None),
        ResultType("Full Heal", "Full Heal", None),
        ResultType("Imp Song", "Imp Song", None),
        ResultType("Sour Mouth", "Sour Mouth", None),
    ],
}

categories = list(category_types.keys())

name_type = {}
name_category = {}
for category in category_types:
    for _type in category_types[category]:
        name_type[_type.name] = _type
        name_category[_type.name] = category

names = list(name_type.keys())

types = [_type for name, _type in name_type.items()]
