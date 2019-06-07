from solid import linear_extrude, minkowski, polygon, sphere, translate, offset
from solidext import Point, XY, XYZ, rounded_rectangle


def triangle_prism(a, b, c, thickness):
    return linear_extrude(thickness)(polygon((a, b, c, a)))


def rounded_triangle_prism(a, b, c, thickness, corner_radius, segments=32):
    return minkowski()(
        triangle_prism(a, b, c, thickness - 2*corner_radius),
        sphere(corner_radius, segments=segments)
    )
