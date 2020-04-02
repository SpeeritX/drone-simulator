#
# Utilities.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#

import pymunk
import pygame

class Utilities:

    WALLWIDTH = 20
    FRICTION = 1
    GROUP = 1
    COLOR = (24, 119, 53, 0)

    def __init__(self, height, width, offset):
        self.height = height
        self.width = width
        self.offset = offset

    def getBorderShape(self, staticBody):
        # box walls
        staticBorder = [pymunk.Segment(staticBody, (self.offset, self.offset),
                                                          (self.width - self.offset, self.offset), self.WALLWIDTH)]

        for s in staticBorder:
            s.friction = self.FRICTION
            s.group = self.GROUP
            s.color = self.COLOR

        return staticBorder