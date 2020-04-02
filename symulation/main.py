import pygame

from Simulator import Simulator

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    simulator = Simulator()
    simulator.startSimulation()
