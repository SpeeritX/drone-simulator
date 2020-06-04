import csv
from random import random

import numpy as np

from ai.DroneState import DroneState
from ai.implementations.FuzzyLogicAI import FuzzyLogicAI


def normalizeAngle(angle):
    return (angle / 6) + 0.5


def normalizeAngularVelocity(angular_velocity):
    return (angular_velocity / 12) + 0.5


def normalizeForce(force):
    return force * 10


def denormalizeForce(force):
    return force / 10


def loadTrainingData(fileName):
    dataset = np.loadtxt(fileName, delimiter=',')

    for row in dataset:
        angle = normalizeAngle(row[2])
        velocity = normalizeAngularVelocity(row[3])
        row[2] = angle
        row[3] = velocity
        row[0] = normalizeForce(row[0])
        row[1] = normalizeForce(row[1])

    dataset = np.unique(dataset, axis=0)

    np.random.shuffle(dataset)
    print(dataset)

    return dataset


def generateTrainingData(fileName, ai=FuzzyLogicAI(), N=4000):
    print('Generating AI training data')

    with open(fileName, 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(0, N):
            if i % (N // 5) == 0:
                print(f"Progress: {int((i / N) * 100)}%")
            angle = random() * 6 - 3
            angularVelocity = random() * 12 - 6

            if random() < 0.5:
                angle /= 4
                angularVelocity /= 4
            elif random() < 0.75:
                angle /= 2
                angularVelocity /= 2

            decision = ai.calculateDecision(DroneState(angle, angularVelocity, 0))

            writer.writerow([decision.leftEngine, decision.rightEngine, angle, angularVelocity])
            writer.writerow([decision.rightEngine, decision.leftEngine, -angle, -angularVelocity])


