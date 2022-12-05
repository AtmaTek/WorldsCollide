from event.event import *
from constants.checks import NARSHE_WEAPON_SHOP, NARSHE_WEAPON_SHOP_MINES

class NarsheWOR(Event):
    def name(self):
        return NARSHE_WEAPON_SHOP.name

    def character_gate(self):
        return self.characters.LOCKE

    def init_rewards(self):

        self.reward1 = self.add_reward(NARSHE_WEAPON_SHOP)
        self.reward2 = self.add_reward(NARSHE_WEAPON_SHOP_MINES)

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(event_bit.MET_LONE_WOLF_WOR),
            field.ClearEventBit(npc_bit.WHELK_GUARD_TRITOCH_NARSHE_WOB),
        )

    def mod(self):
        self.pickpocket_mod()

        self.locke_unlock_doors_mod()
        if self.args.character_gating:
            self.add_gating_condition()
        else:
            # allow doors to be unlocked without any condition
            self.unlock_doors_condition_mod([])

        if self.reward1.type == RewardType.ESPER:
            self.weapon_shop_esper_mod()
        elif self.reward1.type == RewardType.ITEM:
            self.weapon_shop_item_mod()

        self.cursed_shield_mod()

        self.log_reward(self.reward1)
        self.log_reward(self.reward2)

    def pickpocket_mod(self):
        # delete the tile events that trigger lone wolf to appear (at entrance of narshe)
        self.maps.delete_event(0x020, 37, 50)
        self.maps.delete_event(0x020, 38, 50)
        self.maps.delete_event(0x020, 39, 50)

    def locke_unlock_doors_mod(self):
        # allow other characters to unlock doors instead of only locke (who may not be in the party)
        space = Reserve(0xc0a2a, 0xc0a2e, "narshe wor unlock door add rearrange party with locke as leader", field.NOP())
        space = Reserve(0xc0a41, 0xc0a41, "narshe wor locke to party member 0")
        space.write(field_entity.PARTY0)
        space = Reserve(0xc0a4a, 0xc0a4a, "narshe wor locke to party member 0")
        space.write(field_entity.PARTY0)
        space = Reserve(0xc0a50, 0xc0a50, "narshe wor locke to party member 0")
        space.write(field_entity.PARTY0)
        space = Reserve(0xc0a5a, 0xc0a5a, "narshe wor locke to party member 0")
        space.write(field_entity.PARTY0)
        space = Reserve(0xc0a5f, 0xc0a5f, "narshe wor locke to party member 0")
        space.write(field_entity.PARTY0)
        space = Reserve(0xc0a67, 0xc0a67, "narshe wor locke to party member 0")
        space.write(field_entity.PARTY0)
        space = Reserve(0xc0a6c, 0xc0a6c, "narshe wor locke to party member 0")
        space.write(field_entity.PARTY0)
        space = Reserve(0xc0a83, 0xc0a83, "narshe wor locke to party member 0")
        space.write(field_entity.PARTY0)

    def unlock_doors_condition_mod(self, condition_instructions):
        # replace code that branches to locked dialog if locke not in party
        space = Reserve(0xc0a9e, 0xc0aa4, "narshe wor inn door", field.NOP())
        space.write(
            condition_instructions,
        )
        space = Reserve(0xc0aae, 0xc0ab4, "narshe wor weapon shop door", field.NOP())
        space.write(
            condition_instructions,
        )
        space = Reserve(0xc0abe, 0xc0ac4, "narshe wor relic shop door", field.NOP())
        space.write(
            condition_instructions,
        )
        space = Reserve(0xc0ace, 0xc0ad4, "narshe wor store room door", field.NOP())
        space.write(
            condition_instructions,
        )
        space = Reserve(0xc0ade, 0xc0ae4, "narshe wor elder house door", field.NOP())
        space.write(
            condition_instructions,
        )
        space = Reserve(0xc0aee, 0xc0af4, "narshe wor item shop door", field.NOP())
        space.write(
            condition_instructions,
        )

    def add_gating_condition(self):
        LOCKED = 0xc0a9a

        # change doors to unlock if locke is recruited even if not in current party
        self.unlock_doors_condition_mod([
            field.BranchIfEventBitClear(event_bit.character_recruited(self.character_gate()), LOCKED),
        ])

    def weapon_shop_mod(self, dialog_first_line):
        space = Reserve(0xc0b24, 0xc0b26, "narshe wor i wanted to give you this", field.NOP())

        import data.text
        reward1_esper = self.reward1.type == RewardType.ESPER
        reward2_esper = self.reward2.type == RewardType.ESPER
        # item names stored as TEXT2, dialogs are TEXT1
        reward1_esper_line = lambda esper: f"<line><choice> Leave it the stone “" + data.text.convert(self.espers.get_name(esper) + "”", data.text.TEXT1)
        reward2_esper_line = lambda esper: f"<line><choice> Make it the stone “" + data.text.convert(self.espers.get_name(esper) + "”", data.text.TEXT1)
        get_item_line = lambda item: f"<line><choice> Make it “" + data.text.convert(self.items.get_name(item) + "”", data.text.TEXT1)

        add_esper = lambda esper: field.AddEsper(esper, sound_effect = False)
        add_item = lambda item: field.AddItem(item, sound_effect = False)

        reward1 = reward1_esper_line(self.reward1.id) if reward1_esper else get_item_line(self.reward1.id)
        reward2 = reward2_esper_line(self.reward2.id) if reward2_esper else get_item_line(self.reward2.id)

        self.dialogs.set_text(1519, dialog_first_line + reward1  + reward2 + "<end>")

        # if esper or first item chosen, set event bit to know second item should be given by guard
        space = Reserve(0xc0b42, 0xc0b44, "narshe wor ragnarok esper right", field.NOP())
        space.write(
            field.SetEventBit(npc_bit.WHELK_GUARD_TRITOCH_NARSHE_WOB),
        )
        space = Reserve(0xc0b58, 0xc0b5a, "narshe wor ragnarok weapon right", field.NOP())
        space.write(
            field.SetEventBit(npc_bit.WHELK_GUARD_TRITOCH_NARSHE_WOB),
        )

        src = [
            # add reward 1 based on item type
            add_esper(self.reward1.id) if reward1_esper else add_item(self.reward1.id),
            field.SetEventBit(event_bit.GOT_RAGNAROK),
            field.SetEventBit(event_bit.CHOSE_RAGNAROK_ESPER),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "narshe wor choose first reward")
        choose_first_option = space.start_address

        space = Reserve(0xc0b53, 0xc0b56, "narshe wor give party ragnarok esper", field.NOP())
        space.write(
            field.Call(choose_first_option),
        )

        src = [
            # add reward 2 based on item type
            add_esper(self.reward2.id) if reward2_esper else add_item(self.reward2.id),
            field.SetEventBit(event_bit.GOT_RAGNAROK),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "narshe wor choose second reward")
        choose_second_option = space.start_address

        space = Reserve(0xc0b67, 0xc0b6a, "narshe wor give party ragnarok weapon", field.NOP())
        space.write(
            field.Call(choose_second_option),
        )

    def behind_whelk_mod(self):
        from data.npc import NPC
        guard_npc = NPC()
        guard_npc.x = 74
        guard_npc.y = 40
        guard_npc.sprite = 52
        guard_npc.palette = 0
        guard_npc.direction = direction.DOWN
        guard_npc.speed = 3
        guard_npc.event_byte = npc_bit.event_byte(npc_bit.WHELK_GUARD_TRITOCH_NARSHE_WOB) # 0x60
        guard_npc.event_bit = npc_bit.event_bit(npc_bit.WHELK_GUARD_TRITOCH_NARSHE_WOB)   # 0x05

        guard_npc_id = self.maps.append_npc(0x02b, guard_npc)

        add_esper = lambda esper_id: [
            field.AddEsper(esper_id),
            field.Dialog(self.espers.get_receive_esper_dialog(esper_id)),
        ]

        add_item = lambda item_id: [
            field.AddItem(item_id),
            field.Dialog(self.items.get_receive_dialog(item_id))
        ]
        src = [
            field.BranchIfEventBitSet(event_bit.CHOSE_RAGNAROK_ESPER, "RECEIVE_SECONDARY")
        ]

        # Add reward one based on reward type
        src += add_esper(self.reward1.id) if self.reward1.type == RewardType.ESPER else add_item(self.reward1.id)

        src += [
            field.Branch("DELETE_GUARD"),
            "RECEIVE_SECONDARY",
        ]

        # Add reward two based on reward type
        src += [
            add_esper(self.reward2.id) if self.reward2.type == RewardType.ESPER else add_item(self.reward2.id),
        ]

        src += [
            "DELETE_GUARD",
            field.FadeOutScreen(),
            field.WaitForFade(),
            field.HideEntity(guard_npc_id),
            field.ClearEventBit(npc_bit.WHELK_GUARD_TRITOCH_NARSHE_WOB),
            field.RefreshEntities(),
            field.FadeInScreen(),
            field.SetEventBit(event_bit.GOT_BOTH_REWARDS_WEAPON_SHOP),
            field.FinishCheck(),
            field.Return(),
        ]

        space = Write(Bank.CC, src, "narshe wor second weapon shop reward guard npc event")
        guard_event = space.start_address

        guard_npc.set_event_address(guard_event)

    def weapon_shop_esper_mod(self):
        self.weapon_shop_mod("This stone gives off an eerie aura!")
        self.behind_whelk_mod()

    def weapon_shop_item_mod(self):
        magicite_npc_id = 0x11
        magicite_npc = self.maps.get_npc(0x18, magicite_npc_id)
        magicite_npc.sprite = 106
        magicite_npc.palette = 6
        magicite_npc.split_sprite = 1
        magicite_npc.direction = direction.DOWN

        self.weapon_shop_mod("This gives off an eerie aura!")
        self.behind_whelk_mod()


    def cursed_shield_mod(self):
        self.dialogs.set_text(1523, f"“Cursed Shld”…{self.items.cursed_shield_battles}<end>")
        if not self.args.cursed_shield_battles_original:
            self.log_change("Cursed Shield 256", self.items.cursed_shield_battles)
