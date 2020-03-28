#
# Simulator.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
#
from Physics import *
from Utilities import *
from Drone import *
from FpsController import FpsController 
from pygame.locals import *
import pygame

class Simulator:

    def __init__(self):

        self.offset = 10
        self.running = False
        self.startPosition = (400, 100)
        self.pyGameInit()

        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h

        self.fpsController = FpsController()
        self.fpsCounter = 0

        self.physics = Physics(self.screen)

        self.utilities = Utilities( self.screen, self.height, self.width, self.offset)

        self.physics.addToSpace(self.utilities.createBorder(self.physics.getSpace()))

        self.drone = Drone(1, 500, self.physics.getSpace())

        DebugScreen.getInstance().setSize((400, 400))
        DebugScreen.getInstance().setPosition((self.width - 400 - 40, 40))

        self.body, self.droneElement = self.drone.getDrone(self.startPosition)

    def pyGameInit(self):

        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN )
        self.running = True

    def checkEvents(self):

        for event in pygame.event.get():

            if event.type == QUIT or event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):
                self.running = False

            elif event.type == KEYDOWN and event.key == K_r:

                self.physics.removeObject(self.body)

                # remove all Drone items from the screen
                for i in self.droneElement:
                    self.physics.removeObject(i)

                self.body, self.droneElement = self.drone.getDrone(self.startPosition)

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

        self.drone.leftEngine(leftPower)
        self.drone.rightEngine(rightPower)


    def startSimulation(self):


        # Each iteration of this loop will last (at least) 1/60 of a second.
        while self.running:

            if self.fpsController.isReady():
                DebugScreen.getInstance().addInfo("Fps", f'{self.fpsController.getFps()}')


            self.checkEvents()
            # Clear screen
            self.screen.fill(pygame.color.THECOLORS["black"])

            self.utilities.createHelperLine()

            self.physics.drawStuff()
            DebugScreen.getInstance().draw(self.screen)


            pygame.display.flip()
            self.physics.updatePhysics()

            self.fpsController.process()





