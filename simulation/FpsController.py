#
# FpsController.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
# All rights reserved.
#
from DebugScreen import DebugScreen

import fpstimer
import time

class FpsController:

    def __init__(self):

        self.timer = fpstimer.FPSTimer(60)

        self.lastTime = int(round(time.time() * 1000))

        self.currentFps = 0
        self.fpsCounter = 0

    def setFps(self, numberOfFps):
        self.timer = fpstimer.FPSTimer(numberOfFps)

    def waitForReady(self):
        self.timer.sleep()

    def getFps(self):
        return self.currentFps

    def nextFrame(self):
        currentTime = int(round(time.time() * 1000))

        if currentTime - self.lastTime >= 1000:
            self.currentFps = self.fpsCounter
            DebugScreen.getInstance().addInfo("Fps", f'{self.currentFps}')
            self.lastTime = currentTime
            self.fpsCounter = 0
        else:
            self.fpsCounter += 1

        




