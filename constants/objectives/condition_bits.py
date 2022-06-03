import data.event_bit as event_bit
import data.npc_bit as npc_bit
import data.battle_bit as battle_bit
from data.bosses import normal_formation_name, dragon_formation_name

from collections import namedtuple
NameBit = namedtuple("NameBit", ["name", "bit"])

check_bit = [
    NameBit("Ancient Castle", event_bit.GOT_RAIDEN),
    NameBit("Ancient Castle Dragon", event_bit.DEFEATED_ANCIENT_CASTLE_DRAGON),
    NameBit("Baren Falls", event_bit.NAMED_GAU),
    NameBit("Burning House", event_bit.DEFEATED_FLAME_EATER),
    NameBit("Collapsing House", event_bit.FINISHED_COLLAPSING_HOUSE),
    NameBit("Daryl's Tomb", event_bit.DEFEATED_DULLAHAN),
    NameBit("Doma Siege", event_bit.FINISHED_DOMA_WOB),
    NameBit("Doma Dream Door", event_bit.DEFEATED_STOOGES),
    NameBit("Doma Dream Awaken", event_bit.FINISHED_DOMA_WOR),
    NameBit("Doma Dream Throne", event_bit.GOT_ALEXANDR),
    NameBit("Ebot's Rock", event_bit.DEFEATED_HIDON),
    NameBit("Esper Mountain", event_bit.DEFEATED_ULTROS_ESPER_MOUNTAIN),
    NameBit("Fanatic's Tower Dragon", event_bit.DEFEATED_FANATICS_TOWER_DRAGON),
    NameBit("Fanatic's Tower Leader", event_bit.DEFEATED_MAGIMASTER),
    NameBit("Fanatic's Tower Follower", event_bit.RECRUITED_STRAGO_FANATICS_TOWER),
    NameBit("Figaro Castle Throne", event_bit.NAMED_EDGAR),
    NameBit("Figaro Castle Engine", event_bit.DEFEATED_TENTACLES_FIGARO),
    NameBit("Floating Cont. Arrive", event_bit.RECRUITED_SHADOW_FLOATING_CONTINENT),
    NameBit("Floating Cont. Beast", event_bit.DEFEATED_ATMAWEAPON),
    NameBit("Floating Cont. Escape", event_bit.FINISHED_FLOATING_CONTINENT),
    NameBit("Gau's Father's House", event_bit.RECRUITED_SHADOW_GAU_FATHER_HOUSE),
    NameBit("Imperial Camp", event_bit.FINISHED_IMPERIAL_CAMP),
    NameBit("Kefka's Tower Cell Beast", event_bit.DEFEATED_ATMA),
    NameBit("Kefka's Tower Dragon G", event_bit.DEFEATED_KEFKA_TOWER_DRAGON_G),
    NameBit("Kefka's Tower Dragon S", event_bit.DEFEATED_KEFKA_TOWER_DRAGON_S),
    NameBit("Kohlingen Cafe", event_bit.RECRUITED_SHADOW_KOHLINGEN),
    NameBit("Lete River", event_bit.RODE_RAFT_LETE_RIVER),
    NameBit("Lone Wolf Chase", event_bit.CHASING_LONE_WOLF7),
    NameBit("Lone Wolf Moogle Room", event_bit.GOT_BOTH_REWARDS_LONE_WOLF),
    NameBit("Magitek Factory Trash", event_bit.GOT_IFRIT_SHIVA),
    NameBit("Magitek Factory Guard", event_bit.DEFEATED_NUMBER_024),
    NameBit("Magitek Factory Finish", event_bit.DEFEATED_CRANES),
    NameBit("Mobliz Attack", event_bit.RECRUITED_TERRA_MOBLIZ),
    NameBit("Mt. Kolts", event_bit.DEFEATED_VARGAS),
    NameBit("Mt. Zozo", event_bit.FINISHED_MT_ZOZO),
    NameBit("Mt. Zozo Dragon", event_bit.DEFEATED_MT_ZOZO_DRAGON),
    NameBit("Narshe Battle", event_bit.FINISHED_NARSHE_BATTLE),
    NameBit("Narshe Dragon", event_bit.DEFEATED_NARSHE_DRAGON),
    NameBit("Narshe Weapon Shop", event_bit.GOT_RAGNAROK),
    NameBit("Narshe Weapon Shop Mines", event_bit.GOT_BOTH_REWARDS_WEAPON_SHOP),
    NameBit("Opera House Disruption", event_bit.FINISHED_OPERA_DISRUPTION),
    NameBit("Opera House Dragon", event_bit.DEFEATED_OPERA_HOUSE_DRAGON),
    NameBit("Owzer's Mansion", event_bit.DEFEATED_CHADARNOOK),
    NameBit("Phantom Train", event_bit.GOT_PHANTOM_TRAIN_REWARD),
    NameBit("Phoenix Cave", event_bit.RECRUITED_LOCKE_PHOENIX_CAVE),
    NameBit("Phoenix Cave Dragon", event_bit.DEFEATED_PHOENIX_CAVE_DRAGON),
    NameBit("Sealed Gate", npc_bit.BLOCK_SEALED_GATE),
    NameBit("Search The Skies", event_bit.DEFEATED_DOOM_GAZE),
    NameBit("Serpent Trench", event_bit.GOT_SERPENT_TRENCH_REWARD),
    NameBit("South Figaro Prisoner", event_bit.FREED_CELES),
    NameBit("South Figaro Cave", event_bit.DEFEATED_TUNNEL_ARMOR),
    NameBit("Tritoch Cliff", event_bit.GOT_TRITOCH),
    NameBit("Tzen Thief", event_bit.BOUGHT_ESPER_TZEN),
    NameBit("Umaro's Cave", event_bit.RECRUITED_UMARO_WOR),
    NameBit("Veldt", event_bit.VELDT_REWARD_OBTAINED),
    NameBit("Veldt Cave", event_bit.DEFEATED_SR_BEHEMOTH),
    NameBit("Whelk Gate", event_bit.DEFEATED_WHELK),
    NameBit("Zone Eater", event_bit.RECRUITED_GOGO_WOR),
    NameBit("Zozo Tower", event_bit.GOT_ZOZO_REWARD),
]

check_bit += [                                                          # Index
    NameBit("Kefka's Tower Ambush", event_bit.DEFEATED_INFERNO),        # 59
    NameBit("Kefka's Tower Guardian", event_bit.DEFEATED_GUARDIAN),     # 60
    NameBit("KT Left Triad Statue", event_bit.DEFEATED_DOOM),           # 61
    NameBit("KT Mid Triad Statue", event_bit.DEFEATED_POLTERGEIST),      # 62
    NameBit("KT Right Triad Statue", event_bit.DEFEATED_GODDESS),       # 63
]

quest_bit = [
    NameBit("Defeat Sealed Cave Ninja", event_bit.DEFEATED_NINJA_CAVE_TO_SEALED_GATE),
    NameBit("Help Injured Lad", event_bit.HELPED_INJURED_LAD),
    NameBit("Let Cid Die", event_bit.CID_DIED),
    NameBit("Pass Security Checkpoint", event_bit.FINISHED_NARSHE_CHECKPOINT),
    NameBit("Perform In Opera", event_bit.FINISHED_OPERA_PERFORMANCE),
    NameBit("Save Cid", event_bit.CID_SURVIVED),
    NameBit("Set Zozo Clock", event_bit.SET_ZOZO_CLOCK),
    NameBit("Suplex A Train", event_bit.SUPLEXED_TRAIN),
    NameBit("Win An Auction", event_bit.WON_AN_AUCTION),
    NameBit("Win A Coliseum Match", event_bit.WON_A_COLISEUM_MATCH),
]

boss_bit = []
for formation_id in sorted(normal_formation_name, key = normal_formation_name.get):
    boss_bit.append(NameBit(normal_formation_name[formation_id], battle_bit.boss_defeated(formation_id)))

dragon_bit = []
for formation_id in sorted(dragon_formation_name, key = dragon_formation_name.get):
    dragon_bit.append(NameBit(dragon_formation_name[formation_id], battle_bit.dragon_defeated(formation_id)))
