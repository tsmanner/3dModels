from solid import cube, cylinder, intersection, linear_extrude, minkowski, mirror, rotate, sphere, translate, union
from solidext import Point, XY, XYZ, rounded_rectangle


def rounded_cube(size, corner_radius, segments=None, center=False):
    if isinstance(corner_radius, (int, float)):
        corner_radius = XYZ(
            (corner_radius, corner_radius, corner_radius, corner_radius),
            (corner_radius, corner_radius, corner_radius, corner_radius),
            (corner_radius, corner_radius, corner_radius, corner_radius),
        )
    else:
        corner_radius = XYZ(*corner_radius)
    if isinstance(size, (int, float)):
        size = XYZ(size, size, size)
    else:
        size = XYZ(*size)

    shapex = linear_extrude(size.x)(rounded_rectangle(XY(size.z, size.y), corner_radius.z, segments))
    shapex = rotate((0, 90, 0))(shapex)
    shapex = translate(XYZ(0, 0, size.z))(shapex)

    shapey = linear_extrude(size.y)(rounded_rectangle(XY(size.x, size.z), corner_radius.y, segments))
    shapey = rotate((90, 0, 0))(shapey)
    shapey = translate(XYZ(0, size.y, 0))(shapey)

    shapez = linear_extrude(size.z)(rounded_rectangle(XY(size.x, size.y), corner_radius.x, segments))

    # shapey = translate((15, 0, 0))(shapey)
    # shapez = translate((30, 0, 0))(shapez)

    rc = intersection()(
    # rc = union()(
        shapex,
        shapey,
        shapez
    )
    return rc


def minkowski_rounded_cube(size, corner_radius, segments=None, center=False):
    if isinstance(size, (int, float)):
        size = XYZ(
            size - 2 * corner_radius,
            size - 2 * corner_radius,
            size - 2 * corner_radius,
        )
    else:
        size = XYZ(*size) -  2 * corner_radius
    return translate((corner_radius, corner_radius, corner_radius))(
        minkowski()(
            cube(size),
            sphere(corner_radius, segments=segments)
        )
    )
