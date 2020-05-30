import csv
from random import random

from ai.DroneState import DroneState
from ai.implementations.SimpleAI import SimpleAI
from ai.implementations.FuzzyLogicAI import FuzzyLogicAI


# Generates data for training drone
# csv format: [leftEngine, rightEngine, angle, angularVelocity]
def main():
    ai = FuzzyLogicAI()

    N = 2000
    print('Generating AI training data')

    with open('data/ai_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(0, N):
            if i % (N // 20) == 0:
                print(f"Progress: {int((i / N)*100)}%")
            angle = random() * 6 - 3
            angularVelocity = random() * 12 - 6

            decision = ai.calculateDecision(DroneState(angle, angularVelocity, 0))

            writer.writerow([decision.leftEngine, decision.rightEngine, angle, angularVelocity])


if __name__ == "__main__":
    main()

