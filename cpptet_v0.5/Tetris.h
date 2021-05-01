#pragma once

#include "Matrix.h"

enum TetrisState {
    Running, NewBlock, Finished
};
// end of class TetrisState():

class Tetris {
    private:
    int nBlockTypes = 0
    int nBlockDegrees = 0
    int setOfBlockObjects = 0
    int iScreenDw = 0   //larget enough to cover the largest block
    arrayScreen
    arrayScreenDx
    arrayScreenDy
    iScreenDx
    iScreenDy
    iScreenDw
    idxBlockType
    idxBlockDegree
    iScreen
    oScreen
    justStarted
    state
    currBlk
    tempBlk
    top
    left

    public:
    Tetris(setOfBlockArrays):    // constructor. return nothing
    ~Tetris();  // deconstructor
    def createArrayScreen():    // return this.arrayScreen
     void __init__(int iScreenDy, int iScreenDx):  // return nothing
     int accept(int key): // return state
    void deleteFullLines(); // return nothing
};

### end of class Tetris():
