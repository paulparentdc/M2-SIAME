main.o:	
	g++ -c main.cpp
piece.o:
	g++ -c piece.cpp
board.o:
	g++ -c board.cpp
	
tetris: main.o piece.o board.o
	g++ main.o piece.o board.o -o tetris

clean:
	rm *.o