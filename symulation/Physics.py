#
# Physics.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#
import pymunk
import math
from pymunk.pygame_util import DrawOptions


class Physics:

    def __init__(self, screen):

        self.space = pymunk.Space()
        self.space.gravity = 0, -900
        self.screen = screen
        self.draw_options = DrawOptions(self.screen)

        self.fps = 60
        self.dt = 1. / self.fps

    def setFps(self, numberOfFps):
        self.fps = numberOfFps
        self.dt = 1. / self.fps

    def addToSpace(self, object):
        if type(object) is list:
            for i in object:
                self.space.add(i)
        else:
            self.space.add(object)

    def drawStuff(self):
        self.space.debug_draw(self.draw_options)

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

