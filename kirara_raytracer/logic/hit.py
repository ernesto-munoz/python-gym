import glm

from dataclasses import dataclass
from typing import Protocol

from .ray import Ray


# @dataclass(slots=True)
class HitRecord:
    # from .material import Material
    p: glm.vec3 = None
    normal: glm.vec3 = None
    t: glm.c_float = None
    material = None
    front_face: bool = None

    # material: Material = None

    def set_face_normal(self, ray: Ray, outward_normal: glm.vec3):
        front_face = glm.dot(ray.direction, outward_normal) < 0
        self.normal = outward_normal if front_face is True else -outward_normal


class Hittable(Protocol):
    def hit(self, ray: Ray, t_min: glm.c_float, t_max: glm.c_float, record: HitRecord) -> bool:
        ...


class HittableList:
    def __init__(self):
        self._objects: list[Hittable] = list()

    def hit(self, ray: Ray, t_min: glm.c_float, t_max: glm.c_float, record: HitRecord) -> bool:
        hit_anything = False
        closest_so_far = t_max
        for each_object in self._objects:
            if each_object.hit(ray=ray, t_min=t_min, t_max=closest_so_far, record=record) is True:
                hit_anything = True
                closest_so_far = record.t

        return hit_anything

    def add(self, obj: Hittable) -> None:
        self._objects.append(obj)

    def clear(self) -> None:
        self._objects = list()
