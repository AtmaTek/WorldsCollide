# Tools for writing new default values for config values to a FF6 ROM
def rgb2bytes(rgb):
    # Convert RGB value to writeable bytes
    b = [bin(n)[2:].zfill(5) for n in rgb]
    b = '0' + b[2] + b[1] + b[0]         # SNES colors are in BGR order and cover 2 bytes
    return [int(b[8:],2), int(b[:8],2)]  # SNES color bytes are written in backwards order

def bytes2rgb(bytes):
    # Convert read bytes to RGB value
    b = bin(bytes[1])[2:].zfill(8) + bin(bytes[0])[2:].zfill(8)  # SNES color bytes written backwards order
    return [int(b[11:],2), int(b[6:11],2), int(b[1:6],2)]        # SNES colors are in BGR order

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
    0xFFFFFE : "Config2", # RAM $1D54, one byte sets: mbcc csss (controller 2 m, custom buttons b, font and window pallette ccc?, default spell order sss). Note all these are set to 0 in default, there is no default memory location.
    0xFFFFFF : "Config3" # RAM $1D4E, one byte sets: gcsr wwww (gauge g, cursor c, sound s, reequip r, wallpaper wwww (0-7)). Note all these are set to 0 in default, there is no default memory location.
}

config_memory = {v: k for k, v in memory_config.items()}

Config1_default = {
    'Command' : False,
    'MsgSpeed': 3,
    'BatMode':  True,
    'BatSpeed': 3
}

Window_default = {
    'Window1' : [[25, 28, 28], [19, 3, 21], [20, 22, 22], [26, 2, 4], [16, 16, 16], [2, 18, 18], [10, 10, 10], [9, 9, 17]],
    'Window2': [[14, 15, 15], [29, 1, 10], [8, 9, 9], [5, 25, 1], [7, 8, 8], [1, 17, 25], [6, 7, 7], [28, 8, 17]],
    'Window3' : [[7, 13, 16], [1, 18, 17], [6, 10, 13], [21, 1, 25], [4, 7, 10], [8, 25, 16], [3, 6, 7], [28, 16, 0]],
    'Window4': [[17, 12, 4], [17, 24, 27], [15, 11, 4], [17, 16, 11], [14, 9, 3], [13, 0, 3], [12, 8, 2], [9, 24, 12]],
    'Window5': [[13, 11, 8], [1, 1, 27], [12, 11, 8], [1, 1, 19], [12, 10, 7], [29, 24, 10], [11, 9, 6], [25, 16, 2]],
    'Window6': [[19, 19, 19], [14, 10, 27], [13, 15, 15], [29, 17, 2], [10, 12, 11], [13, 1, 18], [8, 10, 9], [5, 17, 1]],
    'Window7': [[15, 21, 14], [26, 1, 11], [12, 17, 11], [14, 9, 26], [9, 15, 8], [1, 25, 9], [7, 13, 6], [25, 8, 17]],
    'Window8': [[20, 12, 13], [21, 9, 6], [25, 24, 22], [27, 2, 29], [20, 19, 16], [2, 18, 14], [26, 17, 0], [2, 8, 14]]
}

def set_config(rom, config_set):
    ### Write configuration values to a ROM.  Currently works for Config set #1 and window palettes.
    # Set default Config1 object & populate with requested options
    con1_set = {k: v for k, v in Config1_default.items()}
    for k in con1_set.keys():
        if k in config_set.keys():
            con1_set[k] = config_set[k]
    # Generate the appropriate byte
    con1_bin = bin(con1_set['Command'])[2:] + bin(con1_set['MsgSpeed']-1)[2:].zfill(3) \
               + bin(con1_set['BatMode'])[2:] + bin(con1_set['BatSpeed']-1)[2:].zfill(3)
    con1 = [int(con1_bin,2)]
    # Write byte to the ROM
    rom.set_bytes(config_memory["Config1"], con1)

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


### Proof of concept program:
# filename = "~/ff6wc_test.smc"  # Path to an already-patched ff6wc rom
# filename_out = "~/ff6wc_configured.smc"
# import config.config as c
# from memory.rom import ROM
# r = ROM(filename, False)  # Note I modified ROM() to disable the valid_rom_file check, since this is processing an already-patched WC rom
# config = {
#   'Command': False,
#   'MsgSpeed': 1,
#   'BatMode': True,
#   'BatSpeed': 6,
#   'Window1': [[0,0,12], [1,0,31], [2,11,4], [10,31,12], [0,31,0], [23,8,0], [0,10,0]],
#   'Font': [[31,31,19]]
# }  # Define configuration values
# c.set_config(r, config)
# r.write(filename_out)