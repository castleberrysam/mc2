#!/usr/bin/env python3

class Instruction:
    opMasks = [
        # Opcode      Mask    Value
        ("AND",       0xf800, 0x0000),
        ("SBIT",      0xf800, 0x0800),
        ("OR",        0xf800, 0x1000),
        ("RBIT",      0xf800, 0x1800),
        ("CMPR",      0xf800, 0x2000),
        ("TBIT",      0xf800, 0x2800),
        ("XOR",       0xf800, 0x3000),
        ("CBIT",      0xf800, 0x3800),
        ("BR",        0xff00, 0x4000),
        ("IBR",       0xff00, 0x4800),
        ("MOVE",      0xf000, 0x5000),
        ("ADDI",      0xf800, 0x6000),
        ("SUBI",      0xf800, 0x6800),
        ("ADD",       0xf800, 0x7000),
        ("SUBR",      0xf800, 0x7800),
        ("CBR",       0xf000, 0x8000),
        ("CALL",      0xf000, 0x9000),
        ("CMPRI",     0xf800, 0xa000),
        ("PUSH",      0xfff8, 0xb000),
        ("RTN",       0xfff8, 0xb100),
        ("ADDC",      0xfff8, 0xb220),
        ("CMPL",      0xfff8, 0xb300),
        ("NEG",       0xfff8, 0xb330),
        ("STRB",      0xfff8, 0xb400),
        ("SHFTR",     0xffc8, 0xb540),
        ("LDRB",      0xff08, 0xb600),
        ("SHFTL",     0xffc8, 0xb700),
        ("LDWI",      0xfff8, 0xb800),
        ("POP",       0xfff8, 0xb900),
        ("LOAD_LONG", 0xf800, 0xc000),
        ("LOAD",      0xf8f8, 0xc800),
        ("STOR_LONG", 0xf800, 0xd000),
        ("STOR",      0xf8f8, 0xd800),
        ("LDBI",      0xf000, 0xe000),
        ("COP",       0xf000, 0xf000)
    ]

    fdTable = [
        "SWB",
        "LJL",
        "NOP",
        "LJU",
        "RJU",
        "UNKNOWN_5",
        "RJL",
        "UNKNOWN_7",
        "UNKNOWN_8",
        "UNKNOWN_9",
        "UNKNOWN_10",
        "UNKNOWN_11",
        "RJ0",
        "RJ1",
        "RJ2",
        "RJ3"
    ]

    ccTable = [
        "FALSE",
        "G",
        "E",
        "GE",
        "L",
        "LG",
        "LE",
        "TRUE"
    ]

    @staticmethod
    def decodeOp(data):
        for op, mask, val in Instruction.opMasks:
            if (data & mask) == val:
                return op
        return "UNKNOWN"

    @staticmethod
    def decodeFD(data):
        return Instruction.fdTable[data & 0x000f]

    @staticmethod
    def decodeCC(data):
        return Instruction.ccTable[data & 0x0007]

    @staticmethod
    def hasImmediate(op):
        return op == "LOAD_LONG" or op == "STOR_LONG" or op == "LDWI"
    
    def __init__(self, op, data, imm=None):
        self.op = op
        self.data = data
        self.imm = imm
        self.size = 2 if (self.imm == None) else 4
        if self.op == "LOAD_LONG" or self.op == "STOR_LONG":
            self.fd = Instruction.decodeFD(self.data >> 4)
            self.indexed = (self.data & 0x0008) != 0
            self.src = (self.data >> 8) & 0x0007
            self.dst = self.data & 0x0007
        elif self.op == "LOAD" or self.op == "STOR":
            self.src = (self.data >> 8) & 0x0007
            self.dst = self.data & 0x0007
        elif self.op == "LDWI" or self.op == "RTN":
            self.dst = self.data & 0x0007
        elif self.op == "LDBI":
            self.dst = (self.data >> 8) & 0x000f
            self.imm = self.data & 0x00ff
        elif self.op == "ADDI" or self.op == "SUBI":
            self.dst = (self.data >> 8) & 0x0007
            self.imm = self.data & 0x00ff
        elif self.op == "CMPRI":
            self.dst = (self.data >> 8) & 0x000f
            self.imm = self.data & 0x00ff
        elif self.op == "BR" or self.op == "IBR":
            self.src = self.data & 0x0007
            self.fd = Instruction.decodeFD(self.data >> 4)
        elif self.op == "CALL" or self.op == "CBR":
            self.indirect = (data & 0x0800) != 0
            self.cc = Instruction.decodeCC(self.data >> 8)
            self.imm = self.data & 0x00ff
        elif self.op == "MOVE":
            self.dst = (self.data >> 8) & 0x000f
            self.src = self.data & 0x000f
            self.fd = Instruction.decodeFD(self.data >> 4)
        elif self.op == "STRB":
            self.dst = self.data & 0x0007
        elif self.op == "CMPL":
            self.dst = self.data & 0x0007
        elif self.op == "ADDC":
            self.dst = self.data & 0x0007
        elif self.op == "NEG":
            self.dst = self.data & 0x0007
        elif self.op == "LDRB":
            self.src = self.data & 0x0007
            self.fd = Instruction.decodeFD(self.data >> 4)
        elif self.op == "ADD" or self.op == "CMPR" or self.op == "SUBR" or self.op == "AND" or self.op == "OR" or self.op == "XOR":
            self.dst = (self.data >> 8) & 0x0007
            self.fd = Instruction.decodeFD(self.data >> 4)
            self.src = self.data & 0x000f
        elif self.op == "SHFTL":
            self.dst = self.data & 0x0007
            self.flag = (self.data & 0x0020) != 0
            if self.flag ^ ((self.data & 0x0010) != 0):
                self.shiftType = "RRL"
            else:
                self.shiftType = "LSL"
        elif self.op == "SHFTR":
            self.dst = self.data & 0x0007
            self.flag = (self.data & 0x0020) != 0
            if self.flag ^ ((self.data & 0x0010) != 0):
                self.shiftType = "RRR"
            else:
                self.shiftType = "LSR"
        elif self.op == "RBIT" or self.op == "SBIT" or self.op == "CBIT" or self.op == "TBIT":
            self.dst = (self.data >> 8) & 0x0007
            self.bitNum = (self.data >> 4) & 0x000f
            self.src = self.data & 0x000f
        elif self.op == "PUSH":
            self.src = self.data & 0x0007
        elif self.op == "POP":
            self.dst = self.data & 0x0007
        elif self.op == "HALT":
            raise NotImplementedError
    
    def __str__(self, dot=False):
        if self.op == "LOAD_LONG":
            if self.indexed:
                return "{} R{} = 0x{:04x}(R{}{})".format(self.op[:4], self.dst, self.imm, self.src, ", " + self.fd if (self.fd != "NOP") else "")
            else:
                return "{} R{} = (0x{:04x})".format(self.op[:4], self.dst, self.imm)
        elif self.op == "STOR_LONG":
            if self.indexed:
                return "{} 0x{:04x}(R{}{}) = R{}".format(self.op[:4], self.imm, self.src, ", " + self.fd if (self.fd != "NOP") else "", self.dst)
            else:
                return "{} (0x{:04x}) = R{}".format(self.op[:4], self.imm, self.dst)
        elif self.op == "LOAD":
            return "{} R{} = (R{})".format(self.op, self.dst, self.src)
        elif self.op == "STOR":
            return "{} (R{}) = R{}".format(self.op, self.src, self.dst)
        elif self.op == "LDWI":
            return "{} R{} = 0x{:04x}".format(self.op, self.dst, self.imm)
        elif self.op == "LDBI":
            return "{} R{} = 0x{:02x}".format(self.op, self.dst, self.imm)
        elif self.op == "ADDI" or self.op == "SUBI" or self.op == "CMPRI":
            return "{} R{}, 0x{:02x}".format(self.op, self.dst, self.imm)
        elif self.op == "BR" or self.op == "IBR" or self.op == "LDRB":
            return "{} R{}{}".format(self.op, self.src, ", " + self.fd if (self.fd != "NOP") else "")
        elif self.op == "CALL" or self.op == "CBR":
            return "{} 0x{:02x}{}{}".format(self.op, self.imm, ", I" if self.indirect else "", " IF " + self.cc if (self.cc != "TRUE") else "")
        elif self.op == "RTN" or self.op == "STRB"or self.op == "ADDC" or self.op == "NEG" or self.op == "CMPL" or self.op == "POP":
            return "{} R{}".format(self.op, self.dst)
        elif self.op == "PUSH":
            return "{} R{}".format(self.op, self.src)
        elif self.op == "MOVE":
            return "{} R{} = R{}{}".format(self.op, self.dst, self.src, ", " + self.fd if (self.fd != "NOP") else "")
        elif self.op == "ADD" or self.op == "SUBR" or self.op == "AND" or self.op == "OR" or self.op == "XOR" or self.op == "CMPR":
            return "{} R{}, R{}{}".format(self.op, self.dst, self.src, ", " + self.fd if (self.fd != "NOP") else "")
        elif self.op == "SHFTL" or self.op == "SHFTR":
            if self.shiftType == "RRL" or self.shiftType == "RRR":
                flag = ", C" if self.flag else ""
            elif self.shiftType == "LSL" or self.shiftType == "LSR":
                flag = ", 1" if self.flag else ", 0"
            else:
                flag = ""
            return "{} {}, R{}{}".format(self.op, self.shiftType, self.dst, flag)
        elif self.op == "SBIT" or self.op == "RBIT" or self.op == "CBIT" or self.op == "TBIT":
            return "{} R{}, R{}({})".format(self.op, self.dst, self.src, self.bitNum)
        elif self.op == "HALT":
            return "{}".format(self.op)
        elif self.op == "COP":
            return "{} 0x{:04x}".format(self.op, self.data)
        else:
            return "0x{:04x}".format(self.data) if dot else ".word 0x{:04x}".format(self.data)
    
    def dotStr(self):
        return self.__str__(True)

