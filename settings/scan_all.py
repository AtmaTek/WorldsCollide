from memory.space import Bank, Reserve, Write, Read
import instruction.asm as asm
import args

class ScanAll:
    def __init__(self):
        if args.scan_all:
            self.teach_scan()

    def teach_scan(self):
        from data.spells import Spells
        from data.spell_names import name_id
        from data.characters import Characters

        learned_spells_start = 0x1a6e
        scan_id = name_id["Scan"]

        start_addr = learned_spells_start + scan_id
        learner_count = Characters.CHARACTER_COUNT - 2 # no gogo/umaro
        last_offset = Spells.SPELL_COUNT * learner_count

        src = [
            Read(0x0bdcc, 0x0bdd6),                 # initialize spells to 0% learned

            asm.LDX(0x00, asm.DIR),                 # x = 0x0000

            "LOOP_START",
            asm.LDA(0xff, asm.IMM8),                # a = 0xff (spell learned value)
            asm.STA(start_addr, asm.ABS_X),         # set scan learned for current character
            asm.A16(),
            asm.TXA(),                              # a = scan address offset for current character
            asm.CLC(),
            asm.ADC(Spells.SPELL_COUNT, asm.IMM16), # go to next character
            asm.TAX(),                              # x = scan address offset for next character
            asm.A8(),
            asm.CPX(last_offset, asm.IMM16),        # all characters done?
            asm.BLT("LOOP_START"),                  # branch if not

            asm.TDC(),
            asm.RTS(),
        ]
        space = Write(Bank.C0, src, "scan all learn_scan")
        learn_scan = space.start_address

        space = Reserve(0x0bdcc, 0x0bdd6, "initialize spells and learn scan", asm.NOP())
        space.write(
            asm.JSR(learn_scan, asm.ABS),
        )
