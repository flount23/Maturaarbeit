import numpy as np
import time

def render(board):
    frame = [[0,0,0],[0,0,0],[0,0,0]]

    for i in range(9):
        if board[i] == -1:
            frame[i//3][i%3] = 'O'
        elif board[i] == 0:
            frame[i//3][i%3] = ' '
        else:
            frame[i//3][i%3] = 'X'

    print(f'-------------\n| {frame[0][0]} | {frame[0][1]} | {frame[0][2]} |\n-------------\n| {frame[1][0]} | {frame[1][1]} | {frame[1][2]} |\n-------------\n| {frame[2][0]} | {frame[2][1]} | {frame[2][2]} |\n-------------')


def emptyCells(board):
    emptyCells = []
    for i in range(len(board)):
        if board[i] == 0:
            emptyCells.append(i)
    return emptyCells

def state(board):
    winningStates = [[board[0],board[1],board[2]],
                     [board[3],board[4],board[5]],
                     [board[6],board[7],board[8]],
                     [board[0],board[3],board[6]],
                     [board[1],board[4],board[7]],
                     [board[2],board[5],board[8]],
                     [board[0],board[4],board[8]],
                     [board[2],board[4],board[6]]]

    if [1,1,1] in winningStates:
        return True, 1
    elif [-1,-1,-1] in winningStates:
        return True, -1
    elif len(emptyCells(board)) == 0:
        return True, 0
    else:
        return False, 0

def score(board):
    done, win = state(board)

    if done:
        return win

    scores = possibleScores(board)

    if len(emptyCells(board)) % 2 == 1:
        return np.max(scores)
    else:
        return np.min(scores)

def possibleScores(board):
    scores = []
    for i in emptyCells(board):
        newBoard = [i for i in board]
        newBoard[i] = len(emptyCells(board)) % 2 * 2 - 1
        scores.append(score(newBoard))
    return scores


def minimax(board):
    eC = emptyCells(board)
    if len(eC) == 0:
        return 0
    elif len(eC) % 2 == 1:
        return eC[np.argmax(possibleScores(board))]
    else:
        return eC[np.argmin(possibleScores(board))]

def mvm(board):
    render(board)
    while not state(board)[0]:
        board[minimax(board)] = -1 + 2 * (len(emptyCells(board))%2)
        render(board)

def mvr(board):
    render(board)
    while not state(board)[0]:
        ec = len(emptyCells(board))
        if ec % 2 == 1:
            board[np.random.choice(emptyCells(board))] = 1
        else:
            board[minimax(board)] = -1
        render(board)

def mvh(board):
    render(board)
    while not state(board)[0]:
        ec = len(emptyCells(board))
        if ec % 2 == 1:
            z = -1
            while z not in emptyCells(board):
                z = int(input('Feld (1-9): ')) - 1
            board[z]=1
        else:
            board[minimax(board)] = -1
        render(board)

t = time.time()
results = [0,0,0]
for i in range(1000):
    if i%10==0:
        print(f'{i} {results}')
    board = [0,0,0,0,0,0,0,0,0]
    while not state(board)[0]:
        ec = len(emptyCells(board))
        if ec % 2 == 1:
            board[np.random.choice(emptyCells(board))] = 1
        else:
            board[minimax(board)] = -1
    if valid:
        results[state(board)[1]+1]+=1
print(results)
print(time.time()-t)
