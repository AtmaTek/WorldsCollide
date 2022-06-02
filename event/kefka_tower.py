from event.event import *
import args

from constants.maps import name_id as map_name_id
from constants.songs import name_id as song_name_id
from constants.sound_effects import name_id as sfx_name_id

final_switch_map_id = map_name_id["KT Final Switch Room"]
inferno_room_id =  map_name_id["Inferno Room"]
guardian_room_id =  map_name_id["Guardian Room"]
poltergeist_room_id =  map_name_id["Poltergeist Room"]
doom_room_id =  map_name_id["Doom Room"]
goddess_room_id =  map_name_id["Goddess Room"]

def change_party(party):
    return [
        field.SetParty(party),
        field.RefreshEntities(),
        field.UpdatePartyLeader(),
    ]


class KefkaTower(Event):
    def name(self):
        return "Kefka's Tower"

    def init_rewards(self):
        self.atma_reward = self.add_reward(RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(npc_bit.POLTRGEIST_STATUE_KEFKA_TOWER),
        )

        import objectives
        self.unlock_final_kefka_result_name = "Unlock Final Kefka"
        if self.unlock_final_kefka_result_name not in objectives.results:
            space.write(
                field.SetEventBit(event_bit.UNLOCKED_FINAL_KEFKA),
            )

    def mod(self):
        self.boss_rush_mod()
        # self.statue_landing_mod()
        self.entrance_landing_mod()
        self.kefka_scene_mod()

        self.item = self.atma_reward.id
        self.atma_battle_mod()
        self.atma_mod()
        self.inferno_mod()
        self.guardian_mod()
        self.doom_mod()
        self.goddess_mod()
        self.poltergeist_mod()

        self.inferno_battle_mod()
        if self.args.fix_boss_skip:
            self.inferno_skip_fix()
            self.poltergeist_skip_fix()

        self.guardian_battle_mod()
        self.doom_battle_mod()
        self.goddess_battle_mod()
        self.poltrgeist_battle_mod()
        self.kefka_battle_mod()

        self.final_kefka_access_mod()
        self.final_scenes_mod()
        self.exit_mod()

        self.log_reward(self.atma_reward)

    def statue_landing_mod(self):
        src = [
            Read(0xa02d6, 0xa030a),
            field.ClearEventBit(event_bit.UNLOCKED_KT_SKIP),

            field.SetEventBit(event_bit.LEFT_WEIGHT_PUSHED_KEFKA_TOWER),
            field.SetEventBit(event_bit.RIGHT_WEIGHT_PUSHED_KEFKA_TOWER),
            field.ClearEventBit(npc_bit.LEFT_UNPUSHED_WEIGHT_KEFKA_TOWER),
            field.SetEventBit(npc_bit.LEFT_PUSHED_WEIGHT_KEFKA_TOWER),
            field.ClearEventBit(npc_bit.RIGHT_UNPUSHED_WEIGHT_KEFKA_TOWER),
            field.SetEventBit(npc_bit.RIGHT_PUSHED_WEIGHT_KEFKA_TOWER),
            field.ClearEventBit(npc_bit.CENTER_DOOR_BLOCK_KEFKA_TOWER),

            field.SetEventBit(event_bit.WEST_PATH_BLOCKED_KEFKA_TOWER),
            field.SetEventBit(event_bit.EAST_PATH_BLOCKED_KEFKA_TOWER),
            field.SetEventBit(event_bit.NORTH_PATH_OPEN_KEFKA_TOWER),
            field.SetEventBit(event_bit.SOUTH_PATH_OPEN_KEFKA_TOWER),
            field.SetEventBit(event_bit.CENTER_DOOR_KEFKA_TOWER),
            field.SetEventBit(event_bit.LEFT_RIGHT_DOORS_KEFKA_TOWER),

            field.LoadMap(0x163, direction.DOWN, default_music = False,
                          x = 39, y = 9, fade_in = False, entrance_event = True),

            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.HoldScreen(),
            field.HideEntity(field_entity.PARTY0),
            field.SetPartyMap(2, 0x163),
            field.SetPartyMap(3, 0x163),
            Read(0xa031e, 0xa0320),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetPosition(39, 0),
            ),
            Read(0xa0327, 0xa032d),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetPosition(43, 0),
            ),
            Read(0xa0334, 0xa033c),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetPosition(35, 0),
                field_entity.AnimateFrontHandsUp(),
                field_entity.SetSpeed(field_entity.Speed.FAST),
            ),
            field.FadeInScreen(),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.DisableWalkingAnimation(),
                field_entity.AnimateSurprised(),
                field_entity.Move(direction.DOWN, 6),
                field_entity.AnimateKneeling(),
                field_entity.EnableWalkingAnimation(),
            ),
            field.PlaySoundEffect(sfx_name_id.get('Chest/Switch')),

            field.SetParty(2),
            field.RefreshEntities(),
            field.UpdatePartyLeader(),
            field.Pause(1),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetSpriteLayer(2),
                field_entity.DisableWalkingAnimation(),
                field_entity.SetSpeed(field_entity.Speed.FASTEST),
                field_entity.AnimateSurprised(),
                field_entity.Move(direction.DOWN, 8),
                field_entity.Move(direction.DOWN, 1),
                field_entity.AnimateKneeling(),
                field_entity.EnableWalkingAnimation(),
                field_entity.SetSpriteLayer(0),
            ),

            field.PlaySoundEffect(sfx_name_id.get('Chest/Switch')),

            field.SetParty(3),
            field.RefreshEntities(),
            field.UpdatePartyLeader(),
            field.FadeOutSong(64),
            field.Pause(0.75),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.Move(direction.DOWN, 6),
                field_entity.AnimateKneeling(),
            ),

            field.PlaySoundEffect(sfx_name_id.get('Chest/Switch')),

            field.Pause(0.75),

            self.post_landing_src(0x163, 35, 6),
        ]
        space = Write(Bank.CA, src, "kefka tower statue landing")
        self.statue_landing = space.start_address

        space = Reserve(0xa03ad, 0xa03af, "kefka tower the statues are up ahead", field.NOP())

    def invoke_kt_battle(self, party, original_pack_name, battle_sound = False):
        boss_id = self.get_boss(original_pack_name, False)
        return [
            field.InvokeBattle(boss_id, battle_sound = True, battle_animation = True),
        ]

    # Trigger five bosses back-to-back
    def boss_rush_mod(self):
        def get_replacement_formation(boss_name):
            from data.bosses import pack_name
            replacement = self.get_boss(boss_name, False)
            location_boss = pack_name[replacement]
            formation_id = self.enemies.formations.get_id(location_boss)
            return self.enemies.formations.formations[formation_id]

        # If encounters are random, it could be a tell when a fight loses its music/victory dance
        def disable_victory_dance(original_encounter_name):
            formation = get_replacement_formation(original_encounter_name)
            formation.disable_victory_dance = formation.disable_victory_dance if self.args.random_encounters_random else 1

        def disable_battle_music(original_encounter_name):
            formation = get_replacement_formation(original_encounter_name)
            formation.disable_battle_music = formation.disable_battle_music if self.args.random_encounters_random else 1

        def disable_all(boss_name):
            disable_victory_dance(boss_name)
            disable_battle_music(boss_name)

        disable_all("Inferno")
        disable_all("Guardian")
        disable_all("Doom")
        disable_all("Goddess")
        disable_all("Poltrgeist")

        src = [
            Read(0xa02d6, 0xa030a),
            field.ClearEventBit(event_bit.UNLOCKED_KT_SKIP),

            field.SetEventBit(event_bit.LEFT_WEIGHT_PUSHED_KEFKA_TOWER),
            field.SetEventBit(event_bit.RIGHT_WEIGHT_PUSHED_KEFKA_TOWER),
            field.ClearEventBit(npc_bit.LEFT_UNPUSHED_WEIGHT_KEFKA_TOWER),
            field.SetEventBit(npc_bit.LEFT_PUSHED_WEIGHT_KEFKA_TOWER),
            field.ClearEventBit(npc_bit.RIGHT_UNPUSHED_WEIGHT_KEFKA_TOWER),
            field.SetEventBit(npc_bit.RIGHT_PUSHED_WEIGHT_KEFKA_TOWER),
            field.ClearEventBit(npc_bit.CENTER_DOOR_BLOCK_KEFKA_TOWER),

            field.SetEventBit(event_bit.WEST_PATH_BLOCKED_KEFKA_TOWER),
            field.SetEventBit(event_bit.EAST_PATH_BLOCKED_KEFKA_TOWER),
            field.SetEventBit(event_bit.NORTH_PATH_OPEN_KEFKA_TOWER),
            field.SetEventBit(event_bit.SOUTH_PATH_OPEN_KEFKA_TOWER),
            field.SetEventBit(event_bit.CENTER_DOOR_KEFKA_TOWER),
            field.SetEventBit(event_bit.LEFT_RIGHT_DOORS_KEFKA_TOWER),
            field.SetEventBit(event_bit.TEMP_SONG_OVERRIDE),

            field.BranchIfEventBitSet(event_bit.DEFEATED_INFERNO, "GUARDIAN"),
            field.Call(self.gauntlet_inferno_cutscene()),
            "GUARDIAN",
            field.BranchIfEventBitSet(event_bit.DEFEATED_GUARDIAN, "DOOM"),
            field.Call(self.gauntlet_guardian_cutscene()),
            "DOOM",
            field.BranchIfEventBitSet(event_bit.DEFEATED_DOOM, "GODDESS"),
            field.Call(self.gauntlet_doom_cutscene()),
            "GODDESS",
            field.BranchIfEventBitSet(event_bit.DEFEATED_GODDESS, "POLTRGEIST"),
            field.Call(self.gauntlet_goddess_cutscene()),
            "POLTRGEIST",
            field.BranchIfEventBitSet(event_bit.DEFEATED_POLTRGEIST, "POST_GAUNTLET"),
            field.Call(self.gauntlet_poltrgeist_cutscene_src()),
            "POST_GAUNTLET",
            field.Call(self.gauntlet_post_battle_cutscene_src()),
        ]
        space = Write(Bank.F0, src, "kefka tower statue landing")
        self.statue_landing = space.start_address

        space = Reserve(0xa03ad, 0xa03af, "kefka tower the statues are up ahead", field.NOP())

        self.maps.delete_short_exit(final_switch_map_id, 103, 49)
        self.maps.delete_short_exit(final_switch_map_id, 109, 46)
        self.maps.delete_short_exit(final_switch_map_id, 115, 48)

    def entrance_landing_mod(self):
        need_more_allies = 2982
        self.dialogs.set_text(need_more_allies, "We need to find more allies.<end>")

        statues_entrance = 1287
        self.dialogs.set_text(statues_entrance,
                              "<choice> (Gauntlet)<line><choice> (Not just yet)<end>")

        space = Reserve(0xa01a2, 0xa02d5, "kefka tower first landing scene", field.NOP())
        space.add_label("STATUE_LANDING", self.statue_landing)
        space.add_label("ENTRANCE_LANDING", space.end_address + 1)
        space.write(
            field.BranchIfEventWordLess(event_word.CHARACTERS_AVAILABLE, 3, "NEED_MORE_ALLIES"),
            field.BranchIfEventBitSet(event_bit.UNLOCKED_KT_SKIP, "LANDING_MENU"),

            field.Pause(2), # NOTE: load-bearing pause, without a pause or dialog before party select the game
                            #       enters an infinite loop. it seems like the game needs time to finish
                            #       fading in after the vehicle map load at 0xca0081

            field.Branch("ENTRANCE_LANDING"),

            "NEED_MORE_ALLIES",
            field.Dialog(need_more_allies),

            "CANCEL_LANDING",
            field.LoadMap(0x01, direction.DOWN, default_music = False,
                          x = 137, y = 197, fade_in = True, airship = True),
            vehicle.End(),
            field.Return(),

            "LANDING_MENU",
            field.DialogBranch(statues_entrance,
                               dest1 = "STATUE_LANDING", dest2 = "ENTRANCE_LANDING", dest3 = "CANCEL_LANDING"),
        )

    def kefka_scene_mod(self):
        space = Reserve(0xc17ff, 0xc1801, "kefka tower defeat the statues, and magical power will not disappear", field.NOP())

        space = Reserve(0xa0620, 0xa0622, "kefka tower welcome, friends", field.NOP())
        space = Reserve(0xa0655, 0xa0657, "kefka tower i knew you'd make it here", field.NOP())

        space = Reserve(0xa065a, 0xa065a, "kefka tower move camera down 7 tiles")
        space.write(field_entity.Move(direction.DOWN, 8))

        space = Reserve(0xa065c, 0xa0892, "kefka tower ultimate power, each party member's joy", field.NOP())
        space.write(
            field.Branch(space.end_address + 1), # skip nops
        )

        space = Reserve(0xa08a0, 0xa08b2, "kefka tower animate kefka joy reaction, change song", field.NOP())
        space.write(
            field.EntityAct(0x10, True,
                field_entity.AnimateKneeling(),
                field_entity.Pause(4),
            ),
            field.Branch(space.end_address + 1), # skip nops
        )

        space = Reserve(0xa08be, 0xa08c0, "kefka tower this is sickening", field.NOP())
        space = Reserve(0xa08da, 0xa08df, "kefka tower now for my next trick", field.NOP())

        space = Reserve(0xa0952, 0xa0e23, "kefka tower wor attack and pillar scenes", field.NOP())
        space.write(
            field.Branch(space.end_address + 1), # skip nops
        )

        space = Reserve(0xa0e28, 0xa0e34, "kefka tower show wor attack and load kefka tower with blue background", field.NOP())
        space.write(
            field.LoadMap(0x0164, direction.DOWN, default_music = False, x = 15, y = 17),
        )

        space = Reserve(0xa0e46, 0xa0f73, "kefka tower shaking screen, its over kefka, terra mobliz scene", field.NOP())
        space.write(
            field.InvokeFinalLineup(),
            field.StartSong(0), # silence
            field.EntityAct(field_entity.CAMERA, True,
                field_entity.SetSpeed(field_entity.Speed.FASTEST),
                field_entity.Move(direction.UP, 6),
            ),
            field.DeleteRotatingPyramids(),
            field.ResetScreenColors(),
            field.InvokeBattle(0x165, background = 0x33, battle_sound = False),
        )

        # make every character available after battle so can see all the scenes
        # (and so i dont have to worry about assuming celes/edgar/setzer recruited)
        for character in range(self.characters.CHARACTER_COUNT):
            space.write(
                # move characters to bottom of screen before they run up
                # this prevents them from briefly flashing after being shown and before running up
                field.CreateEntity(character),
                field.EntityAct(character, True,
                    field_entity.SetPosition(15, 27),
                ),
                field.SetEventBit(event_bit.character_available(character)),
            )
        space.write(
            field.Branch(space.end_address + 1), # skip nops
        )

    def atma_battle_mod(self):
        boss_pack_id = self.get_boss("Atma")

        space = Reserve(0xc18b4, 0xc18ba, "kefka tower invoke battle atma", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

    # Copy no less than 4 bytes between start_target and end_target
    # This will be called after one of the kt encounters has completed, but just prior to finishing the check
    def kt_encounter_objective_mod(self, boss_name, bit, start_target, end_target, description):
        src = Read(start_target, end_target)
        src += [
            field.SetEventBit(bit),
            field.CheckObjectives(),
            field.Return(),
        ]
        post_battle = Write(Bank['CC'], src, f"{boss_name} post-battle. 1) Set event bit. 2) Finish check")

        space = Reserve(start_target, end_target, description, asm.NOP())
        space.write([
            field.Call(post_battle.start_address)
        ])

    def guardian_mod(self):
        self.rom.set_bytes(0xc186c, [asm.NOP(), asm.NOP()])
        self.kt_encounter_objective_mod(
            "Guardian",
            event_bit.DEFEATED_GUARDIAN,
            0xc186c,
            0xc186f,
            "Guardian battle post-script, wait for fade, set bit",
        )

    def inferno_mod(self):
        self.rom.set_byte(0xc18a2, 0xea)
        self.rom.set_bytes(0xc18ae, [0xea, 0xea])

        self.kt_encounter_objective_mod(
            "Inferno",
            event_bit.DEFEATED_INFERNO,
            0xc18ae,
            0xc18b1,
            "Inferno battle post-script, fade in, wait, set bit",
        )

    def doom_mod(self):
        self.kt_encounter_objective_mod(
            "Doom",
            event_bit.DEFEATED_DOOM,
            0xc16f0,
            0xc16f3,
            "Doom battle post-script, Hide NPC 5, set npc bit",
        )

    def goddess_mod(self):
        self.kt_encounter_objective_mod(
            "Goddess",
            event_bit.DEFEATED_GODDESS,
            0xc1730,
            0xc1733,
            "Goddess battle post-script, Hide NPC 2, set npc bit",
        )

    def poltergeist_mod(self):
        self.kt_encounter_objective_mod(
            "Goddess",
            event_bit.DEFEATED_POLTRGEIST,
            0xc1786,
            0xc1789,
            "Poltergeist battle post-script, Hide NPCs, set npc bit",
        )

    def atma_mod(self):
        src = [
            Read(0xc18d3, 0xc18d6), # show save point, set save point npc bit

            field.AddItem(self.item),
            field.Dialog(self.items.get_receive_dialog(self.item)),
            field.SetEventBit(event_bit.DEFEATED_ATMA),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "kefka tower atma reward")
        atma_reward = space.start_address

        space = Reserve(0xc18d3, 0xc18d6, "kefka tower after atma", field.NOP())
        space.write(
            field.Call(atma_reward),
        )

    def inferno_battle_mod(self):
        boss_src = [
            field.StartSong(song_name_id['FierceBattle']),
            self.invoke_kt_battle(3, 'Inferno', True),
            field.Return(),
        ]
        boss_space = Write(Bank.CC, boss_src, "trigger inferno fight, ")
        space = Reserve(0xc18a2, 0xc18a9, "call inferno fight subroutine", asm.NOP())
        space.write([
            field.Call(boss_space.start_address)
        ])

    def inferno_skip_fix(self):
        # not sure why (stairs?) but this npc only blocks skipping the inferno event tile when entering from the east
        # fortunately this means the npc does not block leaving KT from the west after landing at statues

        from data.npc import NPC
        inferno_npc = self.maps.get_npc(0x19a, 0x10)
        invisible_block_npc = NPC()
        invisible_block_npc.x = 30
        invisible_block_npc.y = 18
        invisible_block_npc.direction = direction.UP
        invisible_block_npc.speed = NPC.SLOWEST
        invisible_block_npc.movement = NPC.NO_MOVE
        invisible_block_npc.sprite = 101
        invisible_block_npc.palette = 5
        invisible_block_npc.split_sprite = 1
        invisible_block_npc.const_sprite = 1

        # share event byte/bit with inferno so npc is removed when inferno is
        invisible_block_npc.event_byte = inferno_npc.event_byte
        invisible_block_npc.event_bit = inferno_npc.event_bit
        invisible_block_npc_id = self.maps.append_npc(0x19a, invisible_block_npc)

        src = [
            Read(0xc18aa, 0xc18ad), # copy hide inferno, clear npc bit

            field.HideEntity(invisible_block_npc_id),
            field.Return(),
        ]
        space = Write(Bank.CB, src, "kefka tower hide inferno block")
        hide_inferno_block = space.start_address

        space = Reserve(0xc18aa, 0xc18ad, "kefka tower hide inferno, clear npc bit", field.NOP())
        space.write(
            field.Call(hide_inferno_block),
        )

    def poltergeist_skip_fix(self):
        from data.npc import NPC
        poltergeist_statue_npc = self.maps.get_npc(0x14e, 0x10)
        invisible_block_npc = NPC()
        invisible_block_npc.x = 36
        invisible_block_npc.y = 27
        invisible_block_npc.direction = direction.UP
        invisible_block_npc.speed = NPC.SLOWEST
        invisible_block_npc.movement = NPC.NO_MOVE
        invisible_block_npc.sprite = 101
        invisible_block_npc.palette = 5
        invisible_block_npc.split_sprite = 1
        invisible_block_npc.const_sprite = 1

        # share event byte/bit with inferno so npc is removed when inferno is
        invisible_block_npc.event_byte = poltergeist_statue_npc.event_byte
        invisible_block_npc.event_bit = poltergeist_statue_npc.event_bit
        invisible_block_npc_id = self.maps.append_npc(0x11f, invisible_block_npc)

    def guardian_battle_mod(self):
        boss_pack_id = self.get_boss("Guardian")

        space = Reserve(0xc184a, 0xc1850, "kefka tower invoke battle guardian", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

    def doom_battle_mod(self):
        boss_pack_id = self.get_boss("Doom")

        space = Reserve(0xc16dc, 0xc16e2, "kefka tower invoke battle doom", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

    def goddess_battle_mod(self):
        boss_pack_id = self.get_boss("Goddess")

        space = Reserve(0xc171c, 0xc1722, "kefka tower invoke battle goddess", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

    def poltrgeist_battle_mod(self):
        boss_pack_id = self.get_boss("Poltrgeist")

        space = Reserve(0xc1755, 0xc175b, "kefka tower invoke battle poltrgeist", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

    def kefka_battle_mod(self):
        # remove intro dialog from beginning of kefka final battle
        space = Reserve(0x10ce84, 0x10cee0, "kefka tower kefka battle intro")
        space.copy_from(0x10ce8b, 0x10cede) # keep player animations
        space.write(0xff)

    def final_kefka_access_mod(self):
        objectives_incomplete_dialog_id = 3023
        line2 = self.dialogs.get_centered(self.unlock_final_kefka_result_name)
        line3 = self.dialogs.get_centered("Objective Incomplete!")
        dialog_text = "<line>" + line2 + "<line>" + line3 + "<end>"
        self.dialogs.set_text(objectives_incomplete_dialog_id, dialog_text)

        # move checking if all three parties on switches to make room for access check first
        src = [
            "PARTY1",
            field.LoadActiveParty(),
            field.BranchIfAny([event_bit.multipurpose(1), False,
                               event_bit.multipurpose_party1_step(2), True],
                               "PARTY2"),
            field.PlaySoundEffect(150),
            field.SetEventBit(event_bit.multipurpose_party1_step(2)),

            "PARTY2",
            field.LoadActiveParty(),
            field.BranchIfAny([event_bit.multipurpose(2), False,
                               event_bit.multipurpose_party2_step(2), True],
                               "PARTY3"),
            field.PlaySoundEffect(150),
            field.SetEventBit(event_bit.multipurpose_party2_step(2)),

            "PARTY3",
            field.LoadActiveParty(),
            field.BranchIfAny([event_bit.multipurpose(3), False,
                               event_bit.multipurpose_party3_step(2), True],
                               "ALL_PARTIES"),
            field.PlaySoundEffect(150),
            field.SetEventBit(event_bit.multipurpose_party3_step(2)),

            "ALL_PARTIES",
            field.ReturnIfAny([event_bit.multipurpose_party1_step(2), False,
                               event_bit.multipurpose_party2_step(2), False,
                               event_bit.multipurpose_party3_step(2), False]),

            field.Branch(0xc1970),
        ]
        space = Write(Bank.CC, src, "kefka tower 3 parties on final switches check")
        three_switches_check = space.start_address

        space = Reserve(0xc193f, 0xc196f, "kefka tower final kefka access check", field.NOP())
        space.add_label("THREE_SWITCHES_CHECK", three_switches_check)
        space.write(
            field.BranchIfEventBitSet(event_bit.UNLOCKED_FINAL_KEFKA, "THREE_SWITCHES_CHECK"),

            field.PlaySoundEffect(245),
            field.FlashScreen(field.Flash.RED),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.AnimateAttacked(),
                field_entity.DisableWalkingAnimation(),
                field_entity.SetSpeed(field_entity.Speed.FASTEST),
                field_entity.Move(direction.DOWN, 1),
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
                field_entity.Move(direction.DOWN, 1),
                field_entity.SetSpeed(field_entity.Speed.SLOWEST),
                field_entity.Move(direction.DOWN, 1),
                field_entity.AnimateKneeling(),
            ),
            field.PlaySoundEffect(205),
            field.Dialog(objectives_incomplete_dialog_id),
            field.Return(),
        )

    def final_scenes_mod(self):
        # remove dialogs that require button press so final scenes automatically start
        space = Reserve(0xa1072, 0xa1074, "kefka tower it's breaking up!", field.NOP())
        space = Reserve(0xa11d3, 0xa11d5, "kefka tower there's no time to lose! airship's just ahead", field.NOP())
        space = Reserve(0xa1205, 0xa1207, "kefka tower terra! you're back!", field.NOP())
        space = Reserve(0xa1231, 0xa1233, "kefka tower come on, everybody! we have to work together!", field.NOP())
        space = Reserve(0xa1240, 0xa1242, "kefka tower terra! what's wrong", field.NOP())
        space = Reserve(0xa1321, 0xa1326, "kefka tower the magicite... the espers...", field.NOP())
        space = Reserve(0xa1330, 0xa1332, "kefka tower you mean terra too?", field.NOP())
        space = Reserve(0xa133e, 0xa1340, "kefka tower come with me. i can lead you out", field.NOP())

    # Load character into the given map and position, then return control (with KT prompt)
    def post_landing_src(self, map_id, map_x, map_y):
        return [
            Read(0xa039c, 0xa039f),
            field.LoadMap(map_id, direction.DOWN, default_music = True,
                x = map_x, y = map_y, fade_in = True, entrance_event = True),

            field.FreeScreen(),
            Read(0xa03b0, 0xa03b9),
        ]

    def exit_mod(self):
        # for some reason poltrgeist's statue bit was set when left/right parties opened center door
        # and it was cleared when leaving or warping out
        # there does not seem to be a reason for this and can cause the statue to not appear when landing at statues
        # instead, initialize the bit to set and don't clear when leaving (it is cleared when defeated)

        # leaving with crane or warp stone
        # warp stone call trace: c0c670 -> ca0039 -> ca0108 -> ca014f -> cc0ff6 -> cc0f7d
        space = Reserve(0xc0fbf, 0xc0fc0, "kefka tower exit clear poltrgeist statue bit", asm.NOP())

    def gauntlet_inferno_cutscene(self):
        src = [
            change_party(3),
            field.LoadMap(inferno_room_id, direction.DOWN, default_music = False,
                        x = 27, y = 18, fade_in = False, entrance_event = True),

            # Move main party to east of inferno
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetPosition(39, 18),
            ),
            field.FadeInScreen(3),
            field.EntityAct(field_entity.CAMERA, False,
                field_entity.SetSpeed(field_entity.Speed.SLOW),
                field_entity.Move(direction.RIGHT, 4),
            ),

            field.Pause(1),

            field.EntityAct(field_entity.PARTY0, False,
                field_entity.SetSpeed(field_entity.Speed.FAST),
                field_entity.Move(direction.LEFT, 8),
            ),
            field.Call(0xc1872), # Inferno event tile address
        ]

        space = Write(Bank.F0, src, "Inferno Gauntlet Cutscene")
        return space.start_address


    def gauntlet_guardian_cutscene(self):
        src = [
            field.LoadMap(guardian_room_id, direction.DOWN, default_music = False,
                        x = 12, y = 14, fade_in = False, entrance_event = True),
            # Initialize party positions
            [
                change_party(1),
                field.EntityAct(field_entity.PARTY0, False,
                    field_entity.SetSpeed(field_entity.Speed.NORMAL),
                    field_entity.SetPosition(6, 15),
                    field_entity.Turn(direction.UP),
                ),
                change_party(2),
                field.EntityAct(field_entity.PARTY0, True,
                    field_entity.SetSpeed(field_entity.Speed.FAST),
                    field_entity.SetPosition(12, 17),
                    field_entity.Turn(direction.UP),
                ),

                change_party(3),
                field.EntityAct(field_entity.PARTY0, False,
                    field_entity.SetSpeed(field_entity.Speed.SLOW),
                    field_entity.SetPosition(18, 15),
                    field_entity.Turn(direction.UP),
                ),

                # Move Guardian back 1 cell
                field.EntityAct(0x10, False,
                    field_entity.SetPosition(11, 9)
                ),
                field.EntityAct(0x13, True,
                    field_entity.SetPosition(12, 9)
                ),
                field.EntityAct(0x16, True,
                    field_entity.SetPosition(13, 9)
                ),
            ],
            field.Pause(0.25),
            # Camera position
            field.EntityAct(field_entity.CAMERA, False,
                field_entity.SetSpeed(field_entity.Speed.SLOW),
                field_entity.Move(direction.UP, 2),
            ),
            # Party 1 picking magitek flowers
            [
                change_party(1),
                field.EntityAct(field_entity.PARTY0, False,
                    field_entity.SetSpeed(field_entity.Speed.NORMAL),
                    field_entity.Move(direction.UP, 3),
                    field_entity.Move(direction.LEFT, 1),
                    field_entity.AnimateKneeling(),
                    field_entity.Pause(12),

                    field_entity.Move(direction.DOWN, 2),
                    field_entity.AnimateKneeling(),
                    field_entity.Pause(12),

                    field_entity.Move(direction.UP, 1),
                    field_entity.Move(direction.RIGHT, 2),
                    field_entity.Pause(8),
                    field_entity.AnimateStandingFront(),
                    field_entity.Pause(1),
                    field_entity.AnimateFrontRightHandOnHead(),
                    field_entity.Pause(4),
                    field_entity.AnimateFrontRightHandUp(),
                    field_entity.Pause(5),
                    field_entity.AnimateStandingFront(),
                    field_entity.Pause(5),

                    field_entity.AnimateSurprised(),
                    field_entity.AnimateLowJump(),
                    field_entity.Pause(10),
                    field_entity.SetSpeed(field_entity.Speed.FAST),
                    field_entity.Move(direction.LEFT, 1),
                    field_entity.Move(direction.DOWN, 3),
                    field_entity.SetPosition(0, 0)
                ),
            ],
            # Party 3 walking around
            [
                change_party(3),
                field.EntityAct(field_entity.PARTY0, False,
                    field_entity.SetSpeed(field_entity.Speed.SLOW),
                    field_entity.SetPosition(18, 14),
                    field_entity.Move(direction.UP, 2),
                    field_entity.Move(direction.LEFT, 1),
                    field_entity.Pause(8),
                    field_entity.Move(direction.DOWN, 1),
                    field_entity.Turn(direction.LEFT),
                    field_entity.Pause(10),
                    field_entity.AnimateFrontRightHandOnHead(),
                    field_entity.Pause(3),
                    field_entity.AnimateFrontRightHandUp(),
                    field_entity.Pause(3),
                    field_entity.AnimateFrontRightHandOnHead(),
                    field_entity.Pause(3),
                    field_entity.AnimateFrontRightHandUp(),
                    field_entity.Pause(5),
                    field_entity.AnimateStandingFront(),
                    field_entity.Move(direction.RIGHT, 1),
                    field_entity.Move(direction.UP, 1),
                    field_entity.AnimateSurprised(),
                    field_entity.AnimateLowJump(),
                    field_entity.Pause(5),
                    field_entity.SetSpeed(field_entity.Speed.FAST),
                    field_entity.Move(direction.DOWN, 4),
                    field_entity.SetPosition(0, 0)
                ),
            ],
            field.FadeInScreen(3),
            # Party 2, the initiator
            [
                change_party(2),

                field.Pause(2),
                field.EntityAct(field_entity.PARTY0, True,
                    field_entity.Move(direction.UP, 3),
                    field_entity.AnimateFrontHandsUp(),
                    field_entity.Pause(5),
                    field_entity.AnimateStandingFront(),
                    field_entity.Pause(5),
                    field_entity.AnimateFrontHandsUp(),
                    field_entity.Pause(5),
                    field_entity.AnimateStandingFront(),
                ),
                field.EntityAct(field_entity.PARTY0, False,
                    field_entity.Pause(5),
                    field_entity.AnimateFrontHandsUp(),
                    field_entity.Pause(5),
                    field_entity.AnimateStandingFront(),
                    field_entity.Pause(5),
                    field_entity.AnimateFrontHandsUp(),
                    field_entity.Pause(5),
                    field_entity.AnimateStandingFront(),
                ),
                field.Pause(2),
                # Reaction to alarm
                field.EntityAct(field_entity.PARTY0, False,
                    field_entity.AnimateSurprised(),
                    field_entity.AnimateLowJump(),
                    field_entity.Pause(5),
                    field_entity.AnimateKnockedOut(),
                    field_entity.Pause(13),
                    field_entity.AnimateKneeling(),
                    field_entity.Pause(10),
                    field_entity.AnimateStandingHeadDown(),
                    field_entity.Pause(4),
                    field_entity.AnimateStandingFront(),
                    field_entity.Pause(4),
                    field_entity.AnimatePowerStance(),
                    field_entity.AnimateLowJump(),
                    field_entity.Pause(6),
                    field_entity.Move(direction.UP, 1),
                ),
            ],
            field.Call(0xc1827),
        ]
        space = Write(Bank.F0, src, "Guardian Gauntlet Cutscene")
        return space.start_address


    def gauntlet_doom_cutscene(self):
        src = [
            change_party(1),
            field.LoadMap(doom_room_id, direction.DOWN, default_music = False,
                x = 64, y = 15, fade_in = False, entrance_event = True),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetPosition(64, 21),
            ),
            field.FadeInScreen(3),
            field.EntityAct(field_entity.CAMERA, False,
                field_entity.SetSpeed(field_entity.Speed.SLOWEST),
                field_entity.Move(direction.UP, 3),
            ),
            field.Pause(2),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetSpeed(field_entity.Speed.FAST),
                field_entity.Move(direction.UP, 8),
                field_entity.Move(direction.UP, 1)
            ),

            field.Call(0xc16d6),

            field.HoldScreen(),
            field.EntityAct(field_entity.PARTY0, False,
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
                field_entity.Move(direction.LEFT, 1),
                field_entity.Move(direction.UP, 3),
            ),
            field.FadeOutScreen(3),
            field.Pause(1),
            field.Return(),
        ]

        space = Write(Bank.F0, src, "Doom Gauntlet Cutscene")
        return space.start_address

    def gauntlet_goddess_cutscene(self):
        src = [
            change_party(3),
            field.LoadMap(goddess_room_id, direction.DOWN, default_music = False,
                        x = 12, y = 28, fade_in = False, entrance_event = True),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetPosition(12, 40)
            ),
            field.FadeInScreen(3),
            field.EntityAct(field_entity.CAMERA, False,
                field_entity.SetSpeed(field_entity.Speed.SLOW),
                field_entity.Move(direction.DOWN, 5)
            ),
            field.Pause(1.5),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetSpeed(field_entity.Speed.FAST),
                field_entity.Move(direction.UP, 8)
            ),
            field.Call(0xc1716),
            field.HoldScreen(),
            field.EntityAct(field_entity.PARTY0, False,
                field_entity.SetSpeed(field_entity.Speed.FAST),
                field_entity.Pause(8),
                field_entity.Move(direction.UP, 2),
                field_entity.EnableWalkingAnimation(),
                field_entity.AnimateLowJump(),
            ),
            field.FadeOutScreen(4),
            field.Pause(1),
        ]

        space = Write(Bank.F0, src, "Goddess Gauntlet Cutscene")
        return space.start_address

    def gauntlet_poltrgeist_cutscene_src(self):
        src = [
            change_party(2),
            field.LoadMap(poltergeist_room_id, direction.DOWN, default_music = False,
                    x = 35, y = 22, fade_in = False, entrance_event = True),
            field.EntityAct(field_entity.CAMERA, False,
                field_entity.SetPosition(40, 15),
                field_entity.SetSpeed(field_entity.Speed.SLOW),
                field_entity.Move(direction.LEFT, 2),
                field_entity.MoveDiagonal(direction.LEFT, 1, direction.UP, 1),
                field_entity.MoveDiagonal(direction.LEFT, 1, direction.UP, 1),
                field_entity.MoveDiagonal(direction.LEFT, 1, direction.UP, 1),
                field_entity.MoveDiagonal(direction.LEFT, 1, direction.UP, 1),
                field_entity.Move(direction.UP, 2),
            ),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetPosition(27, 23)
            ),

            field.FadeInScreen(3),

                field.EntityAct(field_entity.PARTY0, False,
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
                field_entity.Move(direction.DOWN, 2),
                field_entity.Move(direction.RIGHT, 2),
                field_entity.Move(direction.DOWN, 3),
                field_entity.AnimateKneeling(),
                field_entity.Pause(10),
                field_entity.AnimateStandingFront(),
                field_entity.Pause(2),
                field_entity.Move(direction.UP, 3),
                field_entity.Move(direction.RIGHT, 1),
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
                field_entity.Move(direction.UP, 3),
                field_entity.SetSpeed(field_entity.Speed.FAST),
                field_entity.Move(direction.UP, 6),
            ),
            field.Pause(2),
            field.PlaySoundEffect(sfx_name_id.get('Chest/Switch')),
            field.Pause(2),
            field.Pause(1.5),

            field.Call(0xc174f),

            field.HoldScreen(),
            field.EntityAct(field_entity.PARTY0, False,
                field_entity.SetSpeed(field_entity.Speed.FAST),
                field_entity.Move(direction.UP, 8),
            ),
            field.FadeOutScreen(4),
            field.Pause(1),
        ]

        space = Write(Bank.F0, src, "Poltrgeist Gauntlet Cutscene")
        return space.start_address

    def gauntlet_post_battle_cutscene_src(self):
        party1_x = 103
        party1_y_dest = 45
        party1_y_offset = 10
        party1_y_start = party1_y_dest - party1_y_offset

        party2_x = 109
        party2_y_dest = 42
        party2_y_offset = 9
        party2_y_start = party2_y_dest - party2_y_offset

        party3_x = 115
        party3_y_dest = 44
        party3_y_offset = 8
        party3_y_start = party3_y_dest - party3_y_offset
        src = [
            [
                # Load final
                field.LoadMap(final_switch_map_id, direction.DOWN, default_music = False,
                            x = 109, y = 43, fade_in = False, entrance_event = False),
                field.FadeOutSong(255),
                field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),

                # Party 1 init position
                [
                    change_party(1),
                    Read(0xa0334, 0xa033c),
                    field.EntityAct(field_entity.PARTY0, True,
                        field_entity.SetPosition(party1_x, party1_y_start),
                        field_entity.AnimateFrontHandsUp(),
                        field_entity.SetSpeed(field_entity.Speed.FAST),
                    ),
                ],
                # Party 2 init position
                [
                    Read(0xa031e, 0xa0320),
                    field.EntityAct(field_entity.PARTY0, True,
                        field_entity.SetPosition(party2_x, party2_y_start),
                        field_entity.SetSpeed(field_entity.Speed.FAST),
                    ),
                ],
                # Party 3 init position
                [
                    Read(0xa0327, 0xa032d),
                    field.EntityAct(field_entity.PARTY0, True,
                        field_entity.SetPosition(party3_x, party3_y_start),
                        field_entity.SetSpeed(field_entity.Speed.FAST),
                    ),
                ],
                field.FadeInScreen(),
            ],
            # party 1 fall
            [
                change_party(1),
                field.PlaySoundEffect(sfx_name_id.get('Falling')),
                field.EntityAct(field_entity.PARTY0, True,
                    field_entity.SetSpeed(field_entity.Speed.FAST),
                    field_entity.DisableWalkingAnimation(),
                    field_entity.AnimateSurprised(),
                    field_entity.Move(direction.DOWN, party1_y_offset - 2),
                    field_entity.Move(direction.DOWN, 2),
                    field_entity.AnimateKneeling(),
                    field_entity.EnableWalkingAnimation(),
                ),
                field.PlaySoundEffect(sfx_name_id.get('Umaro Body Slam')),
            ],
            field.Pause(0.5),
            # party 2 fall
            [
                change_party(2),
                field.Pause(0.25),
                field.PlaySoundEffect(sfx_name_id.get('Falling')),
                field.EntityAct(field_entity.PARTY0, True,
                    field_entity.SetSpeed(field_entity.Speed.FAST),
                    field_entity.SetSpriteLayer(2),
                    field_entity.DisableWalkingAnimation(),
                    field_entity.AnimateSurprised(),
                    field_entity.Move(direction.DOWN, party2_y_offset - 2), # extra offset is added to the next entity script
                    field_entity.SetSpeed(field_entity.Speed.FASTEST),
                    field_entity.AnimateLowJump(),
                    field_entity.AnimateKnockedOut(),
                ),
                field.PauseUnits(3),
                field.PlaySoundEffect(sfx_name_id.get('Chest/Switch')),

                field.EntityAct(field_entity.PARTY0, False,
                    field_entity.Pause(3),
                    field_entity.Move(direction.DOWN, 2),
                    field_entity.AnimateKneeling(),
                    field_entity.EnableWalkingAnimation(),
                    field_entity.SetSpriteLayer(0),
                ),
                field.PauseUnits(20),
                field.PlaySoundEffect(sfx_name_id.get('Umaro Body Slam')),
            ],
            field.Pause(0.5),
            # party 3 fall
            [
                change_party(3),
                field.Pause(0.25),
                field.PlaySoundEffect(sfx_name_id.get('Falling')),

                field.EntityAct(field_entity.PARTY0, True,
                    field_entity.SetSpeed(field_entity.Speed.FAST),
                    field_entity.DisableWalkingAnimation(),
                    field_entity.AnimateSurprised(),
                    field_entity.Move(direction.DOWN, party3_y_offset),
                    field_entity.AnimateKneeling(),
                ),
                field.PlaySoundEffect(sfx_name_id.get('Umaro Body Slam')),
            ],

            field.Pause(0.75),

            self.post_landing_src(final_switch_map_id, party1_x, party1_y_dest),
        ]

        space = Write(Bank.F0, src, "Post-Gauntlet Cutscene")
        return space.start_address
