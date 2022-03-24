from data.magitek import Magitek
from data.ability_data import AbilityData
from data.structures import DataBits, DataArray

from memory.space import Bank, Reserve, Allocate, Write

class Magiteks:
    MAGITEK_COUNT = 8
    FIRE_BEAM, BOLT_BEAM, ICE_BEAM, BIO_BLAST, HEAL_FORCE, CONFUSER, X_FER, TEKMISSILE = range(MAGITEK_COUNT)
    DISABLED_MAGITEK = 0xFF

    NAMES_START = 0x26f9ad 
    NAMES_END = 0x26f9fc
    NAME_SIZE = 10

    ABILITY_DATA_START = 0x0471ea
    ABILITY_DATA_END = 0x047259

    # These 8 bytes control the Magitek that Terra can use
    TERRA_MAGITEK_ATTACKS_START = 0x1910C
    TERRA_MAGITEK_ATTACKS_END = 0x19113
    # These 8 bytes control the Magitek that other characters can use
    OTHER_CHAR_MAGITEK_ATTACKS_START = 0x19114
    OTHER_CHAR_MAGITEK_ATTACKS_END = 0x1911B
    MAGITEK_ATTACKS_SIZE = 1

    def __init__(self, rom, args):
        self.rom = rom
        self.args = args

        self.name_data = DataArray(self.rom, self.NAMES_START, self.NAMES_END, self.NAME_SIZE)
        self.ability_data = DataArray(self.rom, self.ABILITY_DATA_START, self.ABILITY_DATA_END, AbilityData.DATA_SIZE)
        self.other_char_magitek_attacks = DataArray(self.rom, self.OTHER_CHAR_MAGITEK_ATTACKS_START, self.OTHER_CHAR_MAGITEK_ATTACKS_END, self.MAGITEK_ATTACKS_SIZE)

        self.magiteks = []
        for magitek_index in range(len(self.ability_data)):
            magitek = Magitek(magitek_index, self.name_data[magitek_index], self.ability_data[magitek_index])
            self.magiteks.append(magitek)

    def fix_reflectable_beams(self):
        # Set the Fire/Bolt/Ice beams to ignore reflect to avoid graphical glitches
        self.magiteks[self.FIRE_BEAM].flags2 = 0x22
        self.magiteks[self.BOLT_BEAM].flags2 = 0x22
        self.magiteks[self.ICE_BEAM].flags2 = 0x22

    def give_all_magiteks(self):
        # Give all magitek abilities to every character, not just Terra
        # FF = disabled
        # 0 = Fire Beam, ... 7 = TekMissile
        self.other_char_magitek_attacks[self.BIO_BLAST] = self.BIO_BLAST.to_bytes(1, 'little')
        self.other_char_magitek_attacks[self.CONFUSER] = self.CONFUSER.to_bytes(1, 'little')
        self.other_char_magitek_attacks[self.X_FER] = self.X_FER.to_bytes(1, 'little')
        self.other_char_magitek_attacks[self.TEKMISSILE] = self.TEKMISSILE.to_bytes(1, 'little')

    def mod(self):
        self.fix_reflectable_beams()
        self.give_all_magiteks()
        pass

    def write(self):
        if self.args.spoiler_log:
            self.log()

        for magitek_index, magitek in enumerate(self.magiteks):
            self.name_data[magitek_index] = magitek.name_data()
            self.ability_data[magitek_index] = magitek.ability_data()

        self.name_data.write()
        self.ability_data.write()
        self.other_char_magitek_attacks.write()

    def log(self):
        pass

    def print(self):
        for magitek in self.magiteks:
            magitek.print()
