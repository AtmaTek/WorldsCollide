from settings.auto_sprint import AutoSprint
from settings.scan_all import ScanAll
from settings.random_rng import RandomRNG
from settings.permadeath import Permadeath
from settings.y_npc import YNPC

from memory.space import Bank, Reserve, Write
import instruction.asm as asm

__all__ = ["Settings"]
class Settings:
    def __init__(self):
        self.auto_sprint = AutoSprint()
        self.scan_all = ScanAll()
        self.random_rng = RandomRNG()
        self.permadeath = Permadeath()
        self.y_npc = YNPC()

        # do not auto load save file after game over
        space = Reserve(0x00c4fe, 0x00c500, "load where to return to after game over", asm.NOP())
        space.write(
            asm.LDA(0xff, asm.IMM8), # do not auto load save file after game over
        )

        space = Reserve(0x2e8393, 0x2e8393, "wor overworld song")
        space.write(0x4c) # change from dark world to searching for friends

        # Set default memory location for Config #2:
        src = [
            asm.LDA(0x00, asm.IMM8),                    # LDA #$00;
            asm.STA(0x1D54, asm.ABS),                   # STA $1D54;  # Config #2
            asm.RTS(),
            ]
        space = Write(Bank.C3, src, "Config #2 default value")
        print('Wrote Config #2 default location: ' + str(hex(space.start_address)))

        # Update the JSR for Config default #2
        config2_loc = space.start_address
        space = Reserve(0x370c2, 0x370c4, "Config_2_default")  # 0x0370C2: ['20', PP, NN, '20', PP + 06, NN]])  # JSR #$CONF2; JSR #$CONF3
        space.write(
            asm.JSR(config2_loc, asm.ABS),
            )
        print('Wrote JSR address for Config #2')

        # Set default memory location for Config #3:
        src = [
            asm.LDA(0x00, asm.IMM8),  # LDA #$00;
            asm.STA(0x1D4E, asm.ABS),  # STA $1D4E;  # Config #3
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "Config_3_default")
        print('Wrote Config #3 default location: ' + str(hex(space.start_address)))

        # Update the JSR for Config default #3
        config3_loc = space.start_address
        space = Reserve(0x370c5, 0x370c7, "Config_3_default")  # 0x0370C2: ['20', PP, NN, '20', PP + 06, NN]])  # JSR #$CONF2; JSR #$CONF3
        space.write(
            asm.JSR(config3_loc, asm.ABS),
        )
        print('Wrote JSR address for Config #3')

