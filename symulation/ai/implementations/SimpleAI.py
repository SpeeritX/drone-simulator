from DebugScreen import DebugScreen
from ai.AIComponent import AIComponent
from ai.AIDecision import AIDecision


class SimpleAI(AIComponent):

    def onCalculateDecision(self) -> AIDecision:
        # DebugScreen.getInstance().addInfo("target angle", self.droneState.targetAngle)
        DebugScreen.getInstance().addInfo("angle", "{:.4f}".format(self.droneState.angle))
        # DebugScreen.getInstance().addInfo("angle vel", self.droneState.angularVelocity)

        targetAngle = self.droneState.targetAngle

        diff = targetAngle - self.droneState.angle
        if diff < 0:
            diff -= self.droneState.angularVelocity * 0.4
        elif diff > 0:
            diff -= self.droneState.angularVelocity * 0.4
        # DebugScreen.getInstance().addInfo("diff", "{:.2f}".format(diff))

        force = self.calculateForce(diff)
        DebugScreen.getInstance().addInfo("force", "{:.6f}".format(force))

        if diff > 0:
            return AIDecision(0, force)
        elif diff < 0:
            return AIDecision(force, 0)

        return AIDecision(0, 0)

    def calculateForce(self, diff):
        return (abs(diff) * 0.05) ** 2
