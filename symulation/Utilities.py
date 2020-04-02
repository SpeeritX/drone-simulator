#
# Utilities.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#
import pymunk
import pygame

class Utilities:

    def __init__(self, height, width, offset):
        self.height = height
        self.width = width
        self.offset = offset
        self.wallWidth = 20

    def getBorderShape(self, staticBody):
        # box walls
        staticBorder = [pymunk.Segment(staticBody, (self.offset, self.offset),
                                                          (self.width - self.offset, self.offset), self.wallWidth)]

        for s in staticBorder:
            s.friction = 1
            s.group = 1
            s.color = 24, 119, 53

        return staticBorder