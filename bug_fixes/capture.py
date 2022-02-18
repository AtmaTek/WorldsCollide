from memory.space import Bank, Reserve, Write
import instruction.asm as asm
import args

class Capture:
    def __init__(self):
        if args.fix_capture:
            self.weapon_special_mod()
            self.multisteal_mod()

    def multisteal_mod(self):
        # Fixes issue with multiple steals caused by Genji Glove and/or Offering Capture.
        # Issues resolved:
        #    1) the stolen items are not all added to your inventory (only the last successful steal is actually added)
        # Based in part on https://www.angelfire.com/al2/imzogelmo/patches.html#patches's Multi-Steal Fix
        # Code actually derived from Bropedio's Multi-Steal fix: 
        #  https://www.ff6hacking.com/forums/thread-4124-post-40232.html#pid40232
        # Known remaining issue: the message display window does not clear in between steal animations, 
        #  meaning that the first item name is the one that is displayed for all subsequent successful steals. 

        # New subroutine for storing acquired item
        src = [
            asm.TSB(0x3a8c, asm.ABS),   # set character's reserve item to be added
            asm.LDA(0x32f4, asm.ABS_X), # load current reserve item
            asm.PHA(),                  # save reserve item on stack
            asm.XBA(),                  # get new item in A
            asm.STA(0x32f4, asm.ABS_X), # store new item in reserve byte
            asm.PHX(),                  # save X
            asm.JSR(0x62C7, asm.ABS),   # add reserve to obtained-items buffer
            asm.PLX(),                  # restore X
            asm.PLA(),                  # restore previous reserve item
            asm.STA(0x32f4, asm.ABS_X), # store in reserve item byte again
            asm.RTS()
        ]
        space = Write(Bank.C2, src, "Multisteal Fix: store acquired item")
        store_acquired_addr = space.start_address

        # Update steal formula where it stores the acquired item
        space = Reserve(0x239ec, 0x239f4, "Multisteal Fix: call new subroutine", asm.NOP())
        space.write(
            asm.XBA(),                             # store acquired item in B
            asm.LDA(0x3018, asm.ABS_X),            # character's unique bit
            asm.JSR(store_acquired_addr, asm.ABS), # save new item to buffer
        )

        # Fix Item Return Buffer
        space = Reserve(0x112d5, 0x112d7, "Multisteal Fix: avoid item return buffer overrun")
        space.write(
            asm.CPX(0x50, asm.IMM16) # the game only clears #$40 for item buffer, but it expects #$50
        )

    def weapon_special_mod(self):
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

