#
# Utilities.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
#
import pymunk
import pygame

class Utilities:

    def __init__(self, screen, height, width, offset):
        self.screen = screen
        self.height = height
        self.width = width
        self.offset = offset

    def createHelperLine(self):

        for y in range(self.offset, self.height - self.offset, int(self.width / 12)):
            color = pygame.color.THECOLORS['darkgrey']
            pygame.draw.line(self.screen, color, (self.offset, y), (self.width - self.offset, y), 1)

    def createBorder(self, space):
        # box walls
        staticBorder = [pymunk.Segment(space.static_body, (self.offset, self.offset),
                                                          (self.width - self.offset, self.offset), 3)

                      , pymunk.Segment(space.static_body, (self.width - self.offset, self.offset),
                                                          (self.width - self.offset, self.height - self.offset), 3)

                      , pymunk.Segment(space.static_body, (self.width - self.offset, self.height - self.offset),
                                                          (self.offset, self.height - self.offset), 3)

                      , pymunk.Segment(space.static_body, (self.offset, self.height - self.offset),
                                                          (self.offset, self.offset), 3)]

        for s in staticBorder:
            s.friction = 10.
            s.group = 1

        return staticBorder