space = Reserve(0x017D5F, 0x017DCD, "Updated ArmorVil's SwdTech Speed-up patch")
space.write(
	# we start at C17D5F here, or at 0x017D5F in raw hex.
	# we are going to rewrite and optimize the code here so ArmorVil's patch can be used without using any extra free space anywhere in the bank
	asm.LDA(0x07, asm.IMM8),
	asm.SEC(),
	asm.SBC(0x2020, asm.ABS),
	asm.TAX(),
	asm.TDC(),
	asm.TAY(),
	
	"BRANCH_C17D6C",
	asm.LDA(0x02A860, asm.LNG_X),
	asm.STA(0x5DDA, asm.ABS_Y),
	asm.INX(),
	asm.INY(),
	asm.INY(),
	asm.CPY(0x0010, asm.IMM16),
	asm.BNE("BRANCH_C17D6C"),
	
	asm.TDC(),
	asm.TAY(),
	asm.LDA(0x2020, asm.ABS),
	asm.INC(),
	asm.STA(0x36, asm.DIR),
	asm.LDA(0x0E, asm.DIR),
	asm.AND(0x03, asm.IMM8),
	asm.BNE("BRANCH_C17D8D"),
	
	asm.LDA(0x7B82, asm.ABS),
	asm.ADC(0x36, asm.DIR),
	asm.STA(0x7B82, asm.ABS),
	
	"BRANCH_C17D8D",
	asm.LDA(0x7B82, asm.ABS),
	asm.LSR(),
	asm.LSR(),
	asm.LSR(),
	asm.LSR(),
	asm.LSR(),
	asm.CMP(0x36, asm.DIR),
	asm.BNE("BRANCH_C17D9D"),
	
	asm.TDC(),
	asm.STA(0x7B82, asm.ABS),
	
	"BRANCH_C17D9D",
	asm.INC(),
	asm.STA(0x36, asm.DIR),
	asm.TDC(),
	asm.TAX(),
	asm.LDA(0x29, asm.IMM8),
	
	"BRANCH_C17DA4",
	asm.STA(0x5DDA, asm.ABS_X),
	asm.INX(),
	asm.INX(),
	asm.DEC(0x36, asm.DIR),
	asm.BNE("BRANCH_C17DA4"),
	
	asm.LDA(0x7B82, asm.ABS),
	asm.BPL("BRANCH_C17DBF"),
	
	asm.LDA(0xF8, asm.IMM8),
	asm.JSR(0x7DED, asm.ABS),
	asm.LDA(0x7B82, asm.ABS),
	asm.JSR(0x7DCE, asm.ABS),
	asm.BRA("BRANCH_C17DCA"),
	
	"BRANCH_C17DBF",
	asm.JSR(0x7DCE, asm.ABS),
	asm.LDA(0xF0, asm.IMM8),
	asm.JSR(0x7DED, asm.ABS),
	
	"BRANCH_C17DCA",
	asm.INC(0x7B81, asm.ABS),
	asm.RTS(),
	)
)
