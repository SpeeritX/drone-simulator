import math

from DebugScreen import DebugScreen
from ai.AIComponent import AIComponent
from ai.AIDecision import AIDecision
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
import numpy as np


class NeuralNetworkAI(AIComponent):

    def __init__(self):
        super().__init__(False)
        self.model = self.createNeuralNetwork()

    def onCalculateDecision(self) -> AIDecision:

        angularVelocity = self.droneState.angularVelocity
        angularVelocity = self.normalizeAngularVelocity(angularVelocity)

        angle = (math.degrees(self.droneState.angle - self.droneState.targetAngle) + 180) % 360 - 180
        angle = self.normalizeAngle(angle)

        prediction = self.model.predict(np.array([[angularVelocity, angle]]))

        left = self.denormalizeForce(prediction[0, 0])
        right = self.denormalizeForce(prediction[0, 1])

        return AIDecision(left, right)

    def createNeuralNetwork(self):
        print('Training neural network...')

        model = Sequential()
        model.add(Dense(10, input_dim=2, activation='relu'))
        model.add(Dense(4, activation='relu'))
        model.add(Dense(2, activation='sigmoid'))

        model.compile(loss='mse', optimizer='nadam', metrics=['accuracy'])

        dataset = self.prepareTrainingData()
        inputData = dataset[:, 2:4]
        outputData = dataset[:, 0:2]

        model.fit(inputData, outputData, epochs=80, batch_size=20)
        _, accuracy = model.evaluate(inputData, outputData)

        print('Accuracy: %.2f' % (accuracy * 100))
        print('Neural network trained')

        return model

    def prepareTrainingData(self):
        dataset = loadtxt('data/ai_data.csv', delimiter=',')

        for row in dataset:
            angle = self.normalizeAngle(row[2])
            velocity = self.normalizeAngularVelocity(row[3])
            row[2] = angle
            row[3] = velocity
            row[0] = self.normalizeForce(row[0])
            row[1] = self.normalizeForce(row[1])

        dataset = np.unique(dataset, axis=0)

        print(dataset)
        np.random.shuffle(dataset)
        
        return dataset

    def normalizeAngle(self, angle):
        return (np.clip(angle, -3, 3) / 6) + 0.5

    def normalizeAngularVelocity(self, angular_velocity):
        return (np.clip(angular_velocity, -6, 6) / 12) + 0.5

    def normalizeForce(self, force):
        return np.clip((force * 10), 0, 1)

    def denormalizeForce(self, force):
        return np.clip(force, 0, 1) / 10


