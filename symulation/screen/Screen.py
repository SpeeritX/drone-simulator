#
# Screen.py
# Drone simulator
# Created by Milosz Glowaczewski on 28.03.2020.
# All rights reserved.
#

from screen.PhysicsDebugDraw import PhysicsDebugDraw

import pygame
import pymunk
from typing import Tuple
from pygame.rect import Rect
from pygame.surface import Surface
from pymunk import Space, Vec2d
from pymunk.pygame_util import DrawOptions


class Screen:

    LINECOLOR = (26, 129, 57)
    SCREENCOLOR = (0, 0, 0)
    SPACE_BETWEEN_LINES = 300
    
    def __init__(self):
        self.surface: Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.offset = Vec2d(0, 0)
        self.physicsDrawOptions = PhysicsDebugDraw(self.surface)

    def drawPhysics(self, physics: Space):
        physics.debug_draw(self.physicsDrawOptions)

    def clear(self):
        self.surface.fill(self.SCREENCOLOR)

        # Draw horizontal lines
        shiftY = self.offset.y % self.SPACE_BETWEEN_LINES
        amount_of_lines_y = int(self.getHeight() / self.SPACE_BETWEEN_LINES)
        for i in range(0, amount_of_lines_y + 2):
            y = (i-1) * self.SPACE_BETWEEN_LINES - shiftY
            pygame.draw.line(self.surface, self.LINECOLOR, (0, y), (self.getWidth(), y), 1)

        # Draw vertical lines
        shiftX = self.offset.x % self.SPACE_BETWEEN_LINES
        amount_of_lines_x = int(self.getWidth() / self.SPACE_BETWEEN_LINES)
        for i in range(0, amount_of_lines_x + 2):
            x = (i - 1) * self.SPACE_BETWEEN_LINES + shiftX
            pygame.draw.line(self.surface, self.LINECOLOR, (x, 0), (x, self.getHeight()), 1)

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
