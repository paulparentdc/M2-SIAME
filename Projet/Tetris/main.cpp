#include "board.h"
#include <stdlib.h>
#include <ctime>
#include <stdio.h>

int main(void){
    srand((unsigned)time(0));
    
    Board board;
    Piece p(rand()%6, 0);
    board.newPiece(p);
    
    while(1){
        std::system("clear");
        board.print();
        board.deletePossibleLines();
        if(board.isCurrentPieceFallen()){
            Piece pi(rand()%6,0);
            board.newPiece(pi);
        }
        
        char input;
        std::cin >> input;
        switch(input){
            case 'q': board.moveCurrentPieceLeft();
                    break;
            case 'd': board.moveCurrentPieceRight();
                    break;
            case 's': board.moveCurrentPieceDown();
                    break;
            case 'w': board.rotateCurrentPieceLeft();
                    break;
            case 'c': board.rotateCurrentPieceRight();
                    break;
        }
    }
    return 0;
}