#
# Drone.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#

from DebugScreen import DebugScreen
from Engine import Engine

import pymunk
import math
from pymunk.vec2d import Vec2d

class Drone:

    def __init__(self, mass, moment, space):

        self.mass = mass
        self.moment = moment
        self.space = space
        self.body = None

        self.chassisWidth, self.chassisHeight = 140, 10
        self.engineSize = 10

        self.leftEngine = None
        self.rightEngine = None
        self.chassis = None

    def getLeftEnginePosition(self):
        return [-self.chassisWidth / 2, 0]

    def getRightEnginePosition(self):
        return [self.chassisWidth / 2 - self.engineSize, 0]

    def getChassisVec(self):
        return [(-self.chassisWidth / 2, 0),
                ( self.chassisWidth / 2, 0),
                ( self.chassisWidth / 2, self.chassisHeight),
                (-self.chassisWidth / 2, self.chassisHeight)]

    def createChassis(self):
        self.chassis = pymunk.Poly(self.body, self.getChassisVec())
        self.chassis.friction = 0.5
        self.chassis.color = 31, 159, 69
        return self.chassis

    def getDrone(self, position):

        self.body = self.getBody()
        self.body.position = position

        self.leftEngine = Engine(self.body, self.space.gravity.y, self.getLeftEnginePosition(), self.engineSize)
        self.rightEngine = Engine(self.body, self.space.gravity.y, self.getRightEnginePosition(), self.engineSize)

        shapes = self.createShapes()

        for i in shapes:
            self.space.add(i)

        return shapes

    def getBody(self):
        return pymunk.Body(self.mass, self.moment)

    def createShapes(self):
        return [self.body, self.leftEngine.createShape(), self.rightEngine.createShape(), self.createChassis()]

    def getShapes(self):
        return [self.body, self.leftEngine.getShape(), self.rightEngine.getShape(), self.chassis]


