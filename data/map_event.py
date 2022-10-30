class MapEvent():
    DATA_SIZE = 0x05

    def __init__(self):
        self.x = 0
        self.y = 0
        self.event_address = 0

    def from_data(self, data):
        assert(len(data) == self.DATA_SIZE)

        self.x = data[0]
        self.y = data[1]

        self.event_address = data[2] | (data[3] << 8) | (data[4] << 16)

    def to_data(self):
        data = [0x00] * self.DATA_SIZE

        data[0] = self.x
        data[1] = self.y

        data[2] = self.event_address & 0xff
        data[3] = (self.event_address & 0xff00) >> 8
        data[4] = (self.event_address & 0xff0000) >> 16

        return data

    def print(self):
        print("{}, {}: {}".format(self.x, self.y, hex(self.event_address)))
