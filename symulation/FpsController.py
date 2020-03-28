#
# FpsController.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
#
import fpstimer
import time

class FpsController:

    def __init__(self):

        self.timer = fpstimer.FPSTimer(60)

        self.lastTime = int(round(time.time() * 1000))

        self.currentFps = 0
        self.lastUpdate = 0
        self.fpsCounter = 0

    def setFps(self, numberOfFps):
        self.timer = fpstimer.FPSTimer(numberOfFps)

    def isReady(self):

        if self.currentFps != self.lastUpdate:
            return True
        else:
            return False

    def getFps(self):
        self.lastUpdate = self.currentFps
        return self.currentFps

    def process(self):

        currentTime = int(round(time.time() * 1000))

        if currentTime - self.lastTime >= 1000:
            self.lastTime = currentTime
            self.currentFps = self.fpsCounter
            self.fpsCounter = 0
        else:
            self.fpsCounter += 1

        self.timer.sleep()




