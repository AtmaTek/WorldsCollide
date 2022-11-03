from memory.space import Reserve
class TitleGraphics:
    def __init__(self, rom, args):
        self.rom = rom
        self.args = args

    def mod(self):
        # Read in the title graphics bin and write it to 18f000 - 194e95
        with open('graphics/title/WC Spartan Title Data-CDude.bin', "rb") as binFile:
            data = binFile.read()

            space = Reserve(0x18f000, 0x194e95, "title graphics (compressed)")
            if len(space) != len(data):
                raise ValueError(f"Invalid title graphics bin size ({len(data)} should be {len(space)})")

            space.write(data)

    def write(self):
        if self.args.spoiler_log:
            self.log()

    def log(self):
        pass