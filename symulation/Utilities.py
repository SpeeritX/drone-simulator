#
# Utilities.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#
import pymunk
import pygame

class Utilities:

    def __init__(self, screen, height, width, offset):
        self.screen = screen
        self.height = height
        self.width = width
        self.offset = offset
        self.wallWidth = 20

    def createHelperLine(self):

        for y in range(self.offset, self.height - self.offset, int(self.width / 12)):
            color = 26, 129, 57, 255
            pygame.draw.line(self.screen, color, (self.offset, y), (self.width - self.offset, y), 1)

    def createBorder(self, space):
        # box walls
        staticBorder = [pymunk.Segment(space.static_body, (self.offset, self.offset),
                                                          (self.width - self.offset, self.offset), self.wallWidth)

                      , pymunk.Segment(space.static_body, (self.width - self.offset, self.offset),
                                                          (self.width - self.offset, self.height - self.offset),
                                       self.wallWidth)

                      , pymunk.Segment(space.static_body, (self.width - self.offset, self.height - self.offset),
                                                          (self.offset, self.height - self.offset), self.wallWidth)

                      , pymunk.Segment(space.static_body, (self.offset, self.height - self.offset),
                                                          (self.offset, self.offset), self.wallWidth)]

        for s in staticBorder:
            s.friction = 1
            s.group = 1
            s.color = 24, 119, 53

        return staticBorder