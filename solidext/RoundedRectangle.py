from math import cos, radians, sin
from solid import circle, polygon, square, union
from solidext import Point, XY, XYZ


def rounded_rectangle(size: XY, corner_radius, segments):
    if isinstance(size, (int, float)):
        size = XY(size, size)
    if isinstance(corner_radius, (int, float)):
        corner_radius = (corner_radius, corner_radius, corner_radius, corner_radius)

    corner_points = [
        XY(size.x - corner_radius[0], size.y - corner_radius[0]),
        XY(         corner_radius[1], size.y - corner_radius[1]),
        XY(         corner_radius[2],          corner_radius[2]),
        XY(size.x - corner_radius[3],          corner_radius[3]),
    ]

    theta = 0
    dtheta = 90
    theta_step = dtheta / (segments / 4)
    points = []
    # Go counter clockwise just in case we need to calculate a normal
    for cp, r in zip(corner_points, corner_radius):
        t = theta
        while t < theta + dtheta + theta_step:
            points.append(XY(cp.x + r * cos(radians(t)), cp.y + r * sin(radians(t))))
            t += theta_step
        theta += dtheta
    points.append(points[0])  # Close the polygon
    return polygon(points)
