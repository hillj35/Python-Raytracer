from vec3 import vec3 as color

def write_color(file, color):
    rbyte = int(255.999 * color.r)
    gbyte = int(255.999 * color.g)
    bbyte = int(255.999 * color.b)

    file.write(f"{rbyte} {gbyte} {bbyte}\n")
