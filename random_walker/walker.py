import random
from secrets import choice

import numpy as np

import pygame
from pygame.locals import *


class Walker:
    def __init__(self):
        w, h = pygame.display.get_surface().get_size()
        self.position = np.array([w / 2, h / 2])
        self.color = np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
        self._frame_count = 0
        self._previous_choice = -1

    def on_init(self):
        pass

    def on_event(self, event):
        pass

    def on_loop(self):
        choice = random.choice([*range(4)])
        while self._previous_choice == (choice + 2) % 4:
            choice = random.choice([*range(4)])
        self._previous_choice = choice

        if choice == 0:
            self.position[0] += 1
        elif choice == 2:
            self.position[0] -= 1
        elif choice == 1:
            self.position[1] += 1
        elif choice == 3:
            self.position[1] -= 1

        w, h = pygame.display.get_surface().get_size()
        self.position[0] = max(0, min(w, self.position[0]))
        self.position[1] = max(0, min(h, self.position[1]))

        if self._frame_count % 5 == 0:
            self.color += np.array([1, 1, 1])
            self.color = np.vectorize(lambda x: x % 255)(self.color)

        self._frame_count += 1

    def on_render(self):
        pygame.draw.circle(pygame.display.get_surface(), self.color, tuple(self.position), 1)

    def on_cleanup(self):
        pass
