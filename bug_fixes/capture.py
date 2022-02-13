from memory.space import Bank, Reserve, Write
import instruction.asm as asm
import args

class Capture:
    def __init__(self):
        if args.fix_capture:
            self.mod()

    def mod(self):
        # http://assassin17.brinkster.net/patches.htm#anchor18
        NEW_SPECIAL_EFFECT_VAR = 0x2f3d

        #####
        # New subroutines
        #####
        # Null the dog block [displaced Square code], and clear my custom special effect byte.
        src = [
            asm.STA(0x3a83, asm.ABS),                 #Null Dog block
            asm.STZ(NEW_SPECIAL_EFFECT_VAR, asm.ABS), #Clear new special effect variable
            asm.RTS()
        ]
        space = Write(Bank.C2, src, "Capture Fix: null dog block")
        null_dog_block_addr = space.start_address

        #Call Square's per-target special effect function as normal.  Then call it again with
        # a secondary variable so the Capture command can steal, unless the first function call
        # already handled stealing.
        src = [
            asm.PHP(),
            asm.A8(),  # Set 8 bit accumulator
            asm.LDA(0x11a9, asm.ABS), 
            asm.PHP(),
            asm.JSR(0x387e, asm.ABS),
            asm.LDA(NEW_SPECIAL_EFFECT_VAR, asm.ABS),
            asm.CMP(0x1, asm.S),
            asm.BEQ("SKIP_IT"),
            asm.STA(0x11a9, asm.ABS),
            asm.JSR(0x387e, asm.ABS),
            "SKIP_IT",
            asm.PLA(),
            asm.STA(0x11a9, asm.ABS),
            asm.PLP(),
            asm.RTS()
        ]
        space = Write(Bank.C2, src, "Capture Fix: new special effect function")
        new_special_effect_addr = space.start_address

        ##### 
        # Modify data in "Character Executes One Hit" function to use new subroutines and variable
        #####
        space = Reserve(0x23185, 0x23187, "Capture Fix: call new null dog block subroutine")#, asm.NOP())
        space.write(
            asm.JSR(null_dog_block_addr, asm.ABS) #(Null Dog block, then clear my custom special effect
                                                   # variable for Capture)
        )
        space = Reserve(0x231b0, 0x231b2, "Capture Fix: Save Special Effect to new byte")
        space.write(
            asm.STA(NEW_SPECIAL_EFFECT_VAR, asm.ABS) #save special effect in our fancy new byte, so we won't
                                                     # overwrite the weapon's special effect.
        )
        space = Reserve(0x2345c, 0x2345e, "Capture Fix: call new special effect function")
        space.write(
            asm.JSR(new_special_effect_addr, asm.ABS) #Special effect code for target .. customized
        )

        ####
        # Dice Effect
        ####
        # FF6WC note: Rather than transfering Assassin's extensive changes made to the Dice Effect subroutine (C2/4168 - C2/41E5),
        #  which were seemingly made just to save space, I'm just transfering the main change as a subroutine:
        #  replacing the Capture animation with Dice with that of Fight starting at C2/41D9
        src = [ 
            asm.A8(),                 # Set 8 bit accumulator
            asm.LDA(0xb5, asm.DIR),   # Load Command Index
            asm.CMP(0x00, asm.IMM8),  # Maybe unnecessary? Compare Command with Fight
            asm.BEQ("SET_ANIMATION"), # Branch if Fight command
            asm.CMP(0x06, asm.IMM8),  # Compare Command with Capture
            asm.BNE("NO_CHANGE"),     # Branch if not Capture command
            "SET_ANIMATION",
            asm.LDA(0x26, asm.IMM8),
            asm.STA(0xb5, asm.DIR),   # Store a dice toss animation
            "NO_CHANGE",
            asm.RTS()
        ]
        space = Write(Bank.C2, src, "Capture Fix: new dice toss animation")
        dice_toss_animation_addr = space.start_address

        space = Reserve(0x241d9, 0x241e5, "Capture Fix: replace dice toss animation", asm.NOP())
        space.write(
            asm.JSR(dice_toss_animation_addr, asm.ABS), #Jump to our new routine
            asm.RTS()                                   #Done
        )
