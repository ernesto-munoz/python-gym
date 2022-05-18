import math
import multiprocessing
import random
import time
from PIL import Image
import logging
from dataclasses import dataclass
from pathlib import Path
from multiprocessing import Pool, Process, Queue, JoinableQueue, Manager
from typing import Callable, Any, Mapping

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
    ANTIALIASING_SAMPLES: int = 20
    MAX_BOUNCES: int = 50


@dataclass(slots=True)
class InputPixelData:
    row: int
    column: int
    width: int
    height: int


@dataclass(slots=True)
class OutputPixelData:
    row: int
    column: int
    width: int
    height: int
    # color: glm.vec3
    num_of_ray_bounces: int
    output_colors_buffer: np.ndarray


class PixelProcess(Process):
    WHITE = glm.vec3(1.0, 1.0, 1.0)
    BLACK = glm.vec3(0.0, 0.0, 0.0)
    LIGHT_BLUE = glm.vec3(0.5, 0.7, 1.0)
    RED = glm.vec3(1.0, 0.0, 0.0)

    def __init__(self, input_queue, output_queue, world, image_width, image_height, camera) -> None:
        super(PixelProcess, self).__init__()
        self._input_queue = input_queue
        self._output_queue = output_queue
        self._world = world
        self._image_width = image_width
        self._image_height = image_height
        self._camera = camera

        # by pixel data
        self._num_of_ray_bounces = 0

    def run(self) -> None:
        while not self._input_queue.empty():
            self._num_of_ray_bounces = 0
            input_pixel_data: InputPixelData = self._input_queue.get()

            buffer = np.zeros(shape=(input_pixel_data.height, input_pixel_data.width, 3)).astype(np.uint32)

            for row in range(input_pixel_data.height):
                for column in range(input_pixel_data.width):
                    real_pixel_row = input_pixel_data.row + row
                    real_pixel_column = input_pixel_data.column + column
                    color = self._process_pixel(row=real_pixel_row, column=real_pixel_column)
                    try:
                        buffer[row][column] = color  # correct?
                    except IndexError as e:
                        print(row, column)
                        print("Holis:", input_pixel_data)
                        raise e

            self._output_queue.put(
                OutputPixelData(row=input_pixel_data.row, column=input_pixel_data.column, output_colors_buffer=buffer,
                                num_of_ray_bounces=self._num_of_ray_bounces, width=input_pixel_data.width,
                                height=input_pixel_data.height)
            )

    def ray_color(self, r: Ray, current_depth: int) -> glm.vec3:
        if current_depth <= 0:
            return self.BLACK
        self._num_of_ray_bounces += 1

        record = HitRecord()
        if self._world.hit(ray=r, t_min=0.0001, t_max=math.inf, record=record) is True:
            scattered_ray, attenuation_color = record.material.scatter(in_ray=r, record=record)
            if scattered_ray and attenuation_color:
                return attenuation_color * self.ray_color(r=scattered_ray, current_depth=current_depth - 1)
            return self.BLACK

        dir = glm.normalize(r.direction)
        t = 0.5 * (dir.y + 1.0)
        return (1.0 - t) * self.WHITE + t * self.LIGHT_BLUE

    def _process_pixel(self, row, column) -> glm.vec3:
        accum_color = glm.vec3(0.0, 0.0, 0.0)
        for s in range(RaytracerConfig.ANTIALIASING_SAMPLES):
            u = (column + random.random()) / (self._image_width - 1)
            v = (row + random.random()) / (self._image_height - 1)
            ray = self._camera.get_ray(u=u, v=v)
            accum_color = accum_color + self.ray_color(r=ray, current_depth=RaytracerConfig.MAX_BOUNCES)

        accum_color = accum_color * (255 / RaytracerConfig.ANTIALIASING_SAMPLES)
        return accum_color


