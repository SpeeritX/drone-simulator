#
# Drone.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#
from SurfaceUtils import blendColors, colorizeSurface, extendSurface, scaleSurface
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


class Drone(Entity):

    DRONE_WIDTH = 144
    DRONE_HEIGHT = 41
    ENGINE_SIZE = 12
    FRICTION = 0.5
    DRONE_BASE_SPRITE_PATH = 'resources/Sprites/DroneBase.png'
    DRONE_L_ROTOR_SPRITE_PATH = 'resources/Sprites/LeftRotor.png'
    DRONE_R_ROTOR_SPRITE_PATH = 'resources/Sprites/RightRotor.png'

    def __init__(self, mass, moment, spaceGravity, position, aiComponent: AIComponent):

        self.aiController = AIController(aiComponent)
        self.body = pymunk.Body(mass, moment)
        self.body.position = position

        self.leftEngine = Engine(self.body, spaceGravity, self.getLeftEnginePosition(), self.ENGINE_SIZE)
        self.rightEngine = Engine(self.body, spaceGravity, self.getRightEnginePosition(), self.ENGINE_SIZE)

        self.chassis = pymunk.Poly(self.body, self.getChassisVec())
        self.chassis.friction = self.FRICTION
        self.currentDecision = AIDecision(0, 0)

        self.droneBase = pygame.image.load(self.DRONE_BASE_SPRITE_PATH).convert_alpha()
        self.leftRotor = pygame.image.load(self.DRONE_L_ROTOR_SPRITE_PATH).convert_alpha()
        self.rightRotor = pygame.image.load(self.DRONE_R_ROTOR_SPRITE_PATH).convert_alpha()

        DebugScreen.getInstance().addInfo("AIComponent", aiComponent.__class__.__name__)

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
            self.aiController.update(DroneState.fromBody(self.body, targetAngle))

    def getDroneSprite(self):
        # create surface
        image = pygame.Surface((self.DRONE_WIDTH, self.DRONE_HEIGHT), pygame.SRCALPHA).convert_alpha()

        # add base
        image.blit(self.droneBase, ((self.DRONE_WIDTH - self.droneBase.get_rect().size[0]) / 2,
                                    self.DRONE_HEIGHT - self.droneBase.get_rect().size[1]))
        # add left rotor
        colorFactor = min(self.leftEngine.getForce() * 15, 1)
        rotorColor = blendColors((0, 255, 0), (240, 30, 0), colorFactor)
        leftRotor = colorizeSurface(self.leftRotor, rotorColor)
        image.blit(leftRotor, (0, 0))

        # add right rotor
        colorFactor = min(self.rightEngine.getForce() * 15, 1)
        rotorColor = blendColors((0, 255, 0), (240, 30, 0), colorFactor)
        rightRotor = colorizeSurface(self.rightRotor, rotorColor)
        image.blit(rightRotor, ((self.DRONE_WIDTH - rightRotor.get_rect().size[0]), 0))

        # apply transformations on surface
        # image = scaleSurface(image, (self.DRONE_WIDTH, self.DRONE_HEIGHT))
        image = extendSurface(image)  # required for smooth edges when rotating
        image = pygame.transform.rotozoom(image, math.degrees(self.body.angle), 1)
        return image.convert_alpha()

    def getLeftEnginePosition(self):
        return [-self.DRONE_WIDTH / 2, 0]

    def getRightEnginePosition(self):
        return [self.DRONE_WIDTH / 2 - self.ENGINE_SIZE, 0]

    def getChassisVec(self):
        return [(-self.DRONE_WIDTH / 2, 0),
                (self.DRONE_WIDTH / 2, 0),
                (self.DRONE_WIDTH / 2, self.DRONE_HEIGHT),
                (-self.DRONE_WIDTH / 2, self.DRONE_HEIGHT)]

    def getShapes(self):
        return [self.body, self.chassis, self.leftEngine.getShape(), self.rightEngine.getShape()],

    def draw(self, screen):
        screen.draw(self.getDroneSprite(), self.body.position)

