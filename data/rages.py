from data.rage import Rage
from data.structures import DataBits, DataArray

class Rages():
    RAGE_COUNT = 256 # 255 available
    DOOM_DRGN_RAGE_ID = 37
    NIGHTSHADE_RAGE_ID = 51
    PUGS_RAGE_ID = 255 # does not appear in rage list, cannot be used

    INITIAL_RAGES_START = 0x47aa0
    INITIAL_RAGES_END = 0x47abf

    ATTACKS_DATA_START = 0xf4600
    ATTACKS_DATA_END = 0xf47ff
    ATTACKS_DATA_SIZE = 2

    def __init__(self, rom, args, enemies):
        self.rom = rom
        self.args = args
        self.enemies = enemies

        self.init_data = DataBits(self.rom, self.INITIAL_RAGES_START, self.INITIAL_RAGES_END)
        self.attack_data = DataArray(self.rom, self.ATTACKS_DATA_START, self.ATTACKS_DATA_END, self.ATTACKS_DATA_SIZE)

        self.rages = []
        for rage_index in range(len(self.attack_data)):
            rage = Rage(rage_index, self.attack_data[rage_index])
            self.rages.append(rage)

    def start_random_rages(self):
        import random

        self.init_data.clear_all()
        possible_rages = [x for x in range(self.RAGE_COUNT) if x != self.PUGS_RAGE_ID]

        number_initial_rages = random.randint(self.args.start_rages_random_min, self.args.start_rages_random_max)
        initial_rages = random.sample(possible_rages, number_initial_rages)
        for rage_id in initial_rages:
            self.init_data[rage_id] = 1

    def no_leap(self):
        from memory.space import Reserve
        import instruction.asm as asm

        space = Reserve(0x23b71, 0x23b8f, "rages leap command", asm.NOP())
        space.add_label("LEAP_MISS", 0x23bc0)
        space.write(
            asm.BRA("LEAP_MISS"),       # if leap command somehow still executed, always branch to miss
        )
        learn_rages = space.next_address
        space.write(
            asm.XY8(),
            asm.JSR(0x4a07, asm.ABS),   # learn rages
            asm.TDC(),                  # replace removed instr before returning
            asm.RTS(),
        )

        space = Reserve(0x25ebd, 0x25ebf, "rages call learn rages after battle", asm.NOP())
        space.write(
            asm.JSR(learn_rages, asm.ABS),
        )

        space = Reserve(0x2543e, 0x25444, "rages add leap command if on veldt", asm.NOP())
        space.add_label("EMPTY_COMMAND_SLOT", 0x25434)
        space.write(
            asm.BRA("EMPTY_COMMAND_SLOT"),
        )

    def no_charm(self):
        # change nightshade charm to special attack (poison pod)
        self.rages[self.NIGHTSHADE_RAGE_ID].attack2 = 239

    def mod(self):
        if self.args.start_rages_random:
            self.start_random_rages()

        if self.args.rages_no_leap:
            self.no_leap()

        if self.args.rages_no_charm:
            self.no_charm()

    def write(self):
        if self.args.spoiler_log:
            self.log()

        for rage_index, rage in enumerate(self.rages):
            self.attack_data[rage_index] = rage.attack_data()

        self.init_data.write()
        self.attack_data.write()

    def log(self):
        from log import section

        lcolumn = []
        rcolumn = []
        for rage_index in range(len(self.init_data)):
            if self.init_data[rage_index] and rage_index != self.PUGS_RAGE_ID:
                enemy_name = self.enemies.get_name(rage_index)

                if rage_index % 2:
                    rcolumn.append(enemy_name)
                else:
                    lcolumn.append(enemy_name)

        section("Start Rages", lcolumn, rcolumn)

    def print(self):
        for rage in self.rages:
            rage.print()
