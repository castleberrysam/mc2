#!/usr/bin/env python3

import sys
import struct

def read8(memory, base, off):
    addr = base + (off // 2)
    if off & 1:
        return memory[addr] & 0xff
    else:
        return memory[addr] >> 8

def showAllObjects(memory):
    for addr in range(0,0x10000,0x400):
        if memory[addr] is None or memory[addr] != 0xffff:
            continue
        numObjs = memory[addr+5] & 0xff
        for i in range(numObjs):
            objInfo = memory[addr+6+i]
            objType = objInfo >> 10
            objAddr = addr + (objInfo & 0x3ff)
            print("type {} addr {:04x}".format(objType, objAddr))
            if objType == 0:
                objLen = 6
            elif objType == 1:
                objLen = 11
            elif objType == 2:
                objLen = 20 # don't know
            else:
                objLen = 6
            for i in range(objLen):
                print(" {:04x}".format(memory[objAddr+i]))

def findStrByID(memory, myObjID, myStrID):
    myTblAddr = 0
    for addr in range(0,0x10000,0x400):
        if memory[addr] is None or memory[addr] != 0xffff:
            continue
        numObjs = memory[addr+5] & 0xff
        for i in range(numObjs):
            objInfo = memory[addr+6+i]
            objType = objInfo >> 10
            if objType != 1:
                continue
            objAddr = addr + (objInfo & 0x3ff)
            objID = memory[objAddr]
            if (objID & 0xff) != (myObjID & 0xff):
                continue
            if (objID >> 8) < (myObjID >> 8):
                continue
            tblAddr = memory[objAddr+5]
            if tblAddr == 0x0000:
                continue
            myObjID = objID
            myTblAddr = tblAddr
    if myTblAddr == 0:
        return (0,0,0)
    tblMax = memory[tblAddr+1] & 0xff
    if myStrID > tblMax:
        return (0,0,0)
    strBase = memory[tblAddr]
    strStart = read8(memory, tblAddr+2, myStrID)
    strEnd = read8(memory, tblAddr+2, myStrID+1)
    return (strBase,strStart,strEnd-strStart)

def getStr(memory, addr, offset=0, length=-1):
    if addr == 0:
        return "<none>"

    res = ""
    flag = False
    inhibit = False
    objID = 0
    i = 0
    while i != length:
        char = read8(memory, addr, offset+i)
        i += 1
        if char == 0xff:
            break
        if char == 0xfe:
            inhibit = True
            continue
        if char == 0xfd:
            inhibit = False
            continue
        if char >= 0xe0:
            continue
        if char >= 0xc0:
            objID = char - 0xc0
            continue
        if char >= 0x80:
            if flag and not inhibit:
                res += " "
            flag = False
            strAddr,strOff,strLen = findStrByID(memory, objID, char - 0x80)
            res += getStr(memory, strAddr, strOff, strLen)
            if not inhibit:
                res += " "
            continue
        res += chr(char)
        flag = True
    return res

def loadFile(memory, fname, offset=0):
    with open(fname, "rb") as f:
        fdata = f.read()
        while len(fdata) > 0:
            val = struct.unpack('>H', fdata[:2])[0]
            memory[offset] = val
            fdata = fdata[2:]
            offset += 1

def main():
    if len(sys.argv) < 4:
        print("Usage: getstring.py <binary file> <load offset> <obj ID> [string ID]")
        print("       getstring.py <binary file> <load offset> <fmt string addr>")
        exit(1)

    memory = [None] * 64*1024
    loadFile(memory, sys.argv[1], int(sys.argv[2], 16))

    if len(sys.argv) > 4:
        myObjID = int(sys.argv[3], 16)
        myStrID = int(sys.argv[4], 16)
        strAddr,strOff,strLen = findStrByID(memory, myObjID, myStrID)
        print(getStr(memory, strAddr, strOff, strLen))
    elif len(sys.argv[3]) == 2:
        myObjID = int(sys.argv[3], 16)
        for myStrID in range(0x100):
            strAddr,strOff,strLen = findStrByID(memory, myObjID, myStrID)
            if strAddr == 0:
                break
            print(getStr(memory, strAddr, strOff, strLen))
    else:
        print(getStr(memory, int(sys.argv[3], 16)))

if __name__ == "__main__":
    main()