class BasicBlock:
    def __init__(self, memory, addr, bblocks={}):
        self.addr = addr
        self.instructions = []
        for bb_addr, bblock in bblocks.items():
            if bblock != None and bb_addr < addr and (bb_addr+len(bblock.instructions)) > addr:
                print("Splitting existing bblock: {:04x}".format(addr), file=sys.stderr)
                self.call = bblock.call
                bblock.call = True
                self.trueBranch = bblock.trueBranch
                self.falseBranch = bblock.falseBranch
                bblock.trueBranch = None
                bblock.falseBranch = addr
                self.instructions = bblock.instructions[addr-bb_addr:]
                bblock.instructions = bblock.instructions[:addr-bb_addr]
                return
                
        op = ""
        instruction = None
        while op != "BR" and op != "IBR" and op != "CALL" and op != "RTN" and op != "CBR":            
            data = memory[addr]
            op = Instruction.decodeOp(data)
            if Instruction.hasImmediate(op):
                imm = memory[addr+1]
                addr += 2
                instruction = Instruction(op, data, imm)
            else:
                addr += 1
                instruction = Instruction(op, data)
            self.instructions.append(instruction)
            #print("Read instruction (0x{:04x}): {}".format(addr, str(instruction)), file=sys.stderr)
        self.call = op == "CALL"
        self.trueBranch = None
        self.falseBranch = None
        if op == "CALL" or op == "CBR":
            destAddr = ((addr-1)&0xff00)|instruction.imm
            destAddr = memory[destAddr] if instruction.indirect else destAddr
            self.trueBranch = destAddr if instruction.cc != "FALSE" else None
            self.falseBranch = addr if (instruction.cc != "TRUE" or op == "CALL") else None

    def __str__(self, dot=False):
        string = ""
        for instruction in self.instructions:
            string += "{}\\l".format(instruction.dotStr()) if dot else "{}\n".format(str(instruction))
        return string

    def dotStr(self):
        return self.__str__(True)

