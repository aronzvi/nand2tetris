// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LISTENLOOP)
@KBD
D=M

// if kbd == 0 goto CLEARSCREEN
@CLEARSCREEN
D;JEQ

// else, blacken screen
// blacken screen: for each (256 rows * 32) word in screen, set to 1111111111111111 
//i = 0
@i
M=0

(BLAKENSCREENLOOP)
@i
D=M
@8192
D=A-D        // D = 8192 - i
@LISTENLOOP
D;JEQ        // if i == 8192 goto LISTENLOOP
@i
D=M
@SCREEN
A=D+A       // A = SCREEN + i
M=-1        // M[SCREEN + i] = 1111111111111111

@i          // i = i + 1
M=M+1

@BLAKENSCREENLOOP // goto BLAKENSCREENLOOP
0;JMP


(CLEARSCREEN)
//i = 0
@i
M=0

(CLEARSCREENLOOP)
// clearscreen: for each (256 rows * 32 = 8192) word in screen, set to 0000000000000000

@i
D=M
@8192
D=A-D        // D = i - 8192
@LISTENLOOP
D;JEQ        // if i == 8192 goto LISTENLOOP
@i
D=M
@SCREEN
A=D+A       // A = SCREEN + i
M=0         // M[SCREEN + i] = 0000000000000000

@i          // i = i + 1
M=M+1

@CLEARSCREENLOOP // goto CLEARSCREENLOOP
0;JMP


