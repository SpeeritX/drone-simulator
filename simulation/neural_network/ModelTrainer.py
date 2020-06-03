from neural_network import TrainingData
from neural_network.DroneModel import DroneModel


def generateTraining(ai, N):
    TrainingData.generateTrainingData('data/ai_data.csv', ai, N)


def trainDrone(epochs=10, batch_size=32):
    dataset = TrainingData.loadTrainingData('data/ai_data.csv')
    droneModel = DroneModel()
    droneModel.train(dataset, epochs, batch_size)
    droneModel.saveModel('data/drone_model')


# Data:
# generateTraining(SimpleAI(), 20000)
# trainDrone(25, 8)

# generateTraining(FuzzyLogic(), 20000)
# trainDrone(25, 8)
