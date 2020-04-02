#
# PhysicDebugDraw.py
# Drone simulator
# Created by Milosz Glowaczewski on 28.03.2020.
# All rights reserved.
#

from pymunk import Vec2d
from pymunk.pygame_util import DrawOptions


class PhysicsDebugDraw(DrawOptions):

    def __init__(self, screen):
        super().__init__(screen)
        self.offset = Vec2d(0, 0)

    def draw_circle(self, pos, angle, radius, outline_color, fill_color):
        super().draw_circle(self.to_camera(pos), angle, radius, outline_color, fill_color)

    def draw_segment(self, a, b, color):
        super().draw_segment(self.to_camera(a), self.to_camera(b), color)

    def draw_fat_segment(self, a, b, radius, outline_color, fill_color):
        super().draw_fat_segment(self.to_camera(a), self.to_camera(b), radius, outline_color, fill_color)

    def draw_polygon(self, verts, radius, outline_color, fill_color):
        camera_verts = [self.to_camera(v) for v in verts]
        super().draw_polygon(camera_verts, radius, outline_color, fill_color)

    def draw_dot(self, size, pos, color):
        super().draw_dot(size, self.to_camera(pos), color)

    def to_camera(self, pos):
        return pos[0] + self.offset[0], pos[1] + self.offset[1]

    def set_offset(self, offset: Vec2d):
        self.offset = offset

