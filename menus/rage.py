from memory.space import Bank, Reserve, Allocate, Write
import instruction.asm as asm

class RageMenu:
    def __init__(self, rages):
        self.rages = rages

        self.mod()

    def draw_ability_names_mod(self):
        import data.text as text
        from data.spell_names import name_id
        from data.text import text2

        rage_data_address = self.rages.ATTACKS_DATA_START + 0xc00000

        comma_value = int.from_bytes(text.get_bytes(',', text.TEXT3), "little")
        space_value = int.from_bytes(text.get_bytes(' ', text.TEXT3), "little")

        src = [
            asm.LDA(comma_value, asm.IMM8), # load ',' character
            asm.STA(0x2180, asm.ABS),       # add ',' to string
            asm.LDA(space_value, asm.IMM8), # load ' ' character
            asm.STA(0x2180, asm.ABS),       # add ' ' to string
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "draw comma & space")
        draw_comma_space = space.start_address

        # argument: a = rage ability ID
        # returns:  y = length of string, x = pointer to string
        # Based in part on https://github.com/FF6BeyondChaos/BeyondChaosRandomizer/blob/082695ebcb7e817dee5b2a778a4620963af5a4df/BeyondChaos/menufeatures.py#L77
        ability_id_in_ram = 0x38      # RAM variable (1 byte)
        rage_idx_in_ram = 0xE0        # RAM variable (2 bytes)
        src = [
            asm.CMP(0x36, asm.IMM8),                 # less than 54? It's a spell with length 7
            asm.BCC("GET_7_CHAR_SPELL_NAME"),
            asm.CMP(0x51, asm.IMM8),                 # else if less than 81? It's an esper with length 8
            asm.BCC("GET_8_CHAR_ESPER_NAME"),
            # else, it's greater than 81; it's an ability with length 10
            "GET_10_CHAR_ABILITY_NAME",
            asm.SEC(),
            asm.SBC(0x51, asm.IMM8),
            asm.A16(),
            asm.AND(0x00ff, asm.IMM16),
            asm.STA(ability_id_in_ram, asm.ABS), 
            asm.ASL(),
            asm.ASL(),
            asm.CLC(),
            asm.ADC(ability_id_in_ram, asm.ABS),
            asm.ASL(), # A *= 10
            asm.ADC(0x252, asm.IMM16),  # start of attack name - 0x26f567
            asm.TAX(),
            asm.LDY(0x000a, asm.IMM16),  # 10 characters
            asm.A8(),
            asm.RTS(),
            "GET_7_CHAR_SPELL_NAME",
            asm.A16(),
            asm.AND(0x00ff, asm.IMM16),
            asm.STA(ability_id_in_ram, asm.ABS), 
            asm.ASL(),
            asm.ASL(),
            asm.ASL(),  # A *= 8
            asm.SEC(),
            asm.SBC(ability_id_in_ram, asm.DIR), # change it to A *= 7
            asm.TAX(),
            asm.LDY(0x0007, asm.IMM16),  # 7 character length
            asm.A8(),
            asm.RTS(),
            "GET_8_CHAR_ESPER_NAME",
            asm.SEC(),
            asm.SBC(0x36, asm.IMM8),
            asm.A16(),
            asm.AND(0x00ff, asm.IMM16),
            asm.ASL(),
            asm.ASL(),
            asm.ASL(),  # A *= 8
            asm.ADC(0x17a, asm.IMM16),    # start of esper name - 0x26f567
            asm.TAX(),
            asm.LDY(0x0008, asm.IMM16),  # 8 character length
            asm.A8(),
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "get ability name")
        get_ability_name = space.start_address

        # argument: x = rage data index
        src = [
            asm.PHX(),
            asm.PHY(),

            # "Special" ability logic to get the name of the special ability
            asm.LDA(rage_data_address, asm.LNG_X), # a = ability id
            asm.CMP(name_id["Special"], asm.IMM8), # is this a Special ability?
            asm.BNE("GET_ABILITY_NAME"),           # if not, get the name of the ability
            # else, get the Special name instead from 0fd0d0 + rage_idx * 10, length 10
            asm.LDY(0x000a, asm.IMM16),  # 10 characters
            asm.LDA(rage_idx_in_ram, asm.ABS), # rage_idx
            asm.A16(),
            asm.AND(0x00ff, asm.IMM16),
            asm.ASL(),
            asm.ASL(),
            asm.CLC(),
            asm.ADC(rage_idx_in_ram, asm.ABS),
            asm.ASL(), # A *= 10
            asm.TAX(),
            asm.A8(),
            # Write a ! to indicate it's a special attack
            asm.LDA(text2.text_value['!'], asm.IMM8),
            asm.STA(0x2180, asm.ABS),
            "SPECIAL_NAME_LOOP_START",
            # x = offset from start of special names (0fd0d0), y = length (10)
            asm.LDA(0x0fd0d0, asm.LNG_X),           # a = current char in special name
            asm.CMP(space_value, asm.IMM8),         # compare with character ' ' which pads end of ability names
            asm.BEQ("DRAW_ABILITY_NAME_RETURN"),    # branch if reached end of special name
            asm.STA(0x2180, asm.ABS),               # add character to string
            asm.INX(),                              # next character in special name
            asm.DEY(),                              # decrement special name character index
            asm.BNE("SPECIAL_NAME_LOOP_START"),     # branch if not zero
            asm.BRA("DRAW_ABILITY_NAME_RETURN"),    # else, done
            "GET_ABILITY_NAME",
            asm.JSR(get_ability_name, asm.ABS),
            # x = offset from start of ability names (26f567), y = length
            "ABILITY_NAME_LOOP_START",
            asm.LDA(0x26f567, asm.LNG_X),           # a = current char in ability name
            asm.CMP(space_value, asm.IMM8),         # compare with character ' ' which pads end of ability names
            asm.BEQ("DRAW_ABILITY_NAME_RETURN"),    # branch if reached end of ability name
            # skip over magic icons, which don't show up with the variable-width font used
            asm.CMP(text2.text_value['<white magic icon>'], asm.IMM8),
            asm.BEQ("NEXT_CHARACTER"),
            asm.CMP(text2.text_value['<black magic icon>'], asm.IMM8),
            asm.BEQ("NEXT_CHARACTER"),
            asm.CMP(text2.text_value['<gray magic icon>'], asm.IMM8),
            asm.BEQ("NEXT_CHARACTER"),
            asm.STA(0x2180, asm.ABS),               # add character to string
            "NEXT_CHARACTER",
            asm.INX(),                              # next character in ability name
            asm.DEY(),                              # decrement ability name character index
            asm.BNE("ABILITY_NAME_LOOP_START"),     # branch if not zero
            "DRAW_ABILITY_NAME_RETURN",
            asm.PLY(),
            asm.PLX(),
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "draw ability name")
        draw_ability_name = space.start_address

        src = [
            asm.LDX(0x9ec9, asm.IMM16),     # dest WRAM LBs
            asm.STX(0x2181, asm.ABS),       # store dest WRAM LBs

            asm.TDC(),                      # a = 0x0000
            asm.LDA(0x4b, asm.DIR),         # a = cursor index (rage index)
            asm.TAX(),                      # x = cursor index (rage index)
            asm.LDA(0x7e9d89, asm.LNG_X),   # a = rage at cursor index
            asm.CMP(0xff, asm.IMM8),        # compare with no rage
            asm.BEQ("END_STRING_RETURN"),   # branch if rage at cursor index not learned

            asm.A16(),
            asm.STA(rage_idx_in_ram, asm.ABS), # store the rage_idx, as it aligns with the monster index elsewhere to lookup Special abilities
            asm.ASL(),                      # a = rage index * 2 (2 abilities per rage)
            asm.TAX(),                      # x = rage index * 2 (rage ability data index)
            asm.TDC(),                      # clear A of any 16-bit remnants
            asm.A8(),
            asm.JSR(draw_ability_name, asm.ABS),    # draw current ability
            asm.JSR(draw_comma_space, asm.ABS),     # draw ', ' separator
            asm.INX(),                              # next ability
            asm.JSR(draw_ability_name, asm.ABS),    # draw current ability

            "END_STRING_RETURN",
            asm.STZ(0x2180, asm.ABS),       # end string
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "draw ability names")
        draw_ability_names = space.start_address

        sustain_replace = 0x328c6   # handle L and R
        replace_size = 3            # replacing jsr instructions

        src = [
            asm.LDA(0x10, asm.IMM8),# enable description menu flag bitmask
            asm.TRB(0x45, asm.DIR), # enable descriptions
            asm.JSR(0x4c52, asm.ABS),  # displaced code: handle D-Pad
            asm.JMP(draw_ability_names, asm.ABS),
        ]
        space = Write(Bank.C3, src, "sustain rage list")
        sustain_rage_list = space.start_address

        print(f"{space.start_address_snes:x}")

        space = Reserve(sustain_replace, sustain_replace + replace_size - 1, "rage menu sustain handle D-Pad")
        space.write(
            asm.JSR(sustain_rage_list, asm.ABS),
        )

    def mod(self):
        self.draw_ability_names_mod()