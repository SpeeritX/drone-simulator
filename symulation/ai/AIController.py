#
# AIController.py
# Drone simulator
# Created by Milosz Glowaczewski on 02.04.2020.
# All rights reserved.
# Controls AI calls,
# Updates logic at a fixed intervals, in an another thread
#
from __future__ import annotations

from ai.AIComponent import AIComponent
from ai.AIDecision import AIDecision
from ai.DroneState import DroneState

from timeit import default_timer as timer
from typing import Optional


class AIController:

    # aiComponent - an implementation of AIComponent
    def __init__(self, aiComponent: AIComponent) -> None:
        self.decisionInterval = 1.0/60.0
        self.aiComponent = aiComponent
        self.startDecisionTime = timer()
        self.decision = AIDecision(0, 0)

    def update(self, droneState: DroneState) -> None:
        self.decision = None
        self.startDecisionTime = timer()

        self.decision = self.aiComponent.calculateDecision(droneState)

    # Returns true if decision is ready.
    # Waits for thread to return decision and takes care of fixed update intervals
    def isReady(self):
        elapsedTime = timer() - self.startDecisionTime
        return elapsedTime > self.decisionInterval and self.decision is not None

    # Returns calculated decision
    def getDecision(self) -> AIDecision:
        return self.decision





