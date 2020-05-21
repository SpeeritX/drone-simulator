#
# Drone.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#

from ai.AIComponent import AIComponent
from ai.AIController import AIController
from ai.AIDecision import AIDecision
from ai.DroneState import DroneState
from Entity import Entity, scaleImage
from DebugScreen import DebugScreen
from Engine import Engine

import pymunk
import math
from pymunk.vec2d import Vec2d
from pygame.locals import *
import pygame


class Drone(Entity):

    CHASSISWIDTH = 144
    CHASSISHEIGHT = 10
    ENGINESIZE = 12
    FRICTION = 0.5
    DRONE_SPRITE_PATH = 'resources\\Sprites\\Drone.png'

    def __init__(self, mass, moment, spaceGravity, position, aiComponent: AIComponent):

        self.aiController = AIController(aiComponent)
        self.body = pymunk.Body(mass, moment)
        self.body.position = position

        self.leftEngine = Engine(self.body, spaceGravity, self.getLeftEnginePosition(), self.ENGINESIZE)
        self.rightEngine = Engine(self.body, spaceGravity, self.getRightEnginePosition(), self.ENGINESIZE)

        self.chassis = pymunk.Poly(self.body, self.getChassisVec())
        self.chassis.friction = self.FRICTION
        self.currentDecision = AIDecision(0, 0)

        self.image = pygame.image.load(self.DRONE_SPRITE_PATH)
        self.blendColors((255, 0, 0), (0, 255, 0), 0.5)
        # self.sprite.set_colorkey((0, 0, 0))

    def update(self):

        self.leftEngine.setForce(self.currentDecision.leftEngine)
        self.rightEngine.setForce(self.currentDecision.rightEngine)

        if self.aiController.isReady():
            keys = pygame.key.get_pressed()
            targetAngle = 0
            if keys[K_LEFT]:
                targetAngle = 1

            if keys[K_RIGHT]:
                targetAngle = -1

            self.currentDecision = self.aiController.getDecision()
            self.aiController.update(DroneState(self.body, targetAngle))

    def blendColors(self, a, b, t):
        """ Linearly interpolates between colors a and b by t.
            t is clamped between 0 and 1. When t is 0 returns a. When t is 1 returns b. """
        result = tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
        return result

    def getDroneSprite(self):
        # set scale
        scaledImage = scaleImage(self.image, (self.CHASSISWIDTH, self.CHASSISHEIGHT))
        # set rotation
        finalImage = pygame.transform.rotozoom(scaledImage, math.degrees(self.body.angle), 1)
        rect = finalImage.get_rect()
        colorImage = pygame.Surface(rect.size).convert_alpha()

        colorFactor = min(max(self.leftEngine.getForce(), self.rightEngine.getForce())*20, 1)
        newColor = self.blendColors((0, 255, 0), (240, 30, 0), colorFactor)
        colorImage.fill(newColor)
        finalImage.blit(colorImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return finalImage.convert_alpha()

    def getLeftEnginePosition(self):
        return [-self.CHASSISWIDTH / 2, 0]

    def getRightEnginePosition(self):
        return [self.CHASSISWIDTH / 2 - self.ENGINESIZE, 0]

    # TODO: Vec? Is that a right name? Maybe Vertices would be better?
    def getChassisVec(self):
        return [(-self.CHASSISWIDTH / 2, 0),
                ( self.CHASSISWIDTH / 2, 0),
                ( self.CHASSISWIDTH / 2, self.CHASSISHEIGHT),
                (-self.CHASSISWIDTH / 2, self.CHASSISHEIGHT)]

    def getShapes(self):
        return [self.body, self.chassis, self.leftEngine.getShape(), self.rightEngine.getShape()],

    def draw(self, screen):
        screen.draw(self.getDroneSprite(), self.body.position)

