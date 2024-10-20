from abc import ABC, abstractmethod
from TracerTypes.ray import ray
from TracerTypes.vec3 import vec3 as color, vec3 as vec3, random_unit_vector, reflect, dot

class scatter_record:
    attenuation: color = color(0,0,0)
    scattered_ray: ray = ray(vec3(0,0,0), vec3(0,0,0))
    did_scatter: bool = False

class material(ABC):
    @abstractmethod
    def scatter(self, r_in: ray, rec) -> "scatter_record":
        pass


class lambertian(material):
    def __init__(self, albedo: color):
        self.albedo = albedo

    def scatter(self, r_in, rec):
        scatter_rec = scatter_record()
        
        scatter_direction = rec.normal + random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        scatter_rec.scattered_ray = ray(rec.p, scatter_direction)
        scatter_rec.attenuation = self.albedo
        scatter_rec.did_scatter = True

        return scatter_rec


class metal(material):
    def __init__(self, albedo: color, fuzz: float):
        self.albedo = albedo
        self.fuzz = 1 if fuzz > 1 else fuzz

    def scatter(self, r_in, rec):
        scatter_rec = scatter_record()

        scatter_direction = reflect(r_in._direction, rec.normal)
        scatter_direction = scatter_direction.normalized() + (self.fuzz * random_unit_vector())
        scatter_rec.scattered_ray = ray(rec.p, scatter_direction)
        scatter_rec.attenuation = self.albedo
        scatter_rec.did_scatter = dot(scatter_rec.scattered_ray._direction, rec.normal) > 0

        return scatter_rec
