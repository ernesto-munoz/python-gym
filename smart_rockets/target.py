import random
import numpy as np

import pygame
from pygame.locals import *


class Target:
    def __init__(self):
        w, h = pygame.display.get_surface().get_size()
        self.position = np.array([w/2, h])
        self.color = np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
        self.radius = 5

    def on_init(self):
        pass

    def on_event(self, event):
        pass

    def on_loop(self):
        pass

    def on_render(self):
        width, height = 10, 50
        x = self.position[0] - width / 2
        y = self.position[1] - height / 2
        pygame.draw.circle(pygame.display.get_surface(), self.color, tuple(self.position), self.radius)

    def on_cleanup(self):
        pass
