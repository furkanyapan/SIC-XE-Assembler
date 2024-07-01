***ASSEMBLER HAKKINDA BİLGİLER***

-SIC/XE için hazırlanmış olan bu assembler kullanıcıdan text olarak alınan programı object programına çevirmektedir.

-Program Python dili ile yazılmıştır. Arayüz tasarımları Qt Designer ve PyQt5 kullanılarak tasarlanmıştır.

-Tasarlanan assembler  START, RESW,RESB, WORD, BYTE, ORG, LTORG, EQU gibi direktifleri işleyebilmektedir.

-Assembler pc relative, base relative işlemlerini gerçekleştirebilmektedir.

-Assembler kullanıcı dostu bir tasarıma sahiptir. Kullanıcı rahatlıkla programını yazabilir ve ardından assembly et butonuna tıklayarak yazdığı programla ilgili çeşitli tablolar ve object programını görebilmektedir.

-Ekranda kullanıcıya  "Sembol Tablosu" "Literal Tablosu" "Object Kodları" "Object Program" tabloları gösterilmektedir.

-"Sembol Tablosu" ve "Literal Tablosu" pass1 aşamasından sonra kullanıcıya gösterilir.

-"Object Kodları" tablosunda programdaki etiket değerleri, opcode, operant değerleri ve pass 2 aşamasından sonra oluşan object kodları kullanıcıya gösterilmektedir.

-"Object Program" tablosu kısmında header, text, end kayıtları ekranda gösterilmektedir.

***ASSEMBLER ALGORİTMASI***

START PROGRAM

Fonksiyon Tanımla:
    SearchReg
    SearchOpcode
    checkFormat1
    checkFormat2
    checkFormat3
    AscII
    SearchRef
    SearchLit
    SearchBase
    HexaTOBin
    StringBInToHexs
    checkPc
    checkBase
    handle_negative_displacement

OPTAB ve register' ları tanımla

label, inst, ref, locttr, LITTAB, OPCODE' ları initilaze et

input file :
    FOR each line in input.txt:  //kullanıcıdan alınan input ile oluşturulan input.txt
        SPLIT line into parts
        STORE parts in label, inst, ref arrays

CALCULATE location counters:
    IF first instruction is START:
        SET reference address
        SET initial location counters

    FOR each instruction:
        CHECK instruction format
        UPDATE location counter based on instruction format
        HANDLE special instructions: RESW, RESB, WORD, BYTE, ORG, EQU, LTORG

WRITE intermediate file and symbol table:
    FOR each instruction:
        WRITE label, reference, and instruction to intermediate.txt
        IF label exists:
            WRITE label and location counter to SYMTAB.txt
        WRITE program length to SYMTAB.txt

WRITE literal table:
    FOR each instruction:
        IF reference is a literal:
            FIND literal value and WRITE to Literal_Tablosu.txt

GENERATE object code:
    FOR each instruction:
        CHECK instruction format
        GENERATE object code based on instruction format and operands
        HANDLE special instructions: BASE, START, END, WORD, BYTE, RESW, RESB, RSUB, ORG, EQU, LTORG

WRITE object code to file:
    FOR each instruction:
        WRITE label, reference, instruction, and object code to object_code.txt

WRITE object program:
    WRITE header record to object_Program.txt
    FOR each instruction:
        IF instruction is not RESW, RESB, END, ORG, EQU:
            APPEND object code to text record
        IF instruction is special or end:
            WRITE text record to object_Program.txt
            CLEAR text record
    WRITE end record to object_Program.txt

END PROGRAM

***Örnek Olarak Kullanılan Girdi***

COPY START 0
FIRST STL RETADR 
LDB #LENGTH
BASE LENGTH
CLOOP +JSUB RDREC
LDA LENGTH
COMP #0
JEQ ENDFIL
+JSUB WRREC
J CLOOP
ENDFIL LDA =C'EOF'
STA BUFFER
LDA #3
STA LENGTH
+JSUB WRREC
J @RETADR
LTORG
RETADR RESW 1
LENGTH RESW 1
BUFFER RESB 4096
RDREC CLEAR X
CLEAR A
CLEAR S
+LDT #4096
RLOOP TD INPUT
JEQ RLOOP
RD INPUT 
COMPR A,S
JEQ EXIT
STCH BUFFER,X
TIXR T
JLT RLOOP
EXIT STX LENGTH
RSUB
INPUT BYTE X'F1'
WRREC CLEAR X
LDT LENGTH
WLOOP TD OUTPUT
JEQ WLOOP
LDCH BUFFER,X
WD OUTPUT
TIXR T
JLT WLOOP
RSUB
OUTPUT BYTE X'05'
END FIRST
 
