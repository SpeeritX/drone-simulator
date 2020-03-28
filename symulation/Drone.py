#
# Drone.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
#
import pymunk
import math
from pymunk.vec2d import Vec2d

from DebugScreen import DebugScreen


class Drone:

    def __init__(self, mass, moment, space):

        self.mass = mass
        self.moment = moment
        self.space = space

        self.body = None

        self.chassisWidth, self.chassisHeight = 140, 10
        self.triangleSize = 10

        self.ground_velocity = Vec2d.zero()



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

        self.droneElement = []

        self.body = pymunk.Body(self.mass, self.moment)

        self.body.position = position

        chassis = pymunk.Poly(self.body, self.getChassisVec())
        self.droneElement.append(chassis)

        leftEngine = pymunk.Poly(self.body, self.getLeftEngineVec())
        self.droneElement.append(leftEngine)

        rightEngine = pymunk.Poly(self.body, self.getRightEngineVec())
        self.droneElement.append(rightEngine)

        chassis.friction = 0.5
        leftEngine.friction = 0.5
        rightEngine.friction = 0.5

        self.space.add(self.body, chassis, leftEngine, rightEngine)

        return self.body, self.droneElement

    def getEdges(self, direction):

        if direction == 1:
            return (-self.chassisWidth/2, 20)
        elif direction == 2:
            return (self.chassisWidth/2, 20)
        else:
            assert(False, "wrong direction")



    def leftEngine(self, enginePower):
        DebugScreen.getInstance().addInfo('Left engine', "{:.4f}".format(enginePower))

        power = math.sqrt(enginePower * abs(self.space.gravity.y))

        impulse = (0, self.body.mass * (self.ground_velocity.y + power))

        self.body.apply_impulse_at_local_point(impulse, self.getEdges(1))

    def rightEngine(self, enginePower):
        DebugScreen.getInstance().addInfo('Right engine', "{:.4f}".format(enginePower))
        
        power = math.sqrt(enginePower * abs(self.space.gravity.y))

        impulse = (0, self.body.mass * (self.ground_velocity.y + power))

        self.body.apply_impulse_at_local_point(impulse, self.getEdges(2))



