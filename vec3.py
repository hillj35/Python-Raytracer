class vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{{{self.x},{self.y},{self.z}}}"

    def __add__(self, other):
        return vec3(self.x + other.x, self.y - other.y, self.z - other.z)

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

    @property
    def r(self) -> int:
        return self.x
    
    @property
    def g(self) -> int:
        return self.y
    
    @property
    def b(self) -> int:
        return self.z