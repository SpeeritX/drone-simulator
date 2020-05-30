#
# Entity.py
# Drone simulator
# Created by Szymon Gesicki on 28.03.2020.
# All rights reserved.
#
import pygame
from pygame.rect import Rect


class Entity:

    def getShapes(self):
        # virtual method
        raise NotImplementedError()

    def getShape(self):
        # virtual method
        raise NotImplementedError()
