from solid import cube, minkowski, sphere, translate


def rounded_cube(size, corner_radius, segments=None, center=False):
    if isinstance(size, (int, float)):
        size = (size - corner_radius,) * 3
    else:
        size = (item - corner_radius for item in size)
    return translate((corner_radius,)*3)(
        minkowski()(
            cube(size),
            sphere(corner_radius, segments=segments)
        )
    )
