#
# AiComponent.py
# Drone simulator
# Created by Milosz Glowaczewski on 02.04.2020.
# All rights reserved.
# Abstract class, that calculates ai decision
#

from ai.AIDecision import AIDecision
from ai.DroneState import DroneState

from typing import Optional


class AIComponent:

    def __init__(self) -> None:
        self.droneState: Optional[DroneState] = None

    def calculateDecision(self, droneState: DroneState) -> AIDecision:
        self.droneState = droneState
        return self.onCalculateDecision()

    def onCalculateDecision(self) -> AIDecision:
        raise NotImplementedError("calculateDecision is not implemented")
