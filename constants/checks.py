from collections import namedtuple
import data.event_bit as event_bit
import data.npc_bit as npc_bit
from event.event_reward import RewardType

NameBit = namedtuple("NameBit", ["name", "bit", "reward_types"])
CHAR_ESPER_REWARD = RewardType.CHARACTER | RewardType.ESPER
ANY_REWARD = RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM
ESPER_ITEM_REWARD =  RewardType.ESPER | RewardType.ITEM
ITEM_REWARD =  RewardType.ITEM

AUCTION1 =  NameBit("Auction1", event_bit.AUCTION_BOUGHT_ESPER1, ESPER_ITEM_REWARD)
AUCTION2 = NameBit("Auction2", event_bit.AUCTION_BOUGHT_ESPER2, ESPER_ITEM_REWARD)
ANCIENT_CASTLE = NameBit("Ancient Castle", event_bit.GOT_RAIDEN, ANY_REWARD)
BAREN_FALLS = NameBit("Baren Falls", event_bit.NAMED_GAU, ANY_REWARD)
BURNING_HOUSE = NameBit("Burning House", event_bit.DEFEATED_FLAME_EATER, ANY_REWARD)
COLLAPSING_HOUSE = NameBit("Collapsing House", event_bit.FINISHED_COLLAPSING_HOUSE, ANY_REWARD)
DARYLS_TOMB = NameBit("Daryl's Tomb", event_bit.DEFEATED_DULLAHAN, ANY_REWARD)
DOMA_SIEGE = NameBit("Doma Siege", event_bit.FINISHED_DOMA_WOB, ANY_REWARD)
DOMA_DREAM_DOOR = NameBit("Doma Dream Door", event_bit.DEFEATED_STOOGES, ESPER_ITEM_REWARD)
DOMA_DREAM_AWAKEN = NameBit("Doma Dream Awaken", event_bit.FINISHED_DOMA_WOR, CHAR_ESPER_REWARD)
DOMA_DREAM_THRONE = NameBit("Doma Dream Throne", event_bit.GOT_ALEXANDR, ESPER_ITEM_REWARD)
EBOTS_ROCK = NameBit("Ebot's Rock", event_bit.DEFEATED_HIDON, ANY_REWARD)
ESPER_MOUNTAIN = NameBit("Esper Mountain", event_bit.DEFEATED_ULTROS_ESPER_MOUNTAIN, ANY_REWARD)
FANATICS_TOWER_LEADER = NameBit("Fanatic's Tower Leader", event_bit.DEFEATED_MAGIMASTER, ESPER_ITEM_REWARD)
FANATICS_TOWER_FOLLOWER = NameBit("Fanatic's Tower Follower", event_bit.RECRUITED_STRAGO_FANATICS_TOWER, CHAR_ESPER_REWARD)
FIGARO_CASTLE_THRONE = NameBit("Figaro Castle Throne", event_bit.NAMED_EDGAR, ANY_REWARD)
FIGARO_CASTLE_ENGINE = NameBit("Figaro Castle Engine", event_bit.DEFEATED_TENTACLES_FIGARO, ANY_REWARD)
FLOATING_CONT_ARRIVE = NameBit("Floating Cont. Arrive", event_bit.RECRUITED_SHADOW_FLOATING_CONTINENT, CHAR_ESPER_REWARD)
FLOATING_CONT_BEAST = NameBit("Floating Cont. Beast", event_bit.DEFEATED_ATMAWEAPON, ESPER_ITEM_REWARD)
FLOATING_CONT_ESCAPE = NameBit("Floating Cont. Escape", event_bit.FINISHED_FLOATING_CONTINENT, CHAR_ESPER_REWARD)
GAUS_FATHERS_HOUSE = NameBit("Gau's Father's House", event_bit.RECRUITED_SHADOW_GAU_FATHER_HOUSE, ANY_REWARD)
IMPERIAL_CAMP = NameBit("Imperial Camp", event_bit.FINISHED_IMPERIAL_CAMP, ANY_REWARD)
KEFKAS_TOWER_CELL_BEAST = NameBit("Kefka's Tower Cell Beast", event_bit.DEFEATED_ATMA, ITEM_REWARD)
KOHLINGEN_CAFE = NameBit("Kohlingen Cafe", event_bit.RECRUITED_SHADOW_KOHLINGEN, ANY_REWARD)
LETE_RIVER = NameBit("Lete River", event_bit.RODE_RAFT_LETE_RIVER, ANY_REWARD)
LONE_WOLF_CHASE = NameBit("Lone Wolf Chase", event_bit.CHASING_LONE_WOLF7, ANY_REWARD)
LONE_WOLF_MOOGLE_ROOM = NameBit("Lone Wolf Moogle Room", event_bit.GOT_BOTH_REWARDS_LONE_WOLF, ESPER_ITEM_REWARD)
MAGITEK_FACTORY_TRASH = NameBit("Magitek Factory Trash", event_bit.GOT_IFRIT_SHIVA, ESPER_ITEM_REWARD)
MAGITEK_FACTORY_GUARD = NameBit("Magitek Factory Guard", event_bit.DEFEATED_NUMBER_024, ESPER_ITEM_REWARD)
MAGITEK_FACTORY_FINISH = NameBit("Magitek Factory Finish", event_bit.DEFEATED_CRANES, CHAR_ESPER_REWARD)
MOBLIZ_ATTACK = NameBit("Mobliz Attack", event_bit.RECRUITED_TERRA_MOBLIZ, ANY_REWARD)
MT_KOLTS = NameBit("Mt. Kolts", event_bit.DEFEATED_VARGAS, ANY_REWARD)
MT_ZOZO = NameBit("Mt. Zozo", event_bit.FINISHED_MT_ZOZO, ANY_REWARD)
NARSHE_BATTLE = NameBit("Narshe Battle", event_bit.FINISHED_NARSHE_BATTLE, ANY_REWARD)
NARSHE_WEAPON_SHOP = NameBit("Narshe Weapon Shop", event_bit.GOT_RAGNAROK, ESPER_ITEM_REWARD)
NARSHE_WEAPON_SHOP_MINES = NameBit("Narshe Weapon Shop Mines", event_bit.GOT_BOTH_REWARDS_WEAPON_SHOP, ESPER_ITEM_REWARD)
OPERA_HOUSE_DISRUPTION = NameBit("Opera House Disruption", event_bit.FINISHED_OPERA_DISRUPTION, ANY_REWARD)
OWZERS_MANSION = NameBit("Owzer's Mansion", event_bit.DEFEATED_CHADARNOOK, ANY_REWARD)
PHANTOM_TRAIN = NameBit("Phantom Train", event_bit.GOT_PHANTOM_TRAIN_REWARD, ANY_REWARD)
PHOENIX_CAVE = NameBit("Phoenix Cave", event_bit.RECRUITED_LOCKE_PHOENIX_CAVE, ANY_REWARD)
SEALED_GATE = NameBit("Sealed Gate", npc_bit.BLOCK_SEALED_GATE, ANY_REWARD)
SEARCH_THE_SKIES = NameBit("Search The Skies", event_bit.DEFEATED_DOOM_GAZE, ESPER_ITEM_REWARD)
SERPENT_TRENCH = NameBit("Serpent Trench", event_bit.GOT_SERPENT_TRENCH_REWARD, ANY_REWARD)
SOUTH_FIGARO_PRISONER = NameBit("South Figaro Prisoner", event_bit.FREED_CELES, ANY_REWARD)
SOUTH_FIGARO_CAVE = NameBit("South Figaro Cave", event_bit.DEFEATED_TUNNEL_ARMOR, ANY_REWARD)
TRITOCH_CLIFF = NameBit("Tritoch Cliff", event_bit.GOT_TRITOCH, ESPER_ITEM_REWARD)
TZEN_THIEF = NameBit("Tzen Thief", event_bit.BOUGHT_ESPER_TZEN, ESPER_ITEM_REWARD)
UMAROS_CAVE = NameBit("Umaro's Cave", event_bit.RECRUITED_UMARO_WOR, ANY_REWARD)
VELDT = NameBit("Veldt", event_bit.VELDT_REWARD_OBTAINED, ESPER_ITEM_REWARD)
VELDT_CAVE = NameBit("Veldt Cave", event_bit.DEFEATED_SR_BEHEMOTH, ANY_REWARD)
WHELK_GATE = NameBit("Whelk Gate", event_bit.DEFEATED_WHELK, ANY_REWARD)
ZONE_EATER = NameBit("Zone Eater", event_bit.RECRUITED_GOGO_WOR, ANY_REWARD)
ZOZO_TOWER = NameBit("Zozo Tower", event_bit.GOT_ZOZO_REWARD, ANY_REWARD)