class Raytracer:
    def __init__(self, image_width: int = 128, image_height: int = 128):
        self._render_target: np.ndarray or None = None
        self._image_width: int = image_width
        self._image_height: int = image_height
        self._output_filepath: Path or None = None
        self._render_tile_size: int = 25

        self._world: HittableList = HittableList()
        self._world.add(
            obj=Sphere(position=glm.vec3(0, 100.3, -1.0), radius=100, material=Lambert(color=glm.vec3(0.8, 0.8, 0.0))))
        self._world.add(
            obj=Sphere(position=glm.vec3(0.0, 0.0, -1.0), radius=0.5, material=Lambert(color=glm.vec3(0.1, 0.2, 0.5))))
        self._world.add(
            obj=Sphere(position=glm.vec3(-1.0, 0.0, -1.0), radius=0.5, material=Dielectric(index_of_refraction=1.5)))
        self._world.add(obj=Sphere(position=glm.vec3(1.0, 0.0, -1.0), radius=0.5,
                                   material=Metal(color=glm.vec3(0.8, 0.6, 0.2), fuzz=0.0)))

        # self._world.add(obj=Sphere(position=glm.vec3(-1, 0, -1.0), radius=0.5))

        aspect_ratio = self._image_width / self._image_height
        self._camera = Camera(vertical_field_of_view=90.0, aspect_ratio=aspect_ratio)
        self._camera.position = glm.vec3(0, -0.5, 1)
        self._camera.look_at = glm.vec3(0, 0, 0)

        self.publisher = Publisher(events=[e for e in RaytracerEvents])

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
    def render_target(self) -> np.ndarray:
        return self._render_target

    @property
    def camera(self) -> Camera:
        return self._camera

    @property
    def output_filepath(self) -> Path:
        return self._output_filepath

    @output_filepath.setter
    def output_filepath(self, value: Path):
        self._output_filepath = value

    def allocate_render_target(self):
        self._render_target = np.zeros(shape=(self._image_height, self._image_width, 3)).astype(np.uint32)

    def render(self) -> None:
        self.publisher.dispatch(event=RaytracerEvents.PREPARING_RENDER, data=None)
        self.print_render_config()

        if self.render_target is None:
            self.allocate_render_target()

        total_pixels = 0
        num_of_ray_bounces = 0
        with Manager() as manager:
            print("Rendering...")
            output_queue = manager.Queue()
            input_queue = manager.Queue()
            start = time.time()

            for row in range(0, self._image_height, self._render_tile_size):
                for column in range(0, self._image_width, self._render_tile_size):
                    remainder_w = self._image_width - column
                    w = self._render_tile_size if remainder_w > self._render_tile_size else remainder_w

                    remainder_h = self._image_height - row
                    h = self._render_tile_size if remainder_h > self._render_tile_size else remainder_h

                    input_queue.put(InputPixelData(row=row, column=column, width=w, height=h))

            print(f"Data in queue... {time.time() - start}s")

            print("Launching processes...")

            self.publisher.dispatch(event=RaytracerEvents.PREPARED_RENDER, data=None)

            processes = list()
            for _ in range(multiprocessing.cpu_count()):  # multiprocessing.cpu_count() - 1
                p = PixelProcess(input_queue=input_queue, output_queue=output_queue, world=self._world,
                                 image_width=self._image_width, image_height=self._image_height, camera=self._camera)
                processes.append(p)
                p.start()

            print("...launched")
            self.publisher.dispatch(event=RaytracerEvents.RENDER_STARTED, data=None)
            while total_pixels < self._image_width * self._image_height:
                while not output_queue.empty():
                    output_pixel_data: OutputPixelData = output_queue.get()
                    num_of_ray_bounces += output_pixel_data.num_of_ray_bounces


                    buffer = output_pixel_data.output_colors_buffer
                    buffer_w = output_pixel_data.width
                    buffer_h = output_pixel_data.height

                    try:
                        self._render_target[output_pixel_data.row: output_pixel_data.row + buffer_h,
                        output_pixel_data.column: output_pixel_data.column + buffer_w] = buffer
                    except ValueError as e:
                        print(f"{buffer_h=}")
                        print(f"{buffer_w=}")
                        print(output_pixel_data)
                        raise e

                    total_pixels += output_pixel_data.output_colors_buffer.shape[0] * \
                                    output_pixel_data.output_colors_buffer.shape[1]
                    self.publisher.dispatch(event=RaytracerEvents.PIXEL_FINISHED,
                                            data={"output_pixel_data": output_pixel_data}
                                            )
                # time.sleep(0.05)  # wait some time to check again the completed pixels queue

            print("All pixels has been processed.")

            [proc.join() for proc in processes]
            print("All the process are finished!")
            print(f"Num of Ray Bounces: {num_of_ray_bounces}")
            self.publisher.dispatch(event=RaytracerEvents.RENDER_FINISHED, data=None)

    def print_render_config(self):
        print(f"Render Size: {self._image_width}x{self._image_height}")
        print(f"Render Samples:")
        print(f"\tAntialiasing: {RaytracerConfig.ANTIALIASING_SAMPLES}")
        print(f"\tMax Bounces: {RaytracerConfig.MAX_BOUNCES}")
        print(f"Camera:")
        print(f"Position: ({self._camera.position.x}, {self._camera.position.y}, {self._camera.position.z}) ")
        print(f"FOV: {self._camera.vertical_field_of_view}")

    def save_to_image(self, output_filepath: Path = None):
        im = Image.fromarray(np.uint8(self._render_target), "RGB")
        if output_filepath is None:
            print(f"Saving to {self._output_filepath}...")
            im.save(self._output_filepath)
        else:
            print(f"Saving to {output_filepath}...")
            im.save(output_filepath)


if __name__ == '__main__':
    pass
