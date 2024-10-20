from TracerTypes.camera import camera
from TracerTypes.hittable import hittable_list
from TracerTypes.sphere import sphere
from TracerTypes.vec3 import vec3 as color, vec3 as vec3
import TracerTypes.material as material

def write_image(aspect_ratio: float, width: int, filename: str):
    # Materials
    material_ground = material.lambertian(color(0.8, 0.8, 0.0))
    material_center = material.lambertian(color(0.1, 0.2, 0.5))
    material_left = material.metal(color(0.8, 0.8, 0.8), 0.3)
    material_right = material.metal(color(0.8, 0.6, 0.2), 0.9)    
    
    # World
    world = hittable_list()
    world.add(sphere(vec3(0, -100.5, -1), 100, material_ground))
    world.add(sphere(vec3(0,0,-1.2), 0.5, material_center))
    world.add(sphere(vec3(-1.0,0,-1.0), 0.5, material_left))
    world.add(sphere(vec3(1.0,0,-1.0), 0.5, material_right))

    # Camera
    cam = camera()
    cam.aspect_ratio = aspect_ratio
    cam.image_width = width
    cam.samples_per_pixel = 10

    cam.render(world, filename)
