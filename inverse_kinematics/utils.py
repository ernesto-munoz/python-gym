import random
import pygame

from pygame.math import Vector2


class Target:
    def __init__(self, x: float, y: float):
        self._position = Vector2(x, y)
        self._screen_surface = pygame.display.get_surface()
        self._w, self._h = self._screen_surface.get_size()
        self._previous_choice = None

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, value: Vector2):
        self._position = value

    def random_walk(self):
        choice = random.choice([*range(4)])
        while self._previous_choice == (choice + 2) % 4:
            choice = random.choice([*range(4)])
        self._previous_choice = choice

        move = 10
        if choice == 0:
            self.position.x += move
        elif choice == 2:
            self.position.x -= move
        elif choice == 1:
            self.position.y += move
        elif choice == 3:
            self.position.y -= move

        self.position.x = max(0, min(self._w, self.position.x))
        self.position.y = max(0, min(self._h, self.position.y))

    def event(self, event) -> None:
        pass

    def loop(self) -> None:
        pass

    def render(self) -> None:
        color = (115, 45, 190)
        pygame.draw.circle(self._screen_surface, color, self._position, 10, width=1)
        pygame.draw.aaline(self._screen_surface, color, self._position + Vector2(5, 0), self._position + Vector2(14, 0))
        pygame.draw.aaline(self._screen_surface, color, self._position + Vector2(-5, 0),
                           self._position + Vector2(-14, 0))
        pygame.draw.aaline(self._screen_surface, color, self._position + Vector2(0, 5), self._position + Vector2(0, 14))
        pygame.draw.aaline(self._screen_surface, color, self._position + Vector2(0, -5),
                           self._position + Vector2(0, -14))
