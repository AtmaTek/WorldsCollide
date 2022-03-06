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

    def mod(self):
        if self.args.sketch_control_improved_stats:
            self.enable_control_chances_always()

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
