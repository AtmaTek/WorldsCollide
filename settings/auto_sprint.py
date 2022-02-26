from memory.space import Allocate, Bank, Reserve
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
        DASH_SPEED = 4

        if args.auto_sprint:
            self.mod_auto_sprint(WALK_SPEED, SPRINT_SPEED, DASH_SPEED)
            self.sliding_dash_fix()

    def mod_auto_sprint(self, WALK_SPEED, SPRINT_SPEED, DASH_SPEED):
        CONTROLLER1_BYTE2 = 0x4219
        SPRINT_SHOES_BYTE = 0x11df
        SPRINT_SHOES_MASK = 0x20
        B_BUTTON_MASK = 0x80
        FIELD_RAM_SPEED = 0x0875

        walking_src = [

            asm.LDA(SPRINT_SPEED, asm.IMM8),            # load default and push to stack
            asm.PHA(),

            "B_BUTTON",                                 # decrement speed by 1 if b button is held down
            asm.LDA(CONTROLLER1_BYTE2, asm.ABS),
            asm.AND(B_BUTTON_MASK, asm.IMM8),
            asm.BNE("B_BUTTON_DOWN"),
            asm.BRA("SPRINT_SHOES"),

            "B_BUTTON_DOWN",
            asm.PLA(),                                  # pull off stack
            asm.DEC(),                                  # decrement
            asm.PHA(),                                  # push to stack

            "SPRINT_SHOES",                             # incremeby speed by 1 if sprint shoes are on
            asm.LDA(SPRINT_SHOES_BYTE, asm.ABS),
            asm.AND(SPRINT_SHOES_MASK, asm.IMM8),
            asm.BEQ("STORE_SPEED"),

            asm.PLA(),                                  # pull off stack
            asm.INC(),                                  # increment
            asm.PHA(),                                  # push to stack

            "STORE_SPEED",
            asm.PLA(),                                  # load speed off stack
            asm.STA(FIELD_RAM_SPEED, asm.ABS_Y),
            asm.RTS(),
        ]

        walking_space = Allocate(Bank.C0, 40, "walking speed calculation", asm.NOP())
        walking_space.write(walking_src)

        src = [
            asm.JSR(walking_space.start_address, asm.ABS),
        ]

        space = Reserve(0x04e21, 0x04e37, "auto sprint", asm.NOP())
        space.write(src)

    #  DIRECTION VALUE
    #   $087F ------dd
    #         d: facing direction
    #            00 = up
    #            01 = right
    #            10 = down
    #            11 = left

    # https://silentenigma.neocities.org/ff6/index.html
    def sliding_dash_fix(self):
        DIRECTION_VALUE = 0x087f
        subroutine_src = [
            asm.LSR(),
            asm.LSR(),
            asm.PHA(),
            asm.LDA(DIRECTION_VALUE, asm.ABS_Y),
            asm.DEC(),
            asm.BEQ("FOO"),
            asm.DEC(),
            asm.BNE("RETURN"),
            "FOO",
            asm.PLA(),
            asm.INC(),
            asm.PHA(),
            "RETURN",
            asm.PLA(),
            asm.LSR(),
            asm.RTS(),
        ]
        subroutine_space = Allocate(Bank.C0, 40, "walking speed calculation", asm.NOP())
        subroutine_space.write(subroutine_src)

        src = [
            asm.JSR(subroutine_space.start_address, asm.ABS)
        ]

        space = Reserve(0x5885, 0x5887, "Sprite offset calculation 1", asm.NOP())
        space.write(src)

        space = Reserve(0x5892, 0x5894, "Sprite offset calculation 2")
        space.write(src)

# from memory.space import Reserve
# import instruction.asm as asm
# import args

# class AutoSprint:
#     def __init__(self):
#         if args.auto_sprint:
#             self.mod()

#     def mod(self):
#         # set sprint by default, b button to walk, sprint shoes do nothing

#         WALK_SPEED = 4 if args.auto_sprint else 2
#         SPRINT_SPEED = 3

#         CONTROLLER1_BYTE2 = 0x4219
#         B_BUTTON_MASK = 0x80
#         FIELD_RAM_SPEED = 0x0875

#         src = [
#             asm.LDA(CONTROLLER1_BYTE2, asm.ABS),
#             asm.AND(B_BUTTON_MASK, asm.IMM8),
#             asm.BNE("WALK"), # branch if b button down

#             "SPRINT",
#             asm.LDA(SPRINT_SPEED, asm.IMM8),
#             asm.BRA("STORE_SPEED"),

#             "WALK",
#             asm.LDA(WALK_SPEED, asm.IMM8),

#             "STORE_SPEED",
#             asm.STA(FIELD_RAM_SPEED, asm.ABS_Y),
#         ]

#         space = Reserve(0x04e21, 0x04e37, "auto sprint", asm.NOP())
#         space.write(src)
