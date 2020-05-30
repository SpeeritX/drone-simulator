#
# main.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#

import pygame

from Simulator import Simulator, Ai_type

if __name__ == '__main__':

    fullscreen = False

    pygame.init()
    pygame.font.init()
    simulator = Simulator(Ai_type.fuzzy_logic, fullscreen)
    simulator.startSimulation()
