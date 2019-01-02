#!/usr/bin/env python3

import sys
import struct

if len(sys.argv) < 3:
    print("Usage: checksum.py <binary file> <load offset>")
    exit(1)

with open(sys.argv[1], "rb") as f:
    memory = [None] * 64*1024
    fdata = f.read()
    addr = int(sys.argv[2], 16)
    while len(fdata) > 0:
        val = struct.unpack('>H', fdata[:2])[0]
        memory[addr] = val
        fdata = fdata[2:]
        addr += 1

for addr in range(0,0x10000,0x400):
    if memory[addr] is None or memory[addr] != 0xffff:
        continue
    sys.stdout.write("{:04x}: ".format(addr))
    r6 = 0
    r7 = 0
    for off in range(0x400):
        val = memory[addr+off]
        r7 = (r7 + (val & 0xff)) & 0xffff
        r6 = (r6 + (val >> 8)) & 0xffff
    r0 = memory[addr+2]
    r5 = memory[addr+3]
    r5 = ((r5 << 8) | (r5 >> 8)) & 0xffff
    tmp = r0 & 0xff
    r0 = (r0 & 0xff00) | (r5 & 0xff)
    r5 = (r5 & 0xff00) | tmp
    r4 = r0
    r0 = (r0 + (r4 >> 8)) & 0xffff
    r0 = (r0 + (r4 & 0xff)) & 0xffff
    r4 = r5
    r4 = ((r4 << 8) | (r4 >> 8)) & 0xffff
    r4 = (r4 + (r5 >> 8)) & 0xffff
    r4 = (r4 + (r5 & 0xff)) & 0xffff
    if r6 == r0 and r7 == r4:
        print("pass")
    else:
        print("fail")
