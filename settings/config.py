from memory.space import Reserve, Bank, Write
import instruction.asm as asm
import args

class Config:
    def __init__(self):
        self.mod()

    def mod(self):
        # Set default configuration options to the most popular:
        # Config1: Msg Speed = 1 (Fastest), Bat Speed = 6 (Slowest), Bat Mode = 1 (Wait)
        # Config3: Cursor = 1 (Memory)

        # Config 1, set by this code:
        #   C3/70B8:	A92A    	LDA #$2A       ; Bat.Mode, etc.
        # RAM $1D4D, one byte sets: cmmm wbbb (command set c, message spd mmm + 1, battle mode w, battle speed bbb + 1)
        space = Reserve(0x370b9, 0x370b9, "config 1 default")
        space.write(0x0D) # default: 0x2A

        # Config 3, set by this code:
        #   C3/70C5:	9C4E1D  	STZ $1D4E      ; Wallpaper, etc.
        # RAM $1D4E, one byte sets: gcsr wwww (gauge g, cursor c, sound s, reequip r, wallpaper wwww (0-7))
        config3_value = 1 << 6
        src = [
            asm.LDA(config3_value, asm.IMM8),  # default: 0
            asm.STA(0x1D4E, asm.ABS),  
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "Config_3_default")

        # Update the JSR for Config default #3
        config3_loc = space.start_address
        space = Reserve(0x370c5, 0x370c7, "Config_3_default")
        space.write(
            asm.JSR(config3_loc, asm.ABS),
        )
