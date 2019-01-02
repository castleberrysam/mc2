#!/usr/bin/env python3

import math

class Instruction:
    opMasks = [
        # Opcode      Mask    Value
        ("AND",       0xf800, 0x0000),
        ("RBIT",      0xf800, 0x0800),
        ("OR",        0xf800, 0x1000),
        ("SBIT",      0xf800, 0x1800),
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

    statusTable = [
        "PRI0",
        "PRI1",
        "PRI2",
        "ZL",
        "NL",
        "5",
        "6",
        "I",
        "8",
        "9",
        "10",
        "Z",
        "N",
        "C",
        "O",
        "15"
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
    
    def __init__(self, memory, subs, addr, data=False):
        self.data = memory[addr]
        self.imm = None
        self.size = 2
        if data:
            self.op = "DATA"
            return
        
        self.op = Instruction.decodeOp(self.data)
        if Instruction.hasImmediate(self.op):
            self.imm = memory[addr+1]
            self.size += 2
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
            self.indirect = (self.data & 0x0800) != 0
            self.cc = Instruction.decodeCC(self.data >> 8)
            self.imm = (addr & 0xff00) | (self.data & 0x00ff)
            if self.indirect:
                self.imm = memory[self.imm]
            self.target = "{:04x}".format(self.imm)
            if self.target in subs:
                self.target = subs[self.target]
                #print("Found call to sub {}".format(self.target), file=sys.stderr)
            else:
                self.target = "0x" + self.target
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
            self.bitNum = 15 - ((self.data >> 4) & 0x000f)
            self.src = self.data & 0x000f
        elif self.op == "PUSH":
            self.src = self.data & 0x0007
        elif self.op == "POP":
            self.dst = self.data & 0x0007
        elif self.op == "HALT":
            raise NotImplementedError

    @staticmethod
    def getVariable(variables, addr):
        addr_str = "{:04x}".format(addr)
        if addr_str in variables:
            return variables[addr_str]
        return "0x" + addr_str

    def __str__(self, dot=False, variables={}):
        if self.op == "LOAD_LONG":
            if self.indexed:
                return "{} R{} = {}(R{}{})".format(self.op[:4], self.dst, Instruction.getVariable(variables, self.imm), self.src, ", " + self.fd if (self.fd != "NOP") else "")
            else:
                return "{} R{} = ({})".format(self.op[:4], self.dst, Instruction.getVariable(variables, self.imm))
        elif self.op == "STOR_LONG":
            if self.indexed:
                return "{} {}(R{}{}) = R{}".format(self.op[:4], Instruction.getVariable(variables, self.imm), self.src, ", " + self.fd if (self.fd != "NOP") else "", self.dst)
            else:
                return "{} ({}) = R{}".format(self.op[:4], Instruction.getVariable(variables, self.imm), self.dst)
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
            return "{} {}{}".format(self.op, self.target, " IF " + self.cc if (self.cc != "TRUE") else "")
        elif self.op == "RTN" or self.op == "STRB" or self.op == "ADDC" or self.op == "NEG" or self.op == "CMPL" or self.op == "POP":
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
            if self.src == 1:
                bit = Instruction.statusTable[self.bitNum]
            else:
                bit = str(self.bitNum)
            return "{} R{}, R{}({})".format(self.op, self.dst, self.src, bit)
        elif self.op == "HALT":
            return "{}".format(self.op)
        elif self.op == "COP":
            return "{} 0x{:04x}".format(self.op, self.data)
        else:
            return "0x{:04x}".format(self.data) if dot else ".word 0x{:04x}".format(self.data)
    
    def dotStr(self, variables={}):
        return self.__str__(True, variables)

class MathInstruction:
    binOps = [
        "NOP",
        "FADD",
        "FSUB",
        "FMUL",
        "FDIV",
        "FRDIV",
        "FCMP",
        "ADD",
        "SUB",
        "LOAD",
        "LOAD.ITF",
        "LOAD.FTI",
        "STOR",
        "STOR.ITF",
        "STOR.FTI"
    ]

    unOps = [
        "NOP",
        "ITF",
        "FTI",
        "FABS",
        "NEG",
        "ABS"
    ]

    @staticmethod
    def toFloat(high, low):
        sign = "-" if ((high & 0x8000) != 0) else ""
        if ((high & 0x7fff) == 0) and low == 0:
            return sign + "0.0e0"
        if ((high & 0x7fff) == 0x7fff) and low == 0xffff:
            return sign + "inf"
        exp = ((high >> 6) & 0x1ff) - 256
        frac = ((((high & 0x3f) | 0x40) << 16) | low)
        val = frac * (2**(exp-22))
        return "{}{:0.7g}".format(sign, val)
    
    def __init__(self, memory, addr):
        self.data = memory[addr]
        addr += 1

        if (self.data & 0xf000) != 0:
            self.op = MathInstruction.binOps[(self.data & 0xf000) >> 12]
            self.bank = "R2:" if ((self.data & 0x0200) == 0) else "R3:"
            self.offset = "{:03x}".format((self.data & 0x1ff) - 0x20)
            self.size = 2
            self.end = (self.data >> 10) & 3
        elif (self.data & 0x0100) != 0:
            self.op = MathInstruction.binOps[(self.data & 0xf0) >> 4]
            self.bank = "R6:" if ((self.data & 0x0200) == 0) else "R3:"
            self.offset = "{:01x}".format(self.data & 0xf)
            self.size = 2
            self.end = (self.data >> 10) & 3
        elif (self.data & 0x00f0) != 0:
            self.op = MathInstruction.binOps[(self.data & 0xf0) >> 4]
            self.bank = ""
            if self.op in ["FADD","FSUB","FMUL","FDIV","FRDIV","FCMP","LOAD.FTI","STOR.FTI"]:
                self.offset = MathInstruction.toFloat(memory[addr], memory[addr+1])
            else:
                self.offset = "{:04x}{:04x}".format(memory[addr], memory[addr+1])
                if self.op in ["LOAD","STOR"]:
                    self.offset += " ({})".format(MathInstruction.toFloat(memory[addr], memory[addr+1]))
            addr += 2
            self.size = 6
            self.end = ((self.data >> 10) | (self.data >> 2)) & 3
        else:
            self.op = MathInstruction.unOps[self.data & 0xf]
            self.bank = ""
            self.offset = ""
            self.size = 2
            self.end = (self.data >> 10) & 3

        if self.end > 1:
            self.op += " B"
        if self.end == 3:
            self.op = "P{},{} {}".format(memory[addr] >> 8, memory[addr] & 0xff, self.op)
            addr += 1
            self.size += 2

    def __str__(self):
        return ".M({:04x}) {} {}{}".format(self.data, self.op, self.bank, self.offset)

    def dotStr(self, variables={}):
        return self.__str__()
    
class BasicBlock:
    @staticmethod
    def numInsns(bblock, length):
        count = 0
        while length > 0 and count < len(bblock.instructions):
            length -= bblock.instructions[count].size
            count += 1
        if length != 0:
            print("***Warning*** The bblock at addr {:04x} might be split incorrectly".format(bblock.addr), file=sys.stderr)
        return count
    
    def __init__(self, memory, subs, tbls, lnks, datas, mathfuncs, bblocks, addr, isSub=False, isMath=False):
        self.addr = addr
        self.size = 0
        self.instructions = []
        self.jumpTable = []
        
        self.isSub = isSub
        addr_str = "{:04x}".format(addr)
        if addr_str in subs:
            self.isSub = True
            self.name = subs[addr_str]
        else:
            self.name = "bb_" + addr_str

        if addr_str in lnks:
            print("Inserting manual links at addr {}".format(addr_str), file=sys.stderr)
            for case in lnks[addr_str]:
                self.jumpTable.append(case)
        
        for bb_addr, bblock in bblocks.items():
            if bblock == None:
                continue
            bb_end = bb_addr + (bblock.size // 2)
            if bblock != None and bb_addr < addr and bb_end > addr:
                #print("Splitting existing bblock: {:04x}".format(addr), file=sys.stderr)
                self.call = bblock.call
                bblock.call = False
                self.trueBranch = bblock.trueBranch
                self.falseBranch = bblock.falseBranch
                bblock.trueBranch = addr
                bblock.falseBranch = None
                self.size = bblock.size
                bblock.size = (addr - bb_addr) * 2
                self.size -= bblock.size
                numInsns = BasicBlock.numInsns(bblock, bblock.size)
                self.instructions = bblock.instructions[numInsns:]
                bblock.instructions = bblock.instructions[:numInsns]
                self.isSub = bblock.isSub
                self.isMathCall = bblock.isMathCall
                bblock.isMathCall = False
                return
        
        self.trueBranch = None
        self.falseBranch = None
        insn = None
        while True:
            if isMath:
                insn = MathInstruction(memory, addr)
                if insn.end != 0:
                    isMath = False
            else:
                insn = Instruction(memory, subs, addr, addr in datas)
            self.instructions.append(insn)
            self.size += insn.size
            addr += insn.size // 2
            if insn.op in ["BR","IBR","CALL","RTN","CBR"]:
                break
            if addr in bblocks:
                #print("Encountered existing bblock: {:04x}".format(addr), file=sys.stderr)
                self.trueBranch = addr
                break
        
        self.call = insn.op == "CALL"
        self.isMathCall = self.call and insn.imm in mathfuncs
        if insn.op == "CALL" or insn.op == "CBR":
            self.trueBranch = insn.imm if insn.cc != "FALSE" else None
            self.falseBranch = addr if (insn.cc != "TRUE" or insn.op == "CALL") else None
        elif insn.op == "IBR":
            addr_str = "{:04x}".format(addr-1)
            if addr_str in tbls:
                numCases = tbls[addr_str]
                print("Identified jump table {} with length {}".format(addr_str, numCases), file=sys.stderr)
            else:
                sys.stderr.write("How many cases in table for IBR at addr {}?: ".format(addr_str))
                numCases = int(input())
            self.jumpTable.extend(memory[addr:addr+numCases])

    def __str__(self, dot=False, variables={}):
        string = ""
        for instruction in self.instructions:
            string += "{}\\l".format(instruction.dotStr(variables)) if dot else "{}\n".format(str(instruction))
        return string

    def dotStr(self, variables={}):
        return self.__str__(True, variables)

class Program:
    def __init__(self, memory, subs, tbls, lnks, ulnks, datas, mathfuncs, variables, omits, addr):
        self.memory = memory
        self.subs = subs
        self.tbls = tbls
        self.lnks = lnks
        self.datas = datas
        self.ulnks = ulnks
        self.mathfuncs = mathfuncs
        self.variables = variables
        self.omits = omits
        self.bblocks = {}
        self.parseBlocks(addr)

    def shouldLink(self, addr1, addr2):
        addr1_str = "{:04x}".format(addr1)
        if addr1_str in self.ulnks and addr2 in self.ulnks[addr1_str]:
            print("Manually unlinking at addr {}".format(addr1_str), file=sys.stderr)
            return False
        return True

    def parseBlocks(self, addr, isSub=False, isMath=False):
        if addr in self.bblocks:
            #print("Block at {:04x} was already parsed".format(addr), file=sys.stderr)
            return
        if addr in self.omits:
            print("Omitting block at {:04x}".format(addr), file=sys.stderr)
            self.bblocks[addr] = None
            return
        if self.memory[addr] == None:
            print("Block at {:04x} is outside of known memory space".format(addr), file=sys.stderr)
            self.bblocks[addr] = None
            return
        #print("Parsing block at addr {:04x}".format(addr), file=sys.stderr)
        bblock = BasicBlock(self.memory, self.subs, self.tbls, self.lnks, self.datas, self.mathfuncs, self.bblocks, addr, isSub, isMath)
        if not self.shouldLink(addr, bblock.trueBranch):
            bblock.trueBranch = None
        if not self.shouldLink(addr, bblock.falseBranch):
            bblock.falseBranch = None
        self.bblocks[addr] = bblock
        if bblock.trueBranch != None:
            self.parseBlocks(bblock.trueBranch, bblock.isSub and not bblock.call, False)
        if bblock.falseBranch != None:
            self.parseBlocks(bblock.falseBranch, bblock.isSub, bblock.isMathCall)
        for case in bblock.jumpTable:
            self.parseBlocks(case, bblock.isSub, False)

    def addLink(self, string, addr1, addr2, color):
        if addr2 is None:
            return string
        return string + "    bb_{:04x} -> bb_{:04x} [color=\"{}\"];\n".format(addr1, addr2, color)

    def __str__(self, dot=False):
        string = ""
        if dot:
            string += "digraph program {\n"
            for addr, bblock in self.bblocks.items():
                isSub = bblock and bblock.isSub
                name = bblock.name if bblock else "bb_{:04x}".format(addr)
                string += "    bb_{:04x} [shape=box,{}fontname=\"Courier New\",label=\"{}:\\l{}\"];\n".format(addr, "style=filled,fillcolor=yellow," if isSub else "", name, bblock.dotStr(variables) if (bblock != None) else "<unknown>")
            string += "\n"
            for addr, bblock in self.bblocks.items():
                if bblock == None:
                    continue
                if not bblock.call:
                    string = self.addLink(string, addr, bblock.trueBranch, "green" if bblock.falseBranch else "black")
                string = self.addLink(string, addr, bblock.falseBranch, "black" if bblock.call else "red")
                for case in bblock.jumpTable:
                    string = self.addLink(string, addr, case, "purple")
            string += "}"
        else:
            string += "\t.section program, \"rx\"\n"
            for addr, bblock in sorted(self.bblocks.items()):
                if bblock is None:
                    continue
                string += "\n\t.org 0x{:04x}".format(addr)
                string += "\n\t{}".format(str(bblock).replace("\n", "\n\t"))
        return string

    def dotStr(self):
        return self.__str__(True)

if __name__ == "__main__":
    import sys
    if(len(sys.argv) < 5):
        print("Usage: visualize.py <binary file> <load offset> <parse offset> <annotation file>")
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

    subs = {}
    tbls = {}
    lnks = {}
    ulnks = {}
    datas = []
    mathfuncs = []
    variables = {}
    omits = []
    with open(sys.argv[4], "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 1:
                continue
            if parts[0] == "sub":
                subs[parts[1]] = parts[2]
            elif parts[0] == "table":
                tbls[parts[1]] = int(parts[2])
            elif parts[0] == "link":
                if parts[1] not in lnks:
                    lnks[parts[1]] = []
                lnks[parts[1]].append(int(parts[2], 16))
            elif parts[0] == "unlink":
                if parts[1] not in ulnks:
                    ulnks[parts[1]] = []
                ulnks[parts[1]].append(int(parts[2], 16))
            elif parts[0] == "data":
                addr = int(parts[1], 16)
                for i in range(int(parts[2])):
                    datas.append(addr)
                    addr += 1
            elif parts[0] == "mathfunc":
                mathfuncs.append(int(parts[1], 16))
            elif parts[0] == "var":
                variables[parts[1]] = parts[2]
            elif parts[0] == "omit":
                omits.append(int(parts[1], 16))
            
    program = Program(memory, subs, tbls, lnks, ulnks, datas, mathfuncs, variables, omits, int(sys.argv[3], 16))
    print(program.dotStr())
