import sys

from TracerTypes.hittable import hittable
from TracerTypes.ray import ray
from TracerTypes.vec3 import vec3 as vec3, vec3 as color
from TracerTypes.tracer_util import interval
from TracerTypes.color import write_color

class camera:
    aspect_ratio = 1.0
    image_width = 100

    image_height = 0
    center = vec3(0,0,0)
    pixel00_loc = vec3(0,0,0)
    pixel_delta_u = vec3(0,0,0)
    pixel_delta_v = vec3(0,0,0)

    def render(self, world: hittable, filename: str):
        self.initialize()

        # Write headers 
        with open(f"{filename}.ppm", "w") as file:
            file.write("P3\n")
            file.write(f"{self.image_width} {self.image_height}\n255\n")

            for j in range(self.image_height):
                # Progress indicator
                sys.stdout.write("\033[K")
                print(f"Scanlines Remaining: {self.image_height - j}", end="\r")

                for i in range(self.image_width):
                    pixel_center = self.pixel00_loc + (i * self.pixel_delta_u) + (j * self.pixel_delta_v)
                    ray_direction = pixel_center - self.center
                    r = ray(self.center, ray_direction)

                    pixel_color = self.ray_color(r, world)
                    write_color(file, pixel_color)

            sys.stdout.write("\033[K")
            print("Done Writing")


    def initialize(self):
        # Calculate height 
        self.image_height = int(self.image_width / self.aspect_ratio)
        self.image_height = 1 if self.image_height < 1 else self.image_height

        self.center = vec3(0, 0, 0)

        # Camera 
        focal_length = 1.0
        viewport_height = 2.0
        viewport_width = viewport_height * (self.image_width / self.image_height)

        # Calculate vectors across vertical and horizontal viewport edges
        viewport_u = vec3(viewport_width, 0, 0)
        viewport_v = vec3(0, -viewport_height, 0)

        # Horizontal and Vertical delta vectors from pixel to pixel
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # Calculate location of upper left pixel
        viewport_upper_left = self.center - vec3(0, 0, focal_length) - viewport_u / 2 - viewport_v / 2
        self.pixel00_loc = viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)


    def ray_color(self, r: ray, world: hittable) -> color:
        rec = world.hit(r, interval(0, float("inf")))
        if rec.is_hit:
            return 0.5 * (rec.normal + color(1, 1, 1))

        unit_direction = r._direction.normalized()
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(0.5, 0.7, 1.0)