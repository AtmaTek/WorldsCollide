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

        if args.auto_sprint or args.sprint_shoes_b_dash:
            src = self.get_auto_sprint_src(WALK_SPEED, SPRINT_SPEED, DASH_SPEED)
            space = Allocate(Bank.C0, 28, "Sprint subroutine")
            space.write(src)
            src = [
                asm.JSR(space.start_address, asm.ABS),
            ]
            space = Reserve(0x04e21, 0x04e37, "auto sprint", asm.NOP())
            space.write(src)

            self.sliding_dash_fix()

    def get_auto_sprint_src(self, WALK_SPEED, SPRINT_SPEED, DASH_SPEED):
        import args
        CONTROLLER1_BYTE2 = 0x4219
        SPRINT_SHOES_BYTE = 0x11df
        SPRINT_SHOES_MASK = 0x20
        B_BUTTON_MASK = 0x80
        FIELD_RAM_SPEED = 0x0875

        if args.auto_sprint:
            src = [
                asm.LDA(CONTROLLER1_BYTE2, asm.ABS),
                asm.AND(B_BUTTON_MASK, asm.IMM8),
                asm.BNE("WALK"), # branch if b button down

                "SPRINT",
                asm.LDA(SPRINT_SPEED, asm.IMM8),
                asm.BRA("STORE"),

                "WALK",
                asm.LDA(WALK_SPEED, asm.IMM8),
            ]

        if args.sprint_shoes_b_dash:
            src = [
                asm.LDA(CONTROLLER1_BYTE2, asm.ABS),
                asm.AND(B_BUTTON_MASK, asm.IMM8),
                asm.BNE("DASH1"),                           # b button just store default
                "STORE_DEFAULT",
                asm.LDA(SPRINT_SPEED, asm.IMM8),
                asm.BRA("STORE"),

                "DASH1",
                asm.LDA(SPRINT_SHOES_BYTE, asm.ABS),        # If sprint shoes equipped, store dash speed
                asm.AND(SPRINT_SHOES_MASK, asm.IMM8),
                asm.BNE("DASH2"),
                asm.LDA(WALK_SPEED, asm.IMM8),
                asm.BRA("STORE"),

                "DASH2",
                asm.LDA(DASH_SPEED, asm.IMM8),              # load fastest speed (DASH)
            ]

        src += [
            "STORE",
            asm.STA(FIELD_RAM_SPEED, asm.ABS_Y),        # store speed in ram
            asm.RTS(),                                  # return
        ]

        return src


    #  DIRECTION VALUE
    #   $087F ------dd
    #         d: facing direction
    #            00 = up
    #            01 = right
    #            10 = down
    #            11 = left

    # https://silentenigma.neocities.org/ff6/index.html
    # Will leave bits of documentation about in the vent neocities does not stand the test of time

    # With dash enabled, this causes a bug that the player will appear to be standing still when
    # running down or right at move speed 5. This is because two sprite instances are thrown out of
    # the animation cycle when running at that speed; while Up/Left correctly omits the standing
    # sprite, Down/Right omits the stepping sprites, since the offsets lag by an iteration.
    def sliding_dash_fix(self):
        DIRECTION_VALUE = 0x087f

        # C0/0000: 4A         	LSR            ; Shift offset bits right
        # C0/0001: 4A         	LSR            ; Shift offset bits right
        # C0/0002: 48         	PHA            ; Push offset value to stack
        # C0/0003: B9 7F 08   	LDA $087F,y    ; Load direction value
        # C0/0006: C9 01      	CMP #$01       ; Check if direction is Right
        # C0/0008: F0 07      	BEQ $D69E      ; Branch if the direction is Right
        # C0/000A: C9 02      	CMP #$02       ; Check if the direction is Down
        # C0/000C: F0 03      	BEQ $D69E      ; Branch if the direction is Down
        # C0/000E: 68         	PLA            ; Pull offset back off of stack
        # C0/000F: 80 02      	BRA $D6A0      ; Branch to the third LSR
        # C0/0011: 68         	PLA            ; Pull offset back off of stack
        # C0/0012: 1A         	INC            ; Increase the offset value by 1
        # C0/0013: 4A         	LSR            ; Shift offset bits right
        # C0/0014: 60         	RTS            ; Return from subfunction
        subroutine_src = [
            asm.LSR(),
            asm.LSR(),
            asm.PHA(),
            asm.LDA(DIRECTION_VALUE, asm.ABS_Y),
            asm.DEC(),
            asm.BEQ("FACING_RIGHT"),
            asm.DEC(),
            asm.BNE("RETURN"),
            "FACING_RIGHT",
            asm.PLA(),
            asm.INC(),
            asm.PHA(),
            "RETURN",
            asm.PLA(),
            asm.LSR(),
            asm.RTS(),
        ]
        subroutine_space = Allocate(Bank.C0, 20, "walking speed calculation", asm.NOP())
        subroutine_space.write(subroutine_src)

        src = [
            asm.JSR(subroutine_space.start_address, asm.ABS)
        ]

        space = Reserve(0x5885, 0x5887, "Sprite offset calculation 1", asm.NOP())
        space.write(src)

        space = Reserve(0x5892, 0x5894, "Sprite offset calculation 2")
        space.write(src)
