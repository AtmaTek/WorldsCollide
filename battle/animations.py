from memory.space import Bank, Reserve, Read, Write
import data.battle_animation_scripts as battle_animation_scripts
import instruction.asm as asm
import args

class Animations:
    def __init__(self):
        self.health_animation_reflect_mod()

        if args.flashes_remove_most:
            flash_address_arrays = battle_animation_scripts.BATTLE_ANIMATION_FLASHES.values()
            self.remove_battle_flashes_mod(flash_address_arrays)
            self.remove_critical_flash()

        if args.flashes_remove_worst:
            flash_address_arrays = []
            animation_names = ["Boss Death", "Ice 3", "Fire 3", "Bolt 3", "Schiller", "R.Polarity", "X-Zone",
                               "Muddle", "Dispel", "Shock", "Bum Rush", "Quadra Slam", "Slash", "Flash", 
                               "Step Mine", "Rippler", "WallChange", "Ultima", "ForceField"]
            for name in animation_names:
                flash_address_arrays.append(battle_animation_scripts.BATTLE_ANIMATION_FLASHES[name])
            self.remove_battle_flashes_mod(flash_address_arrays)

    def remove_critical_flash(self):
        space = Reserve(0x23410, 0x23413, "Critical hit screen flash", asm.NOP())

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
    
    def health_animation_reflect_mod(self):
        # Ref: https://www.ff6hacking.com/forums/thread-4145.html
        # Banon's Health command casts Cure 2 on the party with a unique animation.
        # Because the animation is unique, it has the step-forward component built into it.  
        # And because Cure 2 can be reflected, if the command hits a mirrored target it will bounce and make Banon step forward again.  
        # Note: this only occurs if the whole party doesn't have reflect, only a subset.
        # Used over and over, Banon can be made to walk completely off-screen.
        # 
        # Fix:
        # We tell the HEALTH animation to ignore block graphics, which prevents the reflect animation from playing.  
        # When encountering a reflection, the regular green Cure 2 animation will follow on the reflect recipient.
        src = [
            asm.INC(0x62C0, asm.ABS), #Makes the animation ignore blocking graphics
            asm.JSR(0xBC35, asm.ABS), #Call the subroutine that got displaced to inject the block override
            asm.RTS()
        ]
        space = Write(Bank.C1, src, "Health animation fix")
        jsrAddr = space.start_address

        # Replace the existing jump with one to our new service routine
        space = Reserve(0x1BB67, 0x1BB69, "Health animation JSR")
        space.write(asm.JSR(jsrAddr, asm.ABS))