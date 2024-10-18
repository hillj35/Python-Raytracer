from TracerTypes.vec3 import vec3 as vec3

class ray:
    def __init__(self, origin: "vec3", direction: "vec3"):
        self._origin = origin
        self._direction = direction

    def at(self, t: float) -> "vec3":
        return self._origin + t * self._direction
    