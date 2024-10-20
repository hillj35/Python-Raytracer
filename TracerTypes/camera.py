import sys

from TracerTypes.hittable import hittable
from TracerTypes.ray import ray
from TracerTypes.vec3 import vec3 as vec3, vec3 as color, random_unit_vector
from TracerTypes.tracer_util import interval, random_float
from TracerTypes.color import write_color

class camera:
    aspect_ratio = 1.0
    image_width = 100
    samples_per_pixel = 10
    max_depth = 10

    image_height = 0
    center = vec3(0,0,0)
    pixel00_loc = vec3(0,0,0)
    pixel_delta_u = vec3(0,0,0)
    pixel_delta_v = vec3(0,0,0)
    pixel_sameples_scale = 0.1

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
                    pixel_color = color(0,0,0)
                    for sample in range(self.samples_per_pixel):
                        r = self.get_ray(i, j)
                        pixel_color += self.ray_color(r, self.max_depth, world)

                    write_color(file, self.pixel_sameples_scale * pixel_color)

            sys.stdout.write("\033[K")
            print("Done Writing")


    def initialize(self):
        # Calculate height 
        self.image_height = int(self.image_width / self.aspect_ratio)
        self.image_height = 1 if self.image_height < 1 else self.image_height

        self.pixel_sameples_scale = 1.0 / self.samples_per_pixel

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


    def ray_color(self, r: ray, depth: int, world: hittable) -> color:
        if depth <= 0:
            return color(0,0,0)

        rec = world.hit(r, interval(0.001, float("inf")))
        if rec.is_hit:
            direction = rec.normal + random_unit_vector()
            return 0.5 * self.ray_color(ray(rec.p, direction), depth - 1, world)

        unit_direction = r._direction.normalized()
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(0.5, 0.7, 1.0)
    
    def get_ray(self, i: int, j: int) -> ray:
        # Construct a camera ray originating from the origin and directed 
        # at randomly sampled point around the pixel location i, j

        offset = self.sample_square()
        pixel_sample = self.pixel00_loc + ((i + offset.x) * self.pixel_delta_u) + ((j + offset.y) * self.pixel_delta_v)
        ray_origin = self.center
        ray_direction = pixel_sample - ray_origin

        return ray(ray_origin, ray_direction)

    def sample_square(self) -> vec3:
        # returns the vector to a random point in the [-0.5, -0.5] - [0.5, 0.5] unit square
        return vec3(random_float(0, 1) - 0.5, random_float(0, 1) - 0.5, 0)