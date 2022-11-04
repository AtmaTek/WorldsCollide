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
    "The longest checks in the game are forced item rewards.",
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

NO_FREE_PROGRESSION_NEW = CheckPreset(
    'nfce',
    "No Free Characters/Espers",
    RewardType.ITEM,
    "All free checks are forced items. Similar to classic, but does not include auction house and tzen thief.",
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

NO_FREE_PROGRESSION_CLASSIC = CheckPreset(
    'nfce-classic',
    "No Free C+E (Classic)",
    RewardType.ITEM,
    "All free checks are forced items. Includes auction house and tzen thief.",
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

SQUID_GAMES = CheckPreset(
    'squid',
    'Squid Games',
    RewardType.CHARACTER,
    'The rewards following the vanilla ultros fights are guaranteed to grant a character. The checks are Esper Mountain, Floating Continent 1, Lete River, Opera House.',
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
    "Most checks/events that involve espers in the base game will grant an esper as the reward.",
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
    NO_FREE_PROGRESSION_NEW,
    NO_FREE_PROGRESSION_CLASSIC,
    SEDENTARY_LIFESTYLE,
    SQUID_GAMES,
    VANILLA_ESPERS,
]

preset_keys = [preset.key for preset in all_presets]
key_preset = {preset.key: preset for (idx, preset) in enumerate(all_presets)}
