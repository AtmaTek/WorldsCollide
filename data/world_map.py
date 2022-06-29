from memory.space import Reserve

class WorldMap:
    def __init__(self, rom, args):
        self.rom = rom
        self.args = args

    def world_minimap_high_contrast_mod(self):
        # Increases the sprite priority for the minimap sprites
        # So it gets drawn on top of the overworld instead of being translucent
        # Thanks to Osteoclave for identifying these changes
        # Colors bytes: gggrrrrr, xbbbbbgg
        space = Reserve(0x2e4146, 0x2e4146, "steal value constant")
        space.write(0x1b) # default: 0x0b

        # High contrast location indicator on minimaps
        location_indicator_addr = [0x12eeb8,  # WoB default: 1100
                                   0x12efb8]  # WoR default: 1100
        for loc_addr in location_indicator_addr:
            space = Reserve(loc_addr, loc_addr+1, "high contrast minimap indicator")
            space.write(0xff, 0x03) # yellow

        location_indicator_addr = [0x12eeba,  # WoB default: 1f00
                                   0x12efba]  # WoR default: 1f00
        for loc_addr in location_indicator_addr:
            space = Reserve(loc_addr, loc_addr+1, "high contrast minimap indicator")
            space.write(0x00, 0x7F) # teal

    def mod(self):
        if self.args.world_minimap_high_contrast:
            self.world_minimap_high_contrast_mod()