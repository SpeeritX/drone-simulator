#
# DebugScreen.py
# Drone simulator
# Created by Milosz Glowaczewski on 28.03.2020.
# All rights reserved.
#

import pygame
import typing
from pygame.rect import Rect
from pygame.surface import Surface

class Camera:
    def __init__(self, width: typing.List, height):

        self.width = width
        self.height = height

        self.offsetX = 0
        self.offsetY = 0
        self.surface = Surface()

    def draw(self, image: Surface, rect: Rect):
        pass

