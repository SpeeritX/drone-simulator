#
# main.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#

import pygame
import argparse

from Simulator import Simulator

if __name__ == '__main__':

    fullscreen = False

    parser = argparse.ArgumentParser(description='Drone simulator')
    parser.add_argument('-ai','--aitype', 
        help='AI type(1-Fuzzy logic, 2-Neural network, 3-PID, 4-Manual',
        required=False, default="1")
    args = vars(parser.parse_args())

    pygame.init()
    pygame.font.init()
    simulator = Simulator(int(args['aitype']), fullscreen)
    simulator.startSimulation()
