import data.battle_bit as battle_bit
import constants.checks as checks
import constants.quests as quests
from data.bosses import normal_formation_name, dragon_formation_name

from collections import namedtuple
NameBit = namedtuple("NameBit", ["name", "bit"])

check_bit = [
    checks.ANCIENT_CASTLE,
    checks.ANCIENT_CASTLE_DRAGON,
    checks.BAREN_FALLS,
    checks.BURNING_HOUSE,
    checks.COLLAPSING_HOUSE,
    checks.DARYLS_TOMB,
    checks.DOMA_SIEGE,
    checks.DOMA_DREAM_DOOR,
    checks.DOMA_DREAM_AWAKEN,
    checks.DOMA_DREAM_THRONE,
    checks.EBOTS_ROCK,
    checks.ESPER_MOUNTAIN,
    checks.FANATICS_TOWER_DRAGON,
    checks.FANATICS_TOWER_LEADER,
    checks.FANATICS_TOWER_FOLLOWER,
    checks.FIGARO_CASTLE_THRONE,
    checks.FIGARO_CASTLE_ENGINE,
    checks.FLOATING_CONT_ARRIVE,
    checks.FLOATING_CONT_BEAST,
    checks.FLOATING_CONT_ESCAPE,
    checks.GAUS_FATHERS_HOUSE,
    checks.IMPERIAL_CAMP,
    checks.KEFKAS_TOWER_CELL_BEAST,
    checks.KEFKAS_TOWER_DRAGON_G,
    checks.KEFKAS_TOWER_DRAGON_S,
    checks.KOHLINGEN_CAFE,
    checks.LETE_RIVER,
    checks.LONE_WOLF_CHASE,
    checks.LONE_WOLF_MOOGLE_ROOM,
    checks.MAGITEK_FACTORY_TRASH,
    checks.MAGITEK_FACTORY_GUARD,
    checks.MAGITEK_FACTORY_FINISH,
    checks.MOBLIZ_ATTACK,
    checks.MT_KOLTS,
    checks.MT_ZOZO,
    checks.MT_ZOZO_DRAGON,
    checks.NARSHE_BATTLE,
    checks.NARSHE_DRAGON,
    checks.NARSHE_WEAPON_SHOP,
    checks.NARSHE_WEAPON_SHOP_MINES,
    checks.OPERA_HOUSE_DISRUPTION,
    checks.OPERA_HOUSE_DRAGON,
    checks.OWZERS_MANSION,
    checks.PHANTOM_TRAIN,
    checks.PHOENIX_CAVE,
    checks.PHOENIX_CAVE_DRAGON,
    checks.SEALED_GATE,
    checks.SEARCH_THE_SKIES,
    checks.SERPENT_TRENCH,
    checks.SOUTH_FIGARO_PRISONER,
    checks.SOUTH_FIGARO_CAVE,
    checks.TRITOCH_CLIFF,
    checks.TZEN_THIEF,
    checks.UMAROS_CAVE,
    checks.VELDT,
    checks.VELDT_CAVE,
    checks.WHELK_GATE,
    checks.ZONE_EATER,
    checks.ZOZO_TOWER,
]

quest_bit = [
    quests.DEFEAT_SEALED_CAVE_NINJA,
    quests.HELP_INJURED_LAD,
    quests.LET_CID_DIE,
    quests.PASS_SECURITY_CHECKPOINT,
    quests.PERFORM_IN_OPERA,
    quests.SAVE_CID,
    quests.SET_ZOZO_CLOCK,
    quests.SUPLEX_A_TRAIN,
    quests.WIN_AN_AUCTION,
    quests.WIN_A_COLISEUM_MATCH,
]

boss_bit = []
for formation_id in sorted(normal_formation_name, key = normal_formation_name.get):
    boss_bit.append(NameBit(normal_formation_name[formation_id], battle_bit.boss_defeated(formation_id)))

dragon_bit = []
for formation_id in sorted(dragon_formation_name, key = dragon_formation_name.get):
    dragon_bit.append(NameBit(dragon_formation_name[formation_id], battle_bit.dragon_defeated(formation_id)))
