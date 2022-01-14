from memory.rom import ROM
from memory.space import Space
from memory.free import free
import args

class Memory:
    def __init__(self):
        self.rom = ROM(args.input_file)
        Space.rom = self.rom
        free()

    def write(self):
        if not args.no_rom_output:
            self.rom.write(args.output_file)
