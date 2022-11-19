import math
import time

import numpy as np


# 1: max, 0 min


class Board:
    def __init__(self):
        self.state = 10378549747928563776 #Corresponding to 1001000000001000000001000000001000000001000000001000000001000000
        self.maxDepth = 1
        self.mapChildren = {}
        self.mapValues = {}
        self.lastState= None
        self.numberOfNodesExpanded=0
    def getDepth(self):
        return self.maxDepth

    def setDepth(self, depth):
        self.maxDepth = depth

    def getChildrenFromMap(self, state):
        try:
            children = self.mapChildren[state]
            return children
        except:
            return None

    def getValueFromMap(self, state):
        try:
            value = self.mapValues[state]
            return value
        except:
            return None


BOARD = Board()

def set_bit(value, bit):
    return value | (1 << bit)


def clear_bit(value, bit):
    return value & ~(1 << bit)


def getLastLocationMask(state, col):
    return ((7 << (60 - (9 * col))) & state) >> (60 - (9 * col))


def decimalToBinary2(n):
    return "{0:b}".format(int(n))


# Check if the state makes the board full
def isGameOver(state):
    k = 60
    for j in range(0, 7):
        maxLocation = (((7 << k) & state) >> k)
        if maxLocation != 7:
            return False
        k -= 9
    return True


def convertToTwoDimensions(state):
    twoDimensionalArray = np.full((6, 7), -1, np.int8)

    k = 60
    startingBits = [59, 50, 41, 32, 23, 14, 5]
    for j in range(0, 7):
        lastLocation = getLastLocationMask(state, j) - 1
        k -= 9
        for row in range(0, lastLocation):
            currentBit = ((1 << (startingBits[j] - row)) & state) >> (startingBits[j] - row)
            twoDimensionalArray[row][j] = currentBit
    return twoDimensionalArray


def convertToNumber(twoDimensionalState):
    n = 1 << 63
    k = 60
    startingBits = [59, 50, 41, 32, 23, 14, 5]
    for j in range(0, 7):
        flag = False
        for i in range(0, 6):
            if twoDimensionalState[i][j] == 1:
                n = set_bit(n, startingBits[j] - i)
            elif twoDimensionalState[i][j] == -1:
                n = (((i + 1) << k) | n)
                flag = True
                break
        if not flag:
            n = ((7 << k) | n)
        k -= 9
    return n


# 3  points for 4 -sure point
# 2  points for 3 -candidate point
# 1  point  for 2 -candidate point
# -4 points for 4 -sure opponent point
# -3 points for 3 -candidate opponent point
# -2 points for 2 -candidate opponent point


# the value is



def check_neigbours(x, y, value, array,state):
    if value == 1:
        other_player = 0
    else:
        other_player = 1
    cost = 0
    map = {}
    map[value] = 1
    map[-1] = 0
    map[other_player] = -50
    last=[]
    k=60
    for i in range(0,7):
        temp = ((7<<k) & state) >> k
        last.append(temp-1)
        k-=9
    # for i in range(0,7):
    #     print(last[i])
    # print(decimalToBinary(state))
    if x <= 2:
        temp = 0
        for i in range(0, 4):
            temp += map[array[x + i][y]]
        if temp ==4:
            cost += 24
        elif temp ==3:
            cost+=13
        elif temp==2:
            cost+=3
        if temp == -47:
            cost -= 10

    if y <= 3:
        temp = 0
        for i in range(0, 4):
            temp += map[array[x][y + i]]
        if temp == 4:
            cost += 24
        elif temp == 3:
            cost += 13
        elif temp == 2:
            cost += 3
        if temp == -47:
            cost -= 10

    if y >= 3:
        temp = 0
        for i in range(0, 4):
                temp += map[array[x][y - i]]
        if temp == 3 and map[array[x][y - 3]]==0 :
                cost += 13
        if temp == 2 and map[array[x][y]]==1 and map[array[x][y - 3]]==0:
                cost += 3
        if temp == -47:
                cost -= 10

    if x <= 2 and y <= 3:
        temp = 0
        level=0
        for i in range(0, 4):
            temp += map[array[x + i][y + i]]
            if x+i <= last[y+i]:
                level+=1
        if temp == 4:
            cost += 24
        elif temp == 3  and level==4:
            cost += 13
        elif temp == 3 and level == 3:
            cost += 7
        elif temp == 2 and level == 4:
            cost += 3
        elif temp == 2 and level < 4:
            cost += 1.5
        if temp == -47:
            cost -= 10

    if x <= 2 and y >= 3:
        temp = 0
        level=0
        for i in range(0, 4):
            temp += map[array[x + i][y - i]]
            if y - i <= last[x + i]:
                level += 1
        if temp == 4:
            cost += 24
        elif temp == 3 and level==4:
            cost += 13
        elif temp == 3 and level == 3:
            cost += 7
        elif temp == 2 and level ==4:
            cost += 3
        elif temp == 2 and level<4:
            cost+=1.5
        if temp == -47:
            cost -= 10

    if value == 1:
        return cost
    else:
        return -cost


