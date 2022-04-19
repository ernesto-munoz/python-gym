import random
import time

import numpy as np

import pygame
from pygame.locals import *

from quadtree import Quadtree, Rectangle, Point

FPS = 120
FPS_CLOCK = pygame.time.Clock()


class App:
    BACKGROUND_COLOR = (15, 15, 15)

    def __init__(self):
        pygame.init()
        self.size = self.weight, self.height = 980, 980
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Quadtree")
        self._font = pygame.font.Font("freesansbold.ttf", 48)
        self._fps_font = pygame.font.Font("freesansbold.ttf", 18)
        self._running = True

        self._quadtree = Quadtree(Rectangle(self.weight // 2, self.height // 2, self.weight // 2, self.height // 2))

        self.query_rectangle = Rectangle(0, 0, 0, 0)
        self._query_points = self._quadtree.query(range=self.query_rectangle)
        self._query_rectangle_start = None

    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[pygame.K_i] is True:
                self._quadtree.insert(Point(event.pos[0], event.pos[1]))
                self._query_points = self._quadtree.query(range=self.query_rectangle)
            else:
                self._query_rectangle_start = event.pos

        if event.type == pygame.MOUSEMOTION and self._query_rectangle_start is not None:
            w = abs(event.pos[0] - self._query_rectangle_start[0]) // 2
            h = abs(event.pos[1] - self._query_rectangle_start[1]) // 2
            start_x = min(event.pos[0], self._query_rectangle_start[0])
            start_y = min(event.pos[1], self._query_rectangle_start[1])
            self.query_rectangle = Rectangle(
                start_x + w,
                start_y + h,
                w, h
            )

        if event.type == pygame.MOUSEBUTTONUP and self._query_rectangle_start is not None:
            self._query_rectangle_start = None
            self._query_points = self._quadtree.query(range=self.query_rectangle)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self._quadtree = Quadtree(Rectangle(self.weight // 2, self.height // 2, self.weight // 2, self.height // 2))
                self._query_points = self._quadtree.query(range=self.query_rectangle)

            if event.key == pygame.K_a:
                for i in range(100):
                    self._quadtree.insert(Point(random.randint(0, self.weight), random.randint(0, self.height)))
                self._query_points = self._quadtree.query(range=self.query_rectangle)

    def loop(self):
        self._quadtree.loop()

    def render(self):
        self._display_surf.fill(self.BACKGROUND_COLOR)
        self._quadtree.render()

        fps = self._fps_font.render(f"fps: {FPS_CLOCK.get_fps():.1f}", True, (200, 10, 10))
        fps_size = fps.get_size()
        self._display_surf.blit(fps, (0, self.height - fps_size[1]))

        pygame.draw.rect(pygame.display.get_surface(), (0, 200, 0),
                         (self.query_rectangle.x - self.query_rectangle.width,
                         self.query_rectangle.y - self.query_rectangle.height,
                         self.query_rectangle.width * 2, self.query_rectangle.height * 2), 2)
        for each_point in self._query_points:
            pygame.draw.circle(pygame.display.get_surface(), (255, 0, 0), (each_point.x, each_point.y), 2)

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
