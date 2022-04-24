from collections import namedtuple
import data.event_bit as event_bit
import data.npc_bit as npc_bit

NameBit = namedtuple("NameBit", ["name", "bit", "free"], defaults={
    'free': False
})

AUCTION1 = NameBit("Auction1", event_bit.AUCTION_BOUGHT_ESPER1)
AUCTION2 = NameBit("Auction2", event_bit.AUCTION_BOUGHT_ESPER2)
ANCIENT_CASTLE = NameBit("Ancient Castle", event_bit.GOT_RAIDEN)
ANCIENT_CASTLE_DRAGON = NameBit("Ancient Castle Dragon", event_bit.DEFEATED_ANCIENT_CASTLE_DRAGON)
BAREN_FALLS = NameBit("Baren Falls", event_bit.NAMED_GAU)
BURNING_HOUSE = NameBit("Burning House", event_bit.DEFEATED_FLAME_EATER)
COLLAPSING_HOUSE = NameBit("Collapsing House", event_bit.FINISHED_COLLAPSING_HOUSE)
DARYLS_TOMB = NameBit("Daryl's Tomb", event_bit.DEFEATED_DULLAHAN)
DOMA_SIEGE = NameBit("Doma Siege", event_bit.FINISHED_DOMA_WOB)
DOMA_DREAM_DOOR = NameBit("Doma Dream Door", event_bit.DEFEATED_STOOGES)
DOMA_DREAM_AWAKEN = NameBit("Doma Dream Awaken", event_bit.FINISHED_DOMA_WOR)
DOMA_DREAM_THRONE = NameBit("Doma Dream Throne", event_bit.GOT_ALEXANDR)
EBOTS_ROCK = NameBit("Ebot's Rock", event_bit.DEFEATED_HIDON)
ESPER_MOUNTAIN = NameBit("Esper Mountain", event_bit.DEFEATED_ULTROS_ESPER_MOUNTAIN)
FANATICS_TOWER_DRAGON = NameBit("Fanatic's Tower Dragon", event_bit.DEFEATED_FANATICS_TOWER_DRAGON)
FANATICS_TOWER_LEADER = NameBit("Fanatic's Tower Leader", event_bit.DEFEATED_MAGIMASTER)
FANATICS_TOWER_FOLLOWER = NameBit("Fanatic's Tower Follower", event_bit.RECRUITED_STRAGO_FANATICS_TOWER)
FIGARO_CASTLE_THRONE = NameBit("Figaro Castle Throne", event_bit.NAMED_EDGAR)
FIGARO_CASTLE_ENGINE = NameBit("Figaro Castle Engine", event_bit.DEFEATED_TENTACLES_FIGARO)
FLOATING_CONT_ARRIVE = NameBit("Floating Cont. Arrive", event_bit.RECRUITED_SHADOW_FLOATING_CONTINENT)
FLOATING_CONT_BEAST = NameBit("Floating Cont. Beast", event_bit.DEFEATED_ATMAWEAPON)
FLOATING_CONT_ESCAPE = NameBit("Floating Cont. Escape", event_bit.FINISHED_FLOATING_CONTINENT)
GAUS_FATHERS_HOUSE = NameBit("Gau's Father's House", event_bit.RECRUITED_SHADOW_GAU_FATHER_HOUSE)
IMPERIAL_CAMP = NameBit("Imperial Camp", event_bit.FINISHED_IMPERIAL_CAMP)
KEFKAS_TOWER_CELL_BEAST = NameBit("Kefka's Tower Cell Beast", event_bit.DEFEATED_ATMA)
KEFKAS_TOWER_DRAGON_G = NameBit("Kefka's Tower Dragon G", event_bit.DEFEATED_KEFKA_TOWER_DRAGON_G)
KEFKAS_TOWER_DRAGON_S = NameBit("Kefka's Tower Dragon S", event_bit.DEFEATED_KEFKA_TOWER_DRAGON_S)
KOHLINGEN_CAFE = NameBit("Kohlingen Cafe", event_bit.RECRUITED_SHADOW_KOHLINGEN)
LETE_RIVER = NameBit("Lete River", event_bit.RODE_RAFT_LETE_RIVER)
LONE_WOLF_CHASE = NameBit("Lone Wolf Chase", event_bit.CHASING_LONE_WOLF7)
LONE_WOLF_MOOGLE_ROOM = NameBit("Lone Wolf Moogle Room", event_bit.GOT_BOTH_REWARDS_LONE_WOLF)
MAGITEK_FACTORY_TRASH = NameBit("Magitek Factory Trash", event_bit.GOT_IFRIT_SHIVA)
MAGITEK_FACTORY_GUARD = NameBit("Magitek Factory Guard", event_bit.DEFEATED_NUMBER_024)
MAGITEK_FACTORY_FINISH = NameBit("Magitek Factory Finish", event_bit.DEFEATED_CRANES)
MOBLIZ_ATTACK = NameBit("Mobliz Attack", event_bit.RECRUITED_TERRA_MOBLIZ)
MT_KOLTS = NameBit("Mt. Kolts", event_bit.DEFEATED_VARGAS)
MT_ZOZO = NameBit("Mt. Zozo", event_bit.FINISHED_MT_ZOZO)
MT_ZOZO_DRAGON = NameBit("Mt. Zozo Dragon", event_bit.DEFEATED_MT_ZOZO_DRAGON)
NARSHE_BATTLE = NameBit("Narshe Battle", event_bit.FINISHED_NARSHE_BATTLE)
NARSHE_DRAGON = NameBit("Narshe Dragon", event_bit.DEFEATED_NARSHE_DRAGON)
NARSHE_WEAPON_SHOP = NameBit("Narshe Weapon Shop", event_bit.GOT_RAGNAROK)
NARSHE_WEAPON_SHOP_MINES = NameBit("Narshe Weapon Shop Mines", event_bit.GOT_BOTH_REWARDS_WEAPON_SHOP)
OPERA_HOUSE_DISRUPTION = NameBit("Opera House Disruption", event_bit.FINISHED_OPERA_DISRUPTION)
OPERA_HOUSE_DRAGON = NameBit("Opera House Dragon", event_bit.DEFEATED_OPERA_HOUSE_DRAGON)
OWZERS_MANSION = NameBit("Owzer's Mansion", event_bit.DEFEATED_CHADARNOOK)
PHANTOM_TRAIN = NameBit("Phantom Train", event_bit.GOT_PHANTOM_TRAIN_REWARD)
PHOENIX_CAVE = NameBit("Phoenix Cave", event_bit.RECRUITED_LOCKE_PHOENIX_CAVE)
PHOENIX_CAVE_DRAGON = NameBit("Phoenix Cave Dragon", event_bit.DEFEATED_PHOENIX_CAVE_DRAGON)
SEALED_GATE = NameBit("Sealed Gate", npc_bit.BLOCK_SEALED_GATE)
SEARCH_THE_SKIES = NameBit("Search The Skies", event_bit.DEFEATED_DOOM_GAZE)
SERPENT_TRENCH = NameBit("Serpent Trench", event_bit.GOT_SERPENT_TRENCH_REWARD)
SOUTH_FIGARO_PRISONER = NameBit("South Figaro Prisoner", event_bit.FREED_CELES)
SOUTH_FIGARO_CAVE = NameBit("South Figaro Cave", event_bit.DEFEATED_TUNNEL_ARMOR)
TRITOCH_CLIFF = NameBit("Tritoch Cliff", event_bit.GOT_TRITOCH)
TZEN_THIEF = NameBit("Tzen Thief", event_bit.BOUGHT_ESPER_TZEN)
UMAROS_CAVE = NameBit("Umaro's Cave", event_bit.RECRUITED_UMARO_WOR)
VELDT = NameBit("Veldt", event_bit.VELDT_REWARD_OBTAINED)
VELDT_CAVE = NameBit("Veldt Cave", event_bit.DEFEATED_SR_BEHEMOTH)
WHELK_GATE = NameBit("Whelk Gate", event_bit.DEFEATED_WHELK)
ZONE_EATER = NameBit("Zone Eater", event_bit.RECRUITED_GOGO_WOR)
ZOZO_TOWER = NameBit("Zozo Tower", event_bit.GOT_ZOZO_REWARD)

