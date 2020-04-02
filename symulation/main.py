#
# main.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#

import pygame

from Simulator import Simulator

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    simulator = Simulator()
    simulator.startSimulation()
