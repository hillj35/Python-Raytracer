import sys
from vec3 import vec3 as color, vec3 as vec3
from color import write_color

def write_image(height, width, filename):
    with open(f"{filename}.ppm", "w") as file:
        # Write headers 
        file.write("P3\n")
        file.write(f"{width} {height}\n255\n")

        for j in range(height):
            # Progress indicator
            sys.stdout.write("\033[K")
            print(f"Scanlines Remaining: {height - j}", end="\r")

            for i in range(width):
                pixel_color = color(i/(width-1), j/(height-1), 0)
                write_color(file, pixel_color)

        sys.stdout.write("\033[K")
        print("Done Writing")