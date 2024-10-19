from abc import ABC, abstractmethod
from TracerTypes.vec3 import vec3, dot
from TracerTypes.ray import ray


class hit_record:
    p = vec3(0,0,0)
    normal = vec3(0,0,0)
    t = 0
    is_front_face = False
    is_hit = False

    def set_face_normal(self, r: ray, outward_normal: vec3):
        """Sets the hit record normal vector.
        The parameter `outward_normal` is assumed to have unit length."""
        self.is_front_face = dot(r._direction, outward_normal) < 0
        self.normal = outward_normal if self.is_front_face else -outward_normal


# abstract class
class hittable(ABC):
    @abstractmethod
    def hit(self, r: ray, ray_tmin: float, ray_tmax: float) -> "hit_record":
        """Return true if ray hits the hittable, false otherwise"""
        pass
    

class hittable_list(hittable):
    objects: list[hittable] = []

    def add(self, object: hittable):
        self.objects.append(object)

    def clear(self):
        self.objects.clear()

    def hit(self, r, ray_tmin, ray_tmax):
        rec = hit_record()
        hit_anything = False
        closest_so_far = ray_tmax

        for object in self.objects:
            temp_rec = object.hit(r, ray_tmin, closest_so_far)
            if temp_rec.is_hit:
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec

        return rec