#
# def check_neigbours(x, y, value, array):
#     if value == 1:
#         other_player = 0
#     else:
#         other_player = 1
#     cost = 0
#     map = {}
#     map[value] = 1
#     map[-1] = 0
#     map[other_player] = -50
#     if x <= 2:
#         temp = 0
#         for i in range(0, 4):
#             temp += map[array[x + i][y]]
#         if temp > 1:
#             # if (value == 1):
#             #     print(str(temp) + " first cond")
#             # else:
#             #     print("-" + str(temp) + " first cond")
#             cost += temp
#         if temp == -47:
#             cost -= 1
#             # print(" -1 y pasha")
#
#     if y <= 3:
#         temp = 0
#         for i in range(0, 4):
#             temp += map[array[x][y + i]]
#         if temp > 1:
#             # if (value == 1):
#             #     print(str(temp) + " second cond")
#             # else:
#             #     print("-" + str(temp) + " second cond")
#             cost += temp
#         if temp == -47:
#             cost -= 1
#             # print(" -1 y pasha")
#
#     if x <= 2 and y <= 3:
#         temp = 0
#         for i in range(0, 4):
#             temp += map[array[x + i][y + i]]
#         if temp > 1:
#             # if (value == 1):
#             #     print(str(temp) + " third cond")
#             # else:
#             #     print("-" + str(temp) + " third cond")
#             cost += temp
#         if temp == -47:
#             cost -= 1
#             # print(" -1 y pasha")
#
#     if x <= 2 and y >= 3:
#         temp = 0
#         for i in range(0, 4):
#             temp += map[array[x + i][y - i]]
#             # print("--" + str(temp) + "---")
#         if temp > 1:
#             # if (value == 1):
#             #     print(str(temp) + " fourth cond")
#             # else:
#             #     print("-" + str(temp) + " fourth cond")
#             cost += temp
#         if temp == -47:
#             cost -= 1
#             # print(" -2 y pasha")
#
#     if value == 1:
#         return cost
#     else:
#         return -cost


def heuristic(state):
    # print("------------------new state ------------------------")
    array = convertToTwoDimensions(state)
    value = 0
    for i in range(0, 6):
        for j in range(0, 7):
            # print(str(i) + "-" + str(j))
            if array[i][j] != -1:
                value += check_neigbours(i, j, array[i][j], array,state)
                # print("--------------")

    # print("----------------------------value is : " + str(value))
    return value


def check_final_score(x, y, value, array):
    if value == 1:
        other_player = 0
    else:
        other_player = 1
    cost = 0
    map = {}
    map[value] = 1
    map[-1] = 0
    map[other_player] = -50
    if x <= 2:
        temp = 0
        for i in range(0, 4):
            temp += map[array[x + i][y]]
        if temp == 4:
            cost += 24
            # print(str(temp) + " 1 cond")

    if y <= 3:
        temp = 0
        for i in range(0, 4):
            temp += map[array[x][y + i]]
        if temp == 4:
            cost += 24
            # print(str(temp) + " 2 cond")

    if x <= 2 and y <= 3:
        temp = 0
        for i in range(0, 4):
            temp += map[array[x + i][y + i]]
        if temp == 4:
            cost += 24
            # print(str(temp) + " 3 cond")

    if x <= 2 and y >= 3:
        temp = 0
        for i in range(0, 4):
            temp += map[array[x + i][y - i]]
        if temp == 4:
            cost += 24
            # print(str(temp) + " fourth cond")

    if value == 1:
        return cost
    else:
        return -cost


def get_final_score(state):
    array = convertToTwoDimensions(state)
    value = 0
    for i in range(0, 6):
        for j in range(0, 7):
            if array[i][j] != -1:
                value += check_final_score(i, j, array[i][j], array)
    return value;



# max =1
# min =0

def getChildren(player, state):
    list = [33, 42, 24, 51, 15, 60, 6]
    children = []
    for i in range(0, 7):
        k = list[i]
        temp_state = state
        temp = ((7 << k) & temp_state) >> k
        if player == 1 and temp != 7:
            temp_state = state | (1 << (k - temp))
            temp_state = clear_bit(temp_state, k)
            temp_state = clear_bit(temp_state, k + 1)
            temp_state = clear_bit(temp_state, k + 2)
            temp_state = temp_state | ((temp + 1) << k)
            children.append(temp_state)
        elif player == 0 and temp != 7:
            temp_state = clear_bit(temp_state, k - temp)
            temp_state = clear_bit(temp_state, k)
            temp_state = clear_bit(temp_state, k + 1)
            temp_state = clear_bit(temp_state, k + 2)
            temp_state = temp_state | ((temp + 1) << k)
            children.append(temp_state)
    return children


def miniMax(maxDepth, depth, isMaxPlayer, state):
    BOARD.numberOfNodesExpanded+=1
    if depth == maxDepth:
        value = heuristic(state)
        BOARD.mapValues[state] = value
        return state, value

    if isGameOver(state):
        value = get_final_score(state)
        BOARD.mapValues[state] = value
        return state, value

    children = getChildren(isMaxPlayer, state)
    BOARD.mapChildren[state] = children
    if isMaxPlayer:
        maxChild = None
        maxValue = -math.inf
        for child in children:
            childValue = miniMax(maxDepth, depth + 1, not isMaxPlayer, child)[1]
            if childValue > maxValue:
                maxChild = child
                maxValue = childValue
        BOARD.mapValues[state] = maxValue
        return maxChild, maxValue
    else:
        minChild = None
        minValue = math.inf
        for child in children:
            childValue = miniMax(maxDepth, depth + 1, not isMaxPlayer, child)[1]
            if childValue < minValue:
                minValue = childValue
                minChild = child
        BOARD.mapValues[state] = minValue
        return minChild, minValue


def miniMaxAlphaBeta(maxDepth, depth, isMaxPlayer, state, alpha, beta):
    BOARD.numberOfNodesExpanded+=1
    if depth == maxDepth:
        value = heuristic(state)
        BOARD.mapValues[state] = value
        return state, value

    if isGameOver(state):
        value = get_final_score(state)
        BOARD.mapValues[state] = value
        return state, value

    children = getChildren(isMaxPlayer, state)
    if isMaxPlayer:
        maxChild = None
        maxValue = -math.inf
        index = 0
        for child in children:
            childValue = miniMaxAlphaBeta(maxDepth, depth + 1, False, child, alpha, beta)[1]
            if childValue > maxValue:
                maxChild = child
                maxValue = childValue
            if maxValue >= beta:
                break
            if maxValue > alpha:
                alpha = maxValue
            index += 1    
        for i in range(index+1,len(children)):
            children[i]= clear_bit(children[i],63)
        BOARD.mapValues[state] = maxValue
        BOARD.mapChildren[state] =children
        return maxChild, maxValue
    else:
        minChild = None
        minValue = math.inf
        index = 0
        for child in children:
            childValue = miniMaxAlphaBeta(maxDepth, depth + 1, True, child, alpha, beta)[1]
            if childValue < minValue:
                minValue = childValue
                minChild = child
            if minValue <= alpha:
                break
            if minValue < beta:
                beta = minValue
            index += 1
        for i in range(index+1,len(children)):
            children[i]= clear_bit(children[i],63)
        BOARD.mapValues[state] = minValue
        BOARD.mapChildren[state] =children
        return minChild, minValue



def nextMove(alphaBetaPruning, state):  # The function returns the next best state in integer form
    start_time = time.time()
    BOARD.numberOfNodesExpanded=0
    BOARD.lastState= state
    if alphaBetaPruning:
        ans= miniMaxAlphaBeta(BOARD.maxDepth, 0, True, state, -math.inf, math.inf)[0]
    else:
        ans =miniMax(BOARD.maxDepth, 0, True, state)[0]
    print(BOARD.numberOfNodesExpanded)
    print(time.time()-start_time)
    return ans
