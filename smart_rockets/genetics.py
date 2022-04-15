import random
import pygame
import numpy as np
from rocket import Rocket
from target import Target
from obstacle import Obstacle


class Genetics:
    LIFE_SPAN = 300

    def __init__(self) -> None:
        w, h = pygame.display.get_surface().get_size()
        self._targets = list()
        target = Target()
        target.position = np.array([w / 1.35, h / 2.9])
        target.radius = 10
        self._targets.append(target)

        self._obstacles = list()
        # obstacle = Obstacle()
        # obstacle.position = np.array([w / 1.5, h / 2])
        # obstacle.width = 300
        # self._obstacles.append(obstacle)

        # obstacle = Obstacle()
        # obstacle.position = np.array([w / 3, h / 1.1])
        # obstacle.width = 500
        # obstacle.height = 15
        # self._obstacles.append(obstacle)

        # obstacle = Obstacle()
        # obstacle.position = np.array([w / 1.3, h / 4])
        # obstacle.width = 15
        # obstacle.height = 200
        # self._obstacles.append(obstacle)

        self._population = Population(life_span=self.LIFE_SPAN, targets=self._targets, obstacles=self._obstacles)
        self.life_span_count = 0

        self.population_count = 0

    def on_loop(self) -> None:
        self._population.on_loop()
        for each_target in self._targets:
            each_target.on_loop()

        self.life_span_count += 1
        if self.life_span_count > self.LIFE_SPAN - 1:
            self._population.evaluate(targets=self._targets)
            self._population.selection()
            self.life_span_count = 0
            self.population_count += 1

    def on_render(self) -> None:
        self._population.on_render()

        for each_obstacle in self._obstacles:
            each_obstacle.on_render()

        for each_target in self._targets:
            each_target.on_render()


class Population:
    POPULATION_SIZE = 500

    def __init__(self, targets: list, obstacles: list, life_span: int = 200) -> None:
        self.LIFE_SPAN = life_span
        self._targets = targets
        self._obstacles = obstacles

        self.rockets = list()
        for i in range(self.POPULATION_SIZE):
            self.rockets.append(Rocket(life_span=self.LIFE_SPAN))

        self.mating_pool = list()
        self.life_span_count = 0

    def on_loop(self) -> None:
        self.life_span_count += 1
        for each_rocket in self.rockets:
            each_rocket.on_loop()

            for each_obstacle in self._obstacles:
                each_rocket.detect(each_obstacle)

            for each_target in self._targets:
                if each_rocket.distance(target=each_target) < 5:
                    each_rocket.set_completed()
                    break

    def on_render(self) -> None:
        for each_rocket in self.rockets:
            each_rocket.on_render()

    def evaluate(self, targets: Target):

        # calculate fitness and find the max
        max_fitness = 0
        for each_rocket in self.rockets:
            f = each_rocket.fitness(targets=self._targets)
            if f > max_fitness:
                max_fitness = f

        # normalize fitness
        for each_rocket in self.rockets:
            each_rocket.fit /= max_fitness

        # self.mating_pool = list()

        fit_sum = sum([each_rocket.fit for each_rocket in self.rockets])
        for each_rocket in self.rockets:
            each_rocket.pick_probability = each_rocket.fit / fit_sum

    def selection(self):

        new_population = list()
        for i in range(self.POPULATION_SIZE):
            parent_a_dna = self.pick_citizen(citicens=self.rockets).dna
            parent_b_dna = self.pick_citizen(citicens=self.rockets).dna
            child_dna = parent_a_dna.crossover(parent_b_dna)
            child_dna.mutation()
            new_population.append(Rocket(life_span=self.LIFE_SPAN, dna=child_dna))

        self.rockets = new_population
        self.life_span_count = 0

    def pick_citizen(self, citicens):
        index = 0
        r = random.random()
        while(r > 0):
            r = r - citicens[index].pick_probability
            index += 1

        return citicens[index - 1]
