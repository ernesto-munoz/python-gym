import pygame
from pygame.math import Vector2
from ikinematics import Bone
from utils import Target

FPS = 60
FPS_CLOCK = pygame.time.Clock()


class App:
    BACKGROUND_COLOR = (15, 15, 15)

    def __init__(self):
        pygame.init()
        self.size = self.weight, self.height = 640, 640
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        # self._bone_parent = Bone(0, 0, 100, 0)
        # self._bone_middle = Bone(50, 0, 100, 0, parent_bone=self._bone_parent)
        # self._bone_child = Bone(100, 0, 100, 0, parent_bone=self._bone_middle)
        # self._bones = [self._bone_child, self._bone_middle, self._bone_parent]

        self._left_bones = self._generate_bones_chain(size=25, total_length=500, color=(0, 0, 255))
        self._right_bones = self._generate_bones_chain(size=10, total_length=400, color=(0, 255, 0))

        self._target = Target(320, 320)
        self._do_random_walk = False

    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self._do_random_walk = not self._do_random_walk

        if event.type == pygame.MOUSEMOTION:
            if self._do_random_walk is False:
                self._target.position = Vector2(event.pos)

    def loop(self):
        for each_bone in self._left_bones:
            each_bone.loop()
        self._left_bones[0].begin = Vector2(210, 640)

        for each_bone in self._right_bones:
            each_bone.loop()
        self._right_bones[0].begin = Vector2(420, 640)

        if self._do_random_walk is True:
            self._target.random_walk()
        self._left_bones[-1].set_follow_target(target=self._target.position)
        self._right_bones[-1].set_follow_target(target=self._target.position)

    def render(self):
        self._display_surf.fill(self.BACKGROUND_COLOR)
        for each_bone in self._left_bones:
            each_bone.render()
        for each_bone in self._right_bones:
            each_bone.render()

        self._target.render()
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

    def _generate_bones_chain(self, size=3, total_length=200, color=(255, 0, 0)) -> list:
        bones = list()
        length = total_length / size
        previous_bone = None
        for index in range(size):
            previous_bone = Bone(0, 0, length, 0, parent_bone=previous_bone)
            previous_bone.color = color
            bones.append(previous_bone)

        for index, each_bone in enumerate(bones[0:-1]):
            each_bone.add_child(bones[index + 1])

        return bones


if __name__ == "__main__":
    theApp = App()
    theApp.execute()
