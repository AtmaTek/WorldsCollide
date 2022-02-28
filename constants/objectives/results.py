from constants.blitzes import id_blitz
from constants.dances import id_dance
from constants.lores import id_lore
from constants.rages import id_rage
from constants.swdtechs import id_swdtech
from constants.spells import id_spell

from collections import namedtuple
ResultType = namedtuple("ResultType", ["id", "name", "format_string", "value_range"])

category_types = {
    "Random" : [],
    "Kefka's Tower" : [],
    "Auto" : [],
    "Battle" : [],
    "Command" : [],
    "Item" : [],
    "Stat" : [],
    "Status" : [],
}

# Random
category_types["Random"].append(ResultType(0, "Random", "Random", None))

# Kefka's Tower
category_types["Kefka's Tower"].append(ResultType(1, "Kefka's Tower", "Random", None))
category_types["Kefka's Tower"].append(ResultType(2, "Unlock Final Kefka", "Unlock Final Kefka", None))
category_types["Kefka's Tower"].append(ResultType(3, "Unlock KT Skip", "Unlock KT Skip", None))

# Auto
category_types["Auto"].append(ResultType(4, "Auto", "Random", None))
category_types["Auto"].append(ResultType(5, "Auto Berserk", "Auto Berserk", None))
category_types["Auto"].append(ResultType(6, "Auto Condemned", "Auto Condemned", None))
category_types["Auto"].append(ResultType(7, "Auto Float", "Auto Float", None))
category_types["Auto"].append(ResultType(8, "Auto Haste", "Auto Haste", None))
category_types["Auto"].append(ResultType(9, "Auto Image", "Auto Image", None))
category_types["Auto"].append(ResultType(10, "Auto Muddle", "Auto Muddle", None))
category_types["Auto"].append(ResultType(11, "Auto Mute", "Auto Mute", None))
category_types["Auto"].append(ResultType(12, "Auto Reflect", "Auto Reflect", None))
category_types["Auto"].append(ResultType(13, "Auto Regen", "Auto Regen", None))
category_types["Auto"].append(ResultType(14, "Auto Safe", "Auto Safe", None))
category_types["Auto"].append(ResultType(15, "Auto Seizure", "Auto Seizure", None))
category_types["Auto"].append(ResultType(16, "Auto Shell", "Auto Shell", None))
category_types["Auto"].append(ResultType(17, "Auto Sleep", "Auto Sleep", None))
category_types["Auto"].append(ResultType(18, "Auto Slow", "Auto Slow", None))

# Battle
category_types["Battle"].append(ResultType(20, "Battle", "Random", None))
category_types["Battle"].append(ResultType(21, "Add Enemy Levels", "Enemy Levels {:+d}", list(range(1, 100))))
category_types["Battle"].append(ResultType(22, "Add Boss Levels", "Boss Levels {:+d}", list(range(1, 100))))
category_types["Battle"].append(ResultType(23, "Add Dragon Levels", "Dragon Levels {:+d}", list(range(1, 100))))
category_types["Battle"].append(ResultType(24, "Add Final Levels", "Final Levels {:+d}", list(range(1, 100))))

# Command
category_types["Command"].append(ResultType(25, "Command", "Random", None))
category_types["Command"].append(ResultType(26, "Learn Blitzes", "Learn {} Blitzes", list(range(1, len(id_blitz) + 1))))
category_types["Command"].append(ResultType(27, "Learn Dances", "Learn {} Dances", list(range(1, len(id_dance) + 1))))
category_types["Command"].append(ResultType(28, "Learn Lores", "Learn {} Lores", list(range(1, len(id_lore) + 1))))
category_types["Command"].append(ResultType(29, "Learn Rages", "Learn {} Rages", list(range(1, len(id_rage) + 1))))
category_types["Command"].append(ResultType(30, "Learn SwdTechs", "Learn {} SwdTechs", list(range(1, len(id_swdtech) + 1))))
category_types["Command"].append(ResultType(31, "Learn Spells", "Learn {} Spells", list(range(1, len(id_spell) + 1))))
category_types["Command"].append(ResultType(32, "Forget Spells", "Forget {} Spells", list(range(1, len(id_spell) + 1))))
category_types["Command"].append(ResultType(33, "Max Morph Duration", "Max Morph Duration", None))

# Item
category_types["Item"].append(ResultType(34, "Item", "Random", None))
category_types["Item"].append(ResultType(35, "Breakable Rods", "Breakable Rods", None))
category_types["Item"].append(ResultType(36, "Dragoon", "Dragoon", None))
category_types["Item"].append(ResultType(37, "Dried Meat", "Dried Meat", None))
category_types["Item"].append(ResultType(38, "Exp. Egg", "Exp. Egg", None))
category_types["Item"].append(ResultType(40, "Illumina", "Illumina", None))
category_types["Item"].append(ResultType(39, "Imp Set", "Imp Set", None))
category_types["Item"].append(ResultType(41, "Rename Cards", "Rename Cards", None))
category_types["Item"].append(ResultType(42, "Ribbon", "Ribbon", None))
category_types["Item"].append(ResultType(43, "Tools", "Tools", None))

# Stat
category_types["Stat"].append(ResultType(44, "Stat", "Random", None))
category_types["Stat"].append(ResultType(45, "MagPwr All", "{:+d} Mag.Pwr All", list(range(-99, 100))))
category_types["Stat"].append(ResultType(46, "Speed All", "{:+d} Speed All", list(range(-99, 100))))
category_types["Stat"].append(ResultType(47, "Stamina All", "{:+d} Stamina All", list(range(-99, 100))))
category_types["Stat"].append(ResultType(48, "Vigor All", "{:+d} Vigor All", list(range(-99, 100))))
category_types["Stat"].append(ResultType(49, "MagPwr Random", "{:+d} Mag.Pwr {}", list(range(-99, 100))))
category_types["Stat"].append(ResultType(50, "Speed Random", "{:+d} Speed {}", list(range(-99, 100))))
category_types["Stat"].append(ResultType(51, "Stamina Random", "{:+d} Stamina {}", list(range(-99, 100))))
category_types["Stat"].append(ResultType(52, "Vigor Random", "{:+d} Vigor {}", list(range(-99, 100))))

# Status
category_types["Status"].append(ResultType(53, "Status", "Random", None))
category_types["Status"].append(ResultType(54, "Fallen One", "Fallen One", None))
category_types["Status"].append(ResultType(55, "Full Heal", "Full Heal", None))
category_types["Status"].append(ResultType(56, "Imp Song", "Imp Song", None))
category_types["Status"].append(ResultType(57, "Sour Mouth", "Sour Mouth", None))

# Add new result types here
category_types["Item"].append(ResultType(58, "High Tier Item", "High Tier Item", None))
category_types["Item"].append(ResultType(59, "Sprint Shoes", "Sprint Shoes", None))


# Order the list of each category type alphabetically
for [index, ct] in enumerate(category_types):
    sorted_list = sorted(category_types[ct], key = lambda h: h.name)
    category_types[ct] = sorted_list

categories = list(category_types.keys())

id_type = {}
name_type = {}
name_category = {}
for category in category_types:
    for _type in category_types[category]:
        id_type[_type.id] = _type
        name_type[_type.name] = _type
        name_category[_type.name] = category

names = list(name_type.keys())

types = [_type for name, _type in name_type.items()]
