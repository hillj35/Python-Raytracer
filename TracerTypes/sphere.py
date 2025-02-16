from TracerTypes.hittable import hittable, hit_record
from TracerTypes.ray import ray
from TracerTypes.material import material
from TracerTypes.vec3 import vec3, dot
import math

class sphere(hittable):
    def __init__(self, center: vec3, radius: float, mat: material):
        self.center = center
        self.radius = max(0, radius)
        self.mat = mat

    def hit(self, r, ray_t):
        rec = hit_record()
        rec.is_hit = False
        
        oc = self.center - r._origin
        a = r._direction.length_squared()
        h = dot(r._direction, oc)
        c = oc.length_squared() - self.radius * self.radius
        discriminant = h * h - a * c
    
        if discriminant < 0:
            return rec
        
        sqrtd = math.sqrt(discriminant)

        # find the nearest root that lies in the acceptable range
        root = (h - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (h + sqrtd) / a
            if not ray_t.surrounds(root):
                return rec
            
        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.mat = self.mat
        rec.is_hit = True

        return rec