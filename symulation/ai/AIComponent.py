from typing import Optional


# Abstract class, that calculates ai decision
from ai.AIDecision import AIDecision
from ai.DroneState import DroneState


class AIComponent:

    def __init__(self) -> None:
        self.droneState: Optional[DroneState] = None

    def calculateDecision(self, droneState: DroneState) -> AIDecision:
        self.droneState = droneState
        return self.onCalculateDecision()

    def onCalculateDecision(self) -> AIDecision:
        raise NotImplementedError("calculateDecision is not implemented")
