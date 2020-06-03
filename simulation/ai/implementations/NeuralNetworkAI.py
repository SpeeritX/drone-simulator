
from ai.AIComponent import AIComponent
from ai.AIDecision import AIDecision
from neural_network.DroneModel import DroneModel


class NeuralNetworkAI(AIComponent):

    def __init__(self):
        super().__init__(False)
        self.model = DroneModel()
        self.model.loadModel('data/drone_model')

    def onCalculateDecision(self) -> AIDecision:

        angle = self.droneState.angle - self.droneState.targetAngle
        angularVelocity = self.droneState.angularVelocity
        left, right = self.model.predict(angle, angularVelocity)

        return AIDecision(left, right)

