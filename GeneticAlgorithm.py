import numpy as np
import copy
import time

def r(x):
    return range(len(x))

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

def convert(board):
    c = [0 if i == -1 else i for i in board]
    c+= [0 if i == 1 else i for i in board]
    return c

def relu(x):
    return np.max(x,0)

def softmax(x):
    x = x[0]
    ex = np.exp(x - np.max(x))
    return ex / np.sum(ex,axis=0)

class NeuralNet:
    def __init__(self, w=[]):
        self.w = w
        if len(w) == 0:
            self.w0 = 2* np.random.random((18,18)) - 1
            self.b0 = 2* np.random.random((1,18)) - 1
            self.w1 = 2* np.random.random((18,18)) - 1
            self.b1 = 2* np.random.random((1,18)) - 1
            self.w2 = 2* np.random.random((18,9)) - 1
            self.b2 = 2* np.random.random((1,9)) - 1
        else:
            self.w0 = np.array(w[0])
            self.b0 = np.array(w[1])
            self.w1 = np.array(w[2])
            self.b1 = np.array(w[3])
            self.w2 = np.array(w[4])
            self.b2 = np.array(w[5])

    def getw(self):
        return [self.w0,self.b0,self.w1,self.b1,self.w2,self.b2]

    def move(self,board):
        a0 = np.array(convert(board))
        a1 = relu(np.dot(a0,self.w0)+self.b0)
        a2 = relu(np.dot(a1,self.w1)+self.b1)
        a3 = softmax(np.dot(a2,self.w2)+self.b2)
        return np.argmax(a3)

    def test(self,enemys):
        score=0
        for enemy in enemys:
            for i in range(2):
                board = [0,0,0,0,0,0,0,0,0]
                valid = True
                while not state(board)[0] and valid:
                    ec = emptyCells(board)
                    if len(ec)%2 == i:
                        m = self.move(board)
                        if m not in ec:
                            score-=1
                            valid = False
                        board[m]=-1+2*i
                    else:
                        m = enemy.move(board)
                        if m not in ec:
                            score+=1
                            valid = False
                        board[m]=1-2*i
                if valid:
                    if i:
                        score-=state(board)[1]
                    else:
                        score+=state(board)[1]
        return score

class Generation:
    def __init__(self,population=[],lastpop=None,):
        if len(population) == 0:
            self.population = [NeuralNet() for i in range(100)]
            self.origin = True
        else:
            self.population = population
            self.fitness = [i.test(lastpop) for i in population]
            self.origin = False

    def getpop(self):
        return self.population

    def metrics(self):
        return (np.max(self.fitness),np.mean(self.fitness))

    def elite(self):
        if self.origin:
            elite=self.population[:8]
        else:
            elite = []
            for i in np.argsort(self.fitness,kind='heapsort')[::-1][:8]:
                elite.append(self.population[i])
        return elite

    def generatenextgen(self):
        parents = self.elite()+[NeuralNet() for i in range(2)]
        nextgen = [i for i in parents]
        for x in r(parents):
            for y in r(parents):
                if x<y:
                    a = parents[x].getw()
                    b = parents[y].getw()
                    for m in range(2):
                        c = []
                        for i in r(a):
                            c.append([])
                            for j in r(a[i]):
                                c[i].append([])
                                for k in r(a[i][j]):
                                    if np.random.random()<0.5:
                                        c[i][j].append(a[i][j][k])
                                    else:
                                        c[i][j].append(b[i][j][k])

                        nextgen.append(NeuralNet(c))
        return Generation(nextgen,self.population)

t=time.time()

g0 = Generation()

g = copy.deepcopy(g0)
for i in range(100):
    g = g.generatenextgen()
    print(f'g{i+1}: {g.metrics()} {g.elite()[0].test(g0.getpop())} {time.time()-t:.2f}')
