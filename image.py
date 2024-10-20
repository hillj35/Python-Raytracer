import math

from TracerTypes.camera import camera
from TracerTypes.hittable import hittable_list
from TracerTypes.sphere import sphere
from TracerTypes.vec3 import vec3 as color, vec3 as vec3
import TracerTypes.material as material
from TracerTypes.tracer_util import random_float

def write_image(aspect_ratio: float, width: int, filename: str):
    # World
    world = hittable_list()

    ground_material = material.lambertian(color(0.5, 0.5, 0.5))
    world.add(sphere(vec3(0, -1000, 0), 1000, ground_material))
              
    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random_float()
            center = vec3(a + 0.9*random_float(), 0.2, b + 0.9 * random_float())

            if ((center - vec3(4, 0.2, 0)).magnitude() > 0.9):
                if choose_mat < 0.8:
                    # diffuse
                    albedo = vec3.random() * vec3.random()
                    sphere_mat = material.lambertian(albedo)
                    world.add(sphere(center, 0.2, sphere_mat))
                elif choose_mat < 0.95:
                    # metal
                    albedo = vec3.random(0.5, 1.0)
                    fuzz = random_float(0, 0.5)
                    sphere_mat = material.metal(albedo, fuzz)
                    world.add(sphere(center, 0.2, sphere_mat))
                else:
                    # glass
                    sphere_mat = material.dielectric(1.5)
                    world.add(sphere(center, 0.2, sphere_mat))

    material1 = material.dielectric(1.5)
    world.add(sphere(vec3(0, 1, 0), 1.0, material1))

    material2 = material.lambertian(color(0.4, 0.2, 0.1))
    world.add(sphere(vec3(-4, 1, 0), 1.0, material2))

    material3 = material.metal(color(0.7, 0.6, 0.5), 0.0)
    world.add(sphere(vec3(4, 1, 0), 1.0, material3))

    

    # Camera
    cam = camera()
    cam.aspect_ratio = aspect_ratio
    cam.image_width = width
    cam.samples_per_pixel = 10

    cam.vfov = 20
    cam.lookfrom = vec3(13, 2, 3)
    cam.lookat = vec3(0, 0, 0)
    cam.vup = vec3(0, 1, 0)

    cam.defocus_angle = 0.6
    cam.focus_dist = 10.0

    cam.render(world, filename)
