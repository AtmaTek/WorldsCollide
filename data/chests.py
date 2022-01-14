from data.chest import Chest
from data.structures import DataArrays

class Chests():
    PTRS_START = 0x2d82f4
    PTRS_END = 0x2d8633
    DATA_START = 0x2d8634
    DATA_END = 0x2d8e5a
    DATA_SIZE = 5

    def __init__(self, rom, args, items):
        self.rom = rom
        self.args = args
        self.items = items

        self.chest_data = DataArrays(self.rom, self.PTRS_START, self.PTRS_END, self.rom.SHORT_PTR_SIZE, self.DATA_START, self.DATA_END, self.DATA_SIZE)

        self.all_chests = []
        self.map_chests = []
        for map_index in range(len(self.chest_data)):
            map_chests = []
            for map_chest_index in range(len(self.chest_data[map_index])):
                chest = Chest(len(self.all_chests), self.chest_data[map_index][map_chest_index])
                self.all_chests.append(chest)
                map_chests.append(chest)
            self.map_chests.append(map_chests)

        self.next_id = 287           # next id to use for new chests
        self.next_opened_bit = 0x103 # next opened bit flag to use for new chests

        # some chests are duplicated on multiple maps (mt kolts, doma, albrook, kefka's tower)
        # list of tuples (<first chest id>, <duplicate chest id>)
        self.duplicates = [(68, 70), (69, 71)] + \
                          [(95, 97), (91, 98), (92, 99), (93, 100), (94, 101), (95, 102), (96, 103)] + \
                          [(202, 203)] + \
                          [(174, 284), (175, 285)]

        # list of all available chests (for shuffling and modifying)
        # exclude lone wolf chest, unreachabe, duplicate chests so they are not modified
        lone_wolf_chest_id = 2
        gem_box_chest_id = 231
        self.unreachable_ids = [0, 32, 33, 34, 141, 142, 143, 144, 145]
        self.chests = [chest for chest in self.all_chests if chest.id not in self.unreachable_ids and \
                                                             chest.id not in [dup[1] for dup in self.duplicates] and \
                                                             chest.id != lone_wolf_chest_id and \
                                                             chest.id != gem_box_chest_id]


    def chest_count(self, map_id):
        return len(self.map_chests[map_id])

    def set_item(self, map_id, x, y, item_id):
        for chest in self.map_chests[map_id]:
            if chest.x == x and chest.y == y:
                chest.type = Chest.ITEM
                chest.contents = item_id
                return
        raise IndexError(f"set_item: could not find chest at ({x}, {y}) on map {hex(map_id):<5}")

    def shuffle(self, types):
        import copy
        chests_shuffle = [copy.deepcopy(chest) for chest in self.chests if chest.type in types]

        import random
        random.shuffle(chests_shuffle)

        shuffle_index = 0
        for chest in self.chests:
            if chest.type in types:
                shuffled_chest = chests_shuffle[shuffle_index]
                shuffle_index += 1

                chest.type = shuffled_chest.type
                chest.contents = shuffled_chest.contents

    def random_tiered(self):
        def get_item():
            import random
            from data.chest_item_tiers import tiers, weights, tier_s_distribution
            from utils.weighted_random import weighted_random

            random_tier = weighted_random(weights)
            if random_tier < len(weights) - 1: # not s tier, use equal distribution
                random_tier_index = random.randrange(len(tiers[random_tier]))
                return tiers[random_tier][random_tier_index]

            weights = [entry[1] for entry in tier_s_distribution]
            random_s_index = weighted_random(weights)
            return tier_s_distribution[random_s_index][0]

        # first shuffle the chests to mix up empty/item/gold positions
        self.shuffle([Chest.EMPTY, Chest.ITEM, Chest.GOLD])

        import random
        for chest in self.chests:
            if chest.type == Chest.GOLD:
                chest.contents = int(random.triangular(1, Chest.MAX_GOLD_VALUE + 1, 1))
                if chest.contents == Chest.MAX_GOLD_VALUE + 1:
                    # triangular max is inclusive, very small chance need to round max down
                    chest.contents = Chest.MAX_GOLD_VALUE
            elif chest.type == Chest.ITEM:
                chest.contents = get_item()

    def shuffle_random(self):
        randomizable_types = [Chest.EMPTY, Chest.ITEM, Chest.GOLD]

        # first shuffle the chests to mix up empty/item/gold positions
        self.shuffle(randomizable_types)
        if self.args.chest_contents_shuffle_random_percent == 0:
            return

        import random
        possible_chests = [chest for chest in self.chests if chest.type in randomizable_types]
        random_percent = self.args.chest_contents_shuffle_random_percent / 100.0
        num_random_chests = int(len(possible_chests) * random_percent)
        random_chests = random.sample(possible_chests, num_random_chests)
        for chest in random_chests:
            if chest.type == Chest.GOLD:
                chest.randomize_gold()
            elif chest.type == Chest.ITEM:
                chest.contents = self.items.get_random()

    def clear_contents(self):
        for chest in self.chests:
            if chest.type == Chest.ITEM or chest.type == Chest.GOLD:
                chest.type = Chest.EMPTY
                chest.contents = 0

    def remove_excluded_items(self):
        exclude = self.items.get_excluded()
        for chest in self.all_chests:
            if chest.type == Chest.ITEM and chest.contents in exclude:
                chest.type = Chest.EMPTY
                chest.contents = 0

    def fix_shared_bits(self):
        # some chests on different maps share the same opened bits but have different contents
        # give them unique bits so both can be opened and contents aren't lost
        from data.area_chests import area_chests

        shared_chests = list(area_chests["Narshe Mines WOB"])
        shared_chests += list(area_chests["South Figaro Cave WOB"])
        shared_chests += list(area_chests["South Figaro Outside WOB"])

        for chest_id in shared_chests:
            self.all_chests[chest_id].bit = self.next_opened_bit
            self.next_opened_bit += 1

    def copy_thamasa_chests(self):
        # the unreachable thamasa map before leo's death has chests that are later lost
        # copy those chests to the wob/wor thamasa maps to make them available

        def copy_chest(self, src_map_id, src_chest_id, dst_map_id):
            import copy
            new_chest = copy.deepcopy(self.map_chests[src_map_id][src_chest_id])

            self.all_chests[self.next_id].x = new_chest.x
            self.all_chests[self.next_id].y = new_chest.y
            self.all_chests[self.next_id].bit = new_chest.bit
            self.all_chests[self.next_id].type = new_chest.type
            self.all_chests[self.next_id].contents = new_chest.contents
            self.next_id += 1

            # delete last chest to free space for new chest
            del self.chest_data[-1][-1]
            del self.map_chests[-1][-1]

            self.chest_data[dst_map_id].append(new_chest.data())
            self.map_chests[dst_map_id].append(new_chest)

        unreachable_thamasa_id = 0x157
        thamasa_wob_id = 0x154
        thamasa_wor_id = 0x158

        for chest_index in range(len(self.map_chests[unreachable_thamasa_id])):
            copy_chest(self, unreachable_thamasa_id, chest_index, thamasa_wob_id)
            copy_chest(self, unreachable_thamasa_id, chest_index, thamasa_wor_id)

    def update_duplicates(self):
        # for chests on multiple maps, only one of them should have been modified (the one with the lower id)
        # copy the first one to the duplicates so they all have the same contents/type/bits
        # they will give the same item and if one is opened the other(s) are no longer available
        for first_duplicate in self.duplicates:
            first_chest = self.all_chests[first_duplicate[0]]
            duplicate_chest = self.all_chests[first_duplicate[1]]

            duplicate_chest.bit = first_chest.bit
            duplicate_chest.type = first_chest.type
            duplicate_chest.contents = first_chest.contents

    def mod(self):
        self.fix_shared_bits()

        if self.args.chest_contents_shuffle_random:
            self.shuffle_random()
        elif self.args.chest_contents_random_tiered:
            self.random_tiered()
        elif self.args.chest_contents_empty:
            self.clear_contents()

        if self.args.chest_monsters_shuffle:
            self.shuffle([Chest.MONSTER])

        self.remove_excluded_items()

        self.copy_thamasa_chests()

        # update duplicates last after other chest mods finished
        self.update_duplicates()

    def write(self):
        if self.args.spoiler_log:
            self.log()

        for map_index in range(len(self.chest_data)):
            for map_chest_index in range(len(self.chest_data[map_index])):
                self.chest_data[map_index][map_chest_index] = self.map_chests[map_index][map_chest_index].data()

        self.chest_data.write()

    def log(self):
        from log import SECTION_WIDTH, section, format_option
        from data.area_chests import area_chests
        from data.item_names import id_name
        from textwrap import wrap

        lcolumn = []
        for area_name, chest_ids in area_chests.items():
            lcolumn.append(area_name)

            contents = []
            for chest_id in chest_ids:
                chest = self.all_chests[chest_id]
                if chest.type == Chest.ITEM:
                    contents.append(id_name[chest.contents])
                elif chest.type == Chest.GOLD:
                    contents.append(f"{chest.contents * 100} GP")
                elif chest.type == Chest.MONSTER:
                    # TODO how to get enemy name?
                    contents.append("MIAB")
                elif chest.type == Chest.EMPTY:
                    contents.append("Empty")

            lines = wrap(", ".join(contents), width = SECTION_WIDTH, \
                         initial_indent = "    ", subsequent_indent = "    ")
            for line in lines:
                lcolumn.append(line)
            lcolumn.append("")
        lcolumn.pop()

        section("Chests", lcolumn, [])

    def print(self):
        for map_index in range(len(self.map_chests)):
            print(f"map {hex(map_index):<5} chests:")
            for map_chest_index in range(len(self.map_chests[map_index])):
                self.map_chests[map_index][map_chest_index].print()