ANCIENT_CASTLE_DRAGON = NameBit("Ancient Castle Dragon", event_bit.DEFEATED_ANCIENT_CASTLE_DRAGON, ITEM_REWARD)
FANATICS_TOWER_DRAGON = NameBit("Fanatic's Tower Dragon", event_bit.DEFEATED_FANATICS_TOWER_DRAGON, ITEM_REWARD)
KEFKAS_TOWER_DRAGON_G = NameBit("Kefka's Tower Dragon G", event_bit.DEFEATED_KEFKA_TOWER_DRAGON_G, ITEM_REWARD)
KEFKAS_TOWER_DRAGON_S = NameBit("Kefka's Tower Dragon S", event_bit.DEFEATED_KEFKA_TOWER_DRAGON_S, ITEM_REWARD)
MT_ZOZO_DRAGON = NameBit("Mt. Zozo Dragon", event_bit.DEFEATED_MT_ZOZO_DRAGON, ITEM_REWARD)
NARSHE_DRAGON = NameBit("Narshe Dragon", event_bit.DEFEATED_NARSHE_DRAGON, ITEM_REWARD)
OPERA_HOUSE_DRAGON = NameBit("Opera House Dragon", event_bit.DEFEATED_OPERA_HOUSE_DRAGON, ITEM_REWARD)
PHOENIX_CAVE_DRAGON = NameBit("Phoenix Cave Dragon", event_bit.DEFEATED_PHOENIX_CAVE_DRAGON, ITEM_REWARD)

# Checks
all_checks = [
    AUCTION1,
    AUCTION2,
    ANCIENT_CASTLE,
    BAREN_FALLS,
    BURNING_HOUSE,
    COLLAPSING_HOUSE,
    DARYLS_TOMB,
    DOMA_SIEGE,
    DOMA_DREAM_DOOR,
    DOMA_DREAM_AWAKEN,
    DOMA_DREAM_THRONE,
    EBOTS_ROCK,
    ESPER_MOUNTAIN,
    FANATICS_TOWER_FOLLOWER,
    FANATICS_TOWER_LEADER,
    FIGARO_CASTLE_THRONE,
    FIGARO_CASTLE_ENGINE,
    FLOATING_CONT_ARRIVE,
    FLOATING_CONT_BEAST,
    FLOATING_CONT_ESCAPE,
    GAUS_FATHERS_HOUSE,
    IMPERIAL_CAMP,
    KOHLINGEN_CAFE,
    LETE_RIVER,
    LONE_WOLF_CHASE,
    LONE_WOLF_MOOGLE_ROOM,
    MAGITEK_FACTORY_TRASH,
    MAGITEK_FACTORY_GUARD,
    MAGITEK_FACTORY_FINISH,
    MOBLIZ_ATTACK,
    MT_KOLTS,
    MT_ZOZO,
    NARSHE_BATTLE,
    NARSHE_WEAPON_SHOP,
    NARSHE_WEAPON_SHOP_MINES,
    OPERA_HOUSE_DISRUPTION,
    OWZERS_MANSION,
    PHANTOM_TRAIN,
    PHOENIX_CAVE,
    SEALED_GATE,
    SEARCH_THE_SKIES,
    SERPENT_TRENCH,
    SOUTH_FIGARO_PRISONER,
    SOUTH_FIGARO_CAVE,
    TRITOCH_CLIFF,
    TZEN_THIEF,
    UMAROS_CAVE,
    VELDT,
    VELDT_CAVE,
    WHELK_GATE,
    ZONE_EATER,
    ZOZO_TOWER,

    # Dragons
    ANCIENT_CASTLE_DRAGON,
    FANATICS_TOWER_DRAGON,
    KEFKAS_TOWER_DRAGON_G,
    KEFKAS_TOWER_DRAGON_S,
    MT_ZOZO_DRAGON,
    NARSHE_DRAGON,
    OPERA_HOUSE_DRAGON,
    PHOENIX_CAVE_DRAGON,

    # KT
    KEFKAS_TOWER_CELL_BEAST,
]

