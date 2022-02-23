from data.enemy_pack import EnemyPack4, EnemyPack2
from data.structures import DataArray
import data.bosses as bosses

class EnemyPacks():
    # the first 256 enemy packs are groups of 4 formations
    PACK4_START = 0xf4800
    PACK4_END = 0xf4fff
    PACK4_SIZE = 8

    # the next 256 enemy packs are groups of 2 formations
    PACK2_START = 0xf5000
    PACK2_END = 0xf53ff
    PACK2_SIZE = 4

    ZONE_EATER = 32
    VELDT = 255 # placeholder for veldt in wob/wor
    PHUNBABA3 = 386
    DOOM_GAZE = 349

    def __init__(self, rom, args, formations):
        self.rom = rom
        self.args = args
        self.formations = formations

        self.pack4_data = DataArray(self.rom, self.PACK4_START, self.PACK4_END, self.PACK4_SIZE)
        self.pack2_data = DataArray(self.rom, self.PACK2_START, self.PACK2_END, self.PACK2_SIZE)

        self.packs = []
        for pack4_index in range(len(self.pack4_data)):
            pack = EnemyPack4(pack4_index, self.pack4_data[pack4_index])
            self.packs.append(pack)

        for pack2_index in range(len(self.pack2_data)):
            pack = EnemyPack2(pack2_index, self.pack2_data[pack2_index])
            self.packs.append(pack)

    def _replaceable_bosses(self):
        replaceable = list(bosses.normal_pack_name)
        if not self.args.shuffle_random_phunbaba3:
            replaceable.remove(self.PHUNBABA3)
            self.event_boss_replacements[self.PHUNBABA3] = self.PHUNBABA3
        if not self.args.doom_gaze_no_escape:
            # if doom gaze can escape, don't shuffle/randomize him
            # possibly having multiple doom gazes while trying to keep track of hp is awkward
            # how would that work with him being in his original spot and the others? How to know when to get bahamut esper?
            replaceable.remove(self.DOOM_GAZE)
            self.event_boss_replacements[self.DOOM_GAZE] = self.DOOM_GAZE
        return replaceable

    def phunbaba3_safety_check(self, bosses_possible):
        import random

        # bababreath in the mine cart ride causes a bug, if phunbaba3 was assigned to the
        # number 128 location then randomly choose a different boss to swap it with
        number_128_id = self.get_id("Number 128")
        if self.event_boss_replacements[number_128_id] == self.PHUNBABA3:
            possible_replacements = []
            for boss in bosses_possible:
                if self.event_boss_replacements[boss] != self.PHUNBABA3:
                    possible_replacements.append(boss)
            if not possible_replacements:
                # in the incredibly unlikely scenario that every single boss has been
                # replaced by phunbaba 3, assign phunbaba 4 to the number 128 location
                self.event_boss_replacements[number_128_id] = self.get_id("Phunbaba 4")
                return

            random.shuffle(possible_replacements)
            swap_target = possible_replacements.pop()
            self.event_boss_replacements[number_128_id] = self.event_boss_replacements[swap_target]
            self.event_boss_replacements[swap_target] = self.PHUNBABA3

    def shuffle_event_bosses(self):
        import random
        self.event_boss_replacements = {}

        if self.args.mix_bosses_dragons:
            bosses_dragons_to_replace = self._replaceable_bosses() + list(bosses.dragon_pack_name)
            bosses_dragons_possible = bosses_dragons_to_replace.copy()

            random.shuffle(bosses_dragons_possible)
            for index, boss in enumerate(bosses_dragons_to_replace):
                self.event_boss_replacements[boss] = bosses_dragons_possible[index]

            self.phunbaba3_safety_check(bosses_dragons_to_replace)
        else:
            bosses_to_replace = self._replaceable_bosses()
            bosses_possible = bosses_to_replace.copy()

            random.shuffle(bosses_possible)
            for index, boss in enumerate(bosses_to_replace):
                self.event_boss_replacements[boss] = bosses_possible[index]

            dragons_to_replace = list(bosses.dragon_pack_name)
            dragons_possible = dragons_to_replace.copy()

            random.shuffle(dragons_possible)
            for index, dragon in enumerate(dragons_to_replace):
                self.event_boss_replacements[dragon] = dragons_possible[index]

            self.phunbaba3_safety_check(bosses_to_replace)

    def randomize_event_bosses(self):
        import args, random, objectives
        from constants.objectives.conditions import names as possible_condition_names

        self.event_boss_replacements = {}

        boss_condition_name = "Boss"
        dragon_condition_name = "Dragon"
        dragons_condition_name = "Dragons"
        assert boss_condition_name in possible_condition_names
        assert dragon_condition_name in possible_condition_names
        assert dragons_condition_name in possible_condition_names

        required_boss_formations = set()
        required_dragon_formations = set()
        min_dragon_formations = 0
        for objective in objectives:
            for condition in objective.conditions:
                if condition.NAME == boss_condition_name:
                    required_boss_formations.add(bosses.name_formation[condition.boss_name()])
                elif condition.NAME == dragon_condition_name:
                    required_dragon_formations.add(bosses.name_formation[condition.dragon_name()])
                elif condition.NAME == dragons_condition_name and condition.count > min_dragon_formations:
                    min_dragon_formations = condition.count

        dragon_formations_needed = min_dragon_formations - len(required_dragon_formations)
        if dragon_formations_needed > 0:
            all_dragon_formations = set(bosses.dragon_formation_name)
            remaining_dragon_formations = list(all_dragon_formations - required_dragon_formations)
            random_dragon_formations = random.sample(remaining_dragon_formations, dragon_formations_needed)
            required_dragon_formations |= set(random_dragon_formations)

        required_boss_packs = set()
        for pack_id, pack_name in bosses.normal_pack_name.items():
            formations = self.get_formations(pack_id)
            for formation_id in formations:
                if formation_id in required_boss_formations:
                    required_boss_packs.add(pack_id)

        required_dragon_packs = set()
        for pack_id, pack_name in bosses.dragon_pack_name.items():
            formations = self.get_formations(pack_id)
            for formation_id in formations:
                if formation_id in required_dragon_formations:
                    required_dragon_packs.add(pack_id)

        if self.args.mix_bosses_dragons:
            bosses_dragons_to_replace = self._replaceable_bosses() + list(bosses.dragon_pack_name)
            random.shuffle(bosses_dragons_to_replace)

            for pack in required_boss_packs:
                self.event_boss_replacements[bosses_dragons_to_replace.pop()] = pack

            for pack in required_dragon_packs:
                self.event_boss_replacements[bosses_dragons_to_replace.pop()] = pack

            # guarantee 8 dragons
            dragons_possible = list(bosses.dragon_pack_name)
            for index in range(len(required_dragon_packs), len(bosses.dragon_pack_name)):
                self.event_boss_replacements[bosses_dragons_to_replace.pop()] = random.choice(dragons_possible)

            bosses_possible = self._replaceable_bosses()
            for boss in bosses_dragons_to_replace:
                self.event_boss_replacements[boss] = random.choice(bosses_possible)

            self.phunbaba3_safety_check(bosses_possible + dragons_possible)
        else:
            bosses_to_replace = self._replaceable_bosses()
            random.shuffle(bosses_to_replace)
            for pack in required_boss_packs:
                self.event_boss_replacements[bosses_to_replace.pop()] = pack

            bosses_possible = self._replaceable_bosses()
            for boss in bosses_to_replace:
                self.event_boss_replacements[boss] = random.choice(bosses_possible)

            dragons_to_replace = list(bosses.dragon_pack_name)
            random.shuffle(dragons_to_replace)
            for pack in required_dragon_packs:
                self.event_boss_replacements[dragons_to_replace.pop()] = pack

            dragons_possible = list(bosses.dragon_pack_name)
            for dragon in dragons_to_replace:
                self.event_boss_replacements[dragon] = random.choice(dragons_possible)

            self.phunbaba3_safety_check(bosses_possible)

    def randomize_packs(self, packs, boss_percent, no_phunbaba3 = False):
        exclude_bosses = None
        if no_phunbaba3 or not self.args.shuffle_random_phunbaba3:
            exclude_bosses = [self.formations.PHUNBABA3]
        if not self.args.doom_gaze_no_escape:
            if exclude_bosses is None:
                exclude_bosses = [self.formations.DOOM_GAZE]
            else:
                exclude_bosses.append(self.formations.DOOM_GAZE)

        import random
        for pack_id in packs:
            if random.random() < boss_percent:
                for formation_index in range(self.packs[pack_id].FORMATION_COUNT):
                    self.packs[pack_id].formations[formation_index] = self.formations.get_random_boss(exclude_bosses)
            else:
                for formation_index in range(self.packs[pack_id].FORMATION_COUNT):
                    self.packs[pack_id].formations[formation_index] = self.formations.get_random_normal()

    def randomize_fixed(self):
        lete_river = [263, 264] # nautiloid, exocite, pterodon
        imperial_camp = [272, 298, 300, 269, 270] # soldier, dogs, templar/soldier, final 3 battles
        doma_wob = [299] # soldier
        phantom_train = [303] # ghost (siegfried unrandomized for style)
        serpent_trench = [275, 276, 277] # anguiform, actaneon, aspik
        narshe_battle = [278, 279, 280] # brown and green soldiers, rider
        opera_house = [281] # sewer rat, vermin
        vector = [257, 285, 284] # guards, garm, commando, protoarmor, pipsqueak
        mine_cart = [297, 400] # mag roaders
        imperial_base = [295, 296] # soldier and magitek
        sealed_cave = [405] # ninja
        burning_house = [301, 287] # balloons
        iaf = [382] # sky armor / spit fire
        floating_continent_escape = [397, 398, 399] # naughty
        owzer_mansion = [402, 403, 407, 404] # dahling, nightshade, souldancer, still life

        self.fixed = lete_river + imperial_camp + doma_wob + phantom_train + serpent_trench + narshe_battle + opera_house + vector
        self.fixed += mine_cart + imperial_base + sealed_cave + burning_house + iaf + floating_continent_escape + owzer_mansion

        boss_percent = self.args.fixed_encounters_random / 100.0

        # fixed packs which are capable of handling bababreath
        phunbaba3_safe = imperial_camp + doma_wob + phantom_train + vector + imperial_base + sealed_cave
        phunbaba3_safe += burning_house + iaf + floating_continent_escape + owzer_mansion
        self.randomize_packs(phunbaba3_safe, boss_percent)

        # for some reason, losing the party leader here makes the raft move very slowly after the battle
        self.randomize_packs(lete_river, boss_percent, no_phunbaba3 = True)

        # bababreath on party leader before the caves causes party to be invisible on entry
        # it also happens if first fight phunbaba3 and then another non-phunbaba3 battle before the cave
        self.randomize_packs(serpent_trench, boss_percent, no_phunbaba3 = True)

        # special event instead of game over (move to save point and try again)
        self.randomize_packs(narshe_battle, boss_percent, no_phunbaba3 = True)

        # special game over event does not refresh objects/party leader
        self.randomize_packs(opera_house, boss_percent, no_phunbaba3 = True)

        # same issue as replacing number 128 with phunbaba3 (removed party member reappears in party after mine cart ride)
        self.randomize_packs(mine_cart, boss_percent, no_phunbaba3 = True)

    def _update_names(self):
        # generate names based on formations and enemies
        self.pack_names = []
        for pack in self.packs:
            name = ""
            unique_formations = []
            for formation_id in pack.formations:
                if formation_id not in unique_formations:
                    unique_formations.append(formation_id)

            if len(unique_formations) == 1:
                name = self.formations.get_name(formation_id)
            else:
                for formation_id in unique_formations:
                    name += f"({self.formations.get_name(formation_id)}) or "
                name = name[:-4]
            self.pack_names.append(name)

    def get_id(self, name):
        if name in bosses.name_pack:
            return bosses.name_pack[name]
        for pack in self.packs:
            if pack.name == name:
                return pack.id

    def get_name(self, pack_id):
        if pack_id in bosses.pack_name:
            return bosses.pack_name[pack_id]
        return self.pack_names[pack_id]

    def get_formations(self, pack_id):
        return self.packs[pack_id].formations

    def has_enemy(self, pack_id, enemy_id):
        for formation_id in self.packs[pack_id].formations:
            if self.formations.has_enemy(formation_id, enemy_id):
                return True
        return False

    def get_event_boss_replacement(self, original_boss_name):
        original_boss_id = self.get_id(original_boss_name)
        if self.event_boss_replacements is None:
            return original_boss_id

        return self.event_boss_replacements[original_boss_id]

    def remove_extra_formations(self):
        # set all packs to not have any formations that are randomized with the subsequent 3
        for pack in self.packs:
            for formation_index in range(pack.FORMATION_COUNT):
                pack.extra_formations[formation_index] = False

    def mod(self):
        if self.args.boss_battles_shuffle:
            self.shuffle_event_bosses()
        elif self.args.boss_battles_random:
            self.randomize_event_bosses()
        else:
            self.event_boss_replacements = None

        if not self.args.fixed_encounters_original:
            self.randomize_fixed()

        if not self.args.random_encounters_original:
            # if shuffled/randomized encounters, need to remove extra formations from floating continent
            # otherwise, it is possible to get a formation on the floating continent where one of the next 3 formations is invalid
            # TODO try and fix this by shuffling/randomizing formations themselves instead of the foramtions in packs
            #      or possibly try to do both for fewer duplicates in packs (and skip shuffling/randomizing the fc pack 112)
            self.remove_extra_formations()

        # after modification, generate names
        self._update_names()

    def write(self):
        pack_index = 0
        for pack4_index in range(len(self.pack4_data)):
            self.pack4_data[pack4_index] = self.packs[pack_index].data()
            pack_index += 1

        for pack2_index in range(len(self.pack2_data)):
            self.pack2_data[pack2_index] = self.packs[pack_index].data()
            pack_index += 1

        self.pack4_data.write()
        self.pack2_data.write()

    def print(self):
        for pack in self.packs:
            pack.print()
