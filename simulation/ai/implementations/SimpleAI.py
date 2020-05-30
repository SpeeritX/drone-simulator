#
# SimpleAi.py
# Drone simulator
# Created by Milosz Glowaczewski on 02.04.2020.
# All rights reserved.
#
from DebugScreen import DebugScreen
from ai.AIComponent import AIComponent
from ai.AIDecision import AIDecision


class SimpleAI(AIComponent):

    Kp = 65
    Ki = -9
    Kd = -0.00000

    ERROR_AMOUNT: int = 10

    def __init__(self):
        super().__init__()
        self.errors = [0] * self.ERROR_AMOUNT
        self.errorNumber: int = 0
        self.lastSpeed = 0

    def onCalculateDecision(self) -> AIDecision:

        acc = self.lastSpeed - self.droneState.angularVelocity

        targetAngle = self.droneState.targetAngle

        diff = targetAngle - self.droneState.angle
        self.errors[self.errorNumber % self.ERROR_AMOUNT] = diff
        self.errorNumber += 1

        pid = self.Kp * diff + self.Ki * self.droneState.angularVelocity + self.Kd * acc

        self.lastSpeed = self.droneState.angularVelocity

        if pid > 0:
            return AIDecision(0, abs(pid)/1000)
        elif pid < 0:
            return AIDecision(abs(pid)/1000, 0)

        return AIDecision(0, 0)

    def calculateForce(self, diff):
        return (abs(diff) * 0.05) ** 2