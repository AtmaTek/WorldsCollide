from memory.space import Bank, Reserve, Allocate, Write
import instruction.asm as asm

def equipable_mod(espers):
    from data.characters import Characters

    character_id_address = 0x1cf8
    gray_out_if_equipped = 0xc35576
    set_text_color = 0xc35595

    space = Allocate(Bank.C3, 145, "equipable espers", asm.NOP())

    equip_table = space.next_address
    for esper in espers.espers:
        space.write(
            esper.equipable_characters.to_bytes(2, "little"),
        )

    store_character_id = space.next_address
    space.copy_from(0x31b61, 0x31b63)   # x = character slot, a = character id
    space.write(
        asm.STA(character_id_address, asm.ABS),
        asm.RTS(),
    )

    check_equipable = space.next_address
    space.write(
        asm.PHX(),
        asm.PHP(),
        asm.STA(0xe0, asm.DIR),         # save esper (for use by callers)
        asm.XY8(),
        asm.A16(),
        asm.ASL(),                      # a = esper id * 2 (2 bytes for character bits)
        asm.TAX(),                      # x = esper id * 2
        asm.PHX(),
        asm.LDA(character_id_address, asm.ABS), # a = character id
        asm.ASL(),                      # a = character id * 2 (2 bytes for character bits)
        asm.TAX(),                      # x = character id * 2
        asm.LDA(0xc39c67, asm.LNG_X),   # a = character bit mask
        asm.PLX(),
        asm.AND(equip_table, asm.LNG_X),# and character bit mask with esper equipable bit mask
        asm.BEQ("NOT_EQUIPABLE"),       # branch if result is zero
        asm.PLP(),
        asm.PLX(),
        asm.JMP(gray_out_if_equipped, asm.ABS),

        "NOT_EQUIPABLE",
        asm.PLP(),
        asm.PLX(),
        asm.LDA(0x28, asm.IMM8),        # load text color (gray)
        asm.JMP(set_text_color, asm.ABS),
    )

    # TODO add new text type for this
    cant_equip_len = len("Can't equip!")
    cant_equip_error_text = space.next_address
    space.write(
        0x82, # C
        0x9a, # a
        0xa7, # n
        0xc3, # '
        0xad, # t
        0xff, #
        0x9e, # e
        0xaa, # q
        0xae, # u
        0xa2, # i
        0xa9, # p
        0xbe, # !
    )

    # change error message from "<character> has it!" to "Can't equip!"
    unequipable_error = space.next_address
    space.write(
        asm.LDA(0x1602, asm.ABS_X),     # a = first letter of name of character with esper equipped
        asm.CMP(0x80, asm.IMM8),        # compare against empty character (no character has esper equipped)
        asm.BCC("UNEQUIPABLE"),         # branch if not already equipped by another character

        "ALREADY_EQIPPED",
        asm.LDY(Characters.NAME_SIZE, asm.IMM8),    # y = name length
        asm.RTS(),

        "UNEQUIPABLE",
        asm.PLX(),                      # pull return address (do not return to vanilla already equipped)
        asm.LDX(0x0000, asm.IMM16),     # start at character zero in error message

        "PRINT_ERROR_LOOP",
        asm.LDA(cant_equip_error_text, asm.LNG_X),  # a = error_message[x]
        asm.STA(0x2180, asm.ABS),                   # print error_message[x]
        asm.INX(),
        asm.CPX(cant_equip_len, asm.IMM16),
        asm.BCC("PRINT_ERROR_LOOP"),
        asm.STZ(0x2180, asm.ABS),                   # print NULL
        asm.JMP(0x7fd9, asm.ABS),                   # print error_message
    )

    space = Reserve(0x31b61, 0x31b63, "skill menu store character id")
    space.write(
        asm.JSR(store_character_id, asm.ABS),
    )

    space = Reserve(0x35594, 0x35594, "already equipped esper name color")
    space.write(
        0x2c, # gray, blue shadow
    )

    space = Reserve(0x355af, 0x355b1, "load name length for esper already equipped error message", asm.NOP())
    space.write(
        asm.JSR(unequipable_error, asm.ABS),
    )

    space = Reserve(0x35524, 0x35526, "load esper palette", asm.NOP())
    space.write(
        asm.JSR(check_equipable, asm.ABS),
    )

    space = Reserve(0x358e1, 0x358e5, "load esper palette", asm.NOP())
    space.write(
        asm.JSR(check_equipable, asm.ABS),
    )

    space = Reserve(0x359b1, 0x359b3, "load esper palette", asm.NOP())
    space.write(
        asm.JSR(check_equipable, asm.ABS),
    )

    space = Reserve(0x358e8, 0x358eb, "equip esper if name not grayed out", asm.NOP())
    space.add_label("EQUIP_ESPER", 0x35902)
    space.write(
        asm.CMP(0x20, asm.IMM8),
        asm.BEQ("EQUIP_ESPER"),
    )
