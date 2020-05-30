#
# Drone.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#
from pymunk import Body

from ai.AIComponent import AIComponent
from ai.AIController import AIController
from ai.AIDecision import AIDecision
from ai.DroneState import DroneState
from Entity import Entity
from DebugScreen import DebugScreen
from Engine import Engine

import pymunk
import math
from pymunk.vec2d import Vec2d
from pygame.locals import *
import pygame


class Platform(Entity):

    WIDTH = 1604
    HEIGHT = 46
    FRICTION = 1
    PLATFORM_SPRITE_PATH = 'resources/Sprites/Platform.png'

    def __init__(self, position=(WIDTH/2, 0)):

        self.position = position
        self.body = pymunk.Body(body_type=Body.STATIC)
        self.shape = pymunk.Poly(self.body, self.getBodyVertices())
        self.shape.friction = self.FRICTION
        self.image = pygame.image.load(self.PLATFORM_SPRITE_PATH)
        # set scale
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))

    def getBodyVertices(self):
        return [(-self.WIDTH / 2, -self.HEIGHT/2),
                (self.WIDTH / 2, -self.HEIGHT/2),
                (self.WIDTH / 2, self.HEIGHT/2),
                (-self.WIDTH / 2, self.HEIGHT/2)]

    def getShapes(self):
        return [self.body, self.shape],

    def draw(self, screen):
        # set rotation
        finalImage = pygame.transform.rotozoom(self.image, math.degrees(self.body.angle), 1)
        # draw
        screen.draw(finalImage.convert_alpha(), self.body.position)

