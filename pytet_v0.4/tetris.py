from matrix import *
from enum import Enum


class TetrisState(Enum):
    Running = 0
    NewBlock = 1
    Finished = 2
# end of class TetrisState():


class Tetris():
    nBlockTypes = 0
    nBlockDegrees = 0
    setOfBlockObjects = 0
    iScreenDw = 0   # larget enough to cover the largest block

    @classmethod
    def init(cls, setOfBlockArrays):
        Tetris.nBlockTypes = len(setOfBlockArrays)  # 7 블럭 개수
        Tetris.nBlockDegrees = len(setOfBlockArrays[0])  # 4 블럭 각도 수
        Tetris.setOfBlockObjects = [[0] * Tetris.nBlockDegrees for _ in range(Tetris.nBlockTypes)]
        arrayBlk_maxSize = 0  # 모양중에 제일 큰거 기록
        for i in range(Tetris.nBlockTypes):
            if arrayBlk_maxSize <= len(setOfBlockArrays[i][0]):
                arrayBlk_maxSize = len(setOfBlockArrays[i][0])
        # larget enough to cover the largest block
        Tetris.iScreenDw = arrayBlk_maxSize

        for i in range(Tetris.nBlockTypes):
            for j in range(Tetris.nBlockDegrees):
                Tetris.setOfBlockObjects[i][j] = Matrix(
                    setOfBlockArrays[i][j])  # 자신 클래스에 별도 저장
        return

    def createArrayScreen(self):  # ArrayScreen(배경화면) 초기화
        self.arrayScreenDx = Tetris.iScreenDw * 2 + self.iScreenDx
        self.arrayScreenDy = self.iScreenDy + Tetris.iScreenDw
        self.arrayScreen = [[0] * self.arrayScreenDx for _ in range(self.arrayScreenDy)]
        for y in range(self.iScreenDy):
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][x] = 1
            for x in range(self.iScreenDx):
                self.arrayScreen[y][Tetris.iScreenDw + x] = 0
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][Tetris.iScreenDw + self.iScreenDx + x] = 1

        for y in range(Tetris.iScreenDw):
            for x in range(self.arrayScreenDx):
                self.arrayScreen[self.iScreenDy + y][x] = 1

        return self.arrayScreen

    def __init__(self, iScreenDy, iScreenDx):  # 게임 화면 크기 설정
        self.iScreenDy = iScreenDy
        self.iScreenDx = iScreenDx
        self.idxBlockDegree = 0
        arrayScreen = self.createArrayScreen()
        self.iScreen = Matrix(arrayScreen)  # ArrayScreen(배경) 만들어서 iScreen넣음
        self.oScreen = Matrix(self.iScreen)  # iScreen으로 oScreen만듬
        self.justStarted = True
        return

    def accept(self, key):
        self.state = TetrisState.Running

        if key >= '0' and key <= '6':
            if self.justStarted == False:
                self.deleteFullLines()
            self.iScreen = Matrix(self.oScreen)  # 현재 oScreen 받아옴
            self.idxBlockType = int(key)  # 들어온 블럭 모양 저장
            self.idxBlockDegree = 0  # 블럭 각도 설정
            # 설정된 값으로 블럭 모양 읽어옴
            self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
            self.top = 0
            self.left = Tetris.iScreenDw + self.iScreenDx//2 - self.currBlk.get_dx()//2  # 블럭 어디에 놓을지 위치 선정
            self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
            # temp block 은 현재 화면에서 잘라온 블럭. currblock은 현재 선택된 블럭
            self.tempBlk = self.tempBlk + self.currBlk
            self.justStarted = False
            print()

            if self.tempBlk.anyGreaterThan(1):  # 넘었는지 체크
                self.state = TetrisState.Finished
            self.oScreen = Matrix(self.iScreen)
            self.oScreen.paste(self.tempBlk, self.top, self.left)  # 아니면 출력
            return self.state
        elif key == 'q':
            pass
        elif key == 'a':  # move left
            self.left -= 1
        elif key == 'd':  # move right
            self.left += 1
        elif key == 's':  # move down
            self.top += 1
        elif key == 'w':  # rotate the block clockwise
            self.idxBlockDegree = (self.idxBlockDegree + 1) % Tetris.nBlockDegrees
            self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
        elif key == ' ':  # drop the block
            while not self.tempBlk.anyGreaterThan(1):
                self.top += 1
                self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
                self.tempBlk = self.tempBlk + self.currBlk
        else:
            print('Wrong key!!!')

        self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
        self.tempBlk = self.tempBlk + self.currBlk

        if self.tempBlk.anyGreaterThan(1):  # 벽 충돌시 undo 수행
            if key == 'a':  # undo: move right
                self.left += 1
            elif key == 'd':  # undo: move left
                self.left -= 1
            elif key == 's':  # undo: move up
                self.top -= 1
                self.state = TetrisState.NewBlock
            elif key == 'w':  # undo: rotate the block counter-clockwise
                self.idxBlockDegree = (
                    self.idxBlockDegree - 1) % Tetris.nBlockDegrees
                self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
            elif key == ' ':  # undo: move up
                self.top -= 1
                self.state = TetrisState.NewBlock

            self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
            self.tempBlk = self.tempBlk + self.currBlk

        self.oScreen = Matrix(self.iScreen)
        self.oScreen.paste(self.tempBlk, self.top, self.left)

        return self.state

    def deleteFullLines(self):
        return

# end of class Tetris():