# Checks that are only able to give items
item_check_name = {
    # dragons
    ANCIENT_CASTLE_DRAGON.bit: ANCIENT_CASTLE_DRAGON.name,
    FANATICS_TOWER_DRAGON.bit: FANATICS_TOWER_DRAGON.name,
    KEFKAS_TOWER_DRAGON_G.bit: KEFKAS_TOWER_DRAGON_G.name,
    KEFKAS_TOWER_DRAGON_S.bit: KEFKAS_TOWER_DRAGON_S.name,
    MT_ZOZO_DRAGON.bit: MT_ZOZO_DRAGON.name,
    NARSHE_DRAGON.bit: NARSHE_DRAGON.name,
    OPERA_HOUSE_DRAGON.bit: OPERA_HOUSE_DRAGON.name,
    PHOENIX_CAVE_DRAGON.bit: PHOENIX_CAVE_DRAGON.name,

    # kt bosses
    KEFKAS_TOWER_CELL_BEAST.bit: KEFKAS_TOWER_CELL_BEAST.name,

    # secondary quest objectives
    LONE_WOLF_MOOGLE_ROOM.bit: LONE_WOLF_MOOGLE_ROOM.name,
    FANATICS_TOWER_LEADER.bit: FANATICS_TOWER_LEADER.name,
    NARSHE_WEAPON_SHOP_MINES.bit: NARSHE_WEAPON_SHOP_MINES.name,
}

