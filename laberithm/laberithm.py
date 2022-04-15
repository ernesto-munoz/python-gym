import random
import time
import pygame

from pathfinding import AStar, PathfindingNode


class Laberithm:
    def __init__(self, rows=16, columns=16):

        self.rows = rows
        self.columns = columns
        if self.rows % 2 == 0:
            self.rows += 1
        if self.columns % 2 == 0:
            self.columns += 1
        self._tiles_width = 5
        self._tiles_height = 5
        self.maze = self._random_maze()
        self._solution = []

        # screen
        self._w, self._h = self.columns * self._tiles_width, self.rows * self._tiles_height
        self._target_sceen = pygame.Surface((self._w, self._h))

        self._start = None
        self._start_color = (225, 50, 50)
        self._end = None
        self._end_color = (52, 69, 224)

        # animation
        self._animation_start_time = None
        self._animation_solution_index = -1

    def _solve(self) -> None:
        if self._start is not None and self._end is not None:
            sn = PathfindingNode(x=self._start[0], y=self._start[1], lab=self)
            gn = PathfindingNode(x=self._end[0], y=self._end[1], lab=self)

            self._pathfinding = AStar()
            self._pathfinding.set_starting_node(node=sn)
            solution_found = self._pathfinding.find(goal_node=gn)
            if solution_found is True:
                solution = self._pathfinding.backtracking()
                self._solution = [(s.x, s.y) for s in solution]
                self._animation_solution_index = 0

    def event(self, event) -> None:
        new_end_start = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed_keys = pygame.key.get_pressed()
            w, h = pygame.display.get_surface().get_size()
            # pos_x = np.interp(event.pos[0], [0, h], [0, self._h])
            # pos_y = np.interp(event.pos[1], [0, w], [0, self._w])
            pos_x = self._maprange(event.pos[0], (0, h), (0, self._h))
            pos_y = self._maprange(event.pos[1], (0, w), (0, self._w))
            c = int(pos_x / self._tiles_width)
            r = int(pos_y / self._tiles_height)
            if self.maze[r][c] == True:

                if pressed_keys[pygame.K_q] is True:
                    self._start = (r, c)
                    new_end_start = True
                if pressed_keys[pygame.K_w] is True:
                    self._end = (r, c)
                    new_end_start = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._solve()

        if new_end_start is True:
            self._solution = list()
            self._solve()
            self._animation_start_time = time.time()
            self._animation_solution_index = 0

    def loop(self) -> None:
        # animation
        if len(self._solution) > 0 and self._animation_solution_index < len(self._solution):
            if time.time() - self._animation_start_time > 0.01:  # one second animation
                self._animation_solution_index += 1
                self._animation_start_time = time.time()

    def render(self) -> None:
        color = {
            True: (255, 255, 255),
            False: (0, 0, 0)
        }
        render_solution = self._solution[0:self._animation_solution_index]
        for r in range(self.rows):
            for c in range(self.columns):
                rect = pygame.Rect(
                    c * self._tiles_width,
                    r * self._tiles_height,
                    self._tiles_width,
                    self._tiles_height
                )
                pygame.draw.rect(self._target_sceen, color[self.maze[r][c]], rect)

        for each_render_solution in render_solution:
            rect = pygame.Rect(
                each_render_solution[1] * self._tiles_width,
                each_render_solution[0] * self._tiles_height,
                self._tiles_width,
                self._tiles_height
            )
            pygame.draw.rect(self._target_sceen, (75, 215, 90), rect)

        if self._start is not None:
            rect = pygame.Rect(
                self._start[1] * self._tiles_width,
                self._start[0] * self._tiles_height,
                self._tiles_width,
                self._tiles_height
            )
            pygame.draw.rect(self._target_sceen, self._start_color, rect)

        if self._end is not None:
            rect = pygame.Rect(
                self._end[1] * self._tiles_width,
                self._end[0] * self._tiles_height,
                self._tiles_width,
                self._tiles_height
            )
            pygame.draw.rect(self._target_sceen, self._end_color, rect)

        return self._target_sceen

    def cleanup(self) -> None:
        pass

    def _random_maze(self):
        table = [[False for i in range(self.columns)] for j in range(self.columns)]
        for r in [*range(1, self.rows, 2)]:
            for c in [*range(1, self.columns, 2)]:
                table[r][c] = True

        for r in [*range(1, self.rows, 2)]:
            run = set()
            current_cell = (r, 1)
            while current_cell[1] < self.columns:
                run.add(current_cell)

                choices = list()
                if current_cell[1] + 2 < self.columns:
                    choices.append("EAST")
                if current_cell[0] - 1 > 0:
                    choices.append("NORTH")
                if len(choices) == 0:
                    break
                choice = random.choice(choices)

                if choice == "EAST":
                    table[current_cell[0]][current_cell[1] + 1] = True
                    current_cell = (current_cell[0], current_cell[1] + 2)
                else:
                    n = random.choice(list(run))
                    if n[0] - 1 > 1:
                        table[n[0]-1][n[1]] = True
                    run = set()
                    current_cell = (n[0], n[1] + 2)
        return table

    def _maprange(self, v, a, b) -> float:
        (a1, a2), (b1, b2) = a, b
        return b1 + ((v - a1) * (b2 - b1) / (a2 - a1))
