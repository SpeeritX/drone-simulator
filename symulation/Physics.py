#
# Physics.py
# Drone simulator
# Created by Szymon Gesicki on 01.03.2020.
#
import pymunk
import math
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import DrawOptions

class Physics:
    def __init__(self, screen):

        # Physics stuff
        self.space = pymunk.Space()
        self.space.gravity = 0, -20
        self.screen = screen
        self.draw_options = DrawOptions(self.screen)
        self.ground_velocity = Vec2d.zero()

        self.fps = 60
        self.dt = 1. / self.fps

    def engineProcess( self, body, power, vec=(0,0)):

        enginePower = math.sqrt(2.0 * power * abs(self.space.gravity.y))

        impulse = (0, body.mass * (self.ground_velocity.y + enginePower))

        body.apply_impulse_at_local_point(impulse, vec)

    # Todo
    # test and fix this method
    def engineProcessForce(self, body, vec):

        assert(False, "Method is still not implemented")
        body.apply_force_at_local_point((7000, 8000), vec)


    def getSpace(self):
        return self.space

    def addToSpace(self, object):
        self.space.add(object)

    def drawStuff(self):
        self.space.debug_draw(self.draw_options)

    def updatePhysics(self):
        self.space.step(self.dt)
        # clock.tick(fps)


