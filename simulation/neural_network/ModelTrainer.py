from ai.DroneState import DroneState
from ai.implementations.NeuralNetworkAI import NeuralNetworkAI
from ai.implementations.SimpleAI import SimpleAI
from neural_network import TrainingData
from neural_network.DroneModel import DroneModel


def generateTraining(ai, N):
    TrainingData.generateTrainingData('data/ai_data.csv', ai, N)


def trainDrone(epochs=10, batch_size=32):
    dataset = TrainingData.loadTrainingData('data/ai_data.csv')
    droneModel = DroneModel()
    droneModel.train(dataset, epochs, batch_size)
    droneModel.saveModel('data/drone_model')


def compare():
    pidAi = SimpleAI()
    nnAi = NeuralNetworkAI()

    states = [DroneState(-1, 0, 0), DroneState(1, 0, 0), DroneState(0, 1, 0), DroneState(1, 1, 0)]

    for state in states:
        decisionPid = pidAi.calculateDecision(state)
        decisionNn = nnAi.calculateDecision(state)

        print("Decision: {:.4f}, {:.4f}  /  {:.4f}, {:.4f}".format(
            decisionPid.leftEngine, decisionPid.rightEngine, decisionNn.leftEngine, decisionNn.rightEngine))




# Data:
# generateTraining(SimpleAI(), 10000)
# trainDrone(5, 16)

# generateTraining(FuzzyLogic(), 10000)
# trainDrone(5, 16)
