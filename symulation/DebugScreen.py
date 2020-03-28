from __future__ import annotations
import pygame
from pymunk.vec2d import Vec2d


class DebugScreen:
    __instance = None

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
        self.fontHeight = 20
        self.rowSpacing = 5
        self.margin = 10

        self.infoDict = {}
        self.posDict = {}
        self.infoCounter = 0
        self.fontColor = (200, 200, 200)
        self.bgColor = (0, 0, 0, 100)

        self.font = pygame.font.Font('resources/ShareTechMono-Regular.ttf', self.fontHeight)
        self.surface: pygame.Surface = pygame.Surface([0, 0])

    def draw(self, screen: pygame.Surface) -> None:

        self.surface.fill(self.bgColor)

        i = 0
        for key in sorted(self.infoDict.keys()):
            self.drawInfo(key)
            i += 1

        rect = pygame.Rect(self.position, self.surface.get_size())
        screen.blit(self.surface, rect)

    def setPosition(self, position: (float, float)) -> None:
        self.position = position

    def setSize(self, size: (int, int)) -> None:
        self.surface: pygame.Surface = pygame.Surface(size).convert_alpha()

    def addInfo(self, key: str, value: str) -> None:
        self.infoDict[key] = value
        if key not in self.posDict:
            pos = self.infoCounter
            self.infoCounter += 1
            self.posDict[key] = pos

    def drawInfo(self, key: str) -> None:
        value = self.infoDict[key]
        text = f'{key}: {value}'
        textSurface = self.font.render(text, True, self.fontColor)
        row = self.posDict[key]
        pos = Vec2d(self.margin, self.margin) + Vec2d(0, row * (self.fontHeight+self.rowSpacing))
        self.surface.blit(textSurface, pos)

