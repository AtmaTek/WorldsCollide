# Tools for writing new default values for config values to a FF6 ROM

# Version 2: Concept
#   - Use WC memory tools to find & patch a default config section of the rom when running wc.py
#   - Have Config.py read the value at 0x0374C2 as a pointer to the config section with relative offsets.
# Memory location stored at:
#   0x0370C2: ['20', PP, NN, '20', PP+06, NN]])  # JSR #$NNPP; JSR #$NNPP+06
# Memory structure at new location:
#   Location:  0xMMNNPP + 00: ['A9', '00', '8D', '54', '1D', '60']  # LDA #$00; STA $1D54; RTS  # Config #2
#   Location:  0xMMNNPP + 06: ['A9', '00', '8D', '4E', '1D', '60']  # LDA #$00; STA $1D4E; RTS  # Config #3

### Relevant code from battle/multipliers.py:
# from memory.space import Bank, Reserve, Write
# import instruction.asm as asm
# import instruction.c2 as c2
# import args
#
# class Multipliers():
#     ...
#     def set_xp_multiplier(self, multiplier):
#         src = [    # Programmatically write your new source code
#             asm.A8(),
#             asm.LDA(multiplier, asm.IMM8),
#             asm.STA(0xe8, asm.DIR),                     # $e8 = given multiplier
#             asm.A16(),
#             asm.LDA(0x3d8c, asm.ABS_X),                 # a = enemy exp
#             asm.JSR(c2.multiply_max_65535, asm.ABS),    # a = enemy exp * multiplier
#             asm.RTS(),
#         ]
#         space = Write(Bank.C2, src, "exp multiply function")
#         multiply_exp = space.start_address
#         ...
#         space = Reserve(0x25dc1, 0x25dc3, "call exp multiply function")
#         space.write(
#             asm.JSR(multiply_exp, asm.ABS),
#         )


def rgb2bytes(rgb):
    # Convert RGB value to writeable bytes
    b = [bin(n)[2:].zfill(5) for n in rgb]
    b = '0' + b[2] + b[1] + b[0]         # SNES colors are in BGR order and cover 2 bytes
    return [int(b[8:],2), int(b[:8],2)]  # SNES color bytes are written in backwards order

def bytes2rgb(bytes):
    # Convert read bytes to RGB value
    b = bin(bytes[1])[2:].zfill(8) + bin(bytes[0])[2:].zfill(8)  # SNES color bytes written backwards order
    return [int(b[11:],2), int(b[6:11],2), int(b[1:6],2)]        # SNES colors are in BGR order

