import random
import copy
from typing import List


# CONST
MAP_SIZE = 8
OFF_SET = 1
TOTAL_SIZE = MAP_SIZE + OFF_SET * 2
NUM_BOMB = 5
BOMB_WEIGHT = 100
BOM_DIRECTIONS = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

class MainSweeper(object):
    def __init__(self):
        self.maps = self.makeTable()
        self.display = self.displayTalbe()
        self.game = True    # Trueの間ゲームを続ける

    # def checkBomb(self, x,y):
    #     return (self.maps[x][y] == BOMB_WEIGHT)

    def returnTable(self, x,y):
        if self.maps[x][y] == BOMB_WEIGHT:
            self.game = False
            self.display[x][y] = '×'
        elif self.maps[x][y] > 0:
            self.display[x][y] = self.maps[x][y]
        elif self.maps[x][y] == 0:
            decidedPlaces = self.checkReturn(x,y)
            for x,y in decidedPlaces:
                self.display[x][y] = self.maps[x][y]

    def checkReturn(self, x,y):
        zeroPlaces = [(x,y)]
        decidedPlaces = []
        while(len(zeroPlaces) != 0):
            for x,y in zeroPlaces:
                decidedPlaces.append((x,y))
                zeroPlaces.remove((x,y))
                for a,b in BOM_DIRECTIONS:
                    nx,ny = x+a,y+b
                    if self.maps[nx][ny] == 0:
                        if (nx,ny) not in decidedPlaces:
                            zeroPlaces.append((nx,ny))
                    elif 0 < self.maps[nx][ny]:
                        decidedPlaces.append((nx,ny))
        return decidedPlaces

    # 初期化のときだけ呼ばれる
    def displayTalbe(self):
        tmp = [['■' for _ in range(TOTAL_SIZE)] for _ in range(TOTAL_SIZE)]
        for i in range(TOTAL_SIZE):
            tmp[0][i] = '-'
            tmp[TOTAL_SIZE-1][i] = '-'
            tmp[i][0] = '-'
            tmp[i][TOTAL_SIZE-1] = '-'
        return tmp

    # マップを初期化する
    def makeTable(self) -> List[int]:
        # map = [['0'] * TOTAL_SIZE] * TOTAL_SIZE
        maps = [[0 for _ in range(TOTAL_SIZE)] for _ in range(TOTAL_SIZE)]
        count = 0
        while(count < NUM_BOMB):
            x = random.randint(OFF_SET,MAP_SIZE)
            y = random.randint(OFF_SET,MAP_SIZE)
            if maps[x][y] == 0:
                maps[x][y] = BOMB_WEIGHT
                count += 1

        # 爆弾が接している方向をタプルで渡す
        bom_direction = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for x in range(1, 1+MAP_SIZE):
            for y in range(1, 1+MAP_SIZE):
                if maps[x][y] == BOMB_WEIGHT:
                    pass
                else:
                    tmp = 0
                    for a,b in bom_direction:
                        tmp += maps[x+a][y+b]
                    maps[x][y] = tmp // BOMB_WEIGHT
        for i in range(TOTAL_SIZE):
            maps[0][i] = -1
            maps[TOTAL_SIZE-1][i] = -1
            maps[i][0] = -1
            maps[i][TOTAL_SIZE-1] = -1
        return maps

    def mainSolve(self):
        for a in axisAppend(changeToString(mains.display)):
            print(a)
        while(self.game):
            while(True):
                cnt = 0
                x = input("Enter x:")
                y = input("Enter y:")
                if x.isdigit():
                    x = int(x)
                    if (0 < x < TOTAL_SIZE-1):
                        cnt += 1
                    else:
                        print("invalid x")
                else:
                    print("invalid x")
                if y.isnumeric():
                    y = int(y)
                    if (0 < y < TOTAL_SIZE-1):
                        cnt += 1
                    else:
                        print("invalid y")
                else:
                    print("invalid y")
                if cnt == 2:
                    break

            self.returnTable(x, y)
            for a in axisAppend(changeToString(mains.display)):
                print(a)
            print('*'*25)
        print('You are dead')
        print('Below is the answer')
        for a in axisAppend(changeToString(mains.maps)):
            print(a)


def changeToBomb(maps):
    # tmp = maps[:] # これで問題起きた！
    tmp = copy.deepcopy(maps)
    for x in range(TOTAL_SIZE):
        for y in range(TOTAL_SIZE):
            if tmp[x][y] == -1:
                tmp[x][y] = '-'
            elif tmp[x][y] == BOMB_WEIGHT:
                tmp[x][y] = '×'
    return tmp
def changeToString(maps):
    tmp = []
    for a in maps:
        lis = map(str, a)
        tmp.append(' '.join(lis))
    return tmp
def axisAppend(stringMaps):
    half = len(stringMaps) // 2
    tmp = ['   ' * half + 'y']
    first = '   ' + '  ' + ' '.join([str(i) for i in(range(1,1+MAP_SIZE))])
    tmp.append(first)
    for i,a in enumerate(stringMaps):
        if i == 0:
            tmp.append('   ' + a)
        else:
            if i == half:
                tmp.append(f'x {half}' + a)
            else:
                tmp.append(f'  {i}' + a)
    return tmp

if __name__ == '__main__':
    mains = MainSweeper()
    mains.mainSolve()

