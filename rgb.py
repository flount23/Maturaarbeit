#Modul für Matrixrechnung
import numpy as np

#Datei mit Samples
import data

#Sigmoidfunktion
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

#Sigmoidfunktion abgeleitet
def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

#Trainingsfunktion
def train(X, Y, epochs, learningrate):
    #zufällige Gewichtsinitialisierung
    w1 = 2 * np.random.random([5, 3]) - 1
    w2 = 2 * np.random.random([1, 5]) - 1

    #zufällige Biasinitialisierung
    b1 = 2 * np.random.random([5, 1]) - 1
    b2 = 2 * np.random.random([1, 1]) - 1

    #Hauptschleife
    for i in range(epochs):
        #Feedforward
        m = len(Y[0])

        a0 = np.array(X).T

        z1 = np.dot(w1, a0) + b1
        a1 = sigmoid(z1)

        z2 = np.dot(w2, a1) + b2
        a2 = sigmoid(z2)

        #Cost
        c = np.square(np.array(Y) - a2)

        #Output von Cost und Accuracy über Zeit
        if (i) % (epochs / 10) == 0:
        	cost = np.sum(c) / m
        	accuracy = 100 - 100 * np.sum(np.abs(np.round(a2) - Y)) / m
        	print('Epoch: {:04} Cost: {:.5f} Accuracy: {:.1f}%'.format(i,cost,accuracy))

        #Backpropagation
        da2 = 2 * (Y - a2)
        dz2 = da2 * sigmoid_derivative(z2)
        dw2 = np.dot(dz2, a1.T) / m
        db2 = np.array([[np.sum(dz2)]]) / m

        da1 = np.dot(w2.T, dz2)
        dz1 = da1 * sigmoid_derivative(z1)
        dw1 = np.dot(dz1, a0.T) / m
        db1 = np.array([[np.sum(dz1)]]) / m

        #Gewichts- und Biasanpassung
        w1 += learningrate * dw1
        b1 += learningrate * db1

        w2 += learningrate * dw2
        b2 += learningrate * db2

    return [w1, w2, b1, b2]

#Testfunktion
def test(weightList, color):
    #Gewichtsinitialisierung nach Eingabe
    w1, w2, b1, b2 = weightList[0], weightList[1], weightList[2], weightList[3]
    rgb = np.array(color)/255
    a0 = rgb

    #Feedforward
    z1 = np.dot(w1, a0) + b1
    a1 = sigmoid(z1)

    z2 = np.dot(w2, a1) + b2
    a2 = sigmoid(z2)

    return a2

#wl = train(data.XXX,data.YYY, 1000, 0.5)
#print(test(wl, [[249],[206],[63]]))
