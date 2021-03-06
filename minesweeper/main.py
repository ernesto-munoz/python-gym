import pygame
from minesweeper import Minesweeper

FPS = 0
FPS_CLOCK = pygame.time.Clock()


class App:
    BACKGROUND_COLOR = (15, 15, 15)

    def __init__(self):
        pygame.init()
        self.size = self.weight, self.height = 640, 640
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Snake")
        self._font = pygame.font.Font("freesansbold.ttf", 48)
        self._fps_font = pygame.font.Font("freesansbold.ttf", 18)
        self._running = True

        self._minesweeper = Minesweeper(rows=20, columns=20, bombs_num=50)

    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        self._minesweeper.event(event=event)

    def loop(self):
        self._minesweeper.loop()

    def render(self):
        self._display_surf.fill(self.BACKGROUND_COLOR)

        screen = self._minesweeper.render()
        self._display_surf.blit(pygame.transform.scale(screen, self._display_surf.get_rect().size), (0, 0))

        fps = self._fps_font.render(f"fps: {FPS_CLOCK.get_fps():.1f}", True, (200, 10, 10))
        fps_size = fps.get_size()
        self._display_surf.blit(fps, (0, self.height - fps_size[1]))

        pygame.display.update()

    def cleanup(self):
        pygame.quit()

    def execute(self):

        while self._running is True:
            for event in pygame.event.get():
                self.event(event)
            self.loop()
            self.render()
            FPS_CLOCK.tick(FPS)
        self.cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.execute()
