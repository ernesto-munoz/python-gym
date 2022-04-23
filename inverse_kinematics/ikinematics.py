import math

import pygame
from pygame.math import Vector2


class Bone:
    def __init__(self, x: float, y: float, length: float, angle: float, parent_bone=None, children_bones=None):
        # parenting relationships
        self._parent_bone = parent_bone
        self._children_bones = children_bones or list()

        self._begin = Vector2(x, y)
        self._end = Vector2()
        self._length = length
        self._angle = angle
        self._calculate_end()
        self._follow_target = None
        self._color = (255, 0, 0)

        self._screen_surface = pygame.display.get_surface()

    def _calculate_end(self) -> None:
        dx = self._length * math.cos(self._angle)
        dy = self._length * math.sin(self._angle)
        self._end.x = self._begin.x + dx
        self._end.y = self._begin.y + dy

        if self._children_bones is not None:
            for each_child_bone in self._children_bones:
                each_child_bone.begin = self._end

    def follow(self, target: Vector2) -> None:
        # calculate direction from beginning to the target position
        direction = (target - self._begin).normalize()
        # calculate the new angle of the bone to be facing the target
        self._angle = -math.radians(direction.angle_to(Vector2(1, 0)))
        # calculate the new end of the bone
        self._calculate_end()
        # change the direction vector to have the length of the bone and
        # inverse to be pointing from target to the beginning
        direction.scale_to_length(self._length)
        direction = direction * -1
        # calculate the new beginning of the bone
        self._begin = target + direction

        if self._parent_bone is not None:
            self._parent_bone.follow(target=self._begin)

    def set_follow_target(self, target: Vector2):
        self._follow_target = target

    def add_child(self, bone):
        if self._children_bones is None:
            self._children_bones = list()
        self._children_bones.append(bone)

    @property
    def begin(self) -> Vector2:
        return self._begin

    @begin.setter
    def begin(self, value: Vector2):
        self._begin = value
        self._calculate_end()

    @property
    def color(self) -> tuple:
        return self._color

    @color.setter
    def color(self, value: tuple):
        self._color = value

    def event(self, event) -> None:
        pass

    def loop(self) -> None:
        if self._follow_target is not None:
            self.follow(target=self._follow_target)

    def render(self) -> None:

        direction = (self._end - self._begin).normalize()
        points = [self._begin,
                  self._begin + direction.rotate(35) * 0.25 * self._length,
                  self._end,
                  self._begin + direction.rotate(-35) * 0.25 * self._length
                  ]
        pygame.draw.aalines(self._screen_surface, self._color, True, points)

    def cleanup(self) -> None:
        pass
