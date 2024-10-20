from TracerTypes.camera import camera
from TracerTypes.hittable import hittable_list
from TracerTypes.sphere import sphere
from TracerTypes.vec3 import vec3

def write_image(aspect_ratio: float, width: int, filename: str):
    # World
    world = hittable_list()
    world.add(sphere(vec3(0,0,-1), 0.5))
    world.add(sphere(vec3(0, -100.5, -1), 100))

    # Camera
    cam = camera()
    cam.aspect_ratio = aspect_ratio
    cam.image_width = width

    cam.render(world, filename)
