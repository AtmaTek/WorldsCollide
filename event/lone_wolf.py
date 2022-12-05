from email.policy import default
from constants.checks import LONE_WOLF_CHASE, LONE_WOLF_MOOGLE_ROOM
from data.map_event import MapEvent
from event.event import *
from music.song_utils import get_character_theme

CHAR_ITEM = RewardType.CHARACTER | RewardType.ITEM
ESPER_ITEM = RewardType.ESPER | RewardType.ITEM

class LoneWolf(Event):
    def name(self):
        return "Lone Wolf"

    def character_gate(self):
        return self.characters.MOG

    def init_rewards(self):
        import random
        
        # Ensure the two checks can only reward one character and one esper.
        reward_char_type = bool(random.getrandbits(1))
        reward1_type = CHAR_ITEM if reward_char_type else ESPER_ITEM
        reward2_type = ESPER_ITEM if reward_char_type else CHAR_ITEM 
        
        self.reward1 = self.add_reward(LONE_WOLF_CHASE, reward1_type)
        self.reward2 = self.add_reward(LONE_WOLF_MOOGLE_ROOM, reward2_type)

    def init_event_bits(self, space):
        space.write(
            field.ClearEventBit(event_bit.GOT_BOTH_REWARDS_LONE_WOLF),
            field.ClearEventBit(npc_bit.MOG_MOOGLE_ROOM_WOR),
        )

        # Load into narshe cliffs (map 23, coordinates 25,20) and lone wolf will be triggerable
        # After choosing lone wolf or mog, exit to the previous map and re-enter the cliff
        # It will then take you to the room before the Moogle Room to easily test the full flow
        # if self.args.debug:
        #     space.write(
        #         field.SetEventBit(572),   # Spectate lone wolf cross the bridge to cliff
        #         field.ClearEventBit(573), # Haven't witnessed lone wolf event
        #         field.SetEventBit(831),   # Visibility bits for lone wolf npcs
        #         field.SetEventBit(832),
        #     )
        #     exit_maps = [x for x in self.maps.exits.long_exits if x.dest_map == 23]
        #     exit = next(iter(exit_maps))
        #     exit.dest_map = 37
        #     exit.dest_x = 14
        #     exit.dest_y = 10

    def mod(self):
        self.mog_npc_id = 0x1c
        self.mog_npc = self.maps.get_npc(0x017, self.mog_npc_id)

        self.lone_wolf_npc_id = 0x1b
        self.lone_wolf_npc = self.maps.get_npc(0x017, self.lone_wolf_npc_id)

        self.mog_moogle_room_npc_id = 0x10
        self.mog_moogle_room_npc = self.maps.get_npc(0x02c, self.mog_moogle_room_npc_id)

        # invisible npc blocking bridge until player chooses either mog or lone wolf
        self.invisible_bridge_block_npc_id = 0x1d

        self.dialog_mod()
        self.chase_mod()

        if self.reward1.type == RewardType.CHARACTER:
            self.character_mod(self.reward1.id)
        elif self.reward1.type == RewardType.ESPER:
            self.esper_mod(self.reward1.id)
        elif self.reward1.type == RewardType.ITEM:
            self.item_mod(self.reward1.id)

        if self.reward2.type == RewardType.CHARACTER:
            self.alternative_character_mod(self.reward2.id)
            self.moogle_room_reward_mod()
        elif self.reward2.type == RewardType.ESPER:
            self.alternative_esper_mod(self.reward2.id)
            self.moogle_room_reward_mod()
        elif self.reward2.type == RewardType.ITEM:
            self.alternative_item_mod(self.reward2.id)
            self.moogle_room_reward_mod()

        self.moogle_room_entrance_event_mod()
        self.lone_wolf_hide_mod()
        self.finish_check_mod()

        self.log_reward(self.reward1)
        self.log_reward(self.reward2)

    def dialog_mod(self):
        space = Reserve(0xcd3ef, 0xcd3f1, "lone wolf G'whoa! I've been made!", field.NOP())
        space = Reserve(0xcd407, 0xcd409, "I am lone wolf, the pickpocket!", field.NOP())
        space = Reserve(0xcd437, 0xcd439, "lone wolf outside treasure room G'heh!", field.NOP())
        space = Reserve(0xcd4a1, 0xcd4a3, "lone wolf Persistent, aren't you!", field.NOP())
        space = Reserve(0xcd54c, 0xcd54e, "lone wolf mog stands dialog Kupo!!", field.NOP())
        space = Reserve(0xcd560, 0xcd562, "lone wolf G'heh! Got a wild one, here", field.NOP())
        space = Reserve(0xcd5a0, 0xcd5a2, "lone wolf kupo before mog falls", field.NOP())
        space = Reserve(0xcd608, 0xcd60a, "lone wolf Thankupo!", field.NOP())

    def chase_mod(self):
        if self.args.character_gating:
            space = Reserve(0xcd3d4, 0xcd3db, "lone wolf saw maduin die and not started lone wolf requirements")
            space.write(
                field.ReturnIfAny([event_bit.character_recruited(self.character_gate()), False, event_bit.CHASING_LONE_WOLF1, True]),
            )

        space = Reserve(0xcd3f3, 0xcd3f4, "lone wolf pauses before beginning to exit", field.NOP())
        space.write(field.Pause(0.5)) # shorten from 1.5 seconds
        space = Reserve(0xcd402, 0xcd402, "lone wolf pauses before turning right")
        space.write(field.Pause(0.5)) # shorten from 2 seconds

    def character_mod(self, character):
        self.mog_npc.sprite = character
        self.mog_npc.palette = self.characters.get_palette(character)

        space = Reserve(0xcd5e5, 0xcd5f3, "lone wolf create char and make available", field.NOP())
        space.write(
            field.CreateEntity(character),
            field.RecruitCharacter(character),
        )

        space = Reserve(0xcd607, 0xcd607, "Song played when recruiting mog")
        space.write(get_character_theme(character))

        # move lone wolf falling up to make room for adding character
        # skip copying lone wolf take this dialog at [0xcd693,0xcd695]
        space = Reserve(0xcd61b, 0xcd67b, "lone wolf mog dialog and naming", field.NOP())
        space.copy_from(0xcd67c, 0xcd692)
        space.copy_from(0xcd696, 0xcd6bf)
        space.write(
            field.Branch(space.end_address + 1), # skip nops
        )

        space = Reserve(0xcd67c, 0xcd6dc, "lone wolf add char", field.NOP())
        space.write(
            field.Call(field.REFRESH_CHARACTERS_AND_SELECT_PARTY),
            field.HideEntity(self.mog_npc_id),
            field.HideEntity(self.invisible_bridge_block_npc_id),
            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.SetEventBit(npc_bit.MOG_MOOGLE_ROOM_WOR),
            field.SetEventBit(event_bit.RECRUITED_MOG_WOB),
            field.RefreshEntities(),
            field.FadeInScreen(),
            field.Branch(space.end_address + 1), # skip nops
        )

    def esper_item_mod(self, add_esper_item, sound_dialog_esper_item):
        space = Reserve(0xcd5df, 0xcd5f3, "lone wolf assign character properties", field.NOP())
        space = Reserve(0xcd693, 0xcd695, "char chosen dialog before lone wolf falls", field.NOP())

        space = Reserve(0xcd61b, 0xcd67b, "lone wolf add esper/item", field.NOP())
        space.write(
            add_esper_item,
            field.SetEventBit(npc_bit.MOG_MOOGLE_ROOM_WOR),
            field.Branch(space.end_address + 1), # skip nops
        )

        space = Reserve(0xcd6bf, 0xcd6c3, "lone wolf add esper/item dialog", field.NOP())
        space.write(
            sound_dialog_esper_item,
        )

    def esper_mod(self, esper):
        self.mog_npc.sprite = self.characters.get_random_esper_item_sprite()
        self.mog_npc.palette = self.characters.get_palette(self.mog_npc.sprite)

        self.esper_item_mod([
            field.AddEsper(esper, sound_effect = False),
        ],
        [
            field.PlaySoundEffect(141),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def item_mod(self, item):
        self.mog_npc.sprite = self.characters.get_random_esper_item_sprite()
        self.mog_npc.palette = self.characters.get_palette(self.mog_npc.sprite)

        self.esper_item_mod([
            field.AddItem(item, sound_effect = False),
        ],
        [
            field.PlaySoundEffect(141),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])

    def lone_wolf_character_sprite_mod(self, character):
        map_sprites = [
            [20, 0x29], # Narshe: South Exterior (WoB)
            [21, 0x10], # Narshe: North Exterior (WoB)
            [23, 0x1a], # Narshe: Cliffs (WoB)
            [23, 0x1b], # Narshe: Cliffs (WoB)
            [30, 0x25], # Narshe: Chest room
            [44, 0x10] # Narshe: Moove cave (WoR)
        ]

        for map_id, npc_id in map_sprites:
            npc = self.maps.get_npc(map_id, npc_id)
            npc.sprite = character
            npc.palette = self.characters.get_palette(character)

    # lone wolf doesnt jump, but instead joins the party..
    def alternative_character_mod(self, character):
        self.lone_wolf_dialog_character_mod(character)
        self.lone_wolf_character_sprite_mod(character)

        # This will skip mog's fall/pause animations to view lone wolf cutscene
        # if self.args.debug:
        #     space = Reserve(0xcd5a3, 0xcd5a3, "wait 30 frames (0.5s)", field.NOP())
        #     space = Reserve(0xcd5a8, 0xcd5a8, "wait 30 frames (0.5s)", field.NOP())
        #     space = Reserve(0xcd5ab, 0xcd5b3, "mog falling", field.NOP())

        space = Reserve(0xcd594, 0xcd59f, "Lone wolf gives item, mog", field.NOP())
        space = Reserve(0xcd5a4, 0xcd5a7, "Party runs at mog", field.NOP())
        space = Reserve(0xcd5b6, 0xcd5bc, "Party running after Mog", field.NOP())
        space = Reserve(0xcd5bd, 0xcd5bd, "wait 60 frames (1s)", field.NOP())
        space = Reserve(0x0cd5c1, 0xcd5d0, "Lone wolf object script, jumps off cliff, plays sound", field.NOP())

        # pick lone wolf up
        src = [
            field.HideEntity(self.invisible_bridge_block_npc_id),
            field.EntityAct(field_entity.PARTY0, False,
                field_entity.SetSpeed(field_entity.Speed.FAST),
                field_entity.DisableWalkingAnimation(),
                field_entity.Move(direction.LEFT, 1)
            ),
            # LW - Jump up from cliff
            field.EntityAct(self.lone_wolf_npc_id, True,
                field_entity.SetSpeed(field_entity.Speed.FAST),
                field_entity.AnimateLowJump(),
                field_entity.Move(direction.LEFT, 1),
                field_entity.Turn(direction.DOWN),
                field_entity.Pause(10)
            ),
            # LW - Blinks
            field.EntityAct(self.lone_wolf_npc_id, True,
                field_entity.AnimateCloseEyes(),
                field_entity.Pause(1),
                field_entity.Turn(direction.DOWN),
                field_entity.Pause(1),
                field_entity.AnimateCloseEyes(),
                field_entity.Pause(1),
                field_entity.Turn(direction.DOWN),
                field_entity.Pause(5),
            ),
            # Party - Blinks
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.AnimateCloseEyes(),
                field_entity.Pause(1),
                field_entity.Turn(direction.DOWN),
                field_entity.Pause(1),
                field_entity.AnimateCloseEyes(),
                field_entity.Pause(1),
                field_entity.Turn(direction.DOWN),
                field_entity.Pause(5),
            ),

            # LW - Attacks player
            field.EntityAct(self.lone_wolf_npc_id, False,
                field_entity.AnimateAttack(),
                field_entity.AnimateLowJump(),
                field_entity.Pause(3),
                field_entity.Turn(direction.DOWN),
                field_entity.EnableWalkingAnimation()
            ),
            #  Player - React to attack
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.Pause(2),
                field_entity.Turn(direction.DOWN),
                field_entity.AnimateSurprised(),
                field_entity.AnimateLowJump(),
                field_entity.Pause(12),
                field_entity.Turn(direction.DOWN),
            ),

            field.SetEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.StartSong(get_character_theme(character)),

            # LW - Laugh in player's face
            field.EntityAct(self.lone_wolf_npc_id, True,
                field_entity.LaughingOne(),
                field_entity.Pause(1),
                field_entity.LaughingTwo(),
                field_entity.Pause(1),
                field_entity.LaughingOne(),
                field_entity.Pause(1),
                field_entity.LaughingTwo(),
                field_entity.Pause(1),
                field_entity.LaughingOne(),
                field_entity.Pause(1),
                field_entity.LaughingTwo(),
                field_entity.Pause(1),
                field_entity.LaughingOne(),
                field_entity.Pause(1),
                field_entity.LaughingTwo(),
                field_entity.Pause(1),
                field_entity.Turn(direction.DOWN),
                field_entity.Pause(12),
                field_entity.AnimateFrontRightHandOnHead(),
                field_entity.Pause(4),
                field_entity.AnimateFrontRightHandUp(),
                field_entity.Pause(8),
            ),
            field.HideEntity(self.lone_wolf_npc_id),
            field.RecruitAndSelectParty(character),
            field.RefreshEntities(),
            field.FadeInScreen(),
            field.FinishCheck(),
            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.Return()
        ]

        character_space = Write(Bank.F0, src, "Recruit lone wolf")

        space.write([
            field.Call(character_space.start_address)
        ])

    def alternative_esper_mod(self, esper):
        # esper lone wolf will give as a reward for not picking self.reward1
        self.lone_wolf_dialog_esper_mod(esper)

        esper_space = Allocate(Bank.CC, 50, "Receive esper from lone wolf", field.NOP())
        esper_space.write([
            field.AddEsper(esper, sound_effect=True),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
            Read(0xcd59d, 0xcd59d), # Wait 30 frames
            field.Return()
        ])

        space = Reserve(0xcd59a, 0xcd59f, "received item dialog; wait 0.5s; take item from lone wolf", field.NOP())
        space.write([
            field.Call(esper_space.start_address)
        ])

    def alternative_item_mod(self, item):
        self.lone_wolf_dialog_item_mod(item)

        # item lone wolf will give as a reward for not picking self.reward1
        space = Reserve(0xcd59f, 0xcd59f, "lone wolf item received", field.NOP())
        space.write(
            item
        )

    # add pause after lone wolf jumps to wait for falling sound effect
    def lone_wolf_hide_mod(self):
        space = Reserve(0xcd5be, 0xcd5c0, "item chosen dialog before lone wolf falls", field.NOP())
        space.write(
            field.SetEventBit(npc_bit.MOG_MOOGLE_ROOM_WOR),
        )

        # add pause after lone wolf jumps to wait for falling sound effect
        src = [
            field.HideEntity(self.lone_wolf_npc_id),
            field.RefreshEntities(),
            field.HideEntity(self.invisible_bridge_block_npc_id),
            field.RefreshEntities(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "lone wolf hide lone wolf and remove bridge block")
        hide_npcs = space.start_address

        space = Reserve(0xcd5d1, 0xcd5d6, "lone wolf hide npcs after fall", field.NOP())
        space.write(
            field.Call(hide_npcs)
        )

    def lone_wolf_dialog_character_mod(self, character):
        import data.text
        character_name = data.text.convert(self.characters.get_name(character), data.text.TEXT1) # data.text.convert(self.items.get_name(self.reward2.id), data.text.TEXT1) # item names are stored as TEXT2, dialogs are TEXT1

        self.dialogs.set_text(1765, "<line><     >Grrrr…<line><     >You'll never get this<line><     >" + character_name + "!<end>")
        # this dialog is explicitly not called later on when recruiting the character in the cave
        self.dialogs.set_text(1742,  f" <line>  Recruited {character_name}!”<end>")

    def lone_wolf_dialog_esper_mod(self, esper):
        import data.text
        esper_name = data.text.convert(self.espers.get_name(esper), data.text.TEXT1) # item names are stored as TEXT2, dialogs are TEXT1

        self.dialogs.set_text(1765, "<line><     >Grrrr…<line><     >You'll never get this<line><     >“" + esper_name + "”!<end>")
        self.dialogs.set_text(1742, f" <line>     Received the Magicite<line>              “{esper_name}.”<end>")

    def lone_wolf_dialog_item_mod(self, item):
        import data.text
        item_name = data.text.convert(self.items.get_name(item), data.text.TEXT1) # item names are stored as TEXT2, dialogs are TEXT1

        self.dialogs.set_text(1765, "<line><     >Grrrr…<line><     >You'll never get this<line><     >“" + item_name + "”!<end>")
        self.dialogs.set_text(1742, "<line><      >Got “" + item_name + "”!<end>")
    def finish_check_mod(self):
        src = [
            field.ClearEventBit(npc_bit.LONE_WOLF_MOG_NARSHE_CLIFF),
            field.ClearEventBit(npc_bit.LONE_WOLF_NARSHE_CLIFF_BRIDGE),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "lone wolf finish check")
        finish_check = space.start_address

        space = Reserve(0xcd6dd, 0xcd6e0, "lone wolf finish saving mog", field.NOP())
        space.write(
            field.Call(finish_check),
        )

        space = Reserve(0xcd5d7, 0xcd5da, "lone wolf finish saving gold hairpin", field.NOP())
        space.write(
            field.Call(finish_check),
        )

    def moogle_room_character_mod(self, character):
        src = [
            field.SetEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.StartSong(get_character_theme(character)),

            field.EntityAct(self.mog_moogle_room_npc_id, True,
                field_entity.AnimateSurprised(),
                field_entity.Pause(8),
                field_entity.AnimateStandingFront(),
            ),

            field.RecruitAndSelectParty(character),
            field.HideEntity(self.mog_moogle_room_npc_id),
            field.ClearEventBit(npc_bit.MOG_MOOGLE_ROOM_WOR),
            field.SetEventBit(event_bit.GOT_BOTH_REWARDS_LONE_WOLF),
            field.RefreshEntities(),
            field.FadeInScreen(),
            field.FinishCheck(),
            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.Return(),
        ]

        space = Write(Bank.F0, src, "lone wolf moogle room npc character reward")
        return space.start_address

    def moogle_room_esper_item_mod(self, esper_item_instructions):
        src = [
            field.DisableEntityCollision(self.mog_moogle_room_npc_id),
            field.EntityAct(self.mog_moogle_room_npc_id, True,
                field_entity.AnimateLowJump(),
                field_entity.Pause(8),
                field_entity.SetSpeed(field_entity.Speed.FASTEST),
                field_entity.Move(direction.DOWN, 8),
            ),

            esper_item_instructions,

            field.FadeOutScreen(),
            field.WaitForFade(),
            field.HideEntity(self.mog_moogle_room_npc_id),
            field.ClearEventBit(npc_bit.MOG_MOOGLE_ROOM_WOR),
            field.SetEventBit(event_bit.GOT_BOTH_REWARDS_LONE_WOLF),
            field.FadeInScreen(),
            field.FinishCheck(),
            field.Return(),
        ]

        space = Write(Bank.F0, src, "lone wolf moogle room npc esper/item reward")
        return space.start_address

    def moogle_room_esper_mod(self, esper):
        return self.moogle_room_esper_item_mod([
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def moogle_room_item_mod(self, item):
        return self.moogle_room_esper_item_mod([
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])

    def moogle_room_reward_mod(self):
        mog_reward = field.RETURN
        if self.reward1.type == RewardType.CHARACTER:
            mog_reward = self.moogle_room_character_mod(self.reward1.id)
        elif self.reward1.type == RewardType.ESPER:
            mog_reward = self.moogle_room_esper_mod(self.reward1.id)
        elif self.reward1.type == RewardType.ITEM:
            mog_reward = self.moogle_room_item_mod(self.reward1.id)

        lone_wolf_reward = field.RETURN
        if self.reward2.type == RewardType.CHARACTER:
            lone_wolf_reward = self.moogle_room_character_mod(self.reward2.id)
        if self.reward2.type == RewardType.ESPER:
            lone_wolf_reward = self.moogle_room_esper_mod(self.reward2.id)
        if self.reward2.type == RewardType.ITEM:
            lone_wolf_reward = self.moogle_room_item_mod(self.reward2.id)

        src = [
            field.BranchIfEventBitSet(event_bit.RECRUITED_MOG_WOB, "LONE_WOLF_FELL"),
            field.Call(mog_reward),
            field.Return(),
            "LONE_WOLF_FELL",
            field.Call(lone_wolf_reward),
            field.Return()
        ]

        space = Write(Bank.F0, src, "lone wolf npc event second reward not chosen")
        npc_event = space.start_address

        space = Reserve(0xc396c, 0xc3970, "lone wolf npc not saved second reward", field.NOP())
        space.write(
            field.Call(npc_event),
            field.Return(),
        )

    def moogle_room_entrance_event_mod(self):
        # initialize mog npc to match the npc that was on the cliff with lone wolf
        self.mog_moogle_room_npc.sprite = self.mog_npc.sprite
        self.mog_moogle_room_npc.palette = self.mog_npc.palette

        # if mog npc is here (i.e. finished lone wolf event and haven't received the second reward yet)
        # and if did not choose to save lone wolf on cliff
        # change mog npc to lone wolf
        src = [
            field.ReturnIfEventBitClear(npc_bit.MOG_MOOGLE_ROOM_WOR),
            field.ReturnIfEventBitClear(event_bit.RECRUITED_MOG_WOB),
            field.SetSprite(self.mog_moogle_room_npc_id, self.lone_wolf_npc.sprite),
            field.SetPalette(self.mog_moogle_room_npc_id, self.lone_wolf_npc.palette),
            field.RefreshEntities(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "lone wolf new moogle room entrance event")

        self.maps.set_entrance_event(0x02c, space.start_address - EVENT_CODE_START)
