from __future__ import annotations

from typing import Optional

from ai.AIComponent import AIComponent
from timeit import default_timer as timer

from ai.AIDecision import AIDecision
from ai.DroneState import DroneState


# Controls AI calls,
# Updates logic at a fixed intervals, in an another thread
class AIController:

    # aiComponent - an implementation of AIComponent
    def __init__(self, aiComponent: AIComponent) -> None:
        self.decisionInterval = 0.1
        self.aiComponent = aiComponent
        self.startDecisionTime = timer()
        self.decision = AIDecision(0, 0)  # Todo: thread safe variable?

    def update(self, droneState: DroneState) -> None:
        self.decision = None
        self.startDecisionTime = timer()

        # Todo: call in a new thread
        self.decision = self.aiComponent.calculateDecision(droneState)

    # Returns true if decision is ready.
    # Waits for thread to return decision and takes care of fixed update intervals
    def isReady(self):
        elapsedTime = timer() - self.startDecisionTime
        return elapsedTime > self.decisionInterval and self.decision is not None

    # Returns calculated decision
    def getDecision(self) -> AIDecision:
        return self.decision





