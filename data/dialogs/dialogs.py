from data.dialogs.dialog import Dialog
from data.structures import DataList
from memory.space import Space
from data.fonts import widths
import data.text

class Dialogs():
    DIALOG_PTRS_START = 0xce602
    DIALOG_PTRS_END = 0xcffff
    DIALOGS_START = 0xd0000
    DIALOGS_END = 0xef0ff

    # the address of the first ptr index which is relative to 0xce0000
    # dialog ptrs < FIRST_CE_PTR_INDEX are relative to 0xcd0000
    # dialog ptrs >= FIRST_CE_PTR_INDEX are relative to 0xce0000
    FIRST_CE_PTR_INDEX_ADDR = 0xce600

    BATTLE_MESSAGE_PTRS_START = 0x11f7a0
    BATTLE_MESSAGE_PTRS_END = 0x11f99f
    BATTLE_MESSAGES_OFFSET = 0x110000
    BATTLE_MESSAGES_START = 0x11f000    # NOTE: battle messages are moved to a different location
    BATTLE_MESSAGES_END = 0x11f79f

    SINGLE_LINE_BATTLE_DIALOG_PTRS_START = 0xfdfe0
    SINGLE_LINE_BATTLE_DIALOG_PTRS_END = 0xfe1df
    SINGLE_LINE_BATTLE_DIALOGS_OFFSET = 0xf0000
    SINGLE_LINE_BATTLE_DIALOGS_START = 0xfe1e0
    SINGLE_LINE_BATTLE_DIALOGS_END = 0xff44f

    MULTI_LINE_BATTLE_DIALOG_PTRS_START = 0x10d000
    MULTI_LINE_BATTLE_DIALOG_PTRS_END = 0x10d1ff
    MULTI_LINE_BATTLE_DIALOGS_OFFSET = 0x100000
    MULTI_LINE_BATTLE_DIALOGS_START = 0x10d200
    MULTI_LINE_BATTLE_DIALOGS_END = 0x10fcff

    from constants.objectives import MAX_OBJECTIVES
    OBJECTIVES = list(range(3084, 3084 + MAX_OBJECTIVES))
    BATTLE_OBJECTIVES = list(range(70, 70 + MAX_OBJECTIVES))

    def __init__(self):
        self.read()
        self.free()
        self.mod()

    def read(self):
        self.read_dialogs()
        self.read_battle_messages()
        self.read_single_line_battle_dialogs()
        self.read_multi_line_battle_dialogs()

    def read_dialogs(self):
        self.dialog_data = DataList(Space.rom, self.DIALOG_PTRS_START, self.DIALOG_PTRS_END,
                                    Space.rom.SHORT_PTR_SIZE, self.DIALOGS_START,
                                    self.DIALOGS_START, self.DIALOGS_END)

        self.dialogs = []
        for dialog_index, dialog_data in enumerate(self.dialog_data):
            dialog = Dialog(dialog_index, data.text.TEXT1, dialog_data)
            self.dialogs.append(dialog)

        # the last used dialog ends with garbage data because the last pointer pointed to the end of
        # the available dialog memory instead of the end of the actual displayed text
        # assign only the displayed text to free that garbage memory
        self.set_text(3083, ("<line><RELM>: How about a nice portrait for you, hmm?!"
                             "<wait 120 frames><wait 1 frame><end>"))

    def read_battle_messages(self):
        self.battle_message_data = DataList(Space.rom, self.BATTLE_MESSAGE_PTRS_START, self.BATTLE_MESSAGE_PTRS_END,
                                            Space.rom.SHORT_PTR_SIZE, self.BATTLE_MESSAGES_OFFSET,
                                            self.BATTLE_MESSAGES_START, self.BATTLE_MESSAGES_END)

        self.battle_messages = []
        for message_index, message_data in enumerate(self.battle_message_data):
            dialog = Dialog(message_index, data.text.TEXT3, message_data)
            self.battle_messages.append(dialog)

        # free garbage memory at end of messages space
        self.set_battle_message_text(255, "<end>")

    def read_single_line_battle_dialogs(self):
        self.single_line_battle_dialog_data = DataList(Space.rom,
                                                       self.SINGLE_LINE_BATTLE_DIALOG_PTRS_START,
                                                       self.SINGLE_LINE_BATTLE_DIALOG_PTRS_END,
                                                       Space.rom.SHORT_PTR_SIZE,
                                                       self.SINGLE_LINE_BATTLE_DIALOGS_OFFSET,
                                                       self.SINGLE_LINE_BATTLE_DIALOGS_START,
                                                       self.SINGLE_LINE_BATTLE_DIALOGS_END)

        self.single_line_battle_dialogs = []
        for dialog_index, dialog_data in enumerate(self.single_line_battle_dialog_data):
            dialog = Dialog(dialog_index, data.text.TEXT3, dialog_data)
            self.single_line_battle_dialogs.append(dialog)

    def read_multi_line_battle_dialogs(self):
        self.multi_line_battle_dialog_data = DataList(Space.rom,
                                                      self.MULTI_LINE_BATTLE_DIALOG_PTRS_START,
                                                      self.MULTI_LINE_BATTLE_DIALOG_PTRS_END,
                                                      Space.rom.SHORT_PTR_SIZE,
                                                      self.MULTI_LINE_BATTLE_DIALOGS_OFFSET,
                                                      self.MULTI_LINE_BATTLE_DIALOGS_START,
                                                      self.MULTI_LINE_BATTLE_DIALOGS_END)

        self.multi_line_battle_dialogs = []
        for dialog_index, dialog_data in enumerate(self.multi_line_battle_dialog_data):
            dialog = Dialog(dialog_index, data.text.TEXT3, dialog_data)
            self.multi_line_battle_dialogs.append(dialog)

    def free(self):
        import data.dialogs.free as free

        self.free_multi_line_battle_dialogs = []
        for dialog_id in free.multi_line_battle_dialogs:
            self.multi_line_battle_dialogs[dialog_id].text = ""
            self.free_multi_line_battle_dialogs.append(dialog_id)

    def set_text(self, id, text):
        self.dialogs[id].text = text

    def set_battle_message_text(self, id, text):
        self.battle_messages[id].text = text

    def set_single_line_battle_text(self, id, text):
        self.single_line_battle_dialogs[id].text = text

    def set_multi_line_battle_text(self, id, text):
        self.multi_line_battle_dialogs[id].text = text

    def allocate_multi_line_battle(self, text):
        dialog_id = self.free_multi_line_battle_dialogs.pop()
        self.set_multi_line_battle_text(dialog_id, text)
        return dialog_id

    def get_multi_line_battle_objective(self, objective_index):
        return self.multi_line_battle_objectives[objective_index]

    def get_centered(self, string):
        MAX_WIDTH = 219
        space_width = 5

        string_width = widths.width(string)
        center_start = (MAX_WIDTH - string_width) // 2 + 1
        left_spaces = center_start // space_width
        return (" " * left_spaces) + string

    def move_battle_messages(self):
        from memory.space import START_ADDRESS_SNES, Bank, Reserve, Allocate, Free
        space = Allocate(Bank.F0, 4000, "battle messages new location")

        # update pointers to messages (leave pointers in d1 bank)
        pointer_shift = (space.start_address & 0xffff) - self.battle_message_data.pointers[0]
        for pointer_index in range(len(self.battle_message_data.pointers)):
            self.battle_message_data.pointers[pointer_index] += pointer_shift
        self.battle_message_data.pointer_offset = space.start_address

        self.battle_message_data.free_space = len(space) - self.battle_message_data.size()
        self.battle_message_data.start_address = space.start_address
        self.battle_message_data.end_address = space.end_address

        # update bank to load battle messages from
        space = Reserve(0x198ff, 0x198ff, "battle messages bank")
        space.write(START_ADDRESS_SNES + self.battle_message_data.pointer_offset >> 16)

        # free previous message data space
        Free(0x11f000, 0x11f79f)

    def objectives_mod(self):
        import objectives
        self.multi_line_battle_objectives = []
        for index, objective in enumerate(objectives):
            line2 = self.get_centered(str(objective.result))
            line3 = self.get_centered("Objective Complete!")
            self.set_text(self.OBJECTIVES[index], "<line>" + line2 + "<line>" + line3 + "<end>")

            self.set_battle_message_text(self.BATTLE_OBJECTIVES[index],
                                         str(objective.result) + " Complete<wait for key><end>")

            line1 = self.get_centered(str(objective.result))
            line2 = self.get_centered("Objective Complete!")
            mlid = self.allocate_multi_line_battle(line1 + "<line>" + line2 + "<wait for key><end>")
            self.multi_line_battle_objectives.append(mlid)

    def mod(self):
        self.move_battle_messages()
        self.objectives_mod()

    def write(self):
        self.dialog_data.assign([dialog.data() for dialog in self.dialogs])
        for dialog_index, dialog in enumerate(self.dialogs):
            if (dialog_index < len(self.dialogs) - 1 and
                    self.dialog_data.pointers[dialog_index] < self.dialog_data.pointers[dialog_index - 1]):
                Space.rom.set_short(self.FIRST_CE_PTR_INDEX_ADDR, dialog_index)
        self.dialog_data.write()

        self.battle_message_data.assign([dialog.data() for dialog in self.battle_messages])
        self.battle_message_data.write()

        self.single_line_battle_dialog_data.assign([dialog.data() for dialog in self.single_line_battle_dialogs])
        self.single_line_battle_dialog_data.write()

        self.multi_line_battle_dialog_data.assign([dialog.data() for dialog in self.multi_line_battle_dialogs])
        self.multi_line_battle_dialog_data.write()

    def print(self):
        for dialog in self.dialogs:
            dialog.print()
        for dialog in self.battle_messages:
            dialog.print()
        for dialog in self.single_line_battle_dialogs:
            dialog.print()
        for dialog in self.multi_line_battle_dialogs:
            dialog.print()
