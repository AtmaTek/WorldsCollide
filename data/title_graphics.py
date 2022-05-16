from memory.space import Reserve
class TitleGraphics:
    def __init__(self, rom, args):
        self.rom = rom
        self.args = args

    def mod(self):
        # Read in the title graphics bin and write it to 18f000 - 194e95
        binFile = open('graphics/title/WC Title Data-CDude.bin', "rb")
        bin = binFile.read(-1)
        space = Reserve(0x18f000, 0x194e95, "title graphics (compressed)")

        if len(space) != len(bin):
            raise ValueError(f"Invalid title graphics bin size ({len(bin)} should be {len(space)})")

        space.write(bin)

    def write(self):
        if self.args.spoiler_log:
            self.log()

    def log(self):
        pass