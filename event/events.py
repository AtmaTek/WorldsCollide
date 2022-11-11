from memory.space import Bank, Allocate
from event.event_reward import RewardType, choose_reward, weighted_reward_choice
import instruction.field as field

class Events():
    def __init__(self, rom, args, data):
        self.rom = rom
        self.args = args

        self.dialogs = data.dialogs
        self.characters = data.characters
        self.items = data.items
        self.maps = data.maps
        self.enemies = data.enemies
        self.espers = data.espers
        self.shops = data.shops

        self.pathing = ""   #used for display but not in logic
        self.pathingdict = {}

        events = self.mod()

        self.validate(events)

    def mod(self):
        # generate list of events from files
        import os, importlib, inspect
        from event.event import Event
        events = []
        name_event = {}
        for event_file in sorted(os.listdir(os.path.dirname(__file__))):
            if event_file[-3:] != '.py' or event_file == 'events.py' or event_file == 'event.py':
                continue

            module_name = event_file[:-3]
            event_module = importlib.import_module('event.' + module_name)

            for event_name, event_class in inspect.getmembers(event_module, inspect.isclass):
                if event_name.lower() != module_name.replace('_', '').lower():
                    continue
                event = event_class(name_event, self.rom, self.args, self.dialogs, self.characters, self.items, self.maps, self.enemies, self.espers, self.shops)
                events.append(event)
                name_event[event.name()] = event

        # select event rewards
        if self.args.character_gating:
            self.character_gating_mod(events, name_event)
        else:
            self.open_world_mod(events)

        # initialize event bits, mod events, log rewards
        log_strings = []
        space = Allocate(Bank.CC, 400, "event/npc bit initialization", field.NOP())
        for event in events:
            event.init_event_bits(space)
            event.mod()

            if self.args.spoiler_log and (event.rewards_log or event.changes_log):
                log_strings.append(event.log_string())

        log_strings.append("* = Esper/Magicite")
        space.write(field.Return())

        if self.args.spoiler_log:
            from log import section
            section("Events", log_strings, [])

    def init_reward_slots(self, events):
        import random
        reward_slots = []
        for event in events:
            event.init_rewards()
            for reward in event.rewards:
                if reward.id is None:
                    reward_slots.append(reward)

        random.shuffle(reward_slots)
        return reward_slots

    def choose_single_possible_type_rewards(self, reward_slots):
        for slot in reward_slots:
            if slot.single_possible_type():
                slot.id, slot.type = choose_reward(slot.possible_types, self.characters, self.espers, self.items, exclude_character=[slot.check.gate_character])

    def choose_char_esper_possible_rewards(self, reward_slots):
        for slot in reward_slots:
            if slot.possible_types == (RewardType.CHARACTER | RewardType.ESPER):
                slot.id, slot.type = choose_reward(slot.possible_types, self.characters, self.espers, self.items)

    def choose_item_possible_rewards(self, reward_slots):
        for slot in reward_slots:
            slot.id, slot.type = choose_reward(slot.possible_types, self.characters, self.espers, self.items)

    def character_gating_mod(self, events, name_event):
        import random
        reward_slots = self.init_reward_slots(events)

        # for every event with only one reward type possible, assign random rewards
        # note: this includes start, which can get up to 4 characters
        self.choose_single_possible_type_rewards(reward_slots)

        readily_available_characters = [x.id for x in reward_slots if x.check and x.check.gate_character is None and x.possible_types == RewardType.CHARACTER]

        # find characters that were assigned to start as well as any ungated characters that were assigned in choose_single_possible_reward_types() above
        characters_available = [reward.id for reward in name_event["Start"].rewards] + readily_available_characters

        # find all the rewards that can be a character
        character_slots = []
        for event in events:
            for reward in event.rewards:
                if reward.possible_types & RewardType.CHARACTER:
                    character_slots.append(reward)

        iteration = 0
        slot_iterations = {} # keep track of how many iterations each slot has been available
        while self.characters.get_available_count():

            # build list of which slots are available and how many iterations those slots have already had
            unlocked_slots = []
            unlocked_slot_iterations = []
            for slot in character_slots:
                slot_empty = slot.id is None
                gate_char = slot.check.gate_character if slot.check else None
                gate_char_available = (gate_char in characters_available or gate_char is None)
                enough_chars_available = len(characters_available) >= slot.event.characters_required()
                if slot_empty and gate_char_available and enough_chars_available:
                    if slot in slot_iterations:
                        slot_iterations[slot] += 1
                    else:
                        slot_iterations[slot] = 0
                    unlocked_slots.append(slot)
                    unlocked_slot_iterations.append(slot_iterations[slot])

            # this means an impossible start has occured.
            # i.e. no character can be retrieved given the starting char + check availability
            assert len(unlocked_slots) > 0

            # pick slot for the next character weighted by number of iterations each slot has been available
            slot_index = weighted_reward_choice(unlocked_slot_iterations, iteration)
            slot = unlocked_slots[slot_index]
            slot.id = self.characters.get_random_available()
            slot.type = RewardType.CHARACTER
            characters_available.append(slot.id)
            self.characters.set_character_path(slot.id, slot.check.gate_character)
            iteration += 1

        if self.args.debug:
            for event in events:
                for reward in event.rewards:
                    if reward.type == RewardType.CHARACTER:
                        self.pathing = self.pathing + "\n" + event.name() + ": " + self.characters.get_name(reward.id) + "/ " + self.characters.get_default_name(reward.id)
                        self.pathingdict[self.characters.get_default_name(reward.id)] = event.name()
                self.print_pathing_tree()

        # get all reward slots still available
        reward_slots = [reward for event in events for reward in event.rewards if reward.id is None]
        random.shuffle(reward_slots) # shuffle to prevent picking them in alphabetical order

        # for every event with only char/esper rewards possible, assign random rewards
        self.choose_char_esper_possible_rewards(reward_slots)

        reward_slots = [slot for slot in reward_slots if slot.id is None]

        # assign rest of rewards where item is possible
        self.choose_item_possible_rewards(reward_slots)
        return

    def open_world_mod(self, events):
        import random
        reward_slots = self.init_reward_slots(events)

        # first choose all the rewards that only have a single type possible
        # this way we don't run out of that reward type before getting to the event
        self.choose_single_possible_type_rewards(reward_slots)

        reward_slots = [slot for slot in reward_slots if not slot.single_possible_type()]

        # next choose all the rewards where only character/esper types possible
        # this way we don't run out of characters/espers before getting to these events
        self.choose_char_esper_possible_rewards(reward_slots)

        reward_slots = [slot for slot in reward_slots if slot.id is None]

        # choose the rest of the rewards, items given to events after all characters/events assigned
        self.choose_item_possible_rewards(reward_slots)

    def validate(self, events):
        char_esper_checks = []
        for event in events:
            char_esper_checks += [r for r in event.rewards if r.possible_types == (RewardType.CHARACTER)]

    def print_pathing_tree(self):
        pathway_with_chars_list = []
        pathway_list = []

        for x in range(14):
            path = self.characters.get_character_path(x)
            pathway_with_chars = ""
            pathway = ""

            ### get the path leading to the character's location
            for req_char_index in path:
                character_location = self.pathingdict[self.characters.DEFAULT_NAME[req_char_index]]
                character_name = self.characters.DEFAULT_NAME[req_char_index]
                pathway += character_location + " -> "
                pathway_with_chars += (character_name + " / " + character_location + " -> ")

            ### get the character's location
            character_location = self.pathingdict[self.characters.DEFAULT_NAME[x]]
            character_name = self.characters.DEFAULT_NAME[x]
            pathway += character_location
            pathway_with_chars += (character_name + " / " + character_location)

            print(pathway_with_chars)
            pathway_with_chars_list.append(pathway_with_chars)
            pathway_list.append(pathway)

