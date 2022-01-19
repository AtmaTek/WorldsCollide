# Tools for writing new default values for config values to a FF6 ROM
def rgb2bytes(rgb):
    # Convert RGB value to writeable bytes
    b = [bin(n)[2:].zfill(5) for n in rgb]
    b = '0' + b[2] + b[1] + b[0]         # SNES colors are in BGR order and cover 2 bytes
    return [int(b[8:],2), int(b[:8],2)]  # SNES color bytes are written in backwards order

memory_config = {         # Memory codes for configuration variables
    0x2d1c02 : "Window1", # Window 1 pallete colors 1--7, 14 bytes
    0x2d1c22 : "Window2", # Window 2 pallete colors 1--7, 14 bytes
    0x2d1c42 : "Window3", # Window 3 pallete colors 1--7, 14 bytes
    0x2d1c62 : "Window4", # Window 4 pallete colors 1--7, 14 bytes
    0x2d1c82 : "Window5", # Window 5 pallete colors 1--7, 14 bytes
    0x2d1cA2 : "Window6", # Window 6 pallete colors 1--7, 14 bytes
    0x2d1cC2 : "Window7", # Window 7 pallete colors 1--7, 14 bytes
    0x2d1cE2 : "Window8", # Window 8 pallete colors 1--7, 14 bytes
    0x18e806 : "Font" # Default font color, 2 bytes.  Note, setting this doesn't change default slider position for some reason.
}

config_memory = {v: k for k, v in memory_config.items()}

def set_config_rgb(rom, conf_name, values):
    # write configuration color values to a rom
    # This currently works for window on the default ROM, but not for font.  Why?  Related to slider position problem?
    i = 0
    for v in values:
        rom.set_bytes(config_memory[conf_name] + 2*i, rgb2bytes(v))
        i += 1  # shift index

