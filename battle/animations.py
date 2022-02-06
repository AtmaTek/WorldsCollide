from memory.space import Read, Write
import data.battle_animation_scripts as battle_animation_scripts
import args

class Animations:
    def __init__(self):
        
        if args.flashes_remove_most:
            flash_address_arrays = battle_animation_scripts.BATTLE_ANIMATION_FLASHES.values()
            self.remove_battle_flashes_mod(flash_address_arrays)
        if args.flashes_remove_worst:
            flash_address_arrays = []
            animation_names = ["Boss Death", "Ice 3", "Fire 3", "Bolt 3", "Schiller", "R.Polarity", "X-Zone",
                               "Muddle", "Dispel", "Shock", "Bum Rush", "Quadra Slam", "Slash", "Flash", 
                               "Step Mine", "Rippler", "WallChange", "Ultima", "ForceField"]
            for name in animation_names:
                flash_address_arrays.append(battle_animation_scripts.BATTLE_ANIMATION_FLASHES[name])
            self.remove_battle_flashes_mod(flash_address_arrays)

    def remove_battle_flashes_mod(self, flash_address_arrays):
        ABSOLUTE_CHANGES = [0xb0, 0xaf]
        RELATIVE_CHANGES = [0xb5, 0xb6]
        # For each battle animation command
        for flash_addresses in flash_address_arrays:
            # For each address in its array
            for flash_address in flash_addresses:
                # Read the current animation command at the address
                animation_cmd = Read(flash_address, flash_address+1)
                if(animation_cmd[0] in ABSOLUTE_CHANGES):
                    # This is an absolute color change. To remove flashing effects, set the value to E0 to cause no background change
                    Write(flash_address+1, 0xE0, "Background color change (absolute)")
                elif(animation_cmd[0] in RELATIVE_CHANGES):
                    # This is a relative color change. To remove flash effects, set the value to F0 to cause no background change
                    Write(flash_address+1, 0xF0, "Background color change (relative)")
                else:
                    # This is an error, reflecting a difference between the disassembly used to generate BATTLE_ANIMATION_FLASHES and the ROM
                    raise ValueError(f"Battle Animation Script Command at 0x{flash_address:x} (0x{animation_cmd[0]:x}) did not match an expected value.")