import math
import pygame
from pygame.math import Vector2
from obstacle import Obstacle


class Emitter:

    def __init__(self, position: Vector2):
        self._position = position
        self._screen_surface = pygame.display.get_surface()
        self._rays = list()

        self._visible_points = list()

        for angle in range(0, 360, 2):
            self._rays.append(
                Ray(position=self._position, direction_angle=math.radians(angle))
            )

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, value: Vector2):
        self._position = value
        for each_ray in self._rays:
            each_ray.position = self._position

    def render(self) -> None:
        color = (220, 70, 120)
        pygame.draw.circle(self._screen_surface, color, self._position, 5, width=1)

        color = (240, 240, 240)
        for each_visible_point in self._visible_points:
            pygame.draw.aaline(self._screen_surface, color, self.position, each_visible_point)

    def look(self, obstacles: list) -> None:
        self._visible_points = list()
        for each_ray in self._rays:
            closest_point = None
            for each_obstacle in obstacles:
                point = each_ray.cast(obstacle=each_obstacle)
                if point is None:
                    continue
                if closest_point is None:
                    closest_point = point
                else:
                    if self._position.distance_to(point) < self._position.distance_to(closest_point):
                        closest_point = point
            if closest_point is not None:
                self._visible_points.append(closest_point)


class Ray:
    def __init__(self, position: Vector2, direction_angle: float):
        self._position = position
        self._direction = Vector2(math.cos(direction_angle), math.sin(direction_angle)).normalize()
        self._screen_surface = pygame.display.get_surface()

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, value: Vector2):
        self._position = value

    @property
    def direction(self) -> Vector2:
        return self._direction

    @direction.setter
    def direction(self, value: Vector2):
        self._direction = value

    def render(self) -> None:
        color = (240, 240, 240)
        pygame.draw.circle(self._screen_surface, color, self._position, 3, width=1)
        pygame.draw.aaline(self._screen_surface, color, self._position, self._position + self._direction * 20)

    def cast(self, obstacle: Obstacle):
        # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
        x1 = obstacle.begin.x
        y1 = obstacle.begin.y
        x2 = obstacle.end.x
        y2 = obstacle.end.y

        x3 = self.position.x
        y3 = self.position.y
        x4 = self.position.x + self._direction.x
        y4 = self.position.y + self._direction.y

        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        # parallel lines
        if denominator == 0:
            return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

        if 0 < t < 1 and u > 0:
            return Vector2(
                x1 + t * (x2 - x1),
                y1 + t * (y2 - y1)
            )

        return None
