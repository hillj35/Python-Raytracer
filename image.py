import sys
import math
from TracerTypes.hittable import hit_record, hittable, hittable_list
from TracerTypes.sphere import sphere
from TracerTypes.vec3 import vec3 as color, vec3 as vec3
from TracerTypes.color import write_color
from TracerTypes.ray import ray

def ray_color(ray: "ray", world: hittable) -> color:
    rec = world.hit(ray, 0, float("inf"))
    if rec.is_hit:
        return 0.5 * (rec.normal + color(1, 1, 1))

    unit_direction = ray._direction.normalized()
    a = 0.5 * (unit_direction.y + 1.0)
    return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(0.5, 0.7, 1.0)
    
def write_image(aspect_ratio: float, width: int, filename: str):
    with open(f"{filename}.ppm", "w") as file:
        # Calculate height 
        height = int(width / aspect_ratio)
        height = 1 if height < 1 else height

        # World
        world = hittable_list()
        world.add(sphere(vec3(0, -100.5, -1), 100))
        world.add(sphere(vec3(0,0,-1), 0.5))

        # Camera 
        focal_length = 1.0
        viewport_height = 2.0
        viewport_width = viewport_height * (width / height)
        camera_center = vec3(0, 0, 0)

        # Calculate vectors across vertical and horizontal viewport edges
        viewport_u = vec3(viewport_width, 0, 0)
        viewport_v = vec3(0, -viewport_height, 0)

        # Horizontal and Vertical delta vectors from pixel to pixel
        pixel_delta_u = viewport_u / width
        pixel_delta_v = viewport_v / height

        # Calculate location of upper left pixel
        viewport_upper_left = camera_center - vec3(0, 0, focal_length) - viewport_u / 2 - viewport_v / 2
        pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

        # Write headers 
        file.write("P3\n")
        file.write(f"{width} {height}\n255\n")

        for j in range(height):
            # Progress indicator
            sys.stdout.write("\033[K")
            print(f"Scanlines Remaining: {height - j}", end="\r")

            for i in range(width):
                pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
                ray_direction = pixel_center - camera_center
                r = ray(camera_center, ray_direction)

                pixel_color = ray_color(r, world)
                write_color(file, pixel_color)

        sys.stdout.write("\033[K")
        print("Done Writing")