#
# SimpleAi.py
# Drone simulator
# Created by Milosz Glowaczewski on 02.04.2020.
# All rights reserved.
#

from ai.AIComponent import AIComponent
from ai.AIDecision import AIDecision


# Implementation of PID controller
# It uses only two components: proportional, derivative
# Integral component is not used, because drone is stable without it and it makes implementation easier
class SimpleAI(AIComponent):

    Kp = 65
    Kd = -9

    def __init__(self):
        super().__init__()

    def onCalculateDecision(self) -> AIDecision:
        errorAngle = self.droneState.targetAngle - self.droneState.angle

        # Components:
        # - proportional: errorAngle
        # - derivative: angularVelocity
        # - integral: not used, algorithm is stable without it
        pid = self.Kp * errorAngle + self.Kd * self.droneState.angularVelocity
        pid /= 1000

        return AIDecision(
            abs(pid) if pid < 0 else 0,
            abs(pid) if pid > 0 else 0)
