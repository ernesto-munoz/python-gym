import glm

from .ray import Ray
from .hit import HitRecord
from .material import Material


class Sphere:
    def __init__(self, position: glm.vec3, radius: glm.c_float, material: Material = None):
        self._position: glm.vec3 = position
        self._radius: glm.c_float = radius
        self._material: Material = material

    @property
    def position(self) -> glm.vec3:
        return self._position

    @position.setter
    def position(self, value: glm.vec3):
        self._position = value

    @property
    def radius(self) -> glm.c_float:
        return self._radius

    @radius.setter
    def radius(self, value: glm.c_float):
        self._radius = value

    @property
    def material(self) -> Material:
        return self._material

    @material.setter
    def material(self, value: Material):
        self._material = value

    def hit(self, ray: Ray, t_min: glm.c_float, t_max: glm.c_float, record: HitRecord) -> bool:
        origin_to_center = ray.origin - self._position
        a = glm.length2(ray.direction)
        half_b = glm.dot(origin_to_center, ray.direction)
        c = glm.length2(origin_to_center) - self._radius * self._radius

        discriminant = half_b * half_b - a * c
        if discriminant < 0:
            return False

        sqrtd = glm.sqrt(discriminant)
        # find the nearest root that lies in the acceptable range
        root = (-half_b - sqrtd) / a
        if root < t_min or root > t_max:
            root = (-half_b + sqrtd) / a
            if root < t_min or root > t_max:
                return False

        record.t = root
        record.p = ray.at(t=record.t)
        record.set_face_normal(ray=ray, outward_normal=(record.p - self._position) / self._radius)
        record.material = self._material
        return True
