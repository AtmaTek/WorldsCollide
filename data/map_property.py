

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
        self.data = self.rom.get_bytes(self.data_start, self.DATA_SIZE)

        self.name_index = self.data[0]
        
        self.enable_warp =              (self.data[1] & 0x02) >> 1
        self.enable_random_encounters = (self.data[5] & 0x80) >> 7
        
        self.song = self.data[28]

    def write(self):
        self.data[1] = (self.data[1] & ~0x02) | (self.enable_warp << 1)
        self.data[5] = (self.data[5] & ~0x80) | (self.enable_random_encounters << 7)
        
        self.data[28] = self.song
        self.rom.set_bytes(self.data_start, self.data)

    def set_warp(self, value):
        self.enable_warp = 1 if value else 0

    def set_random_encounters(self, value):
        self.enable_random_encounters = 1 if value else 0

    def print(self):
        print(f"{self.id}: {self.enable_random_encounters}")
