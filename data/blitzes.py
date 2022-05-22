from data.blitz import Blitz
from data.structures import DataArray

from memory.space import Bank, Reserve, Allocate, Write, Read
import instruction.asm as asm

class Blitzes:
    LEVELS_START = 0x26f498
    LEVELS_END = 0x26f49f

    def __init__(self, rom, args, characters):
        self.rom = rom
        self.args = args
        self.characters = characters

        self.levels = DataArray(self.rom, self.LEVELS_START, self.LEVELS_END, Blitz.LEVEL_SIZE)

        self.blitzes = []
        for blitz_index in range(len(self.levels)):
            blitz = Blitz(blitz_index, self.levels[blitz_index])
            self.blitzes.append(blitz)

    def write_learners_table(self):
        self.learners = self.characters.get_characters_with_command("Blitz")

        space = Allocate(Bank.CF, self.characters.CHARACTER_COUNT, "blitz learners")
        space.write(self.learners)

        self.learners_table = space.start_address
        self.learners_table_end = self.learners_table + len(self.learners)

    def write_is_learner(self):
        import instruction.c0 as c0

        src = [
            asm.PHY(),
            asm.LDX(self.learners_table_end, asm.IMM16),    # offset in bank to last learner in table + 1
            asm.LDY(len(self.learners), asm.IMM16),         # learners table size
            asm.JSR(c0.is_skill_learner, asm.ABS),
            asm.PLY(),
            asm.RTL(),
        ]
        space = Write(Bank.C0, src, "blitz is learner")
        self.is_learner_function = space.start_address_snes

    def event_check_mod(self):
        from memory.space import START_ADDRESS_SNES
        import instruction.c0 as c0

        learn_blitzes = 0x0a201
        character_recruited = c0.character_recruited + START_ADDRESS_SNES

        space = Allocate(Bank.C0, 24, "blitz event check", asm.NOP())
        space.write(
            asm.PHA(),
            asm.JSL(character_recruited),
            asm.CMP(0x00, asm.IMM8),        # compare result with 0
            asm.BEQ("RETURN"),              # branch if character not recruited
        )
        if not self.args.blitzes_everyone_learns:
            space.write(
                asm.PLA(),
                asm.PHA(),
                asm.JSL(self.is_learner_function),
                asm.CMP(0x00, asm.IMM8),    # compare result with 0
                asm.BEQ("RETURN"),          # branch if character not learner
            )
        space.write(
            asm.JSR(learn_blitzes, asm.ABS),

            "RETURN",
            asm.PLA(),
            asm.RTS(),
        )
        check_blitzes = space.start_address

        space = Reserve(0x0a18e, 0x0a194, "event check sabin learn blitzes", asm.NOP())
        if self.learners:
            space.write(
                asm.JSR(check_blitzes, asm.ABS),
            )

    def after_battle_check_mod(self):
        learn_blitzes = 0x261e7

        space = Allocate(Bank.C2, 31, "blitz check after battle", asm.NOP())
        space.write(
            asm.A16(),
            asm.PHA(),
            asm.A8(),
        )
        if not self.args.blitzes_everyone_learns:
            space.write(
                asm.JSL(self.is_learner_function),
                asm.CMP(0x00, asm.IMM8),            # compare result with 0
                asm.BEQ("RETURN"),                  # branch if character not learner
                asm.A16(),
                asm.PLA(),
                asm.PHA(),
                asm.A8(),
            )
        space.write(
            asm.LDX(0x0008, asm.IMM16),
            asm.JSR(learn_blitzes, asm.ABS),

            "RETURN",
            asm.A16(),
            asm.PLA(),
            asm.A8(),
            asm.RTS(),
        )
        check_blitzes = space.start_address

        space = Reserve(0x261e3, 0x261e6, "battle check sabin learn blitzes", asm.NOP())
        if self.learners:
            space.write(
                asm.JSR(check_blitzes, asm.ABS),
            )
        space.write(
            asm.RTS(),
        )

    def blitzes_learned_event_bit(self):
        # when a new blitz is learned, check if 7 total now learned and if so set event bit

        import data.event_bit as event_bit
        can_learn_byte = 0x1e80 + event_bit.byte(event_bit.CAN_LEARN_BUM_RUSH)
        can_learn_bit = 2 ** event_bit.bit(event_bit.CAN_LEARN_BUM_RUSH)

        src = [
            asm.PHX(),
            asm.PHP(),
            asm.LDA(0x1d28, asm.ABS),           # a = known blitzes
            asm.XY8(),
            asm.JSR(0x520e, asm.ABS),           # x = number known blitzes
            asm.CPX(0x07, asm.IMM8),            # 7 blitzes known? (total learnable except bum rush)
            asm.BLT("RETURN"),                  # branch if < 7 blitzes known
            asm.LDA(can_learn_bit, asm.IMM8),   # load can learn bum rush bit
            asm.TSB(can_learn_byte, asm.ABS),   # set can learn bum rush event bit

            "RETURN",
            asm.PLP(),
            asm.PLX(),

            Read(0x261f1, 0x261f4),
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "check/set blitzes learned event bit")
        check_blitzes_learned = space.start_address

        space = Reserve(0x261f1, 0x261f4, "call check/set blitzes learned event bit", asm.NOP())
        space.write(
            asm.JSR(check_blitzes_learned, asm.ABS),
        )

    def mod(self):
        self.write_learners_table()
        self.write_is_learner()

        self.event_check_mod()
        self.after_battle_check_mod()
        self.blitzes_learned_event_bit()

    def write(self):
        if self.args.spoiler_log:
            self.log()

        for blitz_index, blitz in enumerate(self.blitzes):
            self.levels[blitz_index] = blitz.level

        self.levels.write()

    def log(self):
        pass

    def print(self):
        for blitz in self.blitzes:
            blitz.print()
