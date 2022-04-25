import pygame
from pygame.math import Vector2


class Obstacle:
    def __init__(self, begin, end) -> None:
        self._begin = begin
        self._end = end
        self._screen_surface = pygame.display.get_surface()

    @property
    def begin(self) -> Vector2:
        return self._begin

    @begin.setter
    def begin(self, value: Vector2):
        self._begin = value

    @property
    def end(self) -> Vector2:
        return self._end

    @end.setter
    def end(self, value: Vector2):
        self._end = value

    def render(self) -> None:
        color = (240, 240, 240)
        pygame.draw.aaline(self._screen_surface, color, self._begin, self._end)
