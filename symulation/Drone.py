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
    CHASSISHEIGHT = 41
    ENGINESIZE = 12
    FRICTION = 0.5
    DRONE_BASE_SPRITE_PATH = 'resources\\Sprites\\DroneBase.png'
    DRONE_L_ROTOR_SPRITE_PATH = 'resources\\Sprites\\LeftRotor.png'
    DRONE_R_ROTOR_SPRITE_PATH = 'resources\\Sprites\\RightRotor.png'

    def __init__(self, mass, moment, spaceGravity, position, aiComponent: AIComponent):

        self.aiController = AIController(aiComponent)
        self.body = pymunk.Body(mass, moment)
        self.body.position = position

        self.leftEngine = Engine(self.body, spaceGravity, self.getLeftEnginePosition(), self.ENGINESIZE)
        self.rightEngine = Engine(self.body, spaceGravity, self.getRightEnginePosition(), self.ENGINESIZE)

        self.chassis = pymunk.Poly(self.body, self.getChassisVec())
        self.chassis.friction = self.FRICTION
        self.currentDecision = AIDecision(0, 0)

        self.droneBase = pygame.image.load(self.DRONE_BASE_SPRITE_PATH)
        self.leftRotor = pygame.image.load(self.DRONE_L_ROTOR_SPRITE_PATH)
        self.rightRotor = pygame.image.load(self.DRONE_R_ROTOR_SPRITE_PATH)
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

    def colorizeSurface(self, surface, color):
        rect = surface.get_rect()
        colorImage = pygame.Surface(rect.size).convert_alpha()
        colorImage.fill(color)
        colorImage.blit(surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return colorImage

    def blendColors(self, a, b, t):
        """ Linearly interpolates between colors a and b by t.
            t is clamped between 0 and 1. When t is 0 color is a. When t is 1 color is b.
            Applies calculated color on surface """
        result = tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
        return result

    def extendSurface(self, surface, size=4):
        rect = surface.get_rect()
        newSurface = pygame.Surface((rect.size[0] + size, rect.size[1] + size), pygame.SRCALPHA)
        newSurface.blit(surface, (size/2, size/2))
        return newSurface

    def getDroneSprite(self):
        # set scale
        #scaledImage = scaleImage(self.droneBase, (self.CHASSISWIDTH, self.CHASSISHEIGHT))
        # set rotation

        # create surface
        image = pygame.Surface((self.CHASSISWIDTH, self.CHASSISHEIGHT), pygame.SRCALPHA)
        # add base
        image.blit(self.droneBase, ((self.CHASSISWIDTH - self.droneBase.get_rect().size[0])/2,
                                    self.CHASSISHEIGHT - self.droneBase.get_rect().size[1]))
        # add left rotor
        colorFactor = min(self.leftEngine.getForce() * 20, 1)
        rotorColor = self.blendColors((0, 255, 0), (240, 30, 0), colorFactor)
        leftRotor = self.colorizeSurface(self.leftRotor, rotorColor)
        image.blit(leftRotor, (0, 0))

        # add right rotor
        colorFactor = min(self.rightEngine.getForce() * 20, 1)
        rotorColor = self.blendColors((0, 255, 0), (240, 30, 0), colorFactor)
        rightRotor = self.colorizeSurface(self.rightRotor, rotorColor)
        image.blit(rightRotor, ((self.CHASSISWIDTH - rightRotor.get_rect().size[0]), 0))
        finalImage = self.extendSurface(image)
        finalImage = pygame.transform.rotozoom(finalImage, math.degrees(self.body.angle), 1)
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

