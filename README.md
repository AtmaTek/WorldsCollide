# FFVI Worlds Collide
Worlds Collide is an open worlds randomizer for Final Fantasy VI (originally Final Fantasy III in the US).

You start with the airship and can travel freely between the World of Balance and the World of Ruin.  
Complete objectives while searching the worlds for characters, espers, and items until you are ready to challenge Kefka.

## Links

###### Start playing| [ff6wc.com](https|//www.ff6wc.com)
###### More Info| [wiki.ff6wc.com](https|//wiki.ff6wc.com)
###### Community| [discord](https|//discord.gg/5MPeng5)

## Usage

```sh
$ python3 wc.py -i ffiii.smc
```

```sh
$ python3 wc.py -h
```

An FF6 Worlds Collide ROM may be patched with custom configuration options: 

```shell
$ python3 wc_config.py -i ff6wc.smc <config arguments>
```
Controls for configuration are as follows.  All values are optional except -i <filename>.  (Note undeclared options are left as default)

| Option      | flags                                                                | arguments                                    |
|-------------|----------------------------------------------------------------------|----------------------------------------------|
| Input file  | -i                                                                   | input_filename.smc (required)
| Output file | -o                                                                   | output_filename.smc 
| Bat. Mode   | [-b, -B, -batmode, -BatMode]                                         | [a, active, False, 0] / [w, wait, True, 1]   
| Bat. Speed  | [-bs, -BS, -batspeed, -BatSpeed]                                     | [1 -- 6]                                     
| Msg. Speed  | [-ms, -MS, -msgspeed, -MsgSpeed]                                     | [1 -- 6]                                     
| Command     | [-com, -COM, -command, -Command]                                     | [w, window, False, 0] / [s, short, True, 1]  
| Gauge       | [-g, -G, -gauge, -Gauge]                                             | [on, False, 0] / [off, True, 1]              
| Sound       | [-s, -S, -sound, -Sound]                                             | [s, stereo, False, 0] / [m, mono, True, 1]   
| Cursor      | [-c, -C, -cursor, -Cursor]                                           | [r, reset, False, 0] / [m, memory, True, 1]  
| Re-equip    | [-r, -R, -reequip, -Reequip]                                         | [o, optimum, False, 0] / [e, empty, True, 1] 
| Mag. Order  | [-mo, -MO, -magorder, -MagOrder, -so, -SO, -spellorder, -SpellOrder] | [1 -- 6]                                     
| Font        | [-f, -F, -font, -Font]                                               | RGB triple: RRGGBB                           
| Wallpaper   | [-w, -W, -wallpaper, -Wallpaper]                                     | [1--8]                                       
| Window1     | [-w1, -W1, -win1, -Win1,-window1, -Window1]                          | Series of 7 RGB triples separated by '.'     
| Window2     | [-w2, -W2, -win2, -Win2,-window2, -Window2]                          | (Unchanged values may be omitted.            
| Window3     | [-w3, -W3, -win3, -Win3,-window3, -Window3]                          | RGB values must be in range 0--31)           
| Window4     | [-w4, -W4, -win4, -Win4,-window4, -Window4]                          | Example:                                     
| Window5     | [-w5, -W5, -win5, -Win5,-window5, -Window5]                          | 010203.040506.070809....293031               
| Window6     | [-w6, -W6, -win6, -Win6,-window6, -Window6]                          | 
| Window7     | [-w7, -W7, -win7, -Win7,-window7, -Window7]                          |
| Window8     | [-w8, -W8, -win8, -Win8,-window8, -Window8]                          |

example:

```shell
python3 wc_config.py -i ff6wc_test.smc -gauge off -batspeed 6 -msgspeed 1 -magorder 2 -w 2 -f 223122 -w2 121612.020904.000900.050610.050806.040905.000001
```