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

import csv


class AIComponent:

    def __init__(self, logEnabled=False) -> None:
        self.droneState: Optional[DroneState] = None
        self.logEnabled = logEnabled

        if logEnabled:
            self._file = open('data/ai_data.csv', 'w', newline='')
            self._csv = csv.writer(self._file)
            # self._csv.writerow(['left_engine', 'right_engine', 'angular_velocity', 'angle'])

    def calculateDecision(self, droneState: DroneState) -> AIDecision:
        self.droneState = droneState
        decision = self.onCalculateDecision()
        if self.logEnabled:
            self._csv.writerow([decision.leftEngine, decision.rightEngine,
                                droneState.angle - droneState.targetAngle, droneState.angularVelocity])
        return decision

    def onCalculateDecision(self) -> AIDecision:
        raise NotImplementedError("calculateDecision is not implemented")
