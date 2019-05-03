from solid import cube, minkowski, sphere, translate


def rounded_cube(size, corner_radius, segments=None, center=False):
    if isinstance(size, (int, float)):
        size = (
            size - 2 * corner_radius,
            size - 2 * corner_radius,
            size - 2 * corner_radius,
        )
    else:
        size = (
            size[0] - 2 * corner_radius,
            size[1] - 2 * corner_radius,
            size[2] - 2 * corner_radius,
        )
    return translate((corner_radius, corner_radius, corner_radius))(
        minkowski()(
            cube(size),
            sphere(corner_radius, segments=segments)
        )
    )
