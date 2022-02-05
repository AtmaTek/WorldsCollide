from memory.space import Read, Write
import args

class Animations:
    def __init__(self):
        if args.fewer_flashes:
            self.remove_battle_flashes_mod()

    def remove_battle_flashes_mod(self):
        import data.battle_animation_scripts as battle_animation_scripts

        # For each battle animation command
        for key in battle_animation_scripts.BATTLE_ANIMATION_FLASHES:
            # For each address associated with this command
            for animation_cmd_addr in battle_animation_scripts.BATTLE_ANIMATION_FLASHES[key]:
                animation_cmd = Read(animation_cmd_addr, animation_cmd_addr+1)
                if(animation_cmd[0] == 0xB0 or animation_cmd[0] == 0xAF):
                    # This is an absolute color change. To remove flashing effects, set the value to E0 to cause no background change
                    Write(animation_cmd_addr+1, 0xE0, "Background color change (absolute)")
                elif(animation_cmd[0] == 0xB5 or animation_cmd[0] == 0xB6):
                    # This is a relative color change. To remove flash effects, set the value to F0 to cause no background change
                    Write(animation_cmd_addr+1, 0xF0, "Background color change (relative)")
                else:
                    # This is an error, reflecting a difference between the disassembly used to generate BATTLE_ANIMATION_FLASHES and the ROM
                    raise ValueError(f"Battle Animation Script Command at 0x{animation_cmd_addr:x} (0x{animation_cmd[0]:x}) did not match an expected value.")