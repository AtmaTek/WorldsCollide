from event.event import *

class PhoenixCave(Event):
    def name(self):
        return "Phoenix Cave"

    def character_gate(self):
        return self.characters.LOCKE

    def characters_required(self):
        return 2

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def mod(self):
        self.locke_npc_id = 0x10
        self.locke_npc = self.maps.get_npc(0x139, self.locke_npc_id)

        self.landing_mod()
        self.end_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)

    def landing_mod(self):
        self.need_more_characters_dialog = 2978
        self.dialogs.set_text(self.need_more_characters_dialog, "We need to find more allies.<end>")

        self.need_locke_dialog = 2981
        self.dialogs.set_text(self.need_locke_dialog, "We need to find Locke.<end>")

        src = [
            Read(0xa0405, 0xa0408),
            Read(0xa040c, 0xa0428),
        ]
        space = Write(Bank.CA, src, "phoenix cave enter")
        enter_phoenix_cave = space.start_address

        src = [
            field.LoadMap(0x01, direction.DOWN, default_music = False, x = 118, y = 156, fade_in = True, airship = True),
            vehicle.End(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "phoenix cave cancel landing")
        cancel_landing = space.start_address

        src = [
            field.Dialog(self.need_locke_dialog),
            field.Branch(cancel_landing),
        ]
        space = Write(Bank.CA, src, "phoenix cave no locke cancel")
        no_locke_cancel_landing = space.start_address

        src = [
            field.Dialog(self.need_more_characters_dialog),
            field.Branch(cancel_landing),
        ]
        space = Write(Bank.CA, src, "phoenix cave character requirements cancel")
        character_requirements_cancel_landing = space.start_address

        space = Reserve(0xa0405, 0xa0428, "phoenix cave landing checks", field.NOP())
        if self.args.character_gating:
            space.write(
                field.BranchIfEventBitClear(event_bit.character_recruited(self.character_gate()), no_locke_cancel_landing),
            )
        space.write(
            field.BranchIfEventWordLess(event_word.CHARACTERS_AVAILABLE, self.characters_required(), character_requirements_cancel_landing),
            field.Branch(enter_phoenix_cave),
        )

    def end_mod(self):
        space = Reserve(0xc2b74, 0xc2b75, "phoenix cave pause before locke opens chest", field.NOP())
        space = Reserve(0xc2b82, 0xc2b84, "phoenix cave LOCKE!!", field.NOP())
        space = Reserve(0xc2b95, 0xc2b98, "phoenix cave you're all safe", field.NOP())
        space = Reserve(0xc2b9e, 0xc2ba0, "phoenix cave that looks like...", field.NOP())
        space = Reserve(0xc2ba5, 0xc2baf, "phoenix cave celes extra dialog", field.NOP())
        space = Reserve(0xc2bb6, 0xc2bbe, "phoenix cave i wasn't able to save rachel", field.NOP())

    def locke_holding_esper_mod(self):
        space = Reserve(0xc2b7f, 0xc2b81, "phoenix cave play magicite sound effect", field.NOP())
        space = Reserve(0xc2b99, 0xc2b9d, "phoenix cave show magicite", field.NOP())
        space = Reserve(0xc2ba1, 0xc2ba4, "phoenix cave hide magicite", field.NOP())

    def character_mod(self, character):
        self.locke_npc.sprite = character
        self.locke_npc.palette = self.characters.get_palette(character)

        self.locke_holding_esper_mod()

        space = Reserve(0xc2bcb, 0xc2bef, "phoenix cave kohlingen rachel scenes", field.NOP())
        space.write(
            field.RecruitCharacter(character),
            field.Call(field.RETURN_ALL_PARTIES_TO_FALCON),
            field.FinishCheck(),
            field.Return(),
        )

        # TODO this should happen in the entrance event if event already done or if character reward
        #      if come back in cave later the chest will be closed again but cannot be opened
        open_chest_function = space.next_address
        space.copy_from(0xc2b78, 0xc2b7d) # change chest sprite to open
        space.copy_from(0xc2b3a, 0xc2b41) # create/show locke npc
        space.write(
            field.Return(),
        )

        space = Reserve(0xc2b3a, 0xc2b41, "create/show locke npc if phoenix cave not complete")
        space.write(
            field.Call(open_chest_function),
            field.Return(),
        )

        space = Reserve(0xc2b76, 0xc2b7e, "phoenix cave open phoenix chest", field.NOP())

    def esper_item_mod(self, esper_item_instructions):
        self.locke_npc.sprite = self.characters.get_random_esper_item_sprite()
        self.locke_npc.palette = self.characters.get_palette(self.locke_npc.sprite)

        space = Reserve(0xc2bcb, 0xc2bef, "phoenix cave kohlingen rachel scenes", field.NOP())
        space.write(
            esper_item_instructions,
            field.Call(field.RETURN_ALL_PARTIES_TO_FALCON),
            field.FinishCheck(),
            field.Return(),
        )

    def esper_mod(self, esper):
        self.esper_item_mod([
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def item_mod(self, item):
        self.locke_holding_esper_mod()

        self.esper_item_mod([
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])
