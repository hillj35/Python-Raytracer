from abc import ABC, abstractmethod
from TracerTypes.vec3 import vec3, dot
from TracerTypes.material import material
from TracerTypes.ray import ray
from TracerTypes.tracer_util import interval


class hit_record:
    p = vec3(0,0,0)
    normal = vec3(0,0,0)
    mat: material = None
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
    def hit(self, r: ray, ray_t: interval) -> "hit_record":
        """Return true if ray hits the hittable, false otherwise"""
        pass
    

class hittable_list(hittable):
    objects: list[hittable] = []

    def add(self, object: hittable):
        self.objects.append(object)

    def clear(self):
        self.objects.clear()

    def hit(self, r, ray_t):
        rec = hit_record()
        hit_anything = False
        closest_so_far = ray_t.max

        for object in self.objects:
            temp_rec = object.hit(r, interval(ray_t.min, closest_so_far))
            if temp_rec.is_hit:
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec

        return rec