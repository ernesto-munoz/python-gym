import random
import numpy as np

import pygame
from pygame.locals import *


class Obstacle:
    def __init__(self):
        w, h = pygame.display.get_surface().get_size()
        self.position = np.array([w/2, h])
        self.width = 50
        self.height = 50
        self.color = np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])

    def on_init(self):
        pass

    def on_event(self, event):
        pass

    def on_loop(self):
        pass

    def on_render(self):
        x = self.position[0] - self.width / 2
        y = self.position[1] - self.height / 2
        pygame.draw.rect(pygame.display.get_surface(), self.color, pygame.Rect(x, y, self.width, self.height))

    def on_cleanup(self):
        pass

    def is_inside(self, point: np.array):
        x = self.position[0] - self.width / 2
        y = self.position[1] - self.height / 2

        if point[0] > x and point[0] < x + self.width and point[1] > y and point[1] < y + self.height:
            return True
        return False
