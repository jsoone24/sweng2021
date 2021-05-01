#pragma once

#ifndef CTETRIS_H
#define CTETRIS_H

#include "Tetris.h"

//todo which is private
class CTetris : public Tetris
{
public:
        // Matrix Type Variables
        Matrix iCScreen;
        Matrix oCScreen;
        Matrix arrayScreen;
        Matrix *currCBlk;
        static Matrix **setOfCBlockObjects;

        // Constructor and Destructor
        CTetris();
        CTetris(int dy, int dx);
        ~CTetris();

        // Methods
        static void init(int **setOfBlockArrays, int MAX_BLK_TYPES, int MAX_BLK_DEGREES); //initialize
        TetrisState accept(int key);                                                      // return TetrisState
        void deleteFullLines(void);
};
#endif