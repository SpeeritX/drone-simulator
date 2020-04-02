#
# DebugScreen.py
# Drone simulator
# Created by Milosz Glowaczewski on 28.03.2020.
# All rights reserved.
#
from __future__ import annotations

from screen.Screen import Screen

import pygame
from pymunk.vec2d import Vec2d


class DebugScreen:

    __instance = None
    FONTCOLOR = (200, 200, 200)
    BGCOLOR = (0, 0, 0, 100)
    FONTHEIGHT = 20
    ROWSPACING = 5
    MARGIN = 10

    @staticmethod
    def getInstance() -> DebugScreen:
        """ Static access method. """
        if DebugScreen.__instance is None:
            DebugScreen()
        return DebugScreen.__instance

    def __init__(self) -> None:
        """ Virtually private constructor. """
        if DebugScreen.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DebugScreen.__instance = self

        self.position = Vec2d(0, 0)

        self.infoDict = {}
        self.posDict = {}
        self.infoCounter = 0

        self.font = pygame.font.Font('resources/ShareTechMono-Regular.ttf', self.FONTHEIGHT)
        self.surface: pygame.Surface = pygame.Surface([0, 0])

    def draw(self, screen: Screen) -> None:

        self.surface.fill(self.BGCOLOR)

        i = 0
        for key in sorted(self.infoDict.keys()):
            self._drawInfo(key)
            i += 1

        rect = pygame.Rect(self.position, self.surface.get_size())
        screen.drawUI(self.surface, rect)

    def setPosition(self, position: (float, float)) -> None:
        self.position = position

    def setSize(self, size: (int, int)) -> None:
        self.surface: pygame.Surface = pygame.Surface(size).convert_alpha()

    def addFloatInfo(self, key: str, value: float) -> None:
        self.addInfo(key, "{:.2f}".format(value))

    def addInfo(self, key: str, value: str) -> None:
        self.infoDict[key] = value
        if key not in self.posDict:
            pos = self.infoCounter
            self.infoCounter += 1
            self.posDict[key] = pos

    def _drawInfo(self, key: str) -> None:
        value = self.infoDict[key]
        text = f'{key}: {value}'
        textSurface = self.font.render(text, True, self.FONTCOLOR)
        row = self.posDict[key]
        pos = Vec2d(self.MARGIN, self.MARGIN) + Vec2d(0, row * (self.FONTHEIGHT + self.ROWSPACING))
        self.surface.blit(textSurface, pos)

