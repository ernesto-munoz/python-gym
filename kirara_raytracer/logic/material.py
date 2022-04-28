import random
import glm
from glm import vec3, sphericalRand, dot
from abc import ABC, abstractmethod
from .ray import Ray

from .hit import HitRecord


class Material(ABC):
    @abstractmethod
    def scatter(self, in_ray: Ray, record: HitRecord) -> tuple[Ray, vec3] | tuple[None, None]:
        pass

    def _near_zero(self, v: vec3) -> bool:
        s = 1e-8
        return abs(v.x) < s and abs(v.y) < s and abs(v.z) < s


class Lambert(Material):
    def __init__(self, color: vec3):
        self._color = color

    def scatter(self, in_ray: Ray, record: HitRecord) -> tuple[Ray, vec3] | tuple[None, None]:
        scatter_direction = record.normal + sphericalRand(1)
        if self._near_zero(v=scatter_direction) is True:
            scatter_direction = record.normal

        return Ray(origin=record.p, direction=scatter_direction), self._color


class Metal(Material):
    def __init__(self, color: vec3, fuzz: float):
        self._color = color
        self._fuzz = glm.clamp(fuzz, 0.0, 1.0)

    def reflect(self, v: vec3, n: vec3) -> vec3:
        return v - 2 * dot(v, n) * n

    def scatter(self, in_ray: Ray, record: HitRecord) -> tuple[Ray, vec3] | tuple[None, None]:
        reflected: vec3 = self.reflect(
            v=glm.normalize(in_ray.direction),
            n=record.normal
        )
        if dot(reflected, record.normal) < 0:
            return None, None

        return Ray(origin=record.p, direction=reflected + self._fuzz * sphericalRand(1)), self._color


class Dielectric(Material):
    def __init__(self, index_of_refraction: float, color: vec3 = None):
        self._color = color if color is not None else vec3(1.0, 1.0, 1.0)
        self._index_of_refraction = index_of_refraction

    def refract(self, uv: vec3, n: vec3, etai_over_etat: float) -> vec3:
        cos_theta = glm.min(dot(-uv, n), 1.0)
        r_out_perp = etai_over_etat * (uv + cos_theta * n)
        r_out_parallel = -glm.sqrt(glm.abs(1.0 - glm.length2(r_out_perp))) * n
        return r_out_perp + r_out_parallel

    def reflect(self, v: vec3, n: vec3) -> vec3:
        return v - 2 * dot(v, n) * n

    def reflectance(self, cosine: float, ref_idx: float):
        r0 = (1 - ref_idx) / (1 + ref_idx)
        r0 = r0 * r0
        return r0 + (1 - r0) * glm.pow((1 - cosine), 5)

    def scatter(self, in_ray: Ray, record: HitRecord) -> tuple[Ray, vec3] | tuple[None, None]:
        refraction_ratio = 1.0 / self._index_of_refraction if record.front_face is True else self._index_of_refraction

        unit_direction = glm.normalize(in_ray.direction)
        cos_theta = glm.min(dot(-unit_direction, record.normal), 1.0)
        sin_theta = glm.sqrt(1.0 - cos_theta * cos_theta)
        cannot_refract = refraction_ratio * sin_theta > 1.0

        if cannot_refract is True or self.reflectance(cos_theta, refraction_ratio) > random.random():
            direction = self.reflect(unit_direction, record.normal)
        else:
            direction = self.refract(unit_direction, record.normal, refraction_ratio)

        return Ray(origin=record.p, direction=direction), self._color
