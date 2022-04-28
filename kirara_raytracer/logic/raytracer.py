import math
import random

import glm
import numpy as np
from .ray import Ray
from .camera import Camera
from .shere import Sphere
from .hit import HitRecord, HittableList
from ..utils.observer import Publisher
from .raytracer_events import RaytracerEvents
from .material import Lambert, Metal, Dielectric


class RaytracerConfig:
    ANTIALIASING_SAMPLES = 100
    MAX_BOUNCES = 50


class Raytracer:
    WHITE = glm.vec3(1.0, 1.0, 1.0)
    BLACK = glm.vec3(0.0, 0.0, 0.0)
    LIGHT_BLUE = glm.vec3(0.5, 0.7, 1.0)
    RED = glm.vec3(1.0, 0.0, 0.0)

    def __init__(self, image_width: int = 128, image_height: int = 128):
        self._pixels = None
        self._image_width = image_width
        self._image_height = image_height

        self.NUM_OF_RAY_BOUNCES = 0

        self._world: HittableList = HittableList()
        self._world.add(obj=Sphere(position=glm.vec3(0, 100.3, -1.0), radius=100, material=Lambert(color=glm.vec3(0.8, 0.8, 0.0))))
        self._world.add(obj=Sphere(position=glm.vec3(0.0, 0.0, -1.0), radius=0.5, material=Lambert(color=glm.vec3(0.1, 0.2, 0.5))))
        self._world.add(obj=Sphere(position=glm.vec3(-1.0, 0.0, -1.0), radius=0.5, material=Dielectric(index_of_refraction=1.5)))
        self._world.add(obj=Sphere(position=glm.vec3(1.0, 0.0, -1.0), radius=0.5, material=Metal(color=glm.vec3(0.8, 0.6, 0.2), fuzz=0.0)))

        # self._world.add(obj=Sphere(position=glm.vec3(-1, 0, -1.0), radius=0.5))

        aspect_ratio = self._image_width / self._image_height
        self._camera = Camera(vertical_field_of_view=90.0, aspect_ratio=aspect_ratio)

        self.publisher = Publisher(events=[RaytracerEvents.PIXEL_FINISHED])

    @property
    def image_width(self) -> int:
        return self._image_width

    @image_width.setter
    def image_width(self, value: int):
        self._image_width = value

    @property
    def image_height(self) -> int:
        return self._image_height

    @image_height.setter
    def image_height(self, value: int):
        self._image_height = value

    @property
    def pixels(self) -> np.ndarray:
        return self._pixels

    @property
    def camera(self) -> Camera:
        return self._camera

    def ray_color(self, r: Ray, current_depth: int) -> glm.vec3:
        if current_depth <= 0:
            return self.BLACK
        self.NUM_OF_RAY_BOUNCES += 1

        record = HitRecord()
        if self._world.hit(ray=r, t_min=0.0001, t_max=math.inf, record=record) is True:
            scattered_ray, attenuation_color = record.material.scatter(in_ray=r, record=record)
            if scattered_ray and attenuation_color:
                return attenuation_color * self.ray_color(r=scattered_ray, current_depth=current_depth - 1)
            return self.BLACK

        dir = glm.normalize(r.direction)
        t = 0.5 * (dir.y + 1.0)
        return (1.0 - t) * self.WHITE + t * self.LIGHT_BLUE

    def render(self) -> None:
        self.print_render_config()

        self._pixels = np.zeros(shape=(self._image_height, self._image_width, 3)).astype(np.uint32)
        total_pixels = self._image_width * self.image_height
        current_pixels_count = 0

        for row in range(self._image_height):
            for column in range(self._image_width):

                accum_color = glm.vec3(0.0, 0.0, 0.0)
                for s in range(RaytracerConfig.ANTIALIASING_SAMPLES):
                    u = (column + random.random()) / (self._image_width - 1)
                    v = (row + random.random()) / (self._image_height - 1)
                    ray = self._camera.get_ray(u=u, v=v)
                    accum_color = accum_color + self.ray_color(r=ray, current_depth=RaytracerConfig.MAX_BOUNCES)

                self._pixels[row][column] = accum_color * (255 / RaytracerConfig.ANTIALIASING_SAMPLES)
                self.publisher.dispatch(event=RaytracerEvents.PIXEL_FINISHED, data=None)

                # statistics
                current_pixels_count += 1
            # print(f"Render: {current_pixels_count / total_pixels * 100:.2f}%")
        print(f"Num of Ray Bounces: {self.NUM_OF_RAY_BOUNCES}")

    def get_pixels_as_uint32_array(self) -> list:
        # 1111 1111 0000 0000 0000 0000 0000 0000 A
        #           0001 1000 0000 0000 0000 0000 R
        #                     1010 1001 0000 0000 G
        #                               1011 1101 B
        return (255 << 24 | self._pixels[:, :, 0] << 16 | self._pixels[:, :, 1] << 8 | self._pixels[:, :, 2]).flatten()

    def print_render_config(self):
        print(f"Render Size: {self._image_width}x{self._image_height}")
        print(f"Render Samples:")
        print(f"\tAntialiasing: {RaytracerConfig.ANTIALIASING_SAMPLES}")
        print(f"\tMax Bounces: {RaytracerConfig.MAX_BOUNCES}")
        print(f"Camera:")
        print(f"Position: ({self._camera.position.x}, {self._camera.position.y}, {self._camera.position.z}) ")
        print(f"FOV: {self._camera.vertical_field_of_view}")

    if __name__ == '__main__':
        pass
