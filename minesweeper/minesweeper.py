import random
import pygame
from dataclasses import dataclass

from enum import Enum


class GameStatus(Enum):
    IN_PROGRESS = 0
    WIN = 1
    LOSE = 2


@dataclass
class Tile:
    is_hidden: bool = True
    is_bomb: bool = False
    near_bombs: int = 0
    is_flagged: bool = False


class Minesweeper:
    COLORS = {
        "HIDDEN": (20, 20, 20),
        "VISIBLE": (230, 230, 230),
        "FLAGGED": (0, 255, 0),
        "BOMB": (255, 0, 0),
    }

    def __init__(self, rows=16, columns=16, bombs_num=10):

        # force one more column/row for better visuals
        self.rows = rows
        self.columns = columns
        self.bombs_num = bombs_num
        self._tiles_width = 20
        self._tiles_height = 20

        # pygame screen related
        self._w, self._h = self.columns * self._tiles_width, self.rows * self._tiles_height
        self._target_screen = pygame.Surface((self._w, self._h))
        self._number_font = pygame.font.Font("freesansbold.ttf", 256)
        self._win_lose_font = pygame.font.Font("freesansbold.ttf", 64)

        # initialize the variables of the game
        self._game_status = GameStatus.IN_PROGRESS
        self._init_game()

    def _init_game(self):
        self._game_status = GameStatus.IN_PROGRESS
        self.tabletop = list()
        self.tabletop = [[Tile() for c in range(self.columns)] for r in range(self.rows)]

        for index in range(self.bombs_num):
            r, c = random.choice([(r, c) for r in range(self.rows) for c in range(self.columns) if self.tabletop[r][c].is_bomb is False])
            self.tabletop[r][c].is_bomb = True
            for rr in range(-1, 2):
                for cc in range(-1, 2):
                    if r + rr >= 0 and r + rr < self.rows and c + cc >= 0 and c + cc < self.columns:
                        self.tabletop[r + rr][c + cc].near_bombs += 1

    def event(self, event) -> None:

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self._init_game()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._game_status in [GameStatus.LOSE, GameStatus.WIN]:
                return
            w, h = pygame.display.get_surface().get_size()
            pos_x = self._maprange(event.pos[0], (0, h), (0, self._h))
            pos_y = self._maprange(event.pos[1], (0, w), (0, self._w))
            r = int(pos_y / self._tiles_height)
            c = int(pos_x / self._tiles_width)

            if event.button == 1:
                if self.tabletop[r][c].is_hidden is True and self.tabletop[r][c].is_flagged is False:
                    if self.tabletop[r][c].is_bomb is True:
                        self._game_status = GameStatus.LOSE
                    self.tabletop[r][c].is_hidden = False
                    self._expand(row=r, column=c)

            if event.button == 3:
                if self.tabletop[r][c].is_hidden is True:
                    self.tabletop[r][c].is_flagged = not self.tabletop[r][c].is_flagged

            if len(self._check_bombs_flagged()) == self.bombs_num:
                self._game_status = GameStatus.WIN

    def loop(self) -> None:
        pass

    def render(self) -> pygame.surface:

        for r in range(self.rows):
            for c in range(self.columns):
                rect = (c * self._tiles_width, r * self._tiles_height, self._tiles_width, self._tiles_height)
                if self.tabletop[r][c].is_hidden is True:
                    if self.tabletop[r][c].is_flagged is True:
                        pygame.draw.rect(self._target_screen, self.COLORS["FLAGGED"], rect)
                    else:
                        pygame.draw.rect(self._target_screen, self.COLORS["HIDDEN"], rect)
                    pygame.draw.rect(self._target_screen, (0, 0, 0), rect, 1)
                else:
                    if self.tabletop[r][c].is_bomb is True:
                        pygame.draw.rect(self._target_screen, self.COLORS["BOMB"], rect)
                    else:
                        pygame.draw.rect(self._target_screen, self.COLORS["VISIBLE"], rect)

                        # Draw number if needed
                        if self.tabletop[r][c].near_bombs != 0:
                            number = self._number_font.render(f"{self.tabletop[r][c].near_bombs}", True, (255, 20, 0))
                            number = pygame.transform.scale(number, (self._tiles_width - 2, self._tiles_height - 2))
                            self._target_screen.blit(number, (c * self._tiles_width + 1, r * self._tiles_height + 1))

                    pygame.draw.rect(self._target_screen, (0, 0, 0), rect, 1)

        # fps = self._fps_font.render(f"fps: {FPS_CLOCK.get_fps():.1f}", True, (200, 10, 10))
        # fps_size = fps.get_size()
        # self._display_surf.blit(fps, (0, self.height - fps_size[1]))
        # Win or Lose Message
        if self._game_status is not GameStatus.IN_PROGRESS:
            message = "Win"
            if self._game_status == GameStatus.LOSE:
                message = "Lose"
            win_lose_message = self._win_lose_font.render(f"{message}", True, (200, 10, 10))
            self._target_screen.blit(win_lose_message, (0, 0))

        return self._target_screen

    def cleanup(self) -> None:
        pass

    @staticmethod
    def _maprange(v, a, b) -> float:
        (a1, a2), (b1, b2) = a, b
        return b1 + ((v - a1) * (b2 - b1) / (a2 - a1))

    def _expand(self, row, column) -> None:

        tiles_to_check = list()
        if row - 1 >= 0:
            tiles_to_check.append((row - 1, column))
        if row + 1 < self.rows:
            tiles_to_check.append((row + 1, column))
        if column - 1 >= 0:
            tiles_to_check.append((row, column - 1))
        if column + 1 < self.columns:
            tiles_to_check.append((row, column + 1))

        for each_tile in tiles_to_check:
            tile = self.tabletop[each_tile[0]][each_tile[1]]
            if tile.is_hidden is True:
                if tile.near_bombs == 0:
                    tile.is_hidden = False
                    self._expand(row=each_tile[0], column=each_tile[1])
                elif tile.is_bomb is False:
                    tile.is_hidden = False

    def _check_bombs_flagged(self) -> list:
        flagged_bombs = list()
        for r in range(self.rows):
            for c in range(self.columns):
                if self.tabletop[r][c].is_bomb is True and self.tabletop[r][c].is_flagged is True:
                    flagged_bombs.append((r, c))
        return flagged_bombs
