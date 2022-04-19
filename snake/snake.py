import random
import time
import pygame

from enum import Enum

from utils import AStar, AStarNode


class TileType(Enum):
    EMPTY = 0
    WALL = 1
    SNAKE = 2
    FOOD = 3
    SNAKE_HEAD = 4


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class SnakeNode(AStarNode):
    def __init__(self, x, y, tabletop) -> None:
        super().__init__()
        self.x, self.y, self.tabletop = x, y, tabletop
        self._rows = len(self.tabletop)
        self._columns = len(self.tabletop[0])
        self.parent = None

    def heuristic(self, goal_node) -> float:
        super().heuristic(goal_node)
        return abs(self.y - goal_node.y) + abs(self.x - goal_node.x)

    def get_successors(self) -> list:
        super().get_successors()
        allowed_types = [TileType.EMPTY, TileType.FOOD]
        successors = list()
        if self.y + 1 < self._columns and self.tabletop[self.x][self.y+1] in allowed_types:
            s = SnakeNode(x=self.x, y=self.y + 1, tabletop=self.tabletop)
            s.parent = self
            successors.append(s)

        if self.y - 1 >= 0 and self.tabletop[self.x][self.y-1] in allowed_types:
            s = SnakeNode(x=self.x, y=self.y - 1, tabletop=self.tabletop)
            s.parent = self
            successors.append(s)

        if self.x + 1 < self._rows and self.tabletop[self.x + 1][self.y] in allowed_types:
            s = SnakeNode(x=self.x + 1, y=self.y, tabletop=self.tabletop)
            s.parent = self
            successors.append(s)

        if self.x - 1 >= 0 and self.tabletop[self.x - 1][self.y] in allowed_types:
            s = SnakeNode(x=self.x - 1, y=self.y, tabletop=self.tabletop)
            s.parent = self
            successors.append(s)

        return successors

    def __eq__(self, obj):
        return isinstance(obj, SnakeNode) and self.x == obj.x and self.y == obj.y


