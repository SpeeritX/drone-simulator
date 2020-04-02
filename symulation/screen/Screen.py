#
# DebugScreen.py
# Drone simulator
# Created by Milosz Glowaczewski on 28.03.2020.
# All rights reserved.
#
from typing import Tuple

import pygame
import pymunk
from pygame.rect import Rect
from pygame.surface import Surface
from pymunk import Space, Vec2d
from pymunk.pygame_util import DrawOptions

from screen.PhysicsDebugDraw import PhysicsDebugDraw


class Screen:
    def __init__(self):
        self.surface: Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.surface: Surface = pygame.display.set_mode((1400, 900))
        self.offset = Vec2d(0, 0)
        self.physicsDrawOptions = PhysicsDebugDraw(self.surface)

    def drawPhysics(self, physics: Space):
        physics.debug_draw(self.physicsDrawOptions)

    def clear(self):
        self.surface.fill((0, 0, 0))
        for y in range(0, self.getHeight(), int(self.getWidth() / 12)):
            color = 26, 129, 57
            pygame.draw.line(self.surface, color, (0, y - self.offset.y),
                             (self.getWidth(), y - self.offset.y), 1)

    def show(self):
        pygame.display.flip()

    def draw(self, image: Surface, pos):
        self.surface.blit(image, pos)

    def drawUI(self, image: Surface, rect: Rect):
        self.surface.blit(image, rect)

    def drawRect(self, color, rect: Rect):
        if len(color) <= 3:
            pygame.draw.rect(self.surface, color, rect)
        else:
            s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            s.fill(color)
            self.surface.blit(s, rect)

    def setOffset(self, offset):
        # Center screen
        self.offset.x = -offset.x + self.getWidth()/2
        self.offset.y = -offset.y + self.getHeight()/2

        self.physicsDrawOptions.set_offset(self.offset)

    def getWidth(self):
        return self.surface.get_width()

    def getHeight(self):
        return self.surface.get_height()