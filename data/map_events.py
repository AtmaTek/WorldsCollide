from data.map_event import MapEvent

class MapEvents():
    EVENT_COUNT = 1164
    DATA_START_ADDR = 0x040342

    def __init__(self, rom):
        self.rom = rom
        self.read()

    def read(self):
        self.events = []

        for event_index in range(self.EVENT_COUNT):
            event_data_start = self.DATA_START_ADDR + event_index * MapEvent.DATA_SIZE
            event_data = self.rom.get_bytes(event_data_start, MapEvent.DATA_SIZE)

            new_event = MapEvent()
            new_event.from_data(event_data)
            self.events.append(new_event)

    def write(self):
        for event_index, event in enumerate(self.events):
            event_data = event.to_data()
            event_data_start = self.DATA_START_ADDR + event_index * MapEvent.DATA_SIZE
            self.rom.set_bytes(event_data_start, event_data)

    def mod(self):
        pass

    def get_event(self, search_start, search_end, x, y):
        for event in self.events[search_start:search_end + 1]:
            if event.x == x and event.y == y:
                return event
        raise IndexError(f"get_event: could not find event at {x} {y}")

    def add_event(self, index, new_event):
        self.events.insert(index, new_event)
        self.EVENT_COUNT += 1

    def delete_event(self, search_start, search_end, x, y):
        for event in self.events[search_start:search_end + 1]:
            if event.x == x and event.y == y:
                self.events.remove(event)
                self.EVENT_COUNT -= 1
                return
        raise IndexError("delete_event: could not find event at {x} {y}")

    def print_range(self, start, count):
        for offset in range(count):
            self.events[start + offset].print()

    def print(self):
        for event in self.events:
            event.print()
