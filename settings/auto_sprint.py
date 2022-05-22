from memory.space import Reserve
import instruction.asm as asm
import args

class AutoSprint:
    def __init__(self):
        if args.auto_sprint:
            self.mod()

    def mod(self):
        # set sprint by default, b button to walk, sprint shoes do nothing

        WALK_SPEED = 2
        SPRINT_SPEED = 3

        CONTROLLER1_BYTE2 = 0x4219
        B_BUTTON_MASK = 0x80
        FIELD_RAM_SPEED = 0x0875

        src = [
            asm.LDA(CONTROLLER1_BYTE2, asm.ABS),
            asm.AND(B_BUTTON_MASK, asm.IMM8),
            asm.BNE("WALK"), # branch if b button down

            "SPRINT",
            asm.LDA(SPRINT_SPEED, asm.IMM8),
            asm.BRA("STORE_SPEED"),

            "WALK",
            asm.LDA(WALK_SPEED, asm.IMM8),

            "STORE_SPEED",
            asm.STA(FIELD_RAM_SPEED, asm.ABS_Y),
        ]
        space = Reserve(0x04e21, 0x04e37, "auto sprint", asm.NOP())
        space.write(src)
