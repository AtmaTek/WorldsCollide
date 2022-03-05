from data.control import Control
from data.structures import DataArray
from memory.space import Reserve
import instruction.asm as asm

class Controls():
    ATTACKS_DATA_START = 0xf3d00
    ATTACKS_DATA_END = 0xf42ff
    ATTACKS_DATA_SIZE = 4

    def __init__(self, rom, args, enemies, rages):
        self.rom = rom
        self.args = args
        self.enemies = enemies
        self.rages = rages

        self.attack_data = DataArray(self.rom, self.ATTACKS_DATA_START, self.ATTACKS_DATA_END, self.ATTACKS_DATA_SIZE)

        self.controls = []
        for control_index in range(len(self.attack_data)):
            control = Control(control_index, self.attack_data[control_index])
            self.controls.append(control)

    def enable_control_chances_always(self):
        # Always Control if the target is valid
        # NOPing the JSR and BCS that can prevent Control from working
        space = Reserve(0x023ae8, 0x023aec, "control always", asm.NOP())

    def enable_better_control_commands(self):
        from data.spell_names import name_id
        # Ensure that Rage & Special are available (if there are open Controls)
        for control in self.controls:
            # Search for blanks, rages, and specials
            index_of_blank = self.ATTACKS_DATA_SIZE # default to end
            control_has_rage = False
            control_has_special = False
            for attack_index, attack in enumerate(control.attack_data()):
                # Look for the first blank entry
                if index_of_blank == self.ATTACKS_DATA_SIZE and attack == name_id["??????????"]:
                    index_of_blank = attack_index
                # Look for a rage
                if control.id < self.rages.RAGE_COUNT: # Enemy has a rage
                    if attack == self.rages.rages[control.id].attack2 and not control_has_rage:
                        control_has_rage = True
                else:
                    control_has_rage = True # no rages to have
                # Look for a special
                if attack == name_id["Special"] and not control_has_special:
                    control_has_special = True
            
            # If we found that it doesn't have a rage and there's room, add the rage
            if not control_has_rage and index_of_blank < self.ATTACKS_DATA_SIZE:
                control.attack_data_array[index_of_blank] = self.rages.rages[control.id].attack2
                # Avoid duplicate Specials if Rage == Special
                if control.attack_data_array[index_of_blank] == name_id["Special"]:
                    control_has_special = True
                index_of_blank = index_of_blank + 1

            # If we found that it doesn't have a Special and there's room, add the Special
            if not control_has_special and index_of_blank < self.ATTACKS_DATA_SIZE:
                control.attack_data_array[index_of_blank] = name_id["Special"]
                index_of_blank = index_of_blank + 1

    def mod(self):
        if self.args.improve_sketch_control:
            self.enable_control_chances_always()
            self.enable_better_control_commands()

    def write(self):
        if self.args.spoiler_log:
            self.log()

        for control_index, control in enumerate(self.controls):
            self.attack_data[control_index] = control.attack_data()

        self.attack_data.write()

    def log(self):
        pass

    def print(self):
        for control in self.controls:
            control.print()
