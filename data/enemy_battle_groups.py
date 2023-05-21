unused_event_battle_groups = {
    9:   "B.Day Suit/Officer",
    10:  "Merchant/B.Day Suit",
    49:  "Empty",
    50:  "Empty",
    51:  "Empty",
    52:  "Empty",
    54:  "Empty",
    56:  "Empty",
    58:  "Lv60 Magic event battle",
    59:  "Terra vs Officer",
    60:  "Empty",
    61:  "Empty",
    62:  "Empty",
    63:  "Atma (Broken)",
    74:  "Umaro (Dummied)",
    75:  "Unbeatable Guardian",
    76:  "Guardian (Repeat)",
    77:  "Tritoch (Vicks/Wedge/Terra)",
    78:  "Tritoch (Terra)",
    88:  "Dirt Drgn (Broken)",
    97:  "Empty",
    105:  "Empty",
    106:  "Empty",
    111: "White Drgn (repeat)",
    115:  "Terra flashback battle with 3 Soldiers",
    120:  "Tritoch (repeat)",
    121:  "Empty",
    122:  "Empty",
    123:  "Empty",
    124:  "Kefka (Thamasa)",
    127:  "Empty",
    128:  "Phunbaba 1",
    129:  "Phunbaba 2"
}

event_battle_groups_to_avoid = {
    53:  "Zone Eater",
    83:  "Kefka (final)",
    101: "Face/Long Arm/Short Arm"
}

boss_event_battle_groups = {
    6: "Marshal",
    18: "Rizopas",
    46: "Leader",
    57: "Kefka (Narshe)",
    64: "Whelk",
    66: "Vargas",
    67: "TunnelArmr",
    68: "GhostTrain",
    69: "Dadaluma",
    70: "Ifrit/Shiva",
    71: "Cranes",
    72: "Number 024",
    73: "Number 128",
    79: "FlameEater",
    80: "AtmaWeapon",
    81: "Nerapa",
    82: "SrBehemoth",
    84: "Tentacles",
    85: "Dullahan",
    86: "Chadarnook",
    89: "Air Force",
    90: "Stooges",
    92: "Wrexsoul",
    93: "Doom Gaze",
    94: "Hidon",
    98: "Doom",
    99: "Goddess",
    100: "Poltrgeist",
    103: "Ultros 1",
    104: "Ultros 2",
    107: "Ultros/Chupon",
    112: "Atma",
    114: "Inferno",
    117: "Umaro",
    119: "Tritoch",
    125: "Ultros 3",
    130: "Phunbaba 3",
    131: "Phunbaba 4",
    140: "Guardian",
    145: "MagiMaster"
}

dragon_event_battle_groups = {
    132: "Ice Dragon",
    133: "Storm Drgn",
    134: "Dirt Drgn",
    135: "Gold Drgn",
    136: "Skull Drgn",
    137: "Blue Drgn",
    138: "Red Dragon",
    139: "White Drgn",
}

event_battle_group_name = {}
event_battle_group_name.update(boss_event_battle_groups)
event_battle_group_name.update(dragon_event_battle_groups)

name_event_battle_group = {v: k for k, v in event_battle_group_name.items()}