check_name = {check.bit: check.name for (idx, check) in enumerate(all_checks)}
name_check = {check.name: check.bit for (idx, check) in enumerate(all_checks)}
check_reward = {check.bit: check.reward_types for (idx, check) in enumerate(all_checks)}

CELES = [
    MAGITEK_FACTORY_TRASH,
    MAGITEK_FACTORY_GUARD,
    MAGITEK_FACTORY_FINISH,
    OPERA_HOUSE_DISRUPTION,
    SOUTH_FIGARO_PRISONER,
]
CYAN = [
    DOMA_SIEGE,
    DOMA_DREAM_DOOR,
    DOMA_DREAM_AWAKEN,
    DOMA_DREAM_THRONE,
]
EDGAR = [
    ANCIENT_CASTLE,
    FIGARO_CASTLE_THRONE,
    FIGARO_CASTLE_ENGINE,
]
GAU = [
    VELDT,
    SERPENT_TRENCH
]
GOGO = [
    ZONE_EATER
]
LOCKE = [
    NARSHE_WEAPON_SHOP,
    NARSHE_WEAPON_SHOP_MINES,
    SOUTH_FIGARO_CAVE,
    PHOENIX_CAVE,
]
MOG = [
    LONE_WOLF_CHASE,
    LONE_WOLF_MOOGLE_ROOM,
]
RELM = [
    ESPER_MOUNTAIN,
    OWZERS_MANSION,
]
SABIN = [
    BAREN_FALLS,
    COLLAPSING_HOUSE,
    IMPERIAL_CAMP,
    MT_KOLTS,
    PHANTOM_TRAIN,
]
SETZER = [
    DARYLS_TOMB,
    KOHLINGEN_CAFE,
    SEARCH_THE_SKIES,
]
SHADOW = [
    FLOATING_CONT_ARRIVE,
    FLOATING_CONT_BEAST,
    FLOATING_CONT_ESCAPE,
]
STRAGO = [
    BURNING_HOUSE,
    EBOTS_ROCK,
    FANATICS_TOWER_FOLLOWER,
    FANATICS_TOWER_LEADER, # allow getting the chest at top without getting strago
]
TERRA = [
    LETE_RIVER,
    MOBLIZ_ATTACK,
    SEALED_GATE,
    WHELK_GATE,
    ZOZO_TOWER,
]
UMARO = [
    UMAROS_CAVE
]

UNGATED = [
    AUCTION1,
    AUCTION2,
    TZEN_THIEF,

    ## Ungated Boss battled
    NARSHE_BATTLE,
    TRITOCH_CLIFF,

    # KT
    KEFKAS_TOWER_CELL_BEAST,
]
# Dragons
DRAGONS = [
    ANCIENT_CASTLE_DRAGON,
    FANATICS_TOWER_DRAGON,
    KEFKAS_TOWER_DRAGON_G,
    KEFKAS_TOWER_DRAGON_S,
    MT_ZOZO_DRAGON,
    NARSHE_DRAGON,
    OPERA_HOUSE_DRAGON,
    PHOENIX_CAVE_DRAGON,
]