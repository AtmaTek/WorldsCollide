class MapProperty:
    DATA_SIZE = 33
    DATA_START = 0x2d8f00

    def __init__(self, rom, id):
        self.rom = rom

        self.set_id(id)
        self.read()

    def set_id(self, id):
        self.id = id
        self.data_start = self.DATA_START + self.id * self.DATA_SIZE

    def read(self):
        data = self.rom.get_bytes(self.data_start, self.DATA_SIZE)

        self.name_index = data[0]
        self.enable_random_encounters = (data[5] & 0x80) >> 7

    def write(self):
        pass

    def print(self):
        print(f"{self.id}: {self.enable_random_encounters}")
