#
# Drone.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#

from Entity import Entity
from DebugScreen import DebugScreen
from Engine import Engine

import pymunk
import math
from pymunk.vec2d import Vec2d

class Drone(Entity):

    def __init__(self, mass, moment, spaceGravity, position):

        self.body = pymunk.Body(mass, moment)
        self.body.position = position

        self.chassisWidth, self.chassisHeight = 140, 10
        self.engineSize = 10

        self.leftEngine = Engine(self.body, spaceGravity, self.getLeftEnginePosition(), self.engineSize)
        self.rightEngine = Engine(self.body, spaceGravity, self.getRightEnginePosition(), self.engineSize)

        self.chassis = pymunk.Poly(self.body, self.getChassisVec())
        self.chassis.friction = 0.5
        self.chassis.color = 31, 159, 69

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

