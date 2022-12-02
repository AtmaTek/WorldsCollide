from constants.checks import *

from collections import namedtuple
CheckPreset = namedtuple("CheckPreset", ["key", "name", "reward", "description", "locations"])

AH_CLOSED = CheckPreset(
    "ah",
    "Auction House is Closed",
    RewardType.ITEM,
    "The auction house will only have items available.",
    [
        AUCTION1,
        AUCTION2
    ]
)

NO_FREE_CHARACTERS = CheckPreset(
    'nfchar',
    "No Free Characters",
    RewardType.ESPER | RewardType.ITEM,
    "All free checks that can reward characters are guaranteed to reward an ESPER or ITEM",
    [
        COLLAPSING_HOUSE,
        FIGARO_CASTLE_THRONE,
        GAUS_FATHERS_HOUSE,
        KOHLINGEN_CAFE,
        MT_ZOZO,
        SEALED_GATE,
        SOUTH_FIGARO_PRISONER,
    ]
)

NO_FREE_CHARACTERS_ESPERS = CheckPreset(
    'nfce',
    "No Free C+E",
    RewardType.ITEM,
    "All free checks are guaranteed to reward an ITEM. Includes Auction House and Tzen Thief.",
    [
        AUCTION1,
        AUCTION2,
        COLLAPSING_HOUSE,
        FIGARO_CASTLE_THRONE,
        GAUS_FATHERS_HOUSE,
        KOHLINGEN_CAFE,
        MT_ZOZO,
        NARSHE_WEAPON_SHOP,
        NARSHE_WEAPON_SHOP_MINES,
        SEALED_GATE,
        SOUTH_FIGARO_PRISONER,
        TZEN_THIEF,
    ]
)

all_presets = [
    AH_CLOSED,
    NO_FREE_CHARACTERS,
    NO_FREE_CHARACTERS_ESPERS,
]

preset_keys = [preset.key for preset in all_presets]
key_preset = {preset.key: preset for (idx, preset) in enumerate(all_presets)}
