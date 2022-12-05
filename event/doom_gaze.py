from event.event import *

class DoomGaze(Event):
    def name(self):
        return "Doom Gaze"

    def character_gate(self):
        return self.characters.SETZER # gate for airship option

    def init_rewards(self):
        from constants.checks import SEARCH_THE_SKIES
        self.reward = self.add_reward(SEARCH_THE_SKIES)

    def mod(self):
        self.magicite_npc_id = 0x12
        self.magicite_npc = self.maps.get_npc(0x11, self.magicite_npc_id)

        self.dialog_mod()
        if self.args.doom_gaze_no_escape:
            self.doom_gaze_battle_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        if self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)

    def dialog_mod(self):
        space = Reserve(0xa00c2, 0xa00c4, "magicite popped out of doom gaze's mouth dialog", field.NOP())
        space.write(
            field.SetEventBit(event_bit.DEFEATED_DOOM_GAZE),
        )

    def doom_gaze_battle_mod(self):
        import instruction.asm as asm

        boss_pack_id = self.get_boss("Doom Gaze")
        boss_formation_id = self.enemies.packs.get_formations(boss_pack_id)[0]

        src = [
            Read(0x2e6f50, 0x2e6f57),   # copy load/store background and set 8 bit a register
            asm.LDA(0x04, asm.IMM8),    # load 0b0100 into a register for front attack
            asm.STA(0x11e3, asm.ABS),   # store battle type in the same place invoke_battle_type does
            asm.RTS(),
        ]
        space = Write(Bank.EE, src, "doom gaze set battle type")
        set_battle_type = space.start_address

        space = Reserve(0x2e6f46, 0x2e6f57, "doom gaze set formation", asm.NOP())
        space.write(
            asm.LDA(boss_formation_id, asm.IMM16),
            asm.STA(0x11e0, asm.ABS),   # store formation at $11e0 (low byte) and $11e1 (high byte)
            asm.JSR(set_battle_type, asm.ABS),
        )

        # assume only have to fight boss in doom gaze's place once (i.e. no escape and chase until defeated)
        # after the fight, set the doom gaze defeated event bit
        space = Reserve(0x2e019c, 0x2e01a2, "doom gaze defeated check for bahamut scene in airship", asm.NOP())
        space.write(
            asm.LDA(0x01, asm.IMM8),    # doom gaze defeated bit in event byte 1dd2
            asm.TSB(0x1dd2, asm.ABS),   # set doom gaze defeated event bit
        )

    def receive_reward_mod(self, reward_instructions):
        src = [
            reward_instructions,
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "doom gaze receive reward")
        receive_reward = space.start_address

        space = Reserve(0xa00de, 0xa00e2, "doom gaze receive magicite", field.NOP())
        space.write(
            field.Call(receive_reward),
        )

    def character_mod(self, character):
        start_addr = 0xa00a7 # begin magicite animation
        end_addr = 0xa00b6   # end magicite animation
        src = [
            field.EntityAct(self.magicite_npc_id, True,
                # Character "Attacked" animation will often cause clipping with the airship
                field_entity.SetSpriteLayer(1),
                field_entity.DisableWalkingAnimation(),
                field_entity.AnimateAttacked(),
            ),

            # Keep character on the same path as the esper, but change animation once movement has stopped
            self.rom.get_bytes(start_addr, end_addr - start_addr + 1),
            field.EntityAct(self.magicite_npc_id, True,
                field_entity.AnimateKneeling(),
            ),
            field.Return(),
        ]


        spit_out_reward = Write(Bank.F0, src, "doom gaze spits out character").start_address

        # Use preevious event space to call new subroutine recruiting character
        space = Reserve(start_addr, end_addr, "doom gaze spits out magicite", asm.NOP())
        space.write([
            field.Call(spit_out_reward)
        ])

        space = Reserve(0xa00ca, 0xa00dc, "Character pulls reward toward them, hide item, show dialog.", asm.NOP())

        self.magicite_npc.sprite = character
        self.magicite_npc.palette = self.characters.get_palette(character)
        self.magicite_npc.direction = direction.DOWN
        self.magicite_npc.split_sprite = 0

        self.receive_reward_mod([
            field.HideEntity(self.magicite_npc_id),
            field.RecruitAndSelectParty(character),
            field.FadeInScreen(),

            # Party performs small victory dance
            field.EntityAct(field_entity.PARTY0, False,
                field_entity.Turn(direction.LEFT),
                field_entity.Pause(0),
                field_entity.Turn(direction.UP),
                field_entity.Pause(0),
                field_entity.Turn(direction.RIGHT),
                field_entity.Pause(0),
                field_entity.Turn(direction.DOWN),
                field_entity.Pause(0),
                field_entity.Turn(direction.LEFT),
                field_entity.Pause(2),
                field_entity.AnimateArmsRaisedWalking(),
                field_entity.Pause(4),
                field_entity.Turn(direction.LEFT),
                field_entity.Pause(4),
                field_entity.AnimateArmsRaisedWalking(),
                field_entity.Pause(4),
                field_entity.Turn(direction.LEFT),
                field_entity.Pause(4),
                field_entity.AnimateArmsRaisedWalking(),
                field_entity.Pause(4),
                field_entity.Turn(direction.LEFT),
                field_entity.Pause(4),
                field_entity.AnimateArmsRaisedWalking(),
            ),
            field.WaitForFade(),
            field.Pause(1)
        ])

    def esper_mod(self, esper):
        self.receive_reward_mod([
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
            field.AddEsper(esper, sound_effect = False),
        ])

    def item_mod(self, item):
        self.magicite_npc.sprite = 106
        self.magicite_npc.palette = 6
        self.magicite_npc.split_sprite = 1
        self.magicite_npc.direction = direction.DOWN

        space = Reserve(0xa00d6, 0xa00d7, "doom gaze flash screen white when receiving esper", field.NOP())

        self.receive_reward_mod([
            field.Dialog(self.items.get_receive_dialog(item)),
            field.AddItem(item, sound_effect = False),
        ])
