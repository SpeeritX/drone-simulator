#
# DroneState.py
# Drone simulator
# Created by Milosz Glowaczewski on 02.04.2020.
# All rights reserved.
#

from pymunk import Body, Vec2d


class DroneState:

    def __init__(self, body: Body, targetAngle: float):
        self.angle = body.angle
        self.angularVelocity = body.angular_velocity
        self.targetAngle = targetAngle