def bytes2hex(bytes):
    # Convert bytes to hex values
    hex = '0123456789ABCDEF'
    return [hex[b//16] + hex[b%16] for b in bytes]

config_controls = {
    'BatMode'   : ['-b', '-B', '-batmode', '-BatMode'],       # Active (false) / Wait (true)
    'BatSpeed'  : ['-bs', '-BS', '-batspeed', '-BatSpeed'],   # range 1--6
    'MsgSpeed'  : ['-ms', '-MS', '-msgspeed', '-MsgSpeed'],   # range 1--6
    'Command'   : ['-com', '-COM', '-command', '-Command'],   # Window (false) / Short (true)
    'Gauge'     : ['-g', '-G', '-gauge', '-Gauge'],           # On (false) / Off (true)
    'Sound'     : ['-s', '-S', '-sound', '-Sound'],           # Stereo (false) / Mono (true)
    'Cursor'    : ['-c', '-C', '-cursor', '-Cursor'],         # Reset (false) / Memory (true)
    'Reequip'   : ['-r', '-R', '-reequip', '-Reequip'],       # Optimum (false) / Empty (true)
    'SpellOrder': ['-so', '-SO', '-mo', '-MO', '-magorder', '-MagOrder', '-spellorder', '-SpellOrder'], # range 1--6
    'Font'      : ['-f', '-F', '-font', '-Font'],             # RGB color
    'Wallpaper' : ['-w', '-W', '-wallpaper', '-Wallpaper'],   # range 1--8
    'Window1'   : ['-w1', '-W1', '-win1', '-Win1','-window1', '-Window1'],
    'Window2'   : ['-w2', '-W2', '-win2', '-Win2','-window2', '-Window2'],
    'Window3'   : ['-w3', '-W3', '-win3', '-Win3','-window3', '-Window3'],
    'Window4'   : ['-w4', '-W4', '-win4', '-Win4','-window4', '-Window4'],
    'Window5'   : ['-w5', '-W5', '-win5', '-Win5','-window5', '-Window5'],
    'Window6'   : ['-w6', '-W6', '-win6', '-Win6','-window6', '-Window6'],
    'Window7'   : ['-w7', '-W7', '-win7', '-Win7','-window7', '-Window7'],
    'Window8'   : ['-w8', '-W8', '-win8', '-Win8','-window8', '-Window8']
    # Unused controls:
    # 'Controller2' : False,  # Single (false) / Multiple (true)
    # 'CustomButtons': False, # for true, set mapping in $1D50-$1D53 (C3/70A4-C3/70B5)
    # 'FontWindowPaletteSelect':  1,  # Default position of "Color" pointer in config menu. range 1-8.
}

memory_config = {         # Memory codes for configuration variables
    0x2d1c02 : "Window1", # Window 1 pallete colors 1--7, 14 bytes
    0x2d1c22 : "Window2", # Window 2 pallete colors 1--7, 14 bytes
    0x2d1c42 : "Window3", # Window 3 pallete colors 1--7, 14 bytes
    0x2d1c62 : "Window4", # Window 4 pallete colors 1--7, 14 bytes
    0x2d1c82 : "Window5", # Window 5 pallete colors 1--7, 14 bytes
    0x2d1cA2 : "Window6", # Window 6 pallete colors 1--7, 14 bytes
    0x2d1cC2 : "Window7", # Window 7 pallete colors 1--7, 14 bytes
    0x2d1cE2 : "Window8", # Window 8 pallete colors 1--7, 14 bytes
    0x18e806 : "Font1",   # Default font color, 2 bytes.  Note, setting this doesn't change default slider position for some reason.
    0x03709F : "Font2",   # Default font color, 2 bytes.  Does this just affect new game??
    0x0370B9 : "Config1", # RAM $1D4D, one byte sets: cmmm wbbb (command set c, message spd mmm, battle mode w, battle speed bbb)
    #0x03FC19 : "Config2", # RAM $1D54, one byte sets: mbcc csss (controller 2 m, custom buttons b, font and window pallette ccc?, default spell order sss). Note all these are set to 0 in default, there is no default memory location.
    #0x03FC1F : "Config3" # RAM $1D4E, one byte sets: gcsr wwww (gauge g, cursor c, sound s, reequip r, wallpaper wwww (0-7)). Note all these are set to 0 in default, there is no default memory location.
}

config_memory = {v: k for k, v in memory_config.items()}

Config1_default = {
    'Command' : False,  # Window (false) / Short (true)
    'MsgSpeed': 3,      # range 1--6
    'BatMode':  True,   # Active (false) / Wait (true)
    'BatSpeed': 3       # range 1--6
}

Config2_default = {
    'Controller2' : False,  # Single (false) / Multiple (true)
    'CustomButtons': False, # for true, set mapping in $1D50-$1D53 (C3/70A4-C3/70B5)
    'FontWindowPaletteSelect':  1,  # Default position of "Color" pointer in config menu. range 1-8.
    'SpellOrder': 1         # range 1--6
}

Config3_default = {
    'Gauge' : False,        # On (false) / Off (true)
    'Cursor': False,        # Reset (false) / Memory (true)
    'Sound':  False,        # Stereo (false) / Mono (true)
    'Reequip': False,       # Optimum (false) / Empty (true)
    'Wallpaper': 1          # range 1--8
}

Window_default = {
    'Window1' : [[25, 28, 28], [20, 22, 22], [16, 16, 16], [10, 10, 10], [5, 6, 6], [6, 6, 17], [5, 5, 16]],
    'Window2': [[14, 15, 15], [8, 9, 9], [7, 8, 8], [6, 7, 7], [5, 6, 6], [4, 5, 5], [1, 2, 2]],
    'Window3' : [[7, 13, 16], [6, 10, 13], [4, 7, 10], [3, 6, 7], [2, 4, 5], [2, 3, 4], [10, 15, 19]],
    'Window4': [[17, 12, 4], [15, 11, 4], [14, 9, 3], [12, 8, 2], [19, 21, 20], [7, 9, 8], [4, 6, 5]],
    'Window5': [[13, 11, 8], [12, 11, 8], [12, 10, 7], [11, 9, 6], [10, 8, 4], [7, 7, 4], [2, 2, 2]],
    'Window6': [[19, 19, 19], [13, 15, 15], [10, 12, 11], [8, 10, 9], [6, 8, 7], [4, 6, 5], [1, 3, 2]],
    'Window7': [[15, 21, 14], [12, 17, 11], [9, 15, 8], [7, 13, 6], [5, 10, 4], [4, 7, 4], [2, 5, 3]],
    'Window8': [[20, 12, 13], [25, 24, 22], [20, 19, 16], [26, 17, 0], [25, 13, 0], [20, 11, 0], [4, 4, 4]]
}

#def patch_config(rom):
#    # Patch the ROM to create a default value for Config2 and Config3
#    # Patch lines that set default value = zero to jump to subroutines
#    rom.set_bytes(0x0370C2, [int(k, 16) for k in ['20', '18', 'FC', '20', '1E', 'FC']])  # JSR #$FC18; JSR #$FC1E
#    # Subroutine for Config2 ($1D54)
#    rom.set_bytes(0x03FC18, [int(k, 16) for k in ['A9', '00', '8D', '54', '1D', '60']])  # LDA #$00; STA $1D54; RTS
#    # Subroutine for Config3 ($1D4E)
#    rom.set_bytes(0x03FC1E, [int(k, 16) for k in ['A9', '00', '8D', '4E', '1D', '60']])  # LDA #$00; STA $1D4E; RTS


def set_config(rom, config_set):
    ### Write configuration values to a ROM.
    # Version 1: use fixed offset values
    #patch_config(rom) # patch the ROM to accept default config values

    # Version 2: read the variable offset values for Config #2 and #3 from the rom
    conf2_mem = rom.get_bytes_endian_swap(0x0370C3, 2)
    conf3_mem = rom.get_bytes_endian_swap(0x0370C6, 2)
    # Update memory values in config_memory: 1 byte past of the offsets extracted above.
    config2_value = '0x03'+ hex(int(bytes2hex(conf2_mem)[0]+bytes2hex(conf2_mem)[1], 16) + 1)[2:]
    config_memory["Config2"] = int(config2_value, 16)
    config3_value = '0x03'+ hex(int(bytes2hex(conf3_mem)[0]+bytes2hex(conf3_mem)[1], 16) + 1)[2:]
    config_memory["Config3"] = int(config3_value, 16)
    #print('Config #1 default at memory location: ' + str(config_memory["Config1"]))
    #print('Config #2 default at memory location: ' + str(config2_value))
    #print('Config #3 default at memory location: ' + str(config3_value))

    # Set default Config1 object & populate with requested options
    con1_set = {k: v for k, v in Config1_default.items()}
    for k in con1_set.keys():
        if k in config_set.keys():
            con1_set[k] = config_set[k]
    # Generate the appropriate byte
    con1_bin = bin(con1_set['Command'])[2:] + \
               bin(con1_set['MsgSpeed']-1)[2:].zfill(3) + \
               bin(con1_set['BatMode'])[2:] + \
               bin(con1_set['BatSpeed']-1)[2:].zfill(3)
    con1 = [int(con1_bin,2)]
    # Write byte to the ROM
    rom.set_bytes(config_memory["Config1"], con1)

    # Set default Config2 object & populate with requested options
    con2_set = {k: v for k, v in Config2_default.items()}
    for k in con2_set.keys():
        if k in config_set.keys():
            con2_set[k] = config_set[k]
    # Generate the appropriate byte: mbcccsss
    con2_bin = bin(con2_set['Controller2'])[2:] + \
               bin(con2_set['CustomButtons'])[2:] + \
               bin(con2_set['FontWindowPaletteSelect']-1)[2:].zfill(3) + \
               bin(con2_set['SpellOrder']-1)[2:].zfill(3)
    con2 = [int(con2_bin,2)]
    # Write byte to the ROM
    rom.set_bytes(config_memory["Config2"], con2)

    # Set default Config3 object & populate with requested options
    con3_set = {k: v for k, v in Config3_default.items()}
    for k in con3_set.keys():
        if k in config_set.keys():
            con3_set[k] = config_set[k]
    # Generate the appropriate byte: gcsrwwww
    con3_bin = bin(con3_set['Gauge'])[2:] + \
               bin(con3_set['Cursor'])[2:] + \
               bin(con3_set['Sound'])[2:] + \
               bin(con3_set['Reequip'])[2:] + \
               bin(con3_set['Wallpaper']-1)[2:].zfill(4)
    con3 = [int(con3_bin,2)]
    # Write byte to the ROM
    rom.set_bytes(config_memory["Config3"], con3)

    # Write window palettes, if defined
    for k in ['Window'+str(i) for i in range(1,9)]:
        if k in config_set.keys():
            set_config_rgb(rom, k, config_set[k])

    # Write font palette, if defined
    if 'Font' in config_set.keys():
        set_config_rgb(rom, 'Font1', config_set['Font'])  # Set actual font value
        set_config_rgb(rom, 'Font2', config_set['Font'])  # Set font controls


def set_config_rgb(rom, conf_name, values):
    # write configuration color values to a rom
    # This currently works for window on the default ROM, but not for font.  Why?  Related to slider position problem?
    i = 0
    for v in values:
        rom.set_bytes(config_memory[conf_name] + 2*i, rgb2bytes(v))
        i += 1  # shift index

