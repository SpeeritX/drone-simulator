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

from screen.Screen import Screen


class Simulator:

    def __init__(self):

        self.offset = 10
        self.running = True
        self.startPosition = (400, 100)
        self.screen = Screen()

        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h

        self.fpsController = FpsController()
        self.fpsCounter = 0

        self.physics = Physics()

        self.utilities = Utilities(self.height, self.width, self.offset)

        self.physics.addToSpace(self.utilities.createBorder(self.physics.getSpace()))

        self.drone = Drone(1, 500, self.physics.getSpace())

        DebugScreen.getInstance().setSize((400, 400))
        DebugScreen.getInstance().setPosition((self.width - 400 - 40, 40))

        self.drone.getDrone(self.startPosition)

    def checkEvents(self):

        for event in pygame.event.get():

            if event.type == QUIT or event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):
                self.running = False

            elif event.type == KEYDOWN and event.key == K_r:
                # remove all Drone items from the screen
                for i in self.drone.getShapes():
                    self.physics.removeObject(i)

                self.drone.getDrone(self.startPosition)

        keys = pygame.key.get_pressed()

        # engines take values ​​of <0, 1>
        # for physics testing they were introduced permanently

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

        # Each iteration of this loop will last (at least) 1/60 of a second.
        while self.running:

            if self.fpsController.isReady():
                DebugScreen.getInstance().addInfo("Fps", f'{self.fpsController.getFps()}')

            self.checkEvents()

            self.draw()

            self.physics.updatePhysics()

            self.fpsController.process()

    def draw(self):
        self.screen.clear()

        # self.utilities.createHelperLine((self.camera.offsetX, self.camera.offsetY))

        self.screen.setOffset(self.drone.body.position)
        self.screen.drawPhysics(self.physics.space)
        DebugScreen.getInstance().draw(self.screen)

        self.screen.show()





