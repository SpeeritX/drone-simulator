#
# Engine.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#

from Entity import Entity
from DebugScreen import DebugScreen

import math
import pymunk


class Engine(Entity):
    FRICTION = 0.5

    # TODO: Engine should not be 'physical'
    def __init__(self, body, spaceGravity, position, engineSize):
        self.spaceGravity = spaceGravity
        self.body = body
        self.position = position
        self.engineSize = engineSize
        self.strPosition = "Right" if self.position[0] > 0 else "Left"

        self.direction = (self.position[0], 20) if self.strPosition == "Left" \
            else (self.position[0] + self.engineSize, 20)

        self.engineShape = pymunk.Poly(self.body, self.getVec())
        self.engineShape.friction = self.FRICTION

    def getVec(self):
        # draws the engine from the given point to the right
        return [(self.position[0], self.position[1]),
                (self.position[0] + self.engineSize, self.position[1]),
                (self.position[0] + self.engineSize / 2, -self.engineSize + self.position[1])]

    def getShape(self):
        return self.engineShape

    def setForce(self, enginePower):
        DebugScreen.getInstance().addInfo("{} engine ".format(self.strPosition), "{:.4f}".format(enginePower))

        power = math.sqrt(enginePower * abs(self.spaceGravity))

        impulse = (0, self.body.mass * power)

        self.body.apply_impulse_at_local_point(impulse, self.direction)
