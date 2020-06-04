import math

from keras import Sequential
from keras.layers import Dense
import numpy as np
from tensorflow import keras

from neural_network import TrainingData


class DroneModel:

    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(8, input_dim=2, activation='relu'))
        self.model.add(Dense(8, activation='relu'))
        self.model.add(Dense(8, activation='relu'))
        self.model.add(Dense(2))

        optimizer = keras.optimizers.Nadam(learning_rate=0.001)
        self.model.compile(loss='mse', optimizer=optimizer, metrics=[keras.metrics.MeanAbsoluteError()])

    def loadModel(self, file):
        self.model.load_weights(file)

    def train(self, dataset, epochs, batch_size):
        trainData = dataset[:3*len(dataset)//4]
        testData = dataset[3*len(dataset)//4:]

        inputData = trainData[:, 2:4]
        outputData = trainData[:, 0:2]
        self.model.fit(inputData, outputData, epochs=epochs, batch_size=batch_size)

        inputData = testData[:, 2:4]
        outputData = testData[:, 0:2]
        _, accuracy = self.model.evaluate(inputData, outputData)

        print('Accuracy: %.2f' % (accuracy * 100))
        print('Neural network trained')

    def saveModel(self, file):
        self.model.save_weights(file)
        print('Model saved')

    def predict(self, angle, angularVelocity):
        angle = TrainingData.normalizeAngle(angle)
        angularVelocity = TrainingData.normalizeAngularVelocity(angularVelocity)

        prediction = self.model.predict(np.array([[angle, angularVelocity]]))

        left = TrainingData.denormalizeForce(prediction[0, 0])
        right = TrainingData.denormalizeForce(prediction[0, 1])

        if left < 0:
            left = 0

        if right < 0:
            right = 0

        return left, right
