import random
import time
from dataclasses import dataclass
from turtle import width
import pygame

from enum import Enum


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Rectangle:
    x: float
    y: float
    width: float
    height: float

    def contains(self, point: Point) -> bool:
        return point.x >= self.x - self.width and point.x < self.x + self.width and point.y >= self.y - self.height and point.y < self.y + self.height

    def intersects(self, other):
        return other.x - other.width < self.x + self.width or other.x + other.width > self.x - self.width or other.y - other.height < self.y + self.height or other.y + other.height > self.y - self.height


class Quadtree:

    def __init__(self, boundary: Rectangle, capacity=4):
        self._boundary = boundary
        self._capacity = capacity
        self._points = list()
        self._is_subdivided = False

        self._render_boundary: pygame.Rect = pygame.Rect(
            self._boundary.x - self._boundary.width,
            self._boundary.y - self._boundary.height,
            self._boundary.width * 2,
            self._boundary.height * 2
        )

    def event(self, event) -> None:
        pass

    def loop(self) -> None:
        pass

    def render(self) -> None:
        pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), self._render_boundary, 1)
        if self._is_subdivided is True:
            self._north_west.render()
            self._north_east.render()
            self._south_west.render()
            self._south_east.render()

        for each_point in self._points:
            pygame.draw.circle(pygame.display.get_surface(), (255, 255, 255), (each_point.x, each_point.y), 2)

    def cleanup(self) -> None:
        pass

    def insert(self, point: Point) -> bool:

        if self._boundary.contains(point=point) is False:
            return False

        if len(self._points) < self._capacity:
            self._points.append(point)
        else:
            if self._is_subdivided is False:
                self._subdivide()

            self._north_west.insert(point=point)
            self._north_east.insert(point=point)
            self._south_west.insert(point=point)
            self._south_east.insert(point=point)

        return True

    def _subdivide(self):
        x = self._boundary.x
        y = self._boundary.y
        width = self._boundary.width
        height = self._boundary.height

        self._north_west = Quadtree(boundary=Rectangle(x - width / 2, y - height / 2, width / 2, height / 2), capacity=self._capacity)
        self._north_east = Quadtree(boundary=Rectangle(x + width / 2, y - height / 2, width / 2, height / 2), capacity=self._capacity)
        self._south_west = Quadtree(boundary=Rectangle(x - width / 2, y + height / 2, width / 2, height / 2), capacity=self._capacity)
        self._south_east = Quadtree(boundary=Rectangle(x + width / 2, y + height / 2, width / 2, height / 2), capacity=self._capacity)
        self._is_subdivided = True

    def query(self, range):
        found_points = list()
        if self._boundary.intersects(range) is False:
            return found_points

        for each_point in self._points:
            if range.contains(each_point) is True:
                found_points.append(each_point)

        if self._is_subdivided is True:
            found_points.extend(self._north_west.query(range=range))
            found_points.extend(self._north_east.query(range=range))
            found_points.extend(self._south_west.query(range=range))
            found_points.extend(self._south_east.query(range=range))

        return found_points
