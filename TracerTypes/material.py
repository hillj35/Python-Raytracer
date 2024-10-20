from abc import ABC, abstractmethod
import math
from TracerTypes.ray import ray
from TracerTypes.vec3 import vec3 as color, vec3 as vec3, random_unit_vector, reflect, dot, refract

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


class dielectric(material):
    def __init__(self, refraction_index: float):
        self.refraction_index = refraction_index

    def scatter(self, r_in, rec):
        scatter_rec = scatter_record()

        scatter_rec.attenuation = color(1.0, 1.0, 1.0)
        ri = (1.0/self.refraction_index) if rec.is_front_face else self.refraction_index

        unit_direction = r_in._direction.normalized()
        cos_theta = min(dot(-unit_direction, rec.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)

        cannot_refract = ri * sin_theta > 1.0

        if cannot_refract:
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, ri)

        
        scatter_rec.scattered_ray = ray(rec.p, direction)
        scatter_rec.did_scatter = True

        return scatter_rec
    
    # Static methods
    def reflectance(cosine: float, refraction_index: float) -> float:
        r0 = (1 - refraction_index) / (1 + refraction_index)
        r0 = r0 * r0
        return r0 + (1-r0) * math.pow((1 - cosine), 5)
        
