from data.item import Item
from memory.space import Bank, Space, Reserve, Allocate, Free, Write, Read
import data.direction as direction

import data.event_bit as event_bit
import data.event_word as event_word
import data.npc_bit as npc_bit
import data.battle_bit as battle_bit

import instruction.asm as asm
import instruction.field as field
import instruction.field.entity as field_entity
import instruction.world as world
import instruction.vehicle as vehicle

from instruction.event import EVENT_CODE_START
from event.event_reward import RewardType, Reward

class Event():
    def __init__(self, events, rom, args, dialogs, characters, items, maps, enemies, espers, shops):
        self.events = events
        self.rom = rom
        self.args = args
        self.dialogs = dialogs
        self.characters = characters
        self.items = items
        self.maps = maps
        self.enemies = enemies
        self.espers = espers
        self.shops = shops
        self.rewards = []

        self.rewards_log = []
        self.changes_log = []

    def name(self):
        raise NotImplementedError(self.__class__.__name__ + " event name")

    def character_gate(self):
        return None

    def characters_required(self):
        return 1

    def get_reward_type(self, default: RewardType, check_info = None):
        from constants.checks import character_esper_name_check

        fallback_bit = character_esper_name_check.get(self.name())
        bit = check_info.bit if check_info else fallback_bit

        assert (bit or fallback_bit)

        if bit in self.args.item_reward_checks:
            return RewardType.ITEM

        return default

    # check_info can be passed if name / bit differs.
    # This will only be the case when a check is broken up into multiple pieces (Auction House, Floating Contintent, Mtek, etc.)
    # @example
    # from data.checks import AUCTION1, AUCTION2
    # self.reward1 = self.add_reward(RewardType.Esper | RewardType.Item, AUCTION1)
    # self.reward2 = self.add_reward(RewardType.Esper | RewardType.Item, AUCTION2)
    def add_reward(self, possible_types, check_info = None):
        assert possible_types

        new_reward = Reward(self, possible_types)
        # We don't need any extra logic if only one type is selected
        possible_types = possible_types if new_reward.single_possible_type() else self.get_reward_type(possible_types, check_info)
        self.rewards.append(new_reward)
        return new_reward

    def init_rewards(self):
        pass

    def init_event_bits(self, space):
        pass

    def get_boss(self, original_boss_name, log_change = True):
        pack_id = self.enemies.get_event_boss(original_boss_name)

        if (self.args.boss_battles_shuffle or self.args.boss_battles_random) and log_change:
            boss_name = self.enemies.packs.get_name(pack_id)
            self.log_change(original_boss_name, boss_name)
        return pack_id

    def log_reward(self, reward, prefix = "", suffix = ""):
        reward_string = prefix
        if reward.type == RewardType.CHARACTER:
            reward_string += self.characters.get_name(reward.id)
        elif reward.type == RewardType.ESPER:
            reward_string += "*" + self.espers.get_name(reward.id)
        elif reward.type == RewardType.ITEM:
            reward_string += self.items.get_name(reward.id)
        self.rewards_log.append(reward_string + suffix)

    def log_change(self, original, new):
        self.changes_log.append(f"    {original:<14} -> {new}")

    def log_string(self):
        log_string = f"{self.name():<30}"
        if self.rewards_log:
            log_string += f" {', '.join(self.rewards_log)}"
        if self.changes_log:
            log_string += '\n' + '\n'.join(self.changes_log)

        return log_string

    def mod(self):
        raise NotImplementedError(self.__class__.__name__ + " event must implement mod")
