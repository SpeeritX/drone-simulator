from pymunk import Body, Vec2d


class DroneState:

    def __init__(self, body: Body, targetAngle: float):
        self.angle = body.angle
        self.angularVelocity = body.angular_velocity
        self.targetAngle = targetAngle
