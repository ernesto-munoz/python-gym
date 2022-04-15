import random
from typing import List
import numpy as np

import pygame
from pygame.locals import *

from target import Target
from obstacle import Obstacle


class DNA:
    genes: list[np.array] = list()

    def __init__(self, life_span: int = 200, genes: list[np.array] = None) -> None:
        self.LIFE_SPAN = life_span

        if genes is None:
            self.genes = []
            for i in range(self.LIFE_SPAN):
                self.genes.append(np.random.uniform(-0.5, 0.5, 2))
        else:
            self.genes = genes

    def crossover(self, partner: "DNA") -> "DNA":
        middle_point = random.randint(0, len(self.genes))
        new_dna = DNA(life_span=self.LIFE_SPAN, genes=self.genes[0:middle_point] + partner.genes[middle_point:])
        return new_dna

    def mutation(self):
        for i in range(len(self.genes)):
            if random.random() < 0.0001:
                self.genes[i] = np.random.uniform(-0.5, 0.5, 2)


class Rocket:
    def __init__(self, dna=None, life_span=200):
        w, h = pygame.display.get_surface().get_size()
        self.position = np.array([w/2, h])
        self.velocity = np.zeros(2)  # np.random.uniform(-0.5, 0.5, 2)
        self.acceleration = np.zeros(2)
        self.color = np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
        self.dna = dna or DNA(life_span=life_span)
        self.life_span_count = 0
        self.radius = 5
        self.fit = 0
        self.completed = False
        self.completed_time = 0
        self.crashed = False
        self.pick_probability = 0

    def set_completed(self):
        if self.completed is False:
            self.completed = True
            self.completed_time = self.life_span_count

    def apply_force(self, force: np.array):
        self.acceleration = self.acceleration + force

    def fitness(self, targets: list) -> float:
        min_distance = min([self.distance(target=each_target) for each_target in targets])

        #distance = self.distance(target=target)
        self.fit = 1 / min_distance

        if self.completed is True:
            self.fit *= 2 * (self.dna.LIFE_SPAN / self.completed_time)

        if self.crashed is True:
            self.fit = 0

        return self.fit

    def detect(self, obstacle: Obstacle):
        if obstacle.is_inside(point=self.position) is True:
            self.crashed = True

    def distance(self, target: Target) -> float:
        return np.linalg.norm(target.position - self.position)

    def on_init(self):
        pass

    def on_event(self, event):
        pass

    def on_loop(self):
        self.apply_force(force=self.dna.genes[self.life_span_count])
        if self.life_span_count < self.dna.LIFE_SPAN - 1:
            self.life_span_count += 1

        if self.completed is False and self.crashed is False:
            self.velocity += self.acceleration
            self.position += self.velocity
            self.acceleration *= 0

    def on_render(self):
        width, height = 10, 50
        x = self.position[0] - width / 2
        y = self.position[1] - height / 2
        pygame.draw.circle(pygame.display.get_surface(), self.color, tuple(self.position), self.radius)

    def on_cleanup(self):
        pass
