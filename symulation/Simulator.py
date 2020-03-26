#
# Simulator.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
#
from Physics import *
from Utilities import *
from Drone import *

from pygame.locals import *
import pygame

class Simulator:

    def __init__(self):

        self.width, self.height = 800, 600
        self.offset = 10
        self.enginePower = 2
        self.running = False

        self.startPosition = (100, 100)
        self.pyGameInit()

        self.physics = Physics(self.screen)

        self.utilities = Utilities( self.screen, self.height, self.width, self.offset)

        self.physics.addToSpace(self.utilities.createBorder(self.physics.getSpace()))

        self.drone = Drone(1, 500, self.physics.getSpace())

        self.body = self.drone.getDrone(self.startPosition)

    def pyGameInit(self):

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        # self.clock = pygame.time.Clock()
        self.running = True

    def checkEvents(self):

        for event in pygame.event.get():

            if event.type == QUIT or event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):
                self.running = False

            elif event.type == KEYDOWN and event.key == K_r:
                self.body = self.drone.getDrone(self.startPosition)

            elif event.type == KEYDOWN and event.key == K_LEFT:
                # python doesn't easily support enums so 1 means left :D
                # maybe someday TODO
                self.physics.engineProcess( self.body, self.enginePower, self.drone.getEdges(1))

            elif event.type == KEYDOWN and event.key == K_RIGHT:
                self.physics.engineProcess( self.body, self.enginePower, self.drone.getEdges(2))

            elif event.type == KEYDOWN and event.key == K_UP:
                self.physics.engineProcess( self.body, self.enginePower*8)

    def startSimulation(self):

        while self.running:

            self.checkEvents()

            # Clear screen
            self.screen.fill(pygame.color.THECOLORS["black"])

            self.utilities.createHelperLine()

            self.physics.drawStuff()

            pygame.display.flip()

            self.physics.updatePhysics()
