from constants.checks import ANCIENT_CASTLE_DRAGON, FANATICS_TOWER_DRAGON, KEFKAS_TOWER_DRAGON_G, KEFKAS_TOWER_DRAGON_S, MT_ZOZO_DRAGON, NARSHE_DRAGON, OPERA_HOUSE_DRAGON, PHOENIX_CAVE_DRAGON, RECRUITABLE_DRAGONS
from event.event import *

from collections import namedtuple
DragonData = namedtuple("DragonData", ["name", "check", "battle_address", "countdown_address", "map_id", "npc_id"])
dragon_data = [
    DragonData("Ice Dragon", NARSHE_DRAGON, 0xc36df, 0xc36ec, 34, 0x11),
    DragonData("Storm Drgn", MT_ZOZO_DRAGON, 0xc43cd, 0xc43dc, 179, 0x10),
    DragonData("Dirt Drgn", OPERA_HOUSE_DRAGON, 0xab6df, 0xab6f3, 231, 0x28),
    DragonData("Gold Drgn", KEFKAS_TOWER_DRAGON_G, 0xc18f3, 0xc1900, 335, 0x10),
    DragonData("Skull Drgn", KEFKAS_TOWER_DRAGON_S, 0xc1920, 0xc192d, 354, 0x14),
    DragonData("Blue Drgn", ANCIENT_CASTLE_DRAGON, 0xc205b, 0xc2068, 408, 0x13),
    DragonData("Red Dragon", PHOENIX_CAVE_DRAGON, 0xc2048, 0xc2055, 315, 0x10),
    DragonData("White Drgn", FANATICS_TOWER_DRAGON, 0xc558b, 0xc559d, 368, 0x10),
]

class EightDragons(Event):
    def name(self):
        return "8 Dragons"

    def init_rewards(self):
        self.dragon_rewards = []

        import random
        dragon_character_count = random.randint(self.args.dragons_as_characters_min, self.args.dragons_as_characters_max)
        character_rewards = [x.bit for x in random.sample(RECRUITABLE_DRAGONS, dragon_character_count)]

        for dragon in dragon_data:
            reward = dragon.check.reward_types
            bit = dragon.check.bit
            self.dragon_rewards.append(self.add_reward(dragon.check, RewardType.CHARACTER if bit in character_rewards else reward))

    def init_event_bits(self, space):
        space.write(
            field.SetEventWord(event_word.DRAGONS_DEFEATED, 0),
        )

    def mod(self):

        self.dialog_mod()
        self.dragon_battles_mod()
        self.dragon_rewards_mod()
        self.white_dragon_reward_mod()

        for reward in self.dragon_rewards:
            self.log_reward(reward)

    def dialog_mod(self):
        # remove reference to crusader
        self.dialogs.set_text(1593, f"I found this in a 1000 year-old text:<line>8 dragons seal away awesome artifacts.<page>Defeat these dragons, and their power can be released…<end>")

        # remove the number of dragons
        self.dialogs.set_text(1505, "    Dragon Seal broken!!<end>")

    def dragon_battles_mod(self):
        call_size = 6 # invoke battle + call check game over
        for dragon in dragon_data:
            boss_pack_id = self.get_boss(dragon.name)

            space = Reserve(dragon.battle_address, dragon.battle_address + call_size,
                            f"8 dragons invoke battle {dragon.name.lower()}", field.NOP())
            space.write(
                field.InvokeBattle(boss_pack_id),
            )

    def dragon_rewards_mod(self):
        for index, dragon in enumerate(dragon_data):
            reward = self.dragon_rewards[index]

            if reward.type == RewardType.CHARACTER:
                self.dragon_reward_mod(dragon, [
                    field.RecruitAndSelectParty(reward.id),
                    field.RefreshEntities(),
                    field.FadeInScreen(),
                ])
                self.dragon_character_mod(dragon, reward)
            if reward.type == RewardType.ESPER:
                self.dragon_reward_mod(dragon, [
                    field.AddEsper(reward.id),
                    field.Dialog(self.espers.get_receive_esper_dialog(reward.id))
                ])
            if reward.type == RewardType.ITEM:
                self.dragon_reward_mod(dragon, [
                    field.AddItem(reward.id),
                    field.Dialog(self.items.get_receive_dialog(reward.id)),
                ])

    def dragon_character_mod(self, dragon, reward):
        npc = self.maps.get_npc(dragon.map_id, dragon.npc_id)
        npc.sprite = reward.id
        npc.palette = self.characters.get_palette(reward.id)

    def dragon_reward_mod(self, dragon, reward_instructions):
        call_instr_size = 4
        src = [
            field.SetEventBit(dragon.check.bit),
            field.FinishCheck(),
            field.Return(),
        ]
        call_instr_size = 4

        src = reward_instructions

        src += [
            field.SetEventBit(dragon.check.bit),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, f"8 dragons {dragon.name.lower()} receive reward")
        receive_reward = space.start_address

        space = Reserve(dragon.countdown_address, dragon.countdown_address + call_instr_size - 1,
                        f"8 dragons call receive reward {hex(receive_reward)}", field.NOP())
        space.write(
            field.Call(receive_reward),
        )

    def white_dragon_reward_mod(self):
        # white dragon does not drop its item reward
        # it is given after the battle (probably because it can be found on the veldt)
        # remove the reward after the battle in the fanatic's tower
        # and make pearl lance a white dragon drop for shuffled/random bosses
        space = Reserve(0xc5598, 0xc559c, "8 dragons pearl lance obtained after white dragon battle", field.NOP())

        pearl_lance_id = self.items.get_id("Pearl Lance")
        white_dragon_id = self.enemies.get_enemy("White Drgn")
        self.enemies.set_rare_drop(white_dragon_id, pearl_lance_id)
        self.enemies.set_common_drop(white_dragon_id, pearl_lance_id)
