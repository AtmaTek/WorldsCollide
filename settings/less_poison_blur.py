## Inspired by this original mod from Beyond Chaos
## https://github.com/FF6BeyondChaos/BeyondChaosRandomizer/blob/main/BeyondChaos/patches.py
## look for section beginning with "nicer_poison(fout):"
from memory.space import Reserve
import instruction.asm as asm

### reduce poison pixellation effect while walking
### does not affect poison sound effect while on overworld map
class LessPoisonBlur:
    def __init__(self):
        self.mod()

    def mod(self):
        # make poison pixelation effect 1/2 of it's vanilla amount in dungeons/towns
        space = Reserve(0x00e82, 0x00e9f, "town/dungeon poison gfx")
        space.write(
            [0x0F, 0x0F, 0x1F, 0x1F, # vanilla: 0F 1F 2F 3F
             0x2F, 0x2F, 0x3F, 0x3F, # vanilla: 4F 5F 6F 7F
             0x4F, 0x4F, 0x5F, 0x5F, # vanilla: 8F 9F AF BF
             0x6F, 0x6F, 0x7F, 0x7F, # vanilla: CF DF EF FF
             0x6F, 0x6F, 0x5F, 0x5F, # vanilla: EF DF CF BF
             0x4F, 0x4F, 0x3F, 0x3F, # vanilla: AF 9F 8F 7F
             0x2F, 0x2F, 0x1F, 0x1F, # vanilla: 6F 5F 4F 3F
             0x0F, 0x0F]             # vanilla: 2F 1F
        )
        

