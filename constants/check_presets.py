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

SEDENTARY_LIFESTYLE = CheckPreset(
    "sitlife",
    "Sedentary Lifestyle",
    RewardType.ITEM,
    "Longer checks in the game are guaranteed to reward an ITEM.",
    [
        ANCIENT_CASTLE,
        BURNING_HOUSE,
        PHOENIX_CAVE,
        FLOATING_CONT_ARRIVE,
        FLOATING_CONT_BEAST,
        FLOATING_CONT_ESCAPE,
        LETE_RIVER,
        MAGITEK_FACTORY_FINISH,
        OPERA_HOUSE_DISRUPTION,
        PHANTOM_TRAIN,
        FANATICS_TOWER_FOLLOWER,
    ],
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

NO_FREE_PROGRESSION = CheckPreset(
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

NO_FREE_PROGRESSION_NO_GP = CheckPreset(
    'nfcegp',
    "No Free C+E (No AH/Tzen)",
    RewardType.ITEM,
    "All free checks are guaranteed to reward an ITEM. GP-based checks Auction House and Tzen Thief can still reward ESPER or ITEM.",
    [
        COLLAPSING_HOUSE,
        FIGARO_CASTLE_THRONE,
        GAUS_FATHERS_HOUSE,
        KOHLINGEN_CAFE,
        MT_ZOZO,
        NARSHE_WEAPON_SHOP,
        NARSHE_WEAPON_SHOP_MINES,
        SEALED_GATE,
        SOUTH_FIGARO_PRISONER,
    ]
)

SQUID_GAMES = CheckPreset(
    'squid',
    'Squid Games',
    RewardType.CHARACTER,
    'The checks which you fight Ultros in the vanilla game are guaranteed to reward a CHARACTER. The checks are Lete River, Opera House, Esper Mountain, and Floating Continent Arrival.',
    [
        ESPER_MOUNTAIN,
        FLOATING_CONT_ARRIVE,
        LETE_RIVER,
        OPERA_HOUSE_DISRUPTION,
    ]
)

VANILLA_ESPERS = CheckPreset(
    'vanesp',
    "Vanilla Espers",
    RewardType.ESPER,
    "Most checks/events in the vanilla game which revolve around espers are guaranteed to reward an ESPER.",
    [
        ANCIENT_CASTLE,
        MAGITEK_FACTORY_TRASH,
        MAGITEK_FACTORY_GUARD,
        MAGITEK_FACTORY_FINISH,
        SEALED_GATE,
        ESPER_MOUNTAIN,
        PHOENIX_CAVE,
        ZOZO_TOWER,
    ]
)

all_presets = [
    AH_CLOSED,
    NO_FREE_CHARACTERS,
    NO_FREE_PROGRESSION,
    NO_FREE_PROGRESSION_NO_GP,
    SEDENTARY_LIFESTYLE,
    SQUID_GAMES,
    VANILLA_ESPERS,
]

preset_keys = [preset.key for preset in all_presets]
key_preset = {preset.key: preset for (idx, preset) in enumerate(all_presets)}
