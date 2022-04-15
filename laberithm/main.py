import time

import numpy as np

import pygame
from pygame.locals import *

from laberithm import Laberithm

FPS = 60
FPS_CLOCK = pygame.time.Clock()


class App:
    BACKGROUND_COLOR = (15, 15, 15)

    def __init__(self):
        pygame.init()
        self.size = self.weight, self.height = 640, 640
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        self._lab = Laberithm(rows=128, columns=128)

    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        self._lab.event(event=event)

    def loop(self):
        self._lab.loop()

    def render(self):
        self._display_surf.fill(self.BACKGROUND_COLOR)
        screen = self._lab.render()
        self._display_surf.blit(pygame.transform.scale(screen, self._display_surf.get_rect().size), (0, 0))

        pygame.display.update()

    def cleanup(self):
        pygame.quit()

    def execute(self):

        while(self._running):
            for event in pygame.event.get():
                self.event(event)
            self.loop()
            self.render()
            FPS_CLOCK.tick(FPS)
        self.cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.execute()
