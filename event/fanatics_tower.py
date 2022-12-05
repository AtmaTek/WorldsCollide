from constants.checks import FANATICS_TOWER_FOLLOWER, FANATICS_TOWER_LEADER
from data.map_event import MapEvent
from data.npc import NPC
from event.event import *

class FanaticsTower(Event):
    def name(self):
        return "Fanatic's Tower"

    def character_gate(self):
        return self.characters.STRAGO

    def init_event_bits(self, space):
        space.write([
            field.SetEventBit(npc_bit.FANATICS_TOWER_SECONDARY_REWARD),
        ])

    def init_rewards(self):
        self.reward1 = self.add_reward(FANATICS_TOWER_FOLLOWER)
        self.reward2 = self.add_reward(FANATICS_TOWER_LEADER)

    def mod(self):
        self.top_treasure_room_id = 0x16e
        self.strago_npc_id = 0x13
        self.strago_npc = self.maps.get_npc(0x16a, self.strago_npc_id)

        self.relm_event_mod()
        self.magimaster_battle_mod()

        if self.reward1.is_character():
            self.character_mod(self.reward1.id)
        elif self.reward1.is_esper():
            self.esper_mod(self.reward1.id)
        elif self.reward1.is_item():
            self.item_mod(self.reward1.id)

        if self.reward2.is_esper():
          self.tower_top_esper_mod()
        elif self.reward2.is_item():
          self.tower_top_item_mod()

        self.finish_magimaster_check_mod()
        self.finish_strago_check_mod()

        self.log_reward(self.reward1)
        self.log_reward(self.reward2)

    def relm_event_mod(self):
        # normally there are 4 event tiles surrounding player when they enter map and if player steps on one
        # with relm in party and strago not already recruited the relm/strago event is triggered
        # need to move the event tiles to the bottom of the stairs so player can not go around them and miss
        # recruiting the character after defeating magi master
        # create left/right event tiles which move the player to the original north event tile and
        # call the original event code (skipping the old checks for strago recruited/relm in party)
        space = Reserve(0xc522e, 0xc5282, "fanatics tower relm/strago event tiles", field.NOP())

        relm_strago_event = 0xc5283
        left_tile_event = space.next_address
        space.write(
            field.ReturnIfEventBitClear(event_bit.DEFEATED_MAGIMASTER),
            field.ReturnIfEventBitSet(event_bit.RECRUITED_STRAGO_FANATICS_TOWER),
        )
        if self.args.character_gating:
            space.write(
                field.ReturnIfEventBitClear(event_bit.character_recruited(self.character_gate())),
            )
        space.write(
            field.Call(field.DISABLE_COLLISIONS_FOR_PARTY_MEMBERS),

            # move to where event normally happens and call normal event code
            field.EntityAct(0x31, True,
                field_entity.Move(direction.DOWN, 3),
                field_entity.Move(direction.RIGHT, 1),
                field_entity.Turn(direction.UP),
            ),
            field.Call(relm_strago_event),
            field.Return(),
        )

        right_tile_event = space.next_address
        space.write(
            field.ReturnIfEventBitClear(event_bit.DEFEATED_MAGIMASTER),
            field.ReturnIfEventBitSet(event_bit.RECRUITED_STRAGO_FANATICS_TOWER),
        )
        if self.args.character_gating:
            space.write(
                field.ReturnIfEventBitClear(event_bit.character_recruited(self.character_gate())),
            )
        space.write(
            field.Call(field.DISABLE_COLLISIONS_FOR_PARTY_MEMBERS),

            # move to where event normally happens and call normal event code
            field.EntityAct(0x31, True,
                field_entity.Move(direction.DOWN, 3),
                field_entity.Turn(direction.UP),
            ),
            field.Call(relm_strago_event),
            field.Return(),
        )

        self.maps.delete_event(0x16a, 8, 12) # relm/strago event tile (north)
        self.maps.delete_event(0x16a, 7, 13) # relm/strago event tile (west)
        self.maps.delete_event(0x16a, 9, 13) # relm/strago event tile (east)
        self.maps.delete_event(0x16a, 8, 14) # relm/strago event tile (south)

        from data.map_event import MapEvent

        # add event tile to bottom left of stairs
        new_event = MapEvent()
        new_event.x = 7
        new_event.y = 9
        new_event.event_address = left_tile_event - EVENT_CODE_START
        self.maps.add_event(0x16a, new_event)

        # add event tile to bottom right of stairs
        new_event = MapEvent()
        new_event.x = 8
        new_event.y = 9
        new_event.event_address = right_tile_event - EVENT_CODE_START
        self.maps.add_event(0x16a, new_event)

        space = Reserve(0xc528b, 0xc528f, "fanatics tower don't change party for relm", field.NOP())
        space = Reserve(0xc52aa, 0xc52cc, "fanatics tower relm runs up stairs you old fool", field.NOP())
        space = Reserve(0xc5303, 0xc5307, "fanatics tower relm looks up after strago jumps", field.NOP())
        space = Reserve(0xc5316, 0xc5326, "fanatics tower relm and strago face each other", field.NOP())
        space = Reserve(0xc5329, 0xc5350, "fanatics tower various relm animations", field.NOP())
        space = Reserve(0xc5356, 0xc5389, "fanatics tower more relm animations and foul mouthed", field.NOP())
        space = Reserve(0xc5392, 0xc5395, "fanatics tower turn relm left", field.NOP())
        space = Reserve(0xc53a2, 0xc53a5, "fanatics tower turn relm down", field.NOP())
        space = Reserve(0xc53ca, 0xc53df, "fanatics tower all right, make room for me", field.NOP())

        space = Reserve(0xc53fd, 0xc53fd, "fanatics tower party leader head nod", field.NOP())
        space.write(field_entity.PARTY0)

        space = Reserve(0xc5407, 0xc5408, "fanatics tower stop relm song before screen fade", field.NOP())

    def tower_top_esper_mod(self):
        space = Reserve(0xc5548, 0xc554a, "fanatics tower master kefka's treasure", field.NOP())
        space = Reserve(0xc554d, 0xc554e, "fanatics tower long pause before magic master appears", field.NOP())

        # Move the chest to inaccessible location, empty it..
        chest = self.maps.get_chests(0x16e)[0]
        chest.type = chest.EMPTY
        chest.contents = 255
        chest.x = 0
        chest.y = 0

        # This event flips the bit to trigger the MagiMaster fight outside,
        # And also spawns the cultists during the cutscene
        # We copy the relevant code from this event to event_space below
        self.maps.delete_event(self.top_treasure_room_id, 7, 8)

        # Place magicite in front of the chest
        self.magicite_npc = NPC()
        self.magicite_npc.sprite = 91 # Magicite
        self.magicite_npc.palette = 2
        self.magicite_npc.split_sprite = 1
        self.magicite_npc.direction = direction.UP
        self.magicite_npc.x = 7
        self.magicite_npc.y = 8
        self.magicite_npc.event_byte = npc_bit.event_byte(npc_bit.FANATICS_TOWER_SECONDARY_REWARD)
        self.magicite_npc.event_bit = npc_bit.event_bit(npc_bit.FANATICS_TOWER_SECONDARY_REWARD)

        self.magicite_npc_id = self.maps.append_npc(self.top_treasure_room_id, self.magicite_npc)

        event_space = Allocate(Bank.CC, 40, "Give fanatics tower esper subroutine", asm.NOP())
        event_space.write([
            Read(0xc5440, 0xc5441), # Set npc bit hex(730) true  (top treasure received)
            Read(0xc5448, 0xc5449), # Set npc bit hex(1689) true (cultists outside treasure room)
            field.AddEsper(self.reward2.id),
            field.Dialog(self.espers.get_receive_esper_dialog(self.reward2.id)),
            field.ClearEventBit(npc_bit.FANATICS_TOWER_SECONDARY_REWARD),
            field.DeleteEntity(self.magicite_npc_id),
            field.RefreshEntities(),
            field.FinishCheck(),
            field.Return(),
        ])

        # Re-using space from removed event above
        space = Reserve(0xc5440, 0xc544a, "Call esper subroutine", asm.NOP())
        space.write([
            field.Call(event_space.start_address),
            field.Return(),
        ])
        self.magicite_npc.set_event_address(space.start_address)

    def tower_top_item_mod(self):
        space = Reserve(0xc5548, 0xc554a, "fanatics tower master kefka's treasure", field.NOP())
        space = Reserve(0xc554d, 0xc554e, "fanatics tower long pause before magic master appears", field.NOP())

        self.item = self.reward2.id
        self.maps.set_chest_item(self.top_treasure_room_id, 7, 7, self.item)

    def magimaster_battle_mod(self):
        boss_pack_id = self.get_boss("MagiMaster")

        space = Reserve(0xc5578, 0xc557e, "fanatic's tower invoke battle magimaster", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

    def character_mod(self, character):
        self.strago_npc.sprite = character
        self.strago_npc.palette = self.characters.get_palette(character)

        space = Reserve(0xc540d, 0xc542a, "fanatics tower add character", field.NOP())
        space.write(
            field.RecruitAndSelectParty(character),
        )

    def esper_item_mod(self, esper_item_instructions):
        self.strago_npc.sprite = self.characters.get_random_esper_item_sprite()
        self.strago_npc.palette = self.characters.get_palette(self.strago_npc.sprite)

        space = Reserve(0xc5409, 0xc542a, "fanatics tower esper/item reward", field.NOP())
        space.write(
            esper_item_instructions,
            field.FadeOutScreen(4),
            field.WaitForFade(),
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

    def finish_magimaster_check_mod(self):
        src = [
            Read(0xc5583, 0xc5588), # load map
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "fanatic's tower magimaster finish check")
        finish_check = space.start_address

        space = Reserve(0xc5583, 0xc5588, "fanatic's tower load map after magimaster", field.NOP())
        space.write(
            field.Call(finish_check),
        )

    def finish_strago_check_mod(self):
        src = [
            Read(0xc5438, 0xc543d), # load map
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "fanatics tower strago finish check")
        finish_check = space.start_address

        space = Reserve(0xc5438, 0xc543d, "fanatics tower load map after strago", field.NOP())
        space.write(
            field.Call(finish_check),
        )
