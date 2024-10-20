import math
from TracerTypes.vec3 import vec3 as color
from TracerTypes.tracer_util import interval

def linear_to_gamma(linear_component: float) -> float:
    if linear_component > 0:
        return math.sqrt(linear_component)
    
    return 0

def write_color(file, color):
    intensity = interval(0.0, 0.999)

    r = linear_to_gamma(color.r)
    g = linear_to_gamma(color.g)
    b = linear_to_gamma(color.b)

    rbyte = int(256 * intensity.clamp(r))
    gbyte = int(256 * intensity.clamp(g))
    bbyte = int(256 * intensity.clamp(b))

    file.write(f"{rbyte} {gbyte} {bbyte}\n")
