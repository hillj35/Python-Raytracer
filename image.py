import sys

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
                r = i / (width - 1)
                g = j / (height - 1)
                b = 0

                ir = int(255.999 * r)
                ig = int(255.999 * g)
                ib = int(255.999 * b)

                file.write(f"{ir} {ig} {ib}\n")

        sys.stdout.write("\033[K")
        print("Done Writing")