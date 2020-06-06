import numpy as np
import tensorflow.keras as keras
import copy
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

def possibleScores(board):
    scores = []
    for i in emptyCells(board):
        newBoard = [i for i in board]
        newBoard[i] = len(emptyCells(board)) % 2 * 2 - 1
        scores.append(bestMove(newBoard))
    return scores

def bestMove(board):
    done, win = state(board)

    if done:
        return win

    scores = possibleScores(board)

    if len(emptyCells(board)) % 2 == 1:
        return np.max(scores)
    else:
        return np.min(scores)

def minimax(board):
    c = emptyCells(board)
    if len(ec) == 0:
        return 0
    if len(ec) % 2 == 1:
        return ec[np.argmax(possibleScores(board))]
    else:
        return ec[np.argmin(possibleScores(board))]

def dataset(n):
    X, Y = [], []
    for i in range(n):
        board = [0,0,0,0,0,0,0,0,0]
        while not state(board)[0]:
            eC = emptyCells(board)
            p = 2*int(i%2)-1
            if len(eC) % 2 == i%2:
                if len(eC)==9:
                    mm = 0
                else:
                    mm = minimax(board)
                X.append([j for j in board])
                Y.append(mm)
                board[mm] = p
            else:
                board[np.random.choice(eC)] = -p
    return np.array(X), np.array(Y)

def model(x,y,e):
    model = keras.models.Sequential()

    model.add(keras.layers.Dense(units=9, activation='relu', input_dim=9))
    model.add(keras.layers.Dense(units=18, activation='relu'))
    model.add(keras.layers.Dense(units=18, activation='relu'))
    model.add(keras.layers.Dense(units=9, activation='softmax'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(x, y, epochs=e, verbose=True)

    return model

def neuralnet(model,board):
    return np.argmax(model.predict([[board]]))

x,y = dataset(1000)
m = model(x,y,1000)

t=time.time()
results = [0,0,0]
for i in range(1000):
    if i%10==0:
        print(f'{i} {results}')
    board = [0,0,0,0,0,0,0,0,0]
    valid = True
    while not state(board)[0] and valid:
        ec = (emptyCells(board))
        if len(ec) % 2 == 1:
            board[np.random.choice(emptyCells(board))] = 1
        else:
            x = neuralnet(m,board)
            if x in ec:
                board[x] = -1
            else:
                results[2]+=1
                valid=False
    if valid:
        results[state(board)[1]+1]+=1

print(results)
print(time.time()-t)
