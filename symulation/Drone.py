#
# Drone.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#

from ai.AIComponent import AIComponent
from ai.AIController import AIController
from ai.AIDecision import AIDecision
from ai.DroneState import DroneState
from Entity import Entity
from DebugScreen import DebugScreen
from Engine import Engine

import pymunk
import math
from pymunk.vec2d import Vec2d
from pygame.locals import *
import pygame


class Drone(Entity):

    CHASSISWIDTH = 140
    CHASSISHEIGHT = 10
    ENGINESIZE = 10
    FRICTION = 0.5

    def __init__(self, mass, moment, spaceGravity, position, aiComponent: AIComponent):

        self.aiController = AIController(aiComponent)
        self.body = pymunk.Body(mass, moment)
        self.body.position = position

        self.chassisWidth, self.chassisHeight = self.CHASSISWIDTH, self.CHASSISHEIGHT
        self.engineSize = self.ENGINESIZE

        self.leftEngine = Engine(self.body, spaceGravity, self.getLeftEnginePosition(), self.engineSize)
        self.rightEngine = Engine(self.body, spaceGravity, self.getRightEnginePosition(), self.engineSize)

        self.chassis = pymunk.Poly(self.body, self.getChassisVec())
        self.chassis.friction = self.FRICTION
        self.currentDecision = AIDecision(0, 0)

    def update(self):

        self.leftEngine.setForce(self.currentDecision.leftEngine)
        self.rightEngine.setForce(self.currentDecision.rightEngine)

        if self.aiController.isReady():
            keys = pygame.key.get_pressed()
            targetAngle = 0
            if keys[K_LEFT]:
                targetAngle = 1

            if keys[K_RIGHT]:
                targetAngle = -1

            self.currentDecision = self.aiController.getDecision()
            self.aiController.update(DroneState(self.body, targetAngle))

    def getLeftEnginePosition(self):
        return [-self.chassisWidth / 2, 0]

    def getRightEnginePosition(self):
        return [self.chassisWidth / 2 - self.engineSize, 0]

    def getChassisVec(self):
        return [(-self.chassisWidth / 2, 0),
                ( self.chassisWidth / 2, 0),
                ( self.chassisWidth / 2, self.chassisHeight),
                (-self.chassisWidth / 2, self.chassisHeight)]

    def getShapes(self):
        return [self.body, self.chassis, self.leftEngine.getShape(), self.rightEngine.getShape()]

