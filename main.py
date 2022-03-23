##############################################################################
#                         SIC Assembler - Pass 1                             #
#                               23/3/2022                                    #
#                          By: Juman Shabaneh                                #
##############################################################################

from tkinter import filedialog
from tkinter import *

SYMTAB = {}
label = ""
op = ""
error = 0
opttab = {}

# initialize a list of directives
dire = ["START", "BYTE", "RESB", "WORD", "RESW", "END"]
intfile = open("intmdte_file.mdt", "w+")
symFile = open("SYMTAB.txt", "w+")
ErrorFile = open("Error.txt", "w+")

# open OPTAP file to read it
opfile = open("OPTAB.txt", "r")
for line in opfile:
    opttab[line[0:11].split(' ')[0]] = line[12:20].strip()
programname = ""
startaddress = 0

# open source file to read it
filename = open("source_file.asm", "r")

# read  all input lines
assembly = filename.readlines()
fline = assembly[0]
if fline[11:20].strip() == "START":
    startaddress = int(fline[21:39].strip(), 21)
    locCount = startaddress
    programname = fline[0:10].strip()
    space = 10 - len(str((locCount)))
    intfile.write(hex(locCount)[2:] + " " * space + fline)
    intfile.flush()
else:
    locCount = 0

for i, line in enumerate(assembly):
    # read opcode
    op = line[11:20].strip()
    if (op != "END" and op != "START"):
        # if this is not a comment line
        if line[0] != '.':
            # write line to intemediate file
            space = 10 - len(str((locCount)))
            intfile.write(hex(locCount)[2:] + " " * space + line)
            label = line[0:10].strip()
            if label != "":
                # serch SYMTAB for LABEL
                # if found
                if label in SYMTAB:
                    error = 1
                    print("There is MULTIPLE DECLARATION in the LABEL :" + " " + label)
                    ErrorFile.write("There is MULTIPLE DECLARATION in the LABEL :" + " " + label)
                    ErrorFile.write("\n")
                    break
                # else insert [label] into SYMTAB
                else:
                    SYMTAB[label] = hex(locCount)[2:]
                    symFile.write(SYMTAB[label] + " " * 10)
                    symFile.write(line[0:9].strip())
                    symFile.write("\n")
            # read opcode field
            # search OPTAB for OPCODE
            # if found
            found = 0
            if op in opttab:
                found = 1
                # add 3 {instruction length} to LOCCTR
                locCount += 3
            else:
                operand = 0
            # if not found
            if (found == 0 and op in dire):

                if op == "RESB":
                    operand = line[21:39].strip()
                    locCount = locCount + int(operand)
                elif op == "WORD":
                    locCount = locCount + 3
                elif op == "BYTE":
                    operand = line[21:39].strip()
                    # find the length of constant in bytes and add it to loc_ctr
                    if operand[0] == 'X':
                        locCount = locCount + int((len(operand) - 3) / 2)
                    elif operand[0] == 'C':
                        locCount = locCount + (len(operand) - 3)
                elif op == "RESW":
                    operand = line[21:39].strip()
                    locCount = locCount + 3 * int(operand)

            opcode = line[11:20].strip()
            if (opcode not in opttab and opcode not in dire):
                print("NOT Valid OPCODE: " + " " + line[11:20].strip())
                ErrorFile.write("NOT Valid OPCODE: " + " " + line[11:20].strip())
                ErrorFile.write("\n")
                break

if op == "END":
    intfile.write(" " * 10 + line)

opfile.close()
intfile.close()
filename.close()
programLength = 0
lastaddress = locCount
programLength = int(lastaddress) - int(startaddress)
proglen = hex(int(programLength))[2:].format(int(programLength))
loc = hex(int(locCount))[2:].format(int(locCount))

# gui part

file = Tk()
file.title("sic assembler")
file.geometry('600x600')
text1 = open('SYMTAB.txt').read()
prognam = Label(file, text="SIC_Program Name :" + programname, font='time 18 bold', fg='blue')
prognam.pack()
programLength = Label(file, text=" SIC_Program Langth :" + str(proglen), font='time 18 bold', fg='blue')
programLength.pack()
programLength = Label(file, text=" Location Counter :" + str(loc), font='time 18 bold', fg='blue')
programLength.pack()
tit = Label(file, text=" Symbol Table:", font='time 18 bold underline')
tit.pack()
symbol = Text(file, height=120, width=120, font='helvetica 18 bold ')
symbol.configure(background="silver")
symbol.insert(END, SYMTAB)
symbol.pack()

file.mainloop()