def main():
    # Usage:
    # python wc_config.py -i ff6wc.smc <arguments>

    # Get arguments
    import sys
    args = sys.argv

    # Get filename
    try:
        filename = args[args.index('-i') + 1]
    except:
        print('Usage: python wc_config.py -i <filename.smc> <arguments>')
        return

    # Get output filename
    try:
        fileout = args[args.index('-o') + 1]
    except:
        fileout = filename[:filename.index('.smc')] + '_config.smc'

    # Parse input arguments
    import config.config as c
    configuration = {}

    for opt in c.config_controls.keys():
        findflag = [a in args for a in c.config_controls[opt]]
        if True in findflag:
            # Collect the input argument
            this_arg = args[args.index(c.config_controls[opt][findflag.index(True)]) + 1]

            # Battle Mode
            if opt == 'BatMode':
                if this_arg in ['a', 'A', 'active', 'Active', 'false', 'False', '0']:
                    this_val = False
                else:
                    this_val = True  # default value

            # Battle Speed
            elif opt == 'BatSpeed':
                if this_arg in [str(i) for i in range(1,7)]:
                    this_val = int(this_arg)
                else:
                    this_val = 3  # default value

            # Message Speed
            elif opt == 'MsgSpeed':
                if this_arg in [str(i) for i in range(1,7)]:
                    this_val = int(this_arg)
                else:
                    this_val = 3  # default value

            # Command Set
            elif opt == 'Command':
                if this_arg in ['s', 'S', 'short', 'Short', 'true', 'True', '1']:
                    this_val = True
                else:
                    this_val = False # default value

            # Gauge
            elif opt == 'Gauge':
                if this_arg in ['off', 'Off', 'true', 'True', '1']:
                    this_val = True
                else:
                    this_val = False # default value

            # Sound mode
            elif opt == 'Sound':
                if this_arg in ['m', 'mono', 'M', 'Mono', 'true', 'True', '1']:
                    this_val = True
                else:
                    this_val = False  # default value

            # Cursor
            elif opt == 'Cursor':
                if this_arg in ['m', 'M', 'memory', 'Memory', 'true', 'True', '1']:
                    this_val = True
                else:
                    this_val = False  # default value

            # Re-equip
            elif opt == 'Reequip':
                if this_arg in ['e', 'E', 'empty', 'Empty', 'true', 'True', '1']:
                    this_val = True
                else:
                    this_val = False  # default value

            # Spell Order
            elif opt == 'SpellOrder':
                if this_arg in [str(i) for i in range(1,7)]:
                    this_val = int(this_arg)
                else:
                    this_val = 1  # default value

            # Font color:  Input argument is one RGB triple: RRGGBB
            elif opt == 'Font':
                # RGB value: check if valid
                RGB = [int(this_arg)//10000, (int(this_arg)%10000)//100, int(this_arg)%100]
                is_valid = [color > -1 and color < 32 for color in RGB]
                if False not in is_valid:
                    this_val = [RGB]
                else:
                    this_val = [[31, 31, 31]]  # default white

            # Wallpaper selection
            elif opt == 'Wallpaper':
                if this_arg in [str(i) for i in range(1,9)]:
                    this_val = int(this_arg)
                else:
                    this_val = 1  # default value

            # Window color:  Input argument is seven RGB triple: RRGGBB.RRGGBB.RRGGBB.RRGGBB.RRGGBB.RRGGBB.RRGGBB
            # Unchanged values may be omitted (example: 'RRGGBB...RRGGBB...' changes only 1st and 4th value
            elif opt in ['Window'+str(i) for i in range(1,9)]:
                this_val = c.Window_default[opt]  # load default values
                # These will be RGB values separated by '.'
                a = this_arg.split('.')
                for i in range(len(a)):
                    if len(a[i]) == 6:
                        # RGB values: check if valid
                        RGB = [int(a[i])//10000, (int(a[i])%10000)//100, int(a[i])%100]
                        is_valid = [color > -1 and color < 32 for color in RGB]
                        if False not in is_valid:
                            this_val[i] = RGB

            # Write the value to the configuration object
            configuration[opt] = this_val

    # Say the loaded configuration options
    #print(configuration)

    # Load rom
    from config.wcrom import WCROM
    r = WCROM(filename)  # Use modified memory.rom.ROM() to load an already-patched ff6wc file

    # Patch config
    c.set_config(r, configuration)

    # Write the output file
    r.write(fileout)


if __name__ == '__main__':
    main()
