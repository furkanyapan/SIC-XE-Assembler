def SearchReg(reg, registers):
    for i in range(9):
        if reg == registers[i][0]:
            return registers[i][1]
    return None

def SearchOpcode(inst, OPTAB):
    for i in range(59):
        if inst == OPTAB[i][0]:
            return OPTAB[i][2]
    return None

def checkFormat1(inst):
    return inst in ["FIX", "FLOAT", "NORM", "HIO", "SIO", "TIO"]

def checkFormat2(inst):
    return inst in ["CLEAR", "ADDR", "COMPR", "DIVR", "MULR", "RMO", "SHIFTR", "SHIFTL", "SUBR", "SVC", "TIXR"]

def checkFormat3(inst):
    return inst in ["LDA", "ADD", "ADDF", "AND", "COMP", "COMF", "DIV", "DIVF", "J", "JEQ", "JGT", "JLT", "JSUB", "LDB", "LDCH", "LDF", "LDS", "LDT", "LDX", "LPS", "MUL", "MULF", "OR", "RD", "RSUB", "SSK", "STA", "STB", "STCH", "STF", "STI", "STL", "STS", "STSW", "STT", "JLT", "STX", "SUB", "SUBF", "TD", "TIX", "WD"]

def AscII(string):
    return ''.join(format(ord(char), '02X') for char in string)

def SearchRef(ref2, count, label, locter):
    for i in range(count):
        if ref2 == label[i]:
            return locter[i]
    return 0
#
def SearchLit(count, LITTAB):
    for i in range(count):
        if isinstance(LITTAB[i], (int, float)):
            return LITTAB[i]
    return 0
def SearchBase():
    base_index = inst.index("BASE")
    base1 = ref[base_index]
    base2 = label.index(base1)
    base = locttr[base2]
    return base

def HexaTOBin(BinString):
    return bin(int(BinString, 16))[2:]

def StringBInToHexs(Hexa):
    return {
        "0000": "0", "0001": "1", "0010": "2", "0011": "3",
        "0100": "4", "0101": "5", "0110": "6", "0111": "7",
        "1000": "8", "1001": "9", "1010": "A", "1011": "B",
        "1100": "C", "1101": "D", "1110": "E", "1111": "F"
    }.get(Hexa, None)

def checkPc(current_location, TA):
    disp = TA - current_location
    return -2048 <= disp <= 2047

def checkBase(current_location, TA):
    disp = TA - current_location
    return 0 <= disp <= 4095

def handle_negative_displacement(result):
    if result < 0:
        result = (1 << 12) + result  # 12-bit two's complement
    return result


OPTAB = [
    ["FIX", "1", "C4"], ["FLOAT", "1", "C0"], ["HIO", "1", "F4"], ["NORM", "1", "C8"], ["SIO", "1", "F0"], ["TIO", "1", "F8"],
    ["ADDR", "2", "90"], ["CLEAR", "2", "B4"], ["COMPR", "2", "A0"], ["DIVR", "2", "9C"], ["MULR", "2", "98"], ["RMO", "2", "AC"], ["SHIFTL", "2", "A4"], ["SHIFTR", "2", "A8"], ["SUBR", "2", "94"], ["SVC", "2", "B0"], ["TIXR", "2", "B8"],
    ["ADD", "3", "18"], ["ADDF", "3", "58"], ["AND", "3", "40"], ["COMP", "3", "28"], ["COMPF", "3", "88"], ["DIV", "3", "24"], ["DIVF", "3", "64"], ["J", "3", "3C"], ["JEQ", "3", "30"], ["JGT", "3", "34"], ["JLT", "3", "38"], ["JSUB", "3", "48"], ["LDA", "3", "00"], ["LDB", "3", "68"], ["LDCH", "3", "50"], ["LDF", "3", "70"], ["LDL", "3", "08"], ["LDS", "3", "6C"], ["LDT", "3", "74"], ["LDX", "3", "04"], ["LPS", "3", "D0"], ["MUL", "3", "20"], ["MULF", "3", "60"], ["OR", "3", "44"], ["RD", "3", "D8"], ["RSUB", "3", "4C"], ["SSK", "3", "EC"], ["STA", "3", "0C"], ["STB", "3", "78"], ["STCH", "3", "54"], ["STF", "3", "80"], ["STI", "3", "D4"], ["STL", "3", "14"], ["STS", "3", "7C"], ["STSW", "3", "E8"], ["STT", "3", "84"], ["STX", "3", "10"], ["SUB", "3", "1C"], ["SUBF", "3", "5C"], ["TD", "3", "E0"], ["TIX", "3", "2C"], ["WD", "3", "DC"]
]

registers = [
    ["A", "0"], ["X", "1"], ["L", "2"], ["B", "3"], ["S", "4"], ["T", "5"], ["F", "6"], ["PC", "8"], ["SW", "9"]
]

count = 0
label = [""] * 100
inst = [""] * 100
ref = [""] * 100

try:
    with open("input.txt", "r") as myfile:
        lines = myfile.readlines()
        for line in lines:
            parts = line.split()
            if len(parts) == 3:
                label[count] = parts[0]
                inst[count] = parts[1]
                ref[count] = parts[2]
            elif len(parts) == 2:
                label[count] = "     "
                inst[count] = parts[0]
                ref[count] = parts[1]
            elif len(parts) == 1:
                label[count] = "     "
                inst[count] = parts[0]
                ref[count] = "     "
            count += 1
except FileNotFoundError as e:
    print("An error occurred.")
    print(e)

locttr = [0] * 100
LITTAB = [0] * 100

for i in range(1, count):
    if inst[0] == "START":
        reference = int(ref[0], 16)
        locttr[0] = reference
        locttr[1] = reference

        LITTAB[0] = ""
        LITTAB[1] = ""

    if label[i] == "FIRST":
        if checkFormat1(inst[1]):
            locttr[2] = locttr[1] + 1
            LITTAB[2] = ""
        if checkFormat2(inst[1]):
            locttr[2] = locttr[1] + 2
            LITTAB[2] = ""
        if inst[1].startswith("+"):
            locttr[2] = locttr[1] + 4
            LITTAB[2] = ""
        if checkFormat3(inst[1]):
            locttr[2] = locttr[1] + 3
            LITTAB[2] = ""

    if inst[i] == "END":
        locttr[i] = int(ref[0])
        LITTAB[i] = ""

    if checkFormat1(inst[i - 1]):
        locttr[i] = locttr[i - 1] + 1
        LITTAB[i] = ""
    if checkFormat2(inst[i - 1]):
        locttr[i] = locttr[i - 1] + 2
        LITTAB[i] = ""
    if checkFormat3(inst[i - 1]):
        locttr[i] = locttr[i - 1] + 3
        LITTAB[i] = ""
    if inst[i - 1].startswith("+"):
        locttr[i] = locttr[i - 1] + 4
        LITTAB[i] = ""
    if inst[i - 1] == "BASE":
        locttr[i] = locttr[i - 1]
        LITTAB[i] = ""
    if inst[i - 1] == "RESW":
        locttr[i] = locttr[i - 1] + (3 * int(ref[i - 1]))
        LITTAB[i] = ""
    if inst[i - 1] == "RESB":
        locttr[i] = locttr[i - 1] + int(ref[i - 1])
        LITTAB[i] = ""
    if inst[i - 1] == "WORD":
        locttr[i] = locttr[i - 1] + 3
        LITTAB[i] = ""
    if inst[i - 1] == "BYTE":
        if ref[i - 1].startswith("X"):
            len_ref = len(ref[i - 1])
            locttr[i] = locttr[i - 1] + ((len_ref - 3) // 2)
            LITTAB[i] = ""
        if ref[i - 1].startswith("C"):
            locttr[i] = locttr[i - 1] + (len(ref[i - 1]) - 3)
            LITTAB[i] = ""
    if inst[i - 1] == "ORG":
        lbi = label.index(ref[i - 1])
        locttr[i] = locttr[lbi]
        LITTAB[i] = ""
    if inst[i - 1] == "EQU":
        if ref[i - 1] == "*":
            lbn = label[i - 1]
            label[i - 1] = locttr[i - 1]
            locttr[i] = locttr[i - 1]
            LITTAB[i] = ""
    if inst[i - 1] == "LTORG":
        LITTAB[i] = locttr[i - 1]
        locttr[i] = locttr[i - 1] + 3

program_length = locttr[count-1] - locttr[0]
program_length_hexa = format(program_length, 'X')

lochex = [""] * count
for i in range(count):
    lochex[i] = format(locttr[i], '04X').upper()

try:
    with open("intermediate.txt", "w") as writer:
        for i in range(count):
            writer.write(f"{lochex[i]}  {label[i]} {ref[i]} {inst[i]}\n")
except IOError as e:
    print(e)

try:
    with open("SYMTAB.txt", "w") as writer:
        for i in range(count):
            if label[i] != "     ":
                #
                if isinstance(label[i], (int, float)):
                    label[i] = lbn
                writer.write(f"{lochex[i]} {label[i]}\n")
        writer.write(f"Length of program = {program_length_hexa}")
except IOError as e:
    print(e)

try:
    with open("Literal_Tablosu.txt", "w") as writer:
        for i in range(count):
            if ref[i].startswith("="):
                deger = i
        for i in range(count):
            if LITTAB[i] != "":
                writer.write(f"{ref[deger]}  {hex(LITTAB[i])}\n")

except IOError as e:
    print(e)

OPCODE = [["", ""]] * count

for i in range(count):
    if checkFormat1(inst[i]):
        OPCODE[i] = [inst[i], SearchOpcode(inst[i], OPTAB)]
    if checkFormat2(inst[i]):
        OpCOde = SearchOpcode(inst[i], OPTAB)
        RegParts = ref[i].split(",")
        if len(RegParts) == 1:
            OPCODE[i] = [inst[i], OpCOde + SearchReg(RegParts[0], registers) + "0"]
        if len(RegParts) == 2:
            OPCODE[i] = [inst[i], OpCOde + SearchReg(RegParts[0], registers) + SearchReg(RegParts[1], registers)]
            if len(OPCODE[i][1]) < 4:
                OPCODE[i][1] = OPCODE[i][1] + "0"

    if checkFormat3(inst[i]):
        Opcodebin = HexaTOBin(SearchOpcode(inst[i], OPTAB))
        while len(Opcodebin) < 8:
            Opcodebin = "0" + Opcodebin
        OpcodeRes = Opcodebin[:-2]
        part1 = StringBInToHexs(OpcodeRes[:4])
        lastbits = OpcodeRes[4:6]

        if ref[i].startswith("#"):
            s = ref[i][1:]
            if s[0].isdigit():
                hexa = ref[i][1:]
                while len(hexa) < 3:
                    hexa = "0" + hexa
                part4 = hexa.upper()
                n = "0"
                I = "1"
                x = "0"
                b = "0"
                p = "0"
                e = "0"
                cont = x + b + p + e
                part2 = StringBInToHexs(lastbits + n + I)
                part3 = StringBInToHexs(cont)
                Result = part1 + part2 + part3 + part4
                OPCODE[i] = [inst[i], Result]
            else:
                reference = ref[i][1:]
                TA = SearchRef(reference, count, label, locttr)
                if checkPc(locttr[i + 1], TA):
                    result = TA - locttr[i+1]
                    result = handle_negative_displacement(result)
                    part4 = format(result, '03X').upper()
                    n = "0"
                    I = "1"
                    x = "0"
                    b = "0"
                    p = "1"
                    e = "0"
                    cont = x + b + p + e
                    part2 = StringBInToHexs(lastbits + n + I)
                    part3 = StringBInToHexs(cont)
                    Result = part1 + part2 + part3 + part4
                    OPCODE[i] = [inst[i], Result]

        if ref[i].startswith("@"):
            reference = ref[i][1:]
            TA = SearchRef(reference, count, label, locttr)
            if checkPc(locttr[i + 1], TA):
                result = int(TA) - int(locttr[i + 1])
                result = handle_negative_displacement(result)
                hexa = format(result, '03X')
                part4 = hexa.upper()
                n = "1"
                I = "0"
                x = "0"
                b = "0"
                p = "1"
                e = "0"
                cont = x + b + p + e
                part2 = StringBInToHexs(lastbits + n + I)
                part3 = StringBInToHexs(cont)
                Result = part1 + part2 + part3 + part4
                OPCODE[i] = [inst[i], Result]

        Baseloc = SearchBase()

        if not ref[i].startswith("@") and not ref[i].startswith("#"):
            if ",X" in ref[i]:
                x = "1"
                ref[i] = ref[i].replace(",X", "")
            else:
                x = "0"
            if ref[i].startswith("="):
                TA = SearchLit(count, LITTAB)
            else:
                TA = SearchRef(ref[i], count, label, locttr)
            if checkPc(locttr[i + 1], TA):
                result = TA - locttr[i+1]
                result = handle_negative_displacement(result)
                part4 = format(result, '03X')
                if len(part4) > 3:
                    part4 = part4[-3:].upper()
                while len(part4) < 3:
                    part4 = "0" + part4.upper()
                n = "1"
                I = "1"
                b = "0"
                p = "1"
                e = "0"
                cont = x + b + p + e
                part2 = StringBInToHexs(lastbits + n + I)
                part3 = StringBInToHexs(cont)
                Result = part1 + part2 + part3 + part4
                OPCODE[i] = [inst[i], Result]

            elif checkBase(Baseloc, TA):
                base = SearchBase()
                result = TA - base
                result = handle_negative_displacement(result)
                part4 = format(result, '03X')
                if len(part4) > 3:
                    part4 = part4[-3:].upper()
                while len(part4) < 3:
                    part4 = "0" + part4.upper()
                n = "1"
                I = "1"
                b = "1"
                p = "0"
                e = "0"
                cont = x + b + p + e
                part2 = StringBInToHexs(lastbits + n + I)
                part3 = StringBInToHexs(cont)
                Result = part1 + part2 + part3 + part4
                OPCODE[i] = [inst[i], Result]

    if inst[i].startswith("+"):
        Opcodebin = HexaTOBin(SearchOpcode(inst[i][1:], OPTAB))
        while len(Opcodebin) < 8:
            Opcodebin = "0" + Opcodebin
        OpcodeRes = Opcodebin[:-2]
        part1 = StringBInToHexs(OpcodeRes[:4])
        lastbits = OpcodeRes[4:6]
        n = "1"
        I = "1"
        b = "0"
        p = "0"
        e = "1"
        x = "1" if ",X" in ref[i] else "0"
        cont = x + b + p + e
        part2 = StringBInToHexs(lastbits + n + I)
        part3 = StringBInToHexs(cont)
        location = SearchRef(ref[i], count, label, locttr)
        part4 = "0" + format(location, 'X').upper()
        Result = part1 + part2 + part3 + part4
        OPCODE[i] = [inst[i], Result]

    if inst[i].startswith("+") and ref[i].startswith("#"):
        Opcodebin = HexaTOBin(SearchOpcode(inst[i][1:], OPTAB))
        while len(Opcodebin) < 8:
            Opcodebin = "0" + Opcodebin
        OpcodeRes = Opcodebin[:-2]
        part1 = StringBInToHexs(OpcodeRes[:4])
        lastbits = OpcodeRes[4:6]
        n = "0"
        I = "1"
        x = "0"
        b = "0"
        p = "0"
        e = "1"
        cont = x + b + p + e
        part2 = StringBInToHexs(lastbits + n + I)
        part3 = StringBInToHexs(cont)
        hexa = ref[i][1:]
        if hexa[0].isdigit():
            part4 = format(int(ref[i][1:]), 'X').upper()
            while len(part4) < 5:
                part4 = "0" + part4
        else:
            TA = SearchRef(ref[i][1:], count, label, locttr)
            part4 = "0" + format(TA, 'X')
        Result = part1 + part2 + part3 + part4
        OPCODE[i] = [inst[i], Result]

    if inst[i] in ["BASE", "START"]:
        OPCODE[i] = [inst[i], ""]
    if inst[i] == "END":
        OPCODE[i] = [inst[i], ref[0]]
    if inst[i] == "WORD":
        ref[i] = format(int(ref[i]), 'X').upper()
        while len(ref[i]) < 6:
            ref[i] = "0" + ref[i]
        OPCODE[i] = [inst[i], ref[i]]
    if inst[i] == "BYTE":
        if "X'" in ref[i]:
            OpCOde = ref[i][2:-1]
            OPCODE[i] = [inst[i], OpCOde.upper()]
        if "C'" in ref[i]:
            OpCOde = ref[i][2:-1]
            OPCODE[i] = [inst[i], AscII(OpCOde)]
    if inst[i] == "RESW":
        OPCODE[i] = [inst[i], ""]
    if inst[i] == "RESB":
        OPCODE[i] = [inst[i], ""]
    if inst[i] == "RSUB":
        if inst[i].startswith("+"):
            OPCODE[i] = [inst[i], "4F100000"]
        else:
            OPCODE[i] = [inst[i], "4F0000"]
    if inst[i] == "ORG":
        OPCODE[i] = [inst[i], ""]
    if inst[i] == "EQU":
        OPCODE[i] = [inst[i], ""]
    if inst[i] == "LTORG":
        OPCODE[i] = [inst[i], ""]

try:
    with open("object_code.txt", "w") as writer:
        for i in range(count):
            writer.write(f"{lochex[i]}  {label[i]}  {OPCODE[i][0]}  {ref[i]} ---> {OPCODE[i][1]}\n")
except IOError as e:
    print(e)

for i in range(1, count):
    if OPCODE[i][1] in ["", None]:
        continue
    while len(OPCODE[i][1]) < 6:
        OPCODE[i][1] = "0" + OPCODE[i][1]

try:
    with open("object_Program.txt", "w") as writer:
        while len(ref[0]) < 6:
            ref[0] = "0" + ref[0]
        while len(program_length_hexa) < 6:
            program_length_hexa = "0" + program_length_hexa
        writer.write(f"H^{label[0]}^{ref[0]}. {program_length_hexa.upper()}")
        records = []
        location = []
        flag = False
        for i in range(1, count):
            if OPCODE[i][0] not in ["RESW", "RESB", "END", "ORG", "EQU"]:
                flag = True
                if OPCODE[i][0] != "END":
                    records.append(OPCODE[i][1])
                    location.append(locttr[i])
            if (OPCODE[i][0] in ["RESW", "RESB", "END", "ORG", "EQU"]) and flag:
                location.append(locttr[i])
                fisrtpos = format(location[0], 'X')
                while len(fisrtpos) < 6:
                    fisrtpos = "0" + fisrtpos
                writer.write(f"\nT^{fisrtpos.upper()}")
                hexa = format(location[-1] - location[0], 'X')
                writer.write(f"^{hexa.upper()}")
                records = [rec for rec in records if rec != ""]
                for record in records:
                    writer.write(f"^{record}")
                records.clear()
                location.clear()
                flag = False
        writer.write(f"\nE^{ref[0]}")
except IOError as e:
    print(e)
