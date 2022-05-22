from event.event import *

class LeteRiver(Event):
    def name(self):
        return "Lete River"

    def character_gate(self):
        return self.characters.TERRA

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.ClearEventBit(npc_bit.ENTRANCE_BLOCK_RETURNER_HIDEOUT),
            field.ClearEventBit(npc_bit.CHEST_ROOM_BLOCK_RETURNER_HIDEOUT),
            field.ClearEventBit(npc_bit.BANON_IN_ROOM_RETURNER_HIDEOUT),
            field.SetEventBit(npc_bit.RAFT_LETE_RIVER),
        )

    def mod(self):
        self.raft_npc_id = 0x11

        if self.args.character_gating:
            self.add_gating_condition()

        if not self.args.fixed_encounters_original:
            self.fixed_battles_mod()

        self.before_ultros_mod()
        self.ultros_mod()
        self.after_ultros_mod()
        self.remove_raft_mod()
        self.exit_river_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)

    def add_gating_condition(self):
        src = [
            field.ReturnIfEventBitSet(event_bit.character_recruited(self.character_gate())),
            field.HideEntity(self.raft_npc_id),
            field.Return(),
        ]
        space = Write(Bank.CB, src, "lete river entrance event character gate")
        entrance_event_gate = space.start_address

        space = Reserve(0xb0469, 0xb0473, "lete river entrance event", field.NOP())
        space.write(
            field.Call(entrance_event_gate),
        )

    def fixed_battles_mod(self):
        # force front attacks to keep party on the raft
        pack1_id = 263
        pack2_id = 264
        battle_background = 13 # raft, right

        # NOTE third fixed battle at 0xb09c8 is removed, it was part of terra/edgar/banon scenario
        fixed_battles = [(pack1_id, 0xb0498), (pack2_id, 0xb04a1)]
        for pack_id_address in fixed_battles:
            pack_id = pack_id_address[0]
            start_address = pack_id_address[1]
            end_address = start_address + 2

            space = Reserve(start_address, end_address, "lete river invoke fixed battle")
            space.write(
                field.InvokeBattleType(pack_id, field.BattleType.FRONT,
                                       battle_background, check_game_over = False),
            )

    def before_ultros_mod(self):
        space = Reserve(0xb05a5, 0xb05e3, "lete river heal party, here we go", field.NOP())
        if self.args.character_gating:
            space.write(
                field.ReturnIfEventBitClear(event_bit.character_recruited(self.character_gate())),
            )
        space.write(
            field.Branch(space.end_address + 1), # skip nops
        )

        space = Reserve(0xb0617, 0xb063c, "lete river tutorial", field.NOP())

        # skip setting started raft ride bit to avoid side effects (terra/edgar/banon party in narshe)
        space = Reserve(0xb066f, 0xb0670, "lete river set started raft ride bit", field.NOP())

        space = Reserve(0xb08c2, 0xb08da, "lete river take sabin's path to wob", field.NOP())

        space = Reserve(0xb08db, 0xb08e0, "lete river skip ultros battle if already fought", field.NOP())
        space.write(
            field.BranchIfEventBitSet(event_bit.RODE_RAFT_LETE_RIVER, 0xb092b),
        )

        space = Reserve(0xb08ea, 0xb08ec, "lete river what is it?", field.NOP())

    def ultros_mod(self):
        boss_pack_id = self.get_boss("Ultros 1")
        battle_background = 13 # raft, right

        space = Reserve(0xb08ed, 0xb08f3, "lete river invoke battle ultros", field.NOP())
        space.write(
            field.InvokeBattleType(boss_pack_id, field.BattleType.FRONT, battle_background),
        )

        space = Reserve(0x10a1aa, 0x10a276, "lete river battle scene on raft after defeating ultros")
        space.clear(0xff)

    def after_ultros_mod(self):
        src = [
            # set this bit instead of ultros defeated (0x01a) which has many side effects (like tunnel armor)
            field.SetEventBit(event_bit.RODE_RAFT_LETE_RIVER),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CB, src, "lete river after ultros")
        after_ultros = space.start_address

        space = Reserve(0xb0916, 0xb091a, "lete river call after ultros", field.NOP())
        space.write(
            field.Call(after_ultros),
        )

    def remove_raft_mod(self):
        src = [
            field.SetVehicle(field_entity.PARTY0, field.Vehicle.NONE),
            field.SetVehicle(field_entity.PARTY1, field.Vehicle.NONE),
            field.SetVehicle(field_entity.PARTY2, field.Vehicle.NONE),
            field.SetVehicle(field_entity.PARTY3, field.Vehicle.NONE),
            field.Return(),
        ]
        space = Write(Bank.CB, src, "lete river remove raft from party")
        self.remove_raft = space.start_address

    def exit_river_mod(self):
        src = [
            field.SetEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.LoadMap(0x00, direction.LEFT, default_music = False, x = 93, y = 41, airship = True),
            vehicle.SetPosition(93, 41),
            vehicle.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            vehicle.LoadMap(0x00, direction.LEFT, default_music = True, x = 93, y = 41),
            world.End(),
        ]
        space = Write(Bank.CB, src, "lete river exit after ultros")
        self.exit_river = space.start_address

    def character_mod(self, character):
        space = Reserve(0xb08f9, 0xb08f9, "lete river put sabin on vehicle")
        space.write(character)

        space = Reserve(0xb08fc, 0xb08fc, "lete river hide sabin")
        space.write(character)

        space = Reserve(0xb08fe, 0xb0902, "lete river remove sabin from party and delete", field.NOP())
        space.write(
            field.RecruitCharacter(character),
        )

        space = Reserve(0xb0907, 0xb0907, "lete river create sabin")
        space.write(character)

        space = Reserve(0xb0909, 0xb0909, "lete river show sabin")
        space.write(character)

        space = Reserve(0xb090b, 0xb090b, "lete river position sabin in water animated")
        space.write(character)

        space = Reserve(0xb0920, 0xb0920, "lete river sabin floats away")
        space.write(character)

        # change party to follow character instead of go the other way
        space = Reserve(0xb092b, 0xb094d, "lete river party floats away", field.NOP())
        space.write(
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.Pause(2),
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
                field_entity.Move(direction.UP, 3),
                field_entity.MoveDiagonal(direction.UP, 2, direction.RIGHT, 1),
                field_entity.MoveDiagonal(direction.UP, 1, direction.RIGHT, 1),
                field_entity.MoveDiagonal(direction.UP, 1, direction.RIGHT, 1),
                field_entity.SetSpeed(field_entity.Speed.FAST),
                field_entity.Move(direction.UP, 8),
            ),
            field.FadeOutScreen(),
            field.WaitForFade(),

            field.Call(self.remove_raft),
            field.Call(field.REFRESH_CHARACTERS_AND_SELECT_PARTY),
            field.Call(self.exit_river),
            field.Return(),
        )

    def esper_item_mod(self, esper_item_instructions):
        space = Reserve(0xb08f8, 0xb0915, "lete river show sabin on river", field.NOP())
        space.write(
            field.RefreshEntities(),
            field.FadeInScreen(8),
            esper_item_instructions,
            field.Branch(space.end_address + 1),
        )

        space = Reserve(0xb091b, 0xb092a, "lete river sabin floats away from party", field.NOP())

        space = Reserve(0xb093d, 0xb094d, "lete river delete sabin", field.NOP())
        space.write(
            field.Call(self.remove_raft),
            field.Call(self.exit_river),
            field.Return(),
        )

    def esper_mod(self, esper):
        self.esper_item_mod([
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def item_mod(self, item):
        self.esper_item_mod([
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])
