import pygame
from pygame.math import Vector2
from obstacle import Obstacle
from ray import Ray, Emitter

FPS = 120
FPS_CLOCK = pygame.time.Clock()


class App:
    BACKGROUND_COLOR = (15, 15, 15)

    def __init__(self):
        self.size = self.weight, self.height = 640, 640
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF, vsync=False)
        self._running = True

        self._emitter = Emitter(position=Vector2(100, 200))
        self._is_moving_ray_emitter = False

        self._obstacles = list()
        self._obstacles.append(Obstacle(begin=Vector2(300, 100), end=Vector2(300, 300)))

        self._in_development_obstacle_begin = None
        self._in_development_obstacle_end = None

    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        # creating obstacles input
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self._in_development_obstacle_begin = Vector2(event.pos)

        if event.type == pygame.MOUSEMOTION:
            if self._in_development_obstacle_begin is not None:
                self._in_development_obstacle_end = Vector2(event.pos)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            if self._in_development_obstacle_begin is not None and self._in_development_obstacle_end is not None:
                self._obstacles.append(
                    Obstacle(begin=self._in_development_obstacle_begin,
                             end=Vector2(event.pos))
                )
                self._in_development_obstacle_begin = None
                self._in_development_obstacle_end = None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._is_moving_ray_emitter = True
            self._emitter.position = Vector2(event.pos)

        if event.type == pygame.MOUSEMOTION:
            if self._is_moving_ray_emitter is True:
                self._emitter.position = Vector2(event.pos)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._is_moving_ray_emitter is True:
                self._is_moving_ray_emitter = False
                self._emitter.position = Vector2(event.pos)

    def loop(self):
        self._emitter.look(obstacles=self._obstacles)

    def render(self):
        self._display_surf.fill(self.BACKGROUND_COLOR)

        for each_obstacle in self._obstacles:
            each_obstacle.render()
        self._emitter.render()

        if self._in_development_obstacle_begin is not None and self._in_development_obstacle_end is not None:
            pygame.draw.aaline(pygame.display.get_surface(), (220, 0, 0),
                               self._in_development_obstacle_begin, self._in_development_obstacle_end)
        pygame.display.update()

    def cleanup(self):
        pygame.quit()

    def execute(self):
        while self._running:
            for event in pygame.event.get():
                self.event(event)
            self.loop()
            self.render()
            FPS_CLOCK.tick(FPS)
        self.cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.execute()
