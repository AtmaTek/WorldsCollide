from memory.space import Reserve
import instruction.asm as asm

class SketchControl:
    def __init__(self, rom, args):
        self.rom = rom
        self.args = args

    def enable_sketch_control_chances_always(self):
        # Always Sketch or Control if the target is valid
        # NOPing the JSR and BCS that can prevent Sketch and Control from working
        space = Reserve(0x023b3d, 0x023b41, "sketch always", asm.NOP())
        space = Reserve(0x023ae8, 0x023aec, "control always", asm.NOP())

    def mod(self):
        if self.args.sketch_control_chances_always:
            self.enable_sketch_control_chances_always()

    def write(self):
        if self.args.spoiler_log:
            self.log()

    def log(self):
        pass