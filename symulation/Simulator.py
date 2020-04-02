#
# Simulator.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#
from pymunk import Vec2d

from Physics import Physics
from Utilities import Utilities
from Drone import Drone
from FpsController import FpsController 
from DebugScreen import DebugScreen

from pygame.locals import *
import pygame

from screen.Camera import Camera
from screen.Screen import Screen


class Simulator:

    def __init__(self):
        # Screen
        self.offset = 10
        self.running = True
        self.startPosition = (400, 100)

        self.screen = Screen()

        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        # FpsController
        self.fpsController = FpsController()
        self.fpsCounter = 0
        # Physics
        self.physics = Physics()
        # Utilities
        self.utilities = Utilities(self.height, self.width, self.offset)
        # Drone
        self.drone = Drone(1, 500, self.physics.getGravity(), self.startPosition)
        self.camera = Camera(self.drone.body.position)
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
            self.camera.update(self.drone.body.position)
            self.draw()
            self.physics.updatePhysics()
            self.fpsController.waitForReady()
            self.fpsController.nextFrame()

    def draw(self):
        self.screen.clear()

        # self.utilities.createHelperLine((self.camera.offsetX, self.camera.offsetY))

        # Set screen offset based on camera position
        self.screen.setOffset(self.camera.getPosition())
        self.screen.drawPhysics(self.physics.space)
        DebugScreen.getInstance().draw(self.screen)

        self.screen.show()





