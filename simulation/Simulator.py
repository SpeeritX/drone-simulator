#
# Simulator.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#
from Platform import Platform
from ai.implementations.FuzzyLogicAI import FuzzyLogicAI
from ai.implementations.NeuralNetworkAI import NeuralNetworkAI
from ai.implementations.ManualAI import ManualAI
from screen.Camera import Camera
from screen.Screen import Screen
from Physics import Physics
from Drone import Drone
from FpsController import FpsController
from DebugScreen import DebugScreen
from ai.implementations.SimpleAI import SimpleAI

from pymunk import Vec2d
from pygame.locals import *
import pygame
import numpy as np

class AIType:
    fuzzyLogic = 1
    neuronNetwork = 2
    simpleAI = 3
    manualAI = 4

class Simulator:
    OFFSET = 10
    DEBUGSCREENSIZE = (350, 200)
    MASS = 1
    MOMENT = 500

    def __init__(self, ai_type, fullscreen):

        self.ai_type = ai_type
        # Screen
        self.running = True
        self.screen = Screen(fullscreen)

        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.startPoistion = (self.width / 2, self.height / 2)
        # FpsController
        self.fpsController = FpsController()
        self.fpsCounter = 0
        self.setFps(60)
        # Physics
        self.physics = Physics()
        # Drone
        self.drone = self.createDrone()
        self.camera = Camera(self.drone.body.position)
        # Platform
        self.platform = Platform()
        # Add element to space
        self.physics.addToSpace(self.platform.getShapes())
        self.physics.addToSpace(self.drone.getShapes())

        # Create Debug Screen
        DebugScreen.getInstance().setSize(self.DEBUGSCREENSIZE)
        DebugScreen.getInstance().setPosition((self.width - self.DEBUGSCREENSIZE[0] - 10, 10))

    def createDrone(self) -> Drone:
        
        if self.ai_type == AIType.fuzzyLogic:
            return Drone(self.MASS, self.MOMENT, self.physics.getGravity(), self.startPoistion, FuzzyLogicAI())
        elif self.ai_type == AIType.neuronNetwork:
            return Drone(self.MASS, self.MOMENT, self.physics.getGravity(), self.startPoistion, NeuralNetworkAI())
        elif self.ai_type == AIType.simpleAI:
            return Drone(self.MASS, self.MOMENT, self.physics.getGravity(), self.startPoistion, SimpleAI())
        elif self.ai_type == AIType.manualAI:
            return Drone(self.MASS, self.MOMENT, self.physics.getGravity(), self.startPoistion, ManualAI())
        raise RuntimeError("Invalid ai type")


    def setFps(self, numberOfFps):
        # Example of changes fps, default 60
        self.fpsController.setFps(numberOfFps)

    def checkEvents(self):

        for event in pygame.event.get():

            if event.type == QUIT or event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):
                self.running = False

            elif event.type == KEYDOWN and event.key == K_r:

                # Remove all Drone elements from the screen
                self.physics.removeObject(self.drone.getShapes())
                # Create new Drone and add to space
                self.drone = self.createDrone()
                self.physics.addToSpace(self.drone.getShapes())

        keys = pygame.key.get_pressed()

        # Engines take values ​​of <0, 1>
        # For physics testing they were introduced permanently

        leftPower = 0.0
        rightPower = 0.0

        if keys[K_UP]:
            leftPower += 0.2
            rightPower += 0.2

        self.drone.leftEngine.setForce(leftPower)
        self.drone.rightEngine.setForce(rightPower)

    def startSimulation(self):

        # Each iteration of this loop will last (at least) 1/(number of FPS | default 60) of a second.
        while self.running:
            self.checkEvents()

            self.drone.update()
            self.camera.update(self.drone.body.position)
            self.draw()
            self.physics.updatePhysics()
            self.fpsController.waitForReady()
            self.fpsController.nextFrame()

    def draw(self):
        self.screen.clear()

        DebugScreen.getInstance().addInfo("x", "{:.2f}".format(self.drone.body.position.x))
        DebugScreen.getInstance().addInfo("y", "{:.2f}".format(self.drone.body.position.y))

        # Set screen offset based on camera position
        self.screen.setOffset(self.camera.getPosition())

        # self.screen.drawPhysics(self.physics.space)
        self.platform.draw(self.screen)
        self.drone.draw(self.screen)

        DebugScreen.getInstance().draw(self.screen)

        self.screen.show()
