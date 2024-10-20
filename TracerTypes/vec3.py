import math
from TracerTypes.tracer_util import random_float

def dot(lhv: "vec3", rhv: "vec3") -> float:
    return lhv.x * rhv.x + lhv.y * rhv.y + lhv.z * rhv.z

def cross(lhv: "vec3", rhv: "vec3") -> "vec3":
    return vec3(lhv.y * rhv.z - lhv.z * rhv.y,
                lhv.z * rhv.x - lhv.x * rhv.z,
                lhv.x * rhv.y - lhv.y * rhv.x)

def random_unit_vector() -> "vec3":
    while(True):
        p = vec3.random(-1, 1)
        lensq = p.length_squared()
        if 1e-160 < lensq <= 1:
            return p / math.sqrt(lensq)
        
def random_on_hemisphere(normal: "vec3") -> "vec3":
    on_unit_sphere = random_unit_vector()
    if dot(on_unit_sphere, normal) > 0.0:
        return on_unit_sphere
    else:
        return -on_unit_sphere

class vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{{{self.x},{self.y},{self.z}}}"
    
    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "vec3"):
        return vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        
    def __iadd__(self, other): 
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, other: float) -> "vec3":
        return vec3(self.x * other, self.y * other, self.z * other)
    
    def __rmul__(self, other: float) -> "vec3":
        return vec3(self.x * other, self.y * other, self.z * other)
    
    def __truediv__(self, other: float) -> "vec3":
        return vec3(self.x / other, self.y / other, self.z / other)

    @property
    def r(self) -> int:
        return self.x
    
    @property
    def g(self) -> int:
        return self.y
    
    @property
    def b(self) -> int:
        return self.z
    
    def magnitude(self) -> float:
        return math.sqrt(self.length_squared())
    
    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalized(self) -> "vec3":
        return self / self.magnitude()
    
    # static methods
    def random(min: float = 0, max: float = 1) -> "vec3":
        return vec3(random_float(min,max), random_float(min,max), random_float(min,max))
    