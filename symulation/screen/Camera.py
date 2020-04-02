#
# DebugScreen.py
# Drone simulator
# Created by Milosz Glowaczewski on 28.03.2020.
# All rights reserved.
#

from pygame.rect import Rect
from pygame.surface import Surface
from pymunk import Vec2d


class Camera:
    # Distance from center of the screen required for camera to start following the player.
    MIN_DIST_TO_MOVE_CAM = 100
    # Speed of the camera movement, should be much lower than 1
    SPEED = 0.001

    def __init__(self, offset):
        self.position = Vec2d(offset)

    def draw(self, image: Surface, rect: Rect):
        pass

    def update(self, dronePosition):
        distance = self.position - dronePosition

        # Check distance between drone and camera. Move camera only if it is to far from drone
        if distance.length > self.MIN_DIST_TO_MOVE_CAM:
            x = (distance - distance.normalized() * self.MIN_DIST_TO_MOVE_CAM)
            shift = distance.normalized() * (x ** 2) * self.SPEED
            if shift.length > distance.length / 2:
                shift = distance / 2
            self.position -= shift

    def getPosition(self):
        return Vec2d(self.position)
