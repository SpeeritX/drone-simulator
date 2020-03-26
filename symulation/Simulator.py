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

        self.width, self.height = 2000, 800
        self.offset = 10
        self.enginePower = 0.003
        self.running = False

        self.startPosition = (100, 100)
        self.pyGameInit()

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None

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

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            # python doesn't easily support enums so 1 means left :D
            # maybe someday TODO
            self.physics.engineProcess(self.body, self.enginePower * 0.001, self.drone.getEdges(1))

        if keys[K_RIGHT]:
            self.physics.engineProcess(self.body, self.enginePower * 0.001, self.drone.getEdges(2))

        if keys[K_UP]:
            self.physics.engineProcess(self.body, self.enginePower * 4)

        if self.joystick is not None:
            self.handleJoystick()

    def handleJoystick(self):
        force = -self.joystick.get_axis(2)  # trigger
        leftAxis = -self.joystick.get_axis(1)  # left joystick
        rightAxis = -self.joystick.get_axis(3)  # right joystick

        # ignore if it doesn't exceed threshold, joysticks may be inaccurate
        if leftAxis < 0.01:
            leftAxis = 0

        if rightAxis < 0.01:
            rightAxis = 0

        leftAxis *= 0.02
        rightAxis *= 0.02

        leftAxis += force
        rightAxis += force

        if leftAxis > 0.01:
            self.physics.engineProcess(self.body, self.enginePower * 0.9 * leftAxis, self.drone.getEdges(1))

        if rightAxis > 0.01:
            self.physics.engineProcess(self.body, self.enginePower * 0.9 * rightAxis, self.drone.getEdges(2))

        # print(f'{leftAxis}  -  {rightAxis}')

    def startSimulation(self):

        while self.running:

            self.checkEvents()
            # Clear screen
            self.screen.fill(pygame.color.THECOLORS["black"])

            self.utilities.createHelperLine()

            self.physics.drawStuff()

            pygame.display.flip()

            self.physics.updatePhysics()
