import sys
import math

from TracerTypes.hittable import hittable
from TracerTypes.ray import ray
from TracerTypes.vec3 import vec3 as vec3, vec3 as color, cross, random_in_unit_disk
from TracerTypes.tracer_util import interval, random_float, degrees_to_radians
from TracerTypes.color import write_color
from TracerTypes.material import scatter_record

class camera:
    aspect_ratio = 1.0
    image_width = 100
    samples_per_pixel = 10
    max_depth = 10
    
    vfov = 90
    lookfrom = vec3(0,0,0)
    lookat = vec3(0,0,-1)
    vup = vec3(0,1,0)

    defocus_angle = 0
    focus_dist = 10

    image_height = 0
    center = vec3(0,0,0)
    pixel00_loc = vec3(0,0,0)
    pixel_delta_u = vec3(0,0,0)
    pixel_delta_v = vec3(0,0,0)
    pixel_sameples_scale = 0.1
    u = vec3()
    v = vec3()
    w = vec3()
    defocus_disk_u = vec3()
    defocus_disk_v = vec3()

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

        self.center = self.lookfrom

        # Camera 
        theta = degrees_to_radians(self.vfov)
        h = math.tan(theta / 2)
        viewport_height = 2.0 * h * self.focus_dist
        viewport_width = viewport_height * (self.image_width / self.image_height)

        # Calculate u,v,w unit basis vectors for the camera coordinate frame
        self.w = (self.lookfrom - self.lookat).normalized()
        self.u = cross(self.vup, self.w).normalized()
        self.v = cross(self.w, self.u)

        # Calculate vectors across vertical and horizontal viewport edges
        viewport_u = viewport_width * self.u
        viewport_v = viewport_height * -self.v

        # Horizontal and Vertical delta vectors from pixel to pixel
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # Calculate location of upper left pixel
        viewport_upper_left = self.center - (self.focus_dist * self.w) - viewport_u / 2 - viewport_v / 2
        self.pixel00_loc = viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)

        # Calculate the camera defocus disk basis vectors
        defocus_radius = self.focus_dist * math.tan(degrees_to_radians(self.defocus_angle / 2))
        self.defocus_disk_u = self.u * defocus_radius
        self.defocus_disk_v = self.v * defocus_radius


    def ray_color(self, r: ray, depth: int, world: hittable) -> color:
        if depth <= 0:
            return color(0,0,0)

        rec = world.hit(r, interval(0.001, float("inf")))
        if rec.is_hit:
            scatter_rec = rec.mat.scatter(r, rec)
            if scatter_rec.did_scatter:
                return scatter_rec.attenuation * self.ray_color(scatter_rec.scattered_ray, depth - 1, world)
            return color(0,0,0)

        unit_direction = r._direction.normalized()
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(0.5, 0.7, 1.0)
    
    def get_ray(self, i: int, j: int) -> ray:
        # Construct a camera ray originating from the defocus disk and directed 
        # at randomly sampled point around the pixel location i, j

        offset = self.sample_square()
        pixel_sample = self.pixel00_loc + ((i + offset.x) * self.pixel_delta_u) + ((j + offset.y) * self.pixel_delta_v)
        ray_origin = self.center if self.defocus_angle <= 0 else self.defocus_disk_sample()
        ray_direction = pixel_sample - ray_origin

        return ray(ray_origin, ray_direction)

    def sample_square(self) -> vec3:
        # returns the vector to a random point in the [-0.5, -0.5] - [0.5, 0.5] unit square
        return vec3(random_float(0, 1) - 0.5, random_float(0, 1) - 0.5, 0)
    
    def defocus_disk_sample(self) -> vec3:
        """Returns a random point in the camera defocus disk"""
        p = random_in_unit_disk()
        return self.center + (p.x * self.defocus_disk_u) + (p.y * self.defocus_disk_v)