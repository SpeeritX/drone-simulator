#
# DebugScreen.py
# Drone simulator
# Created by Milosz Glowaczewski on 28.03.2020.
# All rights reserved.
#
from math import sqrt

import numpy
import pygame
import typing
from pygame.rect import Rect
from pygame.surface import Surface


class Camera:
    # Distance from center of the screen required for camera to start following the player.
    MIN_DIST_TO_MOVE_CAM = 100
    CAMERA_SPEED = 10

    def __init__(self, width: typing.List, height):

        self.width = width
        self.height = height

        self.offsetX = 0
        self.offsetY = 0
        self.surface = Surface()

    def draw(self, image: Surface, rect: Rect):
        pass

    def update(self, playerPosX, playerPosY):
        distX = self.offsetX - playerPosX
        distY = self.offsetY - playerPosY

        distance = sqrt(distX ** 2 + distY ** 2)

        if distance <= self.MIN_DIST_TO_MOVE_CAM:
            pass




    def getOffset(self):
        return self.offsetX, self.offsetY


