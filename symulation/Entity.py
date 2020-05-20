#
# Entity.py
# Drone simulator
# Created by Szymon Gesicki on 28.03.2020.
# All rights reserved.
#
import pygame
from pygame.rect import Rect


def scaleImage(sprite, rect):
    spriteSize = sprite.get_rect().size
    xRatio = spriteSize[0] / rect[0]
    yRatio = spriteSize[1] / rect[1]
    ratio = min(xRatio, yRatio)
    new_size = (int(spriteSize[0] / ratio), int(spriteSize[1] / ratio))
    return pygame.transform.scale(sprite, new_size)


class Entity:

    def getShapes(self):
        # virtual method
        raise NotImplementedError()

    # TODO: Why? No every entity object needs that?
    def getShape(self):
        # virtual method
        raise NotImplementedError()
