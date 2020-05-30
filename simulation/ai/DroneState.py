#
# DroneState.py
# Drone simulator
# Created by Milosz Glowaczewski on 02.04.2020.
# All rights reserved.
#

from pymunk import Body, Vec2d


class DroneState:

    def __init__(self, angle: float, angularVelocity: float, targetAngle: float):
        self.angle: float = angle
        self.angularVelocity: float = angularVelocity
        self.targetAngle: float = targetAngle

    @staticmethod
    def fromBody(body: Body, targetAngle: float):
        return DroneState(body.angle, body.angular_velocity, targetAngle)