# Checks that can give either character/esper/item
character_esper_check_name = {
    AUCTION1.bit:               AUCTION1.name,
    AUCTION2.bit:               AUCTION2.name,
    ANCIENT_CASTLE.bit:         ANCIENT_CASTLE.name,
    BAREN_FALLS.bit:            BAREN_FALLS.name,
    BURNING_HOUSE.bit:          BURNING_HOUSE.name,
    COLLAPSING_HOUSE.bit:       COLLAPSING_HOUSE.name,
    DARYLS_TOMB.bit:            DARYLS_TOMB.name,
    DOMA_SIEGE.bit:             DOMA_SIEGE.name,
    DOMA_DREAM_DOOR.bit:        DOMA_DREAM_DOOR.name,
    DOMA_DREAM_AWAKEN.bit:      DOMA_DREAM_AWAKEN.name,
    DOMA_DREAM_THRONE.bit:      DOMA_DREAM_THRONE.name,
    EBOTS_ROCK.bit:             EBOTS_ROCK.name,
    ESPER_MOUNTAIN.bit:         ESPER_MOUNTAIN.name,
    FANATICS_TOWER_FOLLOWER.bit:FANATICS_TOWER_FOLLOWER.name,
    FIGARO_CASTLE_THRONE.bit:   FIGARO_CASTLE_THRONE.name,
    FIGARO_CASTLE_ENGINE.bit:   FIGARO_CASTLE_ENGINE.name,
    FLOATING_CONT_ARRIVE.bit:   FLOATING_CONT_ARRIVE.name,
    FLOATING_CONT_BEAST.bit:    FLOATING_CONT_BEAST.name,
    FLOATING_CONT_ESCAPE.bit:   FLOATING_CONT_ESCAPE.name,
    GAUS_FATHERS_HOUSE.bit:     GAUS_FATHERS_HOUSE.name,
    IMPERIAL_CAMP.bit:          IMPERIAL_CAMP.name,
    KOHLINGEN_CAFE.bit:         KOHLINGEN_CAFE.name,
    LETE_RIVER.bit:             LETE_RIVER.name,
    LONE_WOLF_CHASE.bit:        LONE_WOLF_CHASE.name,
    MAGITEK_FACTORY_TRASH.bit:  MAGITEK_FACTORY_TRASH.name,
    MAGITEK_FACTORY_GUARD.bit:  MAGITEK_FACTORY_GUARD.name,
    MAGITEK_FACTORY_FINISH.bit: MAGITEK_FACTORY_FINISH.name,
    MOBLIZ_ATTACK.bit:          MOBLIZ_ATTACK.name,
    MT_KOLTS.bit:               MT_KOLTS.name,
    MT_ZOZO.bit:                MT_ZOZO.name,
    NARSHE_BATTLE.bit:          NARSHE_BATTLE.name,
    NARSHE_WEAPON_SHOP.bit:     NARSHE_WEAPON_SHOP.name,
    OPERA_HOUSE_DISRUPTION.bit: OPERA_HOUSE_DISRUPTION.name,
    OWZERS_MANSION.bit:         OWZERS_MANSION.name,
    PHANTOM_TRAIN.bit:          PHANTOM_TRAIN.name,
    PHOENIX_CAVE.bit:           PHOENIX_CAVE.name,
    SEALED_GATE.bit:            SEALED_GATE.name,
    SEARCH_THE_SKIES.bit:       SEARCH_THE_SKIES.name,
    SERPENT_TRENCH.bit:         SERPENT_TRENCH.name,
    SOUTH_FIGARO_PRISONER.bit:  SOUTH_FIGARO_PRISONER.name,
    SOUTH_FIGARO_CAVE.bit:      SOUTH_FIGARO_CAVE.name,
    TRITOCH_CLIFF.bit:          TRITOCH_CLIFF.name,
    TZEN_THIEF.bit:             TZEN_THIEF.name,
    UMAROS_CAVE.bit:            UMAROS_CAVE.name,
    VELDT.bit:                  VELDT.name,
    VELDT_CAVE.bit:             VELDT_CAVE.name,
    WHELK_GATE.bit:             WHELK_GATE.name,
    ZONE_EATER.bit:             ZONE_EATER.name,
    ZOZO_TOWER.bit:             ZOZO_TOWER.name,
}

all_checks_check_name = character_esper_check_name.copy()
all_checks_check_name.update(item_check_name)

character_esper_name_check = {v: k for k, v in character_esper_check_name.items()}

CYAN = [
    DOMA_SIEGE,
    DOMA_DREAM_DOOR,
    DOMA_DREAM_AWAKEN,
    DOMA_DREAM_THRONE,
]
EDGAR = [
    ANCIENT_CASTLE,
    ANCIENT_CASTLE_DRAGON,
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
    FANATICS_TOWER_LEADER, # allow getting the chest at top without getting strago

    # KT
    KEFKAS_TOWER_CELL_BEAST,

    # dragons
    FANATICS_TOWER_DRAGON,
    KEFKAS_TOWER_DRAGON_G,
    KEFKAS_TOWER_DRAGON_S,
    OPERA_HOUSE_DRAGON,
    PHOENIX_CAVE_DRAGON,
]
