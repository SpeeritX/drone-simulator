#
# Manual.py
# Drone simulator
# Created by Milosz Glowaczewski on 02.04.2020.
# All rights reserved.
#
from DebugScreen import DebugScreen
from ai.AIComponent import AIComponent
from ai.AIDecision import AIDecision


class ManualAI(AIComponent):

    def onCalculateDecision(self) -> AIDecision:

        targetAngle = self.droneState.targetAngle

        if targetAngle > 0:
            return AIDecision(0.015, 0)
        elif targetAngle < 0:
            return AIDecision(0, 0.015)
        else:
            return AIDecision(0, 0)
