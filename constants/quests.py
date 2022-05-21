from collections import namedtuple
import data.event_bit as event_bit

NameBit = namedtuple("NameBit", ["name", "bit"])

DEFEAT_SEALED_CAVE_NINJA = NameBit("Defeat Sealed Cave Ninja", event_bit.DEFEATED_NINJA_CAVE_TO_SEALED_GATE)
HELP_INJURED_LAD = NameBit("Help Injured Lad", event_bit.HELPED_INJURED_LAD)
LET_CID_DIE = NameBit("Let Cid Die", event_bit.CID_DIED)
PASS_SECURITY_CHECKPOINT = NameBit("Pass Security Checkpoint", event_bit.FINISHED_NARSHE_CHECKPOINT)
PERFORM_IN_OPERA = NameBit("Perform In Opera", event_bit.FINISHED_OPERA_PERFORMANCE)
SAVE_CID = NameBit("Save Cid", event_bit.CID_SURVIVED)
SET_ZOZO_CLOCK = NameBit("Set Zozo Clock", event_bit.SET_ZOZO_CLOCK)
SUPLEX_A_TRAIN = NameBit("Suplex A Train", event_bit.SUPLEXED_TRAIN)
WIN_AN_AUCTION = NameBit("Win An Auction", event_bit.WON_AN_AUCTION)
WIN_A_COLISEUM_MATCH = NameBit("Win A Coliseum Match", event_bit.WON_A_COLISEUM_MATCH)