class Snake:

    COLORS = {
        TileType.EMPTY: (240, 240, 240),
        TileType.WALL: (20, 20, 20),
        TileType.SNAKE: (75, 200, 110),
        TileType.SNAKE_HEAD: (45, 130, 70),
        TileType.FOOD: (200, 65, 80)
    }

    def __init__(self, rows=64, columns=64):
        self._automatic = False  # for player input or ia

        # force one more column/row for better visuals
        self.rows = rows
        self.columns = columns
        if self.rows % 2 == 0:
            self.rows += 1
        if self.columns % 2 == 0:
            self.columns += 1
        self._tiles_width = 5
        self._tiles_height = 5

        # pygame screen related
        self._w, self._h = self.columns * self._tiles_width, self.rows * self._tiles_height
        self._target_sceen = pygame.Surface((self._w, self._h))

        # initialize the variables of the game
        self._new_direction = None
        self.is_snake_alive = None
        self._snake_body_time_interval = None
        self._init_game()

    def get_score(self) -> int:
        return self._food_score

    def _init_game(self):
        # table top
        self.tabletop = list()
        for r in range(self.rows):
            self.tabletop.append(list())
            for c in range(self.columns):
                if r == 0 or r == self.rows - 1 or c == 0 or c == self.columns - 1:
                    self.tabletop[r].append(TileType.WALL)
                else:
                    self.tabletop[r].append(TileType.EMPTY)

        # random spots
        self._percentage_random_walls = 0.15
        available_spots = [(r, c) for r in range(1, self.rows - 1) for c in range(1, self.columns - 1)]
        for i in range(int(self.rows * self.columns * self._percentage_random_walls)):
            s = random.choice(available_spots)
            available_spots.remove(s)
            self.tabletop[s[0]][s[1]] = TileType.WALL

        # food
        self._food_position = None
        self._food_score = 0
        self._create_new_food()

        # snake body
        self.is_snake_alive = True
        self._new_direction = None
        self._snake_body = [(int(self.rows / 2) - 1, int(self.columns / 2)),
                            (int(self.rows / 2), int(self.columns / 2))]  # center
        self._update_snake_to_tabletop()

        # loop time
        self._snake_body_time_interval = time.time()
        self._snake_body_speed_time = 0.1

    def _update_snake_to_tabletop(self) -> None:
        """ Update the position in the table-top with the positions in the body of the snake"""
        for r in range(self.rows):
            for c in range(self.columns):
                if self.tabletop[r][c] == TileType.SNAKE:
                    self.tabletop[r][c] = TileType.EMPTY
                if (r, c) in self._snake_body:
                    self.tabletop[r][c] = TileType.SNAKE

        self.tabletop[self._snake_body[-1][0]][self._snake_body[-1][1]] = TileType.SNAKE_HEAD

    def _create_new_food(self) -> None:
        """ Create a new food and update the tabletop with this new position"""
        available_spots = [(r, c) for r in range(self.rows) for c in range(self.columns)
                           if self.tabletop[r][c] == TileType.EMPTY]
        self._food_position = random.choice(available_spots)
        self.tabletop[self._food_position[0]][self._food_position[1]] = TileType.FOOD

    def _solve(self) -> list:
        """ Solve the path between the current snake head and the current food"""
        if self._food_position is not None:
            sn = SnakeNode(x=self._snake_body[-1][0], y=self._snake_body[-1][1], tabletop=self.tabletop)
            gn = SnakeNode(x=self._food_position[0], y=self._food_position[1], tabletop=self.tabletop)

            self._pathfinding = AStar()
            self._pathfinding.set_starting_node(node=sn)
            is_solved = self._pathfinding.find(goal_node=gn)
            solution = []
            if is_solved is True:
                solution = self._pathfinding.backtracking()
            return solution

    def _get_automatic_new_direction(self) -> tuple:
        """ Get the new direction that the snake must move"""
        path = self._solve()
        if len(path) == 0:
            return ()
        snake_head = self._snake_body[-1]
        new_snake_head = (path[-2].x, path[-2].y)

        return new_snake_head[0] - snake_head[0], new_snake_head[1] - snake_head[1]

    def event(self, event) -> None:
        """ Event loop:
        Key a: activates/deactivate automatic mode
        Key r: reset the game
        Key up, down, left, right: move the snake
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self._automatic = not self._automatic
            if event.key == pygame.K_r:
                self._init_game()

            if self._automatic is False:
                if event.key == pygame.K_UP:
                    self._new_direction = Direction.UP.value
                if event.key == pygame.K_DOWN:
                    self._new_direction = Direction.DOWN.value
                if event.key == pygame.K_RIGHT:
                    self._new_direction = Direction.RIGHT.value
                if event.key == pygame.K_LEFT:
                    self._new_direction = Direction.LEFT.value

    def loop(self) -> None:
        # move the snake body
        if self.is_snake_alive is True:
            # only actuate if elapsed time since last action is enough
            if time.time() - self._snake_body_time_interval > self._snake_body_speed_time:
                # calculate an input by ia if automatic mode is on
                if self._automatic is True:
                    self._new_direction = self._get_automatic_new_direction()
                    if not self._new_direction:
                        self.is_snake_alive = False
                        return

                # calculate direction if not direction has been setted by input
                snake_head = self._snake_body[-1]
                snake_neck = self._snake_body[-2]
                if self._new_direction is not None:
                    direction = self._new_direction
                    self._new_direction = None
                else:
                    direction = (snake_head[0] - snake_neck[0], snake_head[1] - snake_neck[1])
                new_snake_head = (snake_head[0] + direction[0], snake_head[1] + direction[1])

                # if the new head is the same as the snake head, not move anything
                if snake_neck == new_snake_head:
                    return

                # if the new head is wall or snake, finished
                if self.tabletop[new_snake_head[0]][new_snake_head[1]] in [TileType.WALL, TileType.SNAKE]:
                    self.is_snake_alive = False
                    return

                # if new head is in the place of a food, create a new food and dont delete the tail
                if self.tabletop[new_snake_head[0]][new_snake_head[1]] not in [TileType.FOOD]:
                    self._snake_body.pop(0)
                else:
                    self._create_new_food()
                    self._food_score += 1
                    self._snake_body_speed_time *= 0.9

                # add the new head to the snake body
                self._snake_body.append(new_snake_head)
                self._update_snake_to_tabletop()
                self._snake_body_time_interval = time.time()

    def render(self) -> pygame.surface:
        for r in range(self.rows):
            for c in range(self.columns):
                rect = pygame.Rect(
                    c * self._tiles_width,
                    r * self._tiles_height,
                    self._tiles_width,
                    self._tiles_height
                )
                pygame.draw.rect(self._target_sceen, self.COLORS[self.tabletop[r][c]], rect)

        return self._target_sceen

    def cleanup(self) -> None:
        pass

    @staticmethod
    def _maprange(v, a, b) -> float:
        (a1, a2), (b1, b2) = a, b
        return b1 + ((v - a1) * (b2 - b1) / (a2 - a1))
