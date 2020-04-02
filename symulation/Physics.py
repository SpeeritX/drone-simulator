#
# Physics.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#

import pymunk
import math
from pymunk.vec2d import Vec2d


class Physics:
    
    SPACEGRAVITY = (0, -900)

    def __init__(self):

        self.space = pymunk.Space()
        self.space.gravity = self.SPACEGRAVITY
        self.ground_velocity = Vec2d.zero()

        self.fps = 60
        self.dt = 1. / self.fps

    def getSpace(self):
        return self.space
        
    def setFps(self, numberOfFps):
        self.fps = numberOfFps
        self.dt = 1. / self.fps

    def addToSpace(self, object):
        if type(object) is list:
            for i in object:
                self.space.add(i)
        else:
            self.space.add(object)

    def updatePhysics(self):
        self.space.step(self.dt)

    def removeObject(self, object):
        if type(object) is list:
            for i in object:
                self.space.remove(i)
        else:
            self.space.remove(object)

    def getGravity(self):
        return self.space.gravity.y

    def getStaticBody(self):
        return self.space.static_body

    # Todo: connect with player
    # function limiting velocity of a body
    # def limit_velocity(body: Body, gravity, damping, dt):
    #     max_velocity = 1000
    #     pymunk.Body.update_velocity(body, gravity, damping, dt)
    #     velocityLength = body.velocity.length
    #     if velocityLength > max_velocity:
    #         scale = max_velocity / velocityLength
    #         body.velocity = body.velocity * scale
    #
    #     angularLength = body.angular_velocity
    #     if angularLength > 20:
    #         body.angular_velocity = 20
    #
    #     if angularLength < -20:
    #         body.angular_velocity = -20
    #
    #
    #
    #     DebugScreen.getInstance().addFloatInfo("angular velocity", self.body.angular_velocity)
    #     DebugScreen.getInstance().addFloatInfo("velocity X", self.body.velocity.x)
    #     DebugScreen.getInstance().addFloatInfo("velocity y", self.body.velocity.y)


