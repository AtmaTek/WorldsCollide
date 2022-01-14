from data.spell import Spell
from data.spell_names import id_name, name_id
from data.ability_data import AbilityData
from data.structures import DataArray

class Spells:
    BLACK_MAGIC_COUNT = 24
    EFFECT_MAGIC_COUNT = 21
    WHITE_MAGIC_COUNT = 9
    SPELL_COUNT = BLACK_MAGIC_COUNT + EFFECT_MAGIC_COUNT + WHITE_MAGIC_COUNT

    NAMES_START = 0x26f567
    NAMES_END = 0x26f6e0
    NAME_SIZE = 7

    ABILITY_DATA_START = 0x046ac0
    ABILITY_DATA_END = 0x046db3

    # (default) order spells appear in menu going left to right, top to bottom
    # put white magic before black and effect magic
    import itertools
    spell_menu_order = itertools.chain(range(45, 54), range(45))

    def __init__(self, rom, args):
        self.rom = rom
        self.args = args

        self.name_data = DataArray(self.rom, self.NAMES_START, self.NAMES_END, self.NAME_SIZE)
        self.ability_data = DataArray(self.rom, self.ABILITY_DATA_START, self.ABILITY_DATA_END, AbilityData.DATA_SIZE)

        self.spells = []
        for spell_index in range(len(self.name_data)):
            spell = Spell(spell_index, self.name_data[spell_index], self.ability_data[spell_index])
            self.spells.append(spell)

    def get_id(self, name):
        return name_id[name]

    def get_name(self, id):
        if id == 0xff:
            return ""
        return self.spells[id].get_name()

    def get_random(self, count = 1, exclude = None):
        if exclude is None:
            exclude = []

        import random
        possible_spell_ids = [spell.id for spell in self.spells if spell.id not in exclude]
        return random.sample(possible_spell_ids, count)

    def no_mp_scan(self):
        scan_id = name_id["Scan"]
        self.spells[scan_id].mp = 0

    def mod(self):
        if self.args.scan_all:
            self.no_mp_scan()

    def write(self):
        for spell_index, spell in enumerate(self.spells):
            self.name_data[spell_index] = spell.name_data()
            self.ability_data[spell_index] = spell.ability_data()

        self.name_data.write()
        self.ability_data.write()

    def print(self):
        for spell in self.spells:
            spell.print()
