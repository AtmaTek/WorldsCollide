from event.event import *

class CidHouse(Event):
    def name(self):
        return "Cid's House"

    def init_event_bits(self, space):
        space.write(
            field.ClearEventBit(npc_bit.CID_IN_BED_CID_HOUSE),
            field.SetEventBit(npc_bit.CID_WALKING_CID_HOUSE),
        )

    def mod(self):
        self.dialog_mod()
        self.entrance_event_mod()
        self.start_feeding_cid_mod()
        self.cid_health_event_word_mod()
        self.finish_feeding_cid_mod()

    def dialog_mod(self):
        # shorten dialog to single line to start feeding event
        self.dialogs.set_text(2175, "CID: I…haven't eaten in 3 or so days, ever since I became ill.<end>")

        # take out celes's name
        self.dialogs.set_text(2176, "CID: I feel much better!<line>Thanks!<end>")
        self.dialogs.set_text(2177, "CID: I…feel I'm not going to be around much longer…<end>")
        self.dialogs.set_text(2178, "CID: Thanks for all you've done for me!<end>")
        self.dialogs.set_text(2186, "Here's a fish! Eat up!<line>CID: Oh! Yum…<line>Chomp, munch, chew…<end>")

    def entrance_event_mod(self):
        CID_GET_IN_BED = 0xaf44c
        SET_CID_DEAD_BIT = 0xaf461
        src = [
            field.ReturnIfEventBitClear(event_bit.STARTED_FEEDING_CID),
            field.BranchIfEventWordLess(event_word.CID_HEALTH, 30, SET_CID_DEAD_BIT),
            field.Branch(CID_GET_IN_BED),
        ]
        space = Write(Bank.CA, src, "cid's house entrance event, check started feeding and health")
        check_health = space.start_address

        space = Reserve(0xaf442, 0xaf44b, "cid's house entrance event, check health", field.NOP())
        space.write(
            field.Branch(check_health),
        )

    def start_feeding_cid_mod(self):
        RANDOMIZE_FISH = 0xa534a    # randomize fish every time talk to cid
        DECREMENT_HEALTH = 0xa533f  # decrement cid's health ~every second
        src = [
            field.Call(RANDOMIZE_FISH),
            field.ReturnIfAny([event_bit.CID_SURVIVED, True, event_bit.CID_DIED, True]),

            # start timer every time talk to cid so if someone starts feeding cid, leaves, and starts
            # a new timer 0 at a different event, talking to cid will resume the hp decreasing loop
            field.StartTimer(0, 64, DECREMENT_HEALTH, pause_in_menu_and_battle = True),
            field.ReturnIfEventBitSet(event_bit.STARTED_FEEDING_CID),

            field.Dialog(2175),
            field.SetEventBit(event_bit.STARTED_FEEDING_CID),
            field.SetEventBit(event_bit.multipurpose_map(0)),
            field.SetEventBit(npc_bit.CID_IN_BED_CID_HOUSE),
            field.ClearEventBit(npc_bit.CID_WALKING_CID_HOUSE),
            field.SetEventWord(event_word.CID_HEALTH, 120),
            field.ResetTimer(0),
            field.StartTimer(0, 64, DECREMENT_HEALTH, pause_in_menu_and_battle = True),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "cid's house begin feeding cid")
        begin_feeding_cid = space.start_address

        space = Reserve(0xa5370, 0xa5373, "cid's house talk to cid walking around", field.NOP())
        space.write(
            field.Call(begin_feeding_cid),
        )

    def cid_health_event_word_mod(self):
        # change event word to not be shared with coral
        event_word_addresses = [
            0xa5340, 0xa539b, 0xa53a7, 0xa53b3, 0xa53bf, 0xa53c6, 0xa53d0,
            0xa53da, 0xa53e4, 0xa53ee, 0xa53f8, 0xa5402, 0xa540c,
        ]
        for address in event_word_addresses:
            space = Reserve(address, address, "cid's house cid health event word")
            space.write(
                event_word.CID_HEALTH,
            )

    def finish_feeding_cid_mod(self):
        src = [
            field.ClearEventBit(npc_bit.CID_IN_BED_CID_HOUSE),
            field.CheckObjectives(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "cid's house finish feeding cid check objectives")
        finish_feeding_cid = space.start_address

        space = Reserve(0xa5426, 0xa54b8, "cid's house let cid die", field.NOP())
        space.write(
            field.Branch(finish_feeding_cid),
            field.Return(),
        )

        space = Reserve(0xa5720, 0xa5744, "cid's house saved cid", field.NOP())
        space.write(
            field.SetEventBit(npc_bit.CID_WALKING_CID_HOUSE),
            field.Branch(finish_feeding_cid),
            field.Return(),
        )
