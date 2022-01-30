# List of addresses within the Battle Animation Scripts for the following commands:
#  B0 - Set background palette color addition (absolute)
#  B5 - Add color to background palette (relative)
#  AF - Set background palette color subtraction (absolute)
#  B6 - Subtract color from background palette (relative)
# By changing address + 1 to E0 (for absolute) or F0 (for relative), it causes no change to the background color (that is, no flash)
BATTLE_ANIMATION_FLASHES = [
    # [ Animation Script $01A2: Goner (bg1) ]
    #0x100088,
    #0x10008C,
    #0x100092,
    #0x100098,
    #0x1000A1,
    #0x1000A3,
    #0x1000D3,
    #0x1000DF,
    #0x100172,
    # [ Animation Script $0284: Misc. Monster Animation $0D: Final KEFKA Death (bg1) ]
    #0x10023A,
    #0x100240,
    #0x100248,
    #0x10024E,
    #0x10025B,
    #0x10025F,
    #0x100265,
    # [ Animation Script $011F: Atom Edge, True Edge (bg1) ]
    0x1003D0,
    0x1003DD,
    0x1003E6,
    0x10044B,
    0x100457,
    # [ Animation Script $027B: Monster Exit $0C: Boss Death (bg1) ]
    #0x100476,
    #0x10047C,
    #0x100484,
    #0x100497,
    # [ Animation Script $023A: Event Animation $0E: Transform into Magicite (bg3) ]
    0x100F30,
    0x100F3F,
    0x100F4E,
    # [ Animation Script $01C2: Meteo (bg3) ]
    #0x1011DC,
    #0x1011E0,
    #0x1011EA,
    # [ Animation Script $00AF: Purifier (bg3) ]
    0x101340,
    0x101348,
    0x101380,
    0x10138A,
    # [ Animation Script $0180: CleanSweep (bg1) ]
    #0x1016E8,
    #0x1016F6,
    #0x101717,
    # [ Animation Script $00FA: Wall (bg1) ]
    0x10177B,
    0x10177F,
    0x101788,
    0x101791,
    0x10179A,
    0x1017A3,
    0x1017AC,
    0x1017B5,
    # [ Animation Script $00E5: Pearl (bg1) ]
    0x10190E,
    0x101913,
    0x10191E,
    # [ Animation Script $00E6: Pearl (bg3) ]
    0x10193E,
    # [ Animation Script $00E0: Ice 3 (sprite) ]
    0x101978,
    0x10197B,
    0x10197E,
    0x101981,
    0x101984,
    0x101987,
    0x10198A,
    0x10198D,
    0x101990,
    # [ Animation Script $00C4: Fire 3 (sprite) ]
    0x1019FA,
    0x101A1C,
    # [ Animation Script $00ED: Sleep (bg1) ]
    0x101A23,
    0x101A29,
    0x101A33,
    # [ Animation Script $0220: 7-Flush (bg1) ]
    0x101B43,
    0x101B47,
    0x101B4D,
    0x101B53,
    0x101B59,
    0x101B5F,
    0x101B65,
    0x101B6B,
    # [ Animation Script $021E: H-Bomb (bg1) ]
    0x101BC5,
    0x101BC9,
    0x101C13,
    # [ Animation Script $0218: Revenger (sprite) ]
    0x101C62,
    0x101C66,
    0x101C6C,
    0x101C72,
    0x101C78,
    0x101C7E,
    0x101C84,
    0x101C86,
    0x101C8C,
    # [ Animation Script $0210: Phantasm (bg3) ]
    0x101DFD,
    0x101E03,
    0x101E07,
    0x101E0D,
    0x101E15,
    0x101E1F,
    0x101E27,
    0x101E2F,
    0x101E3B,
    # [ Animation Script $0215: Zinger (bg1) ]
    0x101E54,
    0x101E5A,
    0x101E6B,
    # [ Animation Script $0208: N. Cross (bg3) ]
    0x101EF9,
    0x101EFD,
    0x101F07,
    # [ Animation Script $01F5: Water Edge (sprite) ]
    #0x10235A,
    #0x10235E,
    #0x102376,
    # [ Animation Script $01F4: Fire Skean (bg1) ]
    #0x1023C7,
    #0x1023CB,
    #0x1023DB,
    # [ Animation Script $01CC: TigerBreak (bg1) ]
    0x10240D,
    0x102411,
    0x102416,
    # [ Animation Script $01F3: Fader (bg1) ]
    0x102480,
    0x102484,
    0x1024C2,
    # [ Animation Script $01F0: Tri-Dazer (bg1) ]
    0x1024D1,
    0x1024D5,
    0x1024E3,
    # [ Animation Script $01EE: Metamorph (bg1) ]
    0x102595,
    0x102599,
    0x1025AF,
    # [ Animation Script $01E9: Cat Rain (bg1) ]
    0x102677,
    0x10267B,
    # [ Animation Script $01E6: Charm (sprite) ]
    0x1026EE,
    0x1026FB,
    # [ Animation Script $01DE: Mirager (sprite) ]
    0x102791,
    0x102795,
    # [ Animation Script $01DC: SabreSoul (bg1) ]
    0x1027D3,
    0x1027DA,
    # [ Animation Script $01CD: Back Blade (bg3) ]
    0x1028D3,
    0x1028DF,
    # [ Animation Script $01CA: RoyalShock (bg1) ]
    0x102967,
    0x10296B,
    0x102973,
    # [ Animation Script $01C1:  ]
    0x102AAD,
    0x102AB1,
    # [ Animation Script $01B8: Absolute 0 (bg1) ]
    0x102BF4,
    0x102BF8,
    0x102C10,
    # [ Animation Script $01B7: Overcast (bg1) ]
    0x102C3A,
    0x102C55,
    0x102C8D,
    0x102C91,
    # [ Animation Script $01B5: Disaster (bg1) ]
    0x102CEE,
    0x102CF2,
    0x102D19,
    # [ Animation Script $01B1: Force Field (bg3) ]
    0x102D3A,
    0x102D48,
    0x102D64,
    # [ Animation Script $01AF: Event Animation $00: Terra/Tritoch Lightning (bg1) ]
    0x102E05,
    0x102E09,
    0x102E24,
    # [ Animation Script $01AD: S. Cross (bg1) ]
    0x102EDA,
    0x102EDE,
    0x102FA8,
    0x102FB1,
    0x102FBE,
    0x102FD9,
    # [ Animation Script $01AB: Mind Blast (bg3) ]
    0x102FED,
    0x102FF1,
    0x102FF7,
    0x102FF9,
    0x102FFF,
    0x103001,
    0x103007,
    0x10300D,
    0x103015,
    0x10301F,
    # [ Animation Script $01A8:  ]
    0x1030CA,
    0x1030CE,
    # [ Animation Script $01A5: Flare Star (bg1) ]
    #0x1030F5,
    #0x103106,
    #0x10310D,
    #0x103123,
    #0x10312E,
    # [ Animation Script $01A0: Quasar (bg1) ]
    0x1031D2,
    0x1031D6,
    0x1031FA,
    # [ Animation Script $019A: R.Polarity (bg1) ]
    0x10328B,
    0x103292,
    # [ Animation Script $0192: Rippler (sprite) ]
    0x1033C6,
    0x1033CA,
    # [ Animation Script $018B: Step Mine (sprite) ]
    0x1034D9,
    0x1034E0,
    # [ Animation Script $0190: L.4 Flare (extra) ]
    0x103585,
    0x10358C,
    0x10359A,
    # [ Animation Script $0185: L.5 Doom (sprite) ]
    0x1035E6,
    0x1035F6,
    # [ Animation Script $0178: Megazerk (bg1) ]
    0x103757,
    0x103761,
    0x10378F,
    0x103795,
    0x10379B,
    0x1037A1,
    0x1037A7,
    0x1037AD,
    0x1037B3,
    0x1037B9,
    0x1037C0,
    # [ Animation Script $0176: Schiller (sprite) ]
    0x103819,
    0x10381D,
    # [ Animation Script $016E: WallChange (sprite) ]
    0x10399E,
    0x1039A3,
    0x1039A9,
    0x1039AF,
    0x1039B5,
    0x1039BB,
    0x1039C1,
    0x1039C7,
    0x1039CD,
    0x1039D4,
    # [ Animation Script $0169:  ]
    0x103AEA,
    0x103AED,
    0x103AF0,
    0x103AF3,
    0x103AF6,
    0x103AF9,
    0x103AFC,
    0x103AFF,
    0x103B02,
    # [ Animation Script $0161: Exploder (bg3) ]
    0x103BC3,
    0x103BC9,
    0x103BCC,
    0x103BDD,
    # [ Animation Script $0137: Plasma (sprite) ]
    0x104426,
    0x10442A,
    0x10443A,
    # [ Animation Script $0125: Sun Bath (extra) ]
    0x10494C,
    0x104950,
    0x10495A,
    # [ Animation Script $0122: Moon Song (sprite) ]
    0x1049B1,
    0x1049B9,
    0x1049D5,
    # [ Animation Script $011A: Chaos Wing (bg1) ]
    0x104ACE,
    0x104AD5,
    0x104AFA,
    # [ Animation Script $0119: Sun Flare (bg1) ]
    0x104C60,
    0x104C6B,
    0x104C77,
    0x104C7C,
    # [ Animation Script $010C: Heal Horn (bg1) ]
    0x104DAF,
    0x104DCA,
    0x104DDE,
    # [ Animation Script $010A: Life Guard (bg1) ]
    0x104E27,
    0x104E4A,
    0x104E64,
    # [ Animation Script $0102: Hope Song (bg3) {Siren}]
    0x10504B,
    0x10507B,
    0x1050FB,
    # [ Animation Script $0100: Gem Dust (sprite) {Shiva}]
    0x105223,
    0x10523C,
    0x10524A,
    0x10524F,
    # [ Animation Script $00FD: Bolt Fist (sprite) {Ramuh}]
    0x1052CE,
    0x1052EC,
    0x105302,
    # [ Animation Script $00F6: Sea Song (bg1) ]
    0x105312,
    0x10531E,
    0x105353,
    # [ Animation Script $00F5: Earth Aura (sprite) ]
    0x105432,
    0x105438,
    0x105444,
    # [ Animation Script $0252: Demon Eye (sprite) {Shoat}]
    0x105455,
    0x105477,
    0x105481,
    # [ Animation Script $00EF: Inferno (bg1) {Ifrit}]
    0x1055F0,
    0x1055FC,
    0x105601,
    0x105606,
    0x10560B,
    0x10565C,
    # [ Animation Script $00E7: Ultima (bg1) ]
    0x1056CB,
    0x1056CF,
    0x1056ED,
    0x1056F5,
    # [ Animation Script $00D7: Flare (sprite) ]
    0x1057AD,
    0x1057B1,                      
    0x1057DD,
    # [ Animation Script $00EA: Bolt 3, Giga Volt (sprite) ]
    0x10588E,
    0x105893,
    0x105896,
    0x105899,
    0x10589C,
    0x1058A1,
    0x1058A6,
    0x1058AB,
    0x1058B0,
    # [ Animation Script $00D9: Merton (bg3) ]
    0x1059EF,
    0x105A08,
    0x105A1C,
    # [ Animation Script $00D2: X-Zone (bg3) ]
    0x105A5D,
    0x105A6A,
    0x105A79,              
    # [ Animation Script $00CF: Meteor (bg1) ]
    0x105AF7,
    0x105AFB,
    0x105B17,
    # [ Animation Script $00BF: Dispel (bg1) ]
    0x105DC2,
    0x105DC9,
    0x105DD2,
    0x105DDB,
    0x105DE4,
    0x105DED,
    # [ Animation Script $00AA: Muddle, L.3 Muddle, Confusion (sprite) ]
    0x1060EA,
    0x1060EE,
    # [ Animation Script $0081: Shock (bg1) ]
    0x1068BE,
    0x1068D0,
    # [ Animation Script $0070: Spiraler (bg1) ]
    0x106B8A,
    0x106B8F,
    0x106BF4,
    # [ Animation Script $006F: Bum Rush (sprite) ]
    0x106C3E,
    0x106C47,
    0x106C53,
    0x106C7E,
    0x106C87,
    0x106C95,
    0x106C9E,
    # [ Animation Script $006B: Fire Dance (bg1) ]
    #0x106D83,
    #0x106D89,
    #0x106DB5,
    # [ Animation Script $01D7: Empowerer (bg1) ]
    0x106FA2,
    0x106FA8,
    0x106FB9,
    0x106FC0,
    0x106FC8,
    # [ Animation Script $01D6: Stunner (sprite) ]
    0x1071BA,
    0x1071C1,
    0x1071CA,
    0x1071D5,
    0x1071DE,
    0x1071E9,
    0x1071F2,
    0x1071FD,
    0x107206,
    0x107211,
    0x10721A,
    0x10725A,
    # [ Animation Script $01D3: Quadra Slam, Quadra Slice (sprite) ]
    0x1073DC,
    0x1073EE,
    0x1073F3,
    0x107402,
    0x107424,
    0x107429,
    0x107436,
    0x107458,
    0x10745D,
    0x107490,
    0x1074B2,
    0x1074B7,
    # [ Animation Script $01D1: Slash (sprite) ]
    0x1074F4,
    0x1074FD,
    0x107507,
    # [ Animation Script $0052: Flash (sprite) ]
    0x107850,
    0x10785C
]