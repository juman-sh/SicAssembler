from main import proglen, startaddress, SYMTAB, opttab, dire
from builtins import str
from nt import write
import struct

objpgm = open("ObjectProgram.lst", "w")
inter = open("intmdte_file.mdt", "r")
objcode = open("ObjectCode.obj", "w+")


f = ""
f1 = ""
l = []
addrlist = []
assembly = inter.readlines()
fline = assembly[0]
for line in assembly:
    ls = line
    opcode = ls[21:30].strip()
    address = ls[0:5].strip()

    if opcode != "START":
        addrlist.append(address)

    label = ls[10:20].strip()
    operand = ls[32:40].strip()
    if opcode == "START":
        addrlist.append(ls[0:5].strip())
        objpgm.write("H^" + label+"  " + "^00" + ls[0:5].strip().upper() + "^00" + proglen.upper())
        l.append("")
    elif opcode == "END":
        l.append("")
    else:
        if opcode in opttab.keys() or opcode in dire:

            op = opcode
            if op == "RSUB":
                code = opttab[opcode[0:]]
                op = code + "0000"
                l.append(op)
                objcode.write(op)
                objcode.write("\n")

            elif opcode not in dire and ",X" not in operand:
                code = opttab[opcode[0:]]
                if operand in SYMTAB.keys():
                    sym = SYMTAB[operand[0:]]
                    objcode.write(code + sym)
                    objcode.write("\n")
                    l.append(code + sym)

            elif operand[-2:] == ",X":
                opend = operand[:-2]
                if opend in SYMTAB.keys():
                    first = SYMTAB[opend][0:1]
                    sec = SYMTAB[opend[0:]]
                    value4 = hex(int(bin(int(1))[-1:] + "00" + bin(int(first))[2:]))[-1:]
                    op = opttab[opcode[0:]] + value4 + (sec[1] + sec[2] + sec[3])
                    objcode.write(op)
                    objcode.write("\n")
                    l.append(op)

            elif opcode == "RESW" or opcode == "RESB":
                l.append("")

            elif opcode == "WORD":
                code = hex(int(operand))
                code1 = str(code)
                code1 = code1[2:]
                if len(code1) < 6:
                    for i in range(6 - len(code1)):
                        code1 = "0" + code1
                objcode.write(code1)
                objcode.write("\n")
                l.append(code1)

            elif opcode == "BYTE":
                temp = operand[2:len(operand) - 1]
                if "X'" in operand:
                    objcode.write(temp)
                    objcode.write("\n")
                    l.append(temp)

                elif "C'" in operand:
                    for i in temp:
                        hexcode = hex(ord(i))[2:]
                        objcode.write(str(hexcode))
                        f += hexcode
                    l.append(f)
                    objcode.write("\n")

                else:
                   l.append("")

i = 1

while i < len(l):
    if i == 1:
        addr = addrlist[1]
    else:
        addr = addrlist[i]
    cont = 0
    if l[i] != "":
        objpgm.write("\nT^00" + addr.upper() + "^")
        pointer = objpgm.tell()
        objpgm.write("  ")
        j = i
        while j < len(l) and l[j] != "" and cont < 10:
            objpgm.write("^" + l[j].upper())
            cont += 1
            j += 1
        i = j - 1
        objpgm.seek(pointer)
        tempaddr = str(int(addrlist[i], 16) - int(addr, 16) + int(3))
        tempaddr1 = hex(int(tempaddr))
        taddr = tempaddr1[2:4]
        if len(taddr) == 1:
            taddr = "0" + taddr
        if taddr == "03":
            taddr = "01"
        objpgm.write(taddr.upper())
        objpgm.seek(0, 2)

    i += 1
objpgm.write("\n" + "E" + "^00" + str(hex(startaddress))[2:])
objpgm.close()
inter.close()
objcode.close()