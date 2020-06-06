#Modul für Matrixrechnung
import numpy as np

#Datei mit Samples
import data

#Sigmoidactivationfunction
#Output zwischen 0 und 1
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

#Ableitung der Sigmoidfunktion
def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

#Trainingsfunktion
#Input: X und Y, Anzahl Epochen und Lernrate
#Output: trainierte Gewichte und Bias als Liste
def train(rawX, rawY, epochs, learningrate):
    X = np.array(rawX)
    Y = np.array(rawY)

    netdims = [len(X[0]),5,len(Y)]
    #zufällige Gewichtsinitialisierung
    w1 = 2 * np.random.random([netdims[1], netdims[0]]) - 1
    w2 = 2 * np.random.random([netdims[2], netdims[1]]) - 1

    #zufällige Biasinitialisierung
    b1 = 2 * np.random.random([netdims[1], 1]) - 1
    b2 = 2 * np.random.random([netdims[2], 1]) - 1

    for i in range(epochs):
        #Feedforward, Output berechnen
        m = len(Y[0])

        a0 = X.T

        z1 = np.dot(w1, a0) + b1
        a1 = sigmoid(z1)

        z2 = np.dot(w2, a1) + b2
        a2 = sigmoid(z2)
        #Fehlerquadrat anhand von Output und Y
        c = np.square(Y - a2)

        #Trainingsupdate für User
        if (i) % (epochs / 10) == 0:
            cost = np.sum(c) / m
            accuracy = 100 - 100 * np.sum(np.abs(np.round(a2) - Y)) / m
            print('Epoch: {:04} Cost: {:.5f} Accuracy: {:.1f}%'.format(i,cost,accuracy))

        #Gradient Descend, partielle Ableitungen nach Gewichten und Bias
        da2 = 2 * (Y - a2)
        dz2 = da2 * sigmoid_derivative(z2)
        dw2 = np.dot(dz2, a1.T) / m
        db2 = np.array([[np.sum(dz2)]]) / m
        #Backpropagation, gleiches für vorherigen Layer
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
#Input: trainierte Gewichte und Bias als Liste, Farbwert
#Output: Vorhersage des NNs für eingegebene Farbe
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

#Test
wl = train(data.X100,data.Y100, 10, 0.5)
