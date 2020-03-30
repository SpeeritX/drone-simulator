#
# Simulator.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#
from Physics import Physics
from Utilities import Utilities
from Drone import Drone
from FpsController import FpsController 
from DebugScreen import DebugScreen

from pygame.locals import *
import pygame

class Simulator:

    def __init__(self):
        # Screen
        self.offset = 10
        self.running = False
        self.startPosition = (400, 100)
        self.pyGameInit()
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        # FpsController
        self.fpsController = FpsController()
        self.fpsCounter = 0
        # Physics
        self.physics = Physics(self.screen)
        # Utilities
        self.utilities = Utilities( self.screen, self.height, self.width, self.offset)
        # Drone
        self.drone = Drone(1, 500, self.physics.getGravity(), self.startPosition)
        # Add element to space
        self.physics.addToSpace(self.utilities.getBorderShape(self.physics.getStaticBody()))
        self.physics.addToSpace(self.drone.getShapes())
        # Create Debug Screen
        DebugScreen.getInstance().setSize((400, 400))
        DebugScreen.getInstance().setPosition((self.width - 400 - 40, 40))

    def setFps(self, numberOfFps):
        # Example of changes fps, default 60
        self.physics.setFps(numberOfFps)
        self.fpsController.setFps(numberOfFps)

    def pyGameInit(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN )
        self.running = True

    def checkEvents(self):

        for event in pygame.event.get():

            if event.type == QUIT or event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):
                self.running = False

            elif event.type == KEYDOWN and event.key == K_r:

                # Remove all Drone elements from the screen
                self.physics.removeObject(self.drone.getShapes())
                # Create new Drone and add to space
                self.drone = Drone(1, 500, self.physics.getGravity(), self.startPosition)
                self.physics.addToSpace(self.drone.getShapes())

        keys = pygame.key.get_pressed()

        # Engines take values ​​of <0, 1>
        # For physics testing they were introduced permanently

        leftPower = 0.0
        rightPower = 0.0

        if keys[K_LEFT]:
            leftPower += 0.01

        if keys[K_RIGHT]:
            rightPower += 0.01

        if keys[K_UP]:
            leftPower += 0.2
            rightPower += 0.2

        self.drone.leftEngine.setForce(leftPower)
        self.drone.rightEngine.setForce(rightPower)

    def startSimulation(self):

        # Each iteration of this loop will last (at least) 1/(number of FPS | default 60) of a second.
        while self.running:
                
            self.checkEvents()
            # Clear screen
            self.screen.fill(pygame.color.THECOLORS["black"])

            self.utilities.drawHelperLine()

            self.physics.drawStuff()

            DebugScreen.getInstance().draw(self.screen)

            pygame.display.flip()

            self.physics.updatePhysics()

            self.fpsController.waitForReady()

            self.fpsController.nextFrame()





