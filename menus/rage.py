from memory.space import Bank, Reserve, Allocate, Write
import instruction.asm as asm
from data.spell_names import name_id, id_name


class RageMenu:
    def __init__(self, rages, enemies):
        self.rages = rages
        self.enemies = enemies

        # Build an array to lookup enemy-specific Special command effects
        from constants.status_effects import A, B, C, D
        self.status_effects = []
        self.status_effects.extend(list(A.id_name.values()))
        self.status_effects.extend(list(B.id_name.values()))
        self.status_effects.extend(list(C.id_name.values()))
        self.status_effects.extend(list(D.id_name.values()))

        # Remove death from the status effects list, as it requires a second bit from flags1 
        self.status_effects = list(map(lambda x: x.replace("Death", ""), self.status_effects))

        # Remove other statuses that aren't really relevant
        self.status_effects = list(map(lambda x: x.replace("Near Fatal", ""), self.status_effects))
        self.status_effects = list(map(lambda x: x.replace("Hide", ""), self.status_effects))

        self.special_effects = []  
        self.special_effects.extend(self.status_effects)
        for i in range(15, 95, 5): # going from 1.5x - 9.0x damage
            dmg_multiplier = i / 10
            self.special_effects.append(f"{dmg_multiplier:.1f}x dmg")
        self.special_effects.append("Drain HP")
        self.special_effects.append("Drain MP")
        self.special_effects.append("Remove Reflect")

        self.element_strings = ["<fire>", "<ice>", "<lightning>", "<poison>", "<wind>", "<pearl>", "<earth>", "<water>"] # in bit order for spell.element

        self.mod()

    def get_rage_string(self, id, attack_id):
        from data.spell_names import id_name, name_id


        if attack_id == name_id["Special"]:
            # handle special name lookup + special attack info (dmg multipler, status effect)
            enemy = self.enemies.enemies[id]
            special_name = enemy.special_name
            special_effect = enemy.special_effect

            rage_str = f"{special_name}: "
            rage_str += self.special_effects[special_effect]
        elif attack_id == name_id["Pep Up"]:
            rage_str = "Pep Up: Remove Caster+Heal Ally"
        elif attack_id == name_id["Flare Star"]:
            rage_str = "Flare Star: <fire> E.Lvl*80 IgnDef<line>All Enemies"
        elif attack_id == name_id["Dischord"]:
            rage_str = "Dischord: Halve Enemy Level"
        elif attack_id == name_id["Revenge"]:
            rage_str = "Revenge: dmg = Max - Curr.HP"
        elif attack_id == name_id["Blow Fish"]:
            rage_str = "Blow Fish: 1000 dmg"
        elif attack_id == name_id["Pearl Wind"]:
            rage_str = "Pearl Wind: Heal Curr.HP<line>Party"
        elif attack_id == name_id["Step Mine"]:
            rage_str = "Step Mine: dmg = Steps/32"
        else:
            rage_str = f"{id_name[attack_id]}"

            ability = self.rages.abilities[attack_id]
            ability_details = ""

            # Add the element graphic to the rage string for any element bits that are set
            spell_elements = ability.elements
            for bit in range(0,8):
                if (spell_elements >> bit) & 1:
                    ability_details += self.element_strings[bit]
            if (ability.status1 & 0x80) and (ability.flags1 & 0x02): # Instant-death effect
                ability_details += "<death>"

            if ability.power > 1: # Ignoring 1, which includes special damage skills like Exploder & Blow Fish
                if ability_details != "":
                    ability_details += " "

                if ability.flags3 & 0x80: # fractional damage
                    from fractions import Fraction
                    hp_fraction = Fraction(ability.power/16)
                    ability_details += f"{str(hp_fraction)} HP"
                else:
                    ability_details += f"{ability.power}"
                    if (ability.flags1 & 1):
                        # Physical damage
                        ability_details += "P"
                    else:
                        # Magic damage
                        ability_details += "M"
                    ability_details += "Pwr"

                    if ability.flags1 & 0x20: #ignore def
                        ability_details += " IgnDef"

            # Add status effects
            offset = 0
            bits_set = 0
            status_details = " "
            statuses = [ability.status1, ability.status2, ability.status3, ability.status4]
            for status in statuses:
                for bit in range(0,8):
                    if(status >> bit) & 1:
                        status_details += f"{self.status_effects[offset + bit]} "
                        bits_set += 1
                offset += 8
            if bits_set > 2:
                # we only have room to show 2 statuses
                status_details = " Multi-Status"
            ability_details += status_details

            # Indicate multi-target spells
            if ability.targets & 0x08: # Select One Group flag 
                if ability.targets & 0x40: # Enemy selected
                    ability_details += "<line>All Enemies"
                else:
                    ability_details += "<line>Party"
            elif ability.targets & 0x04: # Select all targets (both groups)
                ability_details += "<line>All"

            # Add ability_details to rage_string if it's not empty and the description doesn't match the name
            if ability_details.strip() != "" and ability_details.strip() != id_name[attack_id]:
                rage_str += f": {ability_details}"

        # # remove duplicate white spaces
        import re
        rage_str = re.sub(' +', ' ', rage_str)

        # add a space after <poison> due to it overlapping to the right
        rage_str = rage_str.replace("<poison>", "<poison> ")
        # remove spaces before <line>
        rage_str = rage_str.replace(" <line>", "<line>")

        # remove leading and trailing spaces
        rage_str = rage_str.strip()
        return rage_str

    def draw_ability_names_mod(self):
        import data.text as text

        # Get the custom strings for each rage to be written to the ROM
        lines = []
        for rage in self.rages.rages:
            # Only focusing on attack2, as attack1 is simply "Battle" -- if that changes in the future, this string can be revisited
            rage_str = f"{self.get_rage_string(rage.id, rage.attack2)}<end>"
            lines.append(rage_str)

        line_offsets = [0]
        running_offset = 0
        # Write the lines to F0
        src = []
        for line in lines:
            # convert to bytes
            bytes = text.get_bytes(line, text.TEXT3)
            running_offset += len(bytes)
            line_offsets.append(running_offset)
            src.append(bytes)
        space = Write(Bank.F0, src, "rage description lines table")
        lines_table = space.start_address_snes

        # write the 2-byte line offsets to F0
        src = []
        for offset in line_offsets:
            src.append(offset.to_bytes(2, 'little'))
        space = Write(Bank.F0, src, "rage description lines table offsets")
        lines_table_offsets = space.start_address_snes

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
            asm.ASL(),                      # a = rage index * 2 (2 bytes per table offset)
            asm.TAX(),                      # x = rage index * 2 
            asm.LDA(lines_table_offsets, asm.LNG_X), # get the offset
            asm.TAX(),
            asm.A8(),
            "STRING_LOOP_START",
            asm.LDA(lines_table, asm.LNG_X), # get the character
            asm.STA(0x2180, asm.ABS),        # add character to string
            asm.CMP(0x00, asm.IMM8),         # was it the end of the string? 
            asm.BEQ("RETURN"),               # if so, be done
            asm.INX(),                       # move to next character in ability name
            asm.BRA("STRING_LOOP_START"),    
            "END_STRING_RETURN",
            asm.STZ(0x2180, asm.ABS),       # end string
            "RETURN",
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

        space = Reserve(sustain_replace, sustain_replace + replace_size - 1, "rage menu sustain handle D-Pad")
        space.write(
            asm.JSR(sustain_rage_list, asm.ABS),
        )

    def mod(self):
        self.draw_ability_names_mod()