#
# Drone.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
#
import pymunk

class Drone:

    def __init__(self, mass, moment, space):

        self.mass = mass
        self.moment = moment
        self.space = space

        self.body = None

        self.chassisWidth, self.chassisHeight = 140, 10
        self.triangleSize = 10

    def getChassisVec(self):

        return [(-self.chassisWidth / 2, self.triangleSize),
                ( self.chassisWidth / 2, self.triangleSize),
                ( self.chassisWidth / 2, self.triangleSize + self.chassisHeight),
                (-self.chassisWidth / 2, self.triangleSize + self.chassisHeight)]

    def getLeftEngineVec(self):
        return [(-self.chassisWidth / 2, self.triangleSize),
                (-self.chassisWidth / 2 + self.triangleSize, self.triangleSize),
                (-self.chassisWidth / 2 + self.triangleSize / 2, 0)]

    def getRightEngineVec(self):
        return [(self.chassisWidth / 2, self.triangleSize),
                (self.chassisWidth / 2 - self.triangleSize, self.triangleSize),
                (self.chassisWidth / 2 - self.triangleSize / 2, 0)]

    def getDrone(self, position):

        self.body = pymunk.Body(self.mass, self.moment)

        self.body.position = position

        chassis = pymunk.Poly(self.body, self.getChassisVec())

        leftEngine = pymunk.Poly(self.body, self.getLeftEngineVec())

        rightEngine = pymunk.Poly(self.body, self.getRightEngineVec())

        leftEngine.friction = 0.5
        rightEngine.friction = 0.5

        self.space.add(self.body, chassis, leftEngine, rightEngine)

        return self.body

    def getEdges(self, direction):
        if direction == 1:
            return (-self.chassisWidth/2, 20)
        elif direction == 2:
            return (self.chassisWidth/2, 20)
        else:
            assert(False, "wrong direction")



