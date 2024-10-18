import math

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

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

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