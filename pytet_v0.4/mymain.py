from ctetris import *
from random import *
from enum import Enum
from collections import OrderedDict

import os
import sys
import tty
import termios
import signal

TextColor = [["red", "\033[31m"],
             ["green", "\033[32m"],
             ["yellow", "\033[33m"],
             ["blue", "\033[34m"],
             ["purple", "\033[35m"],
             ["cyan", "\033[36m"],
             ["pink", "\033[95m"],
             ["white", "\033[37m"]]

# end of dict TextColor():

def clearScreen(numlines=100):
    if os.name == 'posix':
        os.system('clear')
    elif os.name in ['nt', 'dos', 'ce']:
        os.system('CLS')
    else:
        print('\n' * numlines)
    return


def printScreen(board):
    clearScreen()
    # board는 CTetris 객체, oScreen은 Matrix 객체 get_array()는 2차원 행렬 리턴
    array = board.oScreen.get_array()

    # get_dy()는 세로 길이 리턴, iScreenDW는 테트리스 너비
    for y in range(board.oScreen.get_dy() - Tetris.iScreenDw):
        line = ''
        for x in range(Tetris.iScreenDw, board.oScreen.get_dx() - Tetris.iScreenDw):
            if array[y][x] == 0:
                line += TextColor[7][1] + '□'
            elif array[y][x] >= 1:
                line += TextColor[array[y][x]-1][1] + '■'
            else:
                line += 'XX'
        print(line)

    print()
    return


def unregisterAlarm():
    signal.alarm(0)
    return


def registerAlarm(handler, seconds):
    unregisterAlarm()
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    return


def timeout_handler(signum, frame):
    # print("timeout!")
    raise RuntimeError  # we have to raise error to wake up any blocking function
    return


def getChar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def readKey():
    c1 = getChar()
    if ord(c1) != 0x1b:  # ESC character
        return c1
    c2 = getChar()
    if ord(c2) != 0x5b:  # '[' character
        return c1
    c3 = getChar()
    return chr(0x10 + ord(c3) - 65)

def readKeyWithTimeOut():
    registerAlarm(timeout_handler, 1)   # 1초뒤 인터럽트 걸리게 설정
    try:
        key = readKey() # 일단 키를 읽고 잘 리턴되면 키값 리턴
        unregisterAlarm()
        return key
    except RuntimeError as e:   # 1초뒤에 이런 안되면 여기로 빠짐
        pass # print('readkey() interrupted!')

    return


def rotate(m_array):
    size = len(m_array)
    r_array = [[0] * size for _ in range(size)]

    for y in range(size):
        for x in range(size):
            r_array[x][size - 1 - y] = m_array[y][x]

    return r_array


def initSetOfBlockArrays():
    global nBlocks

    arrayBlks = [[[0, 0, 1, 0],  # I shape
                  [0, 0, 1, 0],
                  [0, 0, 1, 0],
                  [0, 0, 1, 0]],
                 [[1, 0, 0],  # J shape
                  [1, 1, 1],
                  [0, 0, 0]],
                 [[0, 0, 1],  # L shape
                  [1, 1, 1],
                  [0, 0, 0]],
                 [[1, 1],  # O shape
                  [1, 1]],
                 [[0, 1, 1],  # S shape
                  [1, 1, 0],
                  [0, 0, 0]],
                 [[0, 1, 0],  # T shape
                  [1, 1, 1],
                  [0, 0, 0]],
                 [[1, 1, 0],  # Z shape
                  [0, 1, 1],
                  [0, 0, 0]]
                 ]

    nBlocks = len(arrayBlks)
    setOfBlockArrays = [[0] * 4 for _ in range(nBlocks)]

    for idxBlockType in range(nBlocks):
        temp_array = [[idxBlockType + 1 if y > 0 else 0 for y in x]
                      for x in arrayBlks[idxBlockType]]
        setOfBlockArrays[idxBlockType][0] = temp_array
        for idxBlockDegree in range(1, 4):
            temp_array = rotate(temp_array)
            setOfBlockArrays[idxBlockType][idxBlockDegree] = temp_array

    return setOfBlockArrays


def processKey(board, key):
    global nBlocks

    state = board.accept(key)  # 키를 넘겨 새로 게임 화면을 만든다.
    printScreen(board)  # 만들어진 게임화면을 출력한다.

    if state != TetrisState.NewBlock:  # 땅에 떨어지지 않은 경우 함수 끝.
        return state

    idxBlockType = randint(0, nBlocks - 1)  # 땅에 떨어져서 새로 블럭을 생성
    key = '0' + str(idxBlockType)
    state = board.accept(key)  # accept에서 상태 갱신

    if state != TetrisState.Finished:  # 새로 만들었는데, 더 이상 들어갈 수 없어 게임 끝
        return state

    printScreen(board)

    return state


if __name__ == "__main__":
    setOfBlockArrays = initSetOfBlockArrays()  # 블럭 모양 초기화. 회전, 모양 등

    CTetris.init(setOfBlockArrays)  # 블럭 모양들 가지고 CTetris 클래스에서 블럭 모양 정보 가져가서 저장
    board = CTetris(20, 15)  # 테트리스 게임 크기 설정
    # board는 CTetris Class. 내부의 oScreen, iScreen은 Matrix 객체

    idxBlockType = randint(0, nBlocks - 1)  # 7가지 모양중에 하나 고름
    key = '0' + str(idxBlockType)  # string으로 붙임
    state = board.accept(key)  # 키를 화면에 붙임
    printScreen(board)  # 화면에 출력

    while True:
        key = readKeyWithTimeOut()  # 시간마다 계속 내려가게 함 시간 지나면

        if not key:  # 인터럽트로 인한 제대로 된 키가 리턴되지 않으면 그냥 한칸 내림
            key = 's'
        # print(repr(key))

        if key == 'q':
            state = TetrisState.Finished
            print('Game aborted...')
            break

        state = processKey(board, key)  # quit이 아니면 여기로 와서 board와 키를 넘겨준다.
        if state == TetrisState.Finished:
            print('Game Over!!!')
            break

    unregisterAlarm()  # 인터럽트 끔
    print('Program terminated...')

# end of main.py
