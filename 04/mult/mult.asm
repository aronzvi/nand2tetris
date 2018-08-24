// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here

// a = R0
@R0
D=M

@a
M=D

// b = R1
@R1
D=M

@b
M=D

// R2 = 0
@R2
M=0

// i = 0
@i
M=0

(LOOP)
// if i == b goto END
@i
D=M

@b
D=M-D

@END
D;JEQ

// product: R2 = R2 + a 
@a
D=M

@R2
M=D+M

//i++
@i
M=M+1

@LOOP
0;JMP

(END)
@END
0;JMP
