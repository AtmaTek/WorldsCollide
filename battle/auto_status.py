from memory.space import Bank, START_ADDRESS_SNES, Reserve, Write
import instruction.asm as asm

import constants.status_effects as status_effects
import data.event_bit as event_bit
import objectives

class _AutoStatus:
    def __init__(self):
        auto_b_status_effects = ["Condemned", "Image", "Mute", "Berserk", "Muddle", "Seizure", "Sleep"]
        auto_c_status_effects = ["Float", "Regen", "Slow", "Haste", "Shell", "Safe", "Reflect"]

        auto_addresses = []
        for status in auto_b_status_effects:
            auto_addresses.append(self.auto_status(status, status_effects.B))
        for status in auto_c_status_effects:
            auto_addresses.append(self.auto_status(status, status_effects.C))

        src = [
            # original replaced code
            asm.LDA(0xbc, asm.DIR),
            asm.STA(0x3c6c, asm.ABS_X),     # store status b granted by equipment
            asm.LDA(0xd4, asm.DIR),
            asm.STA(0x3c6d, asm.ABS_X),     # store status c granted by equipment
        ]

        # auto status effects granted by objectives
        for address in auto_addresses:
            src += [
                asm.JSR(address, asm.ABS),
            ]
        src += [
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "auto status effects")
        auto_status_effects = space.start_address

        space = Reserve(0x228bf, 0x228c8, "equipment status effects", asm.NOP())
        space.write(
            asm.JSL(START_ADDRESS_SNES + auto_status_effects),
        )

    def auto_status(self, status_name, status_effects_group):
        status_name = status_name.capitalize()
        auto_status_name = "Auto " + status_name
        auto_status_name_upper = auto_status_name.upper()

        if status_name == "Float":
            status_bit = 1 << status_effects_group.name_id["Dance"]
        else:
            status_bit = 1 << status_effects_group.name_id[status_name]
        if status_effects_group == status_effects.B:
            status_address = 0x3c6c
        elif status_effects_group == status_effects.C:
            status_address = 0x3c6d

        src = []
        if auto_status_name in objectives.results:
            for objective in objectives.results[auto_status_name]:
                objective_event_bit = event_bit.objective(objective.id)
                bit = event_bit.bit(objective_event_bit)
                address = event_bit.address(objective_event_bit)

                src += [
                    asm.LDA(address, asm.ABS),
                    asm.AND(2 ** bit, asm.IMM8),
                    asm.BNE(auto_status_name_upper),
                ]
        src += [
            "NO_ " + auto_status_name_upper,
            asm.RTS(),

            auto_status_name_upper,
            asm.LDA(status_address, asm.ABS_X),
            asm.ORA(status_bit, asm.IMM8),
            asm.STA(status_address, asm.ABS_X),
            asm.RTS(),
        ]
        space = Write(Bank.F0, src, auto_status_name)
        return space.start_address
auto_status = _AutoStatus()