class Program:
    def __init__(self, memory, addr):
        self.memory = memory
        self.bblocks = {}
        self.parseBlocks(addr)

    def parseBlocks(self, addr):
        if addr in self.bblocks:
            #print("Block at {:04x} was already parsed".format(addr), file=sys.stderr)
            return
        elif self.memory[addr] == None:
            print("Block at {:04x} is outside of known memory space".format(addr), file=sys.stderr)
            self.bblocks[addr] = None
            return
        #print("Parsing block at addr {:04x}".format(addr), file=sys.stderr)
        bblock = BasicBlock(self.memory, addr, self.bblocks)
        self.bblocks[addr] = bblock
        if bblock.trueBranch != None:
            self.parseBlocks(bblock.trueBranch)
        if bblock.falseBranch != None:
            self.parseBlocks(bblock.falseBranch)
    
    def __str__(self, dot=False):
        string = ""
        if dot:
            string += "digraph program {\n"
            for addr, bblock in self.bblocks.items():
                string += "    bb_{:04x} [shape=box,fontname=\"Courier New\",label=\"\\N:\\l{}\"];\n".format(addr, bblock.dotStr() if (bblock != None) else "<unknown>")
            string += "\n"
            for addr, bblock in self.bblocks.items():
                if bblock == None:
                    continue
                if bblock.trueBranch != None:
                    string += "    bb_{:04x} -> bb_{:04x} [color=\"{}\"];\n".format(addr, bblock.trueBranch, "blue" if bblock.call else ("green" if (bblock.falseBranch != None) else "black"))
                if bblock.falseBranch != None:
                    string += "    bb_{:04x} -> bb_{:04x} [color=\"{}\"];\n".format(addr, bblock.falseBranch, "black" if bblock.call else "red")
            string += "}"
        else:
            string += "\t.section program, \"rx\"\n"
            for addr, bblock in self.bblocks.items():
                string += "\n.org {}\n".format(addr)
                string += "\t{}\n".format(str(bblock))
        return string

    def dotStr(self):
        return self.__str__(True)

if __name__ == "__main__":
    import sys
    if(len(sys.argv) < 4):
        print("Usage: visualize.py <binary file> <load offset> <parse offset>")
        exit(1)
    
    import struct
    with open(sys.argv[1], "rb") as f:
        memory = [None] * 64*1024
        fdata = f.read()
        addr = int(sys.argv[2], 16)
        while len(fdata) > 0:
            val = struct.unpack('>H', fdata[:2])[0]
            memory[addr] = val
            fdata = fdata[2:]
            addr += 1
            
    program = Program(memory, int(sys.argv[3], 16))
    print(program.dotStr())
