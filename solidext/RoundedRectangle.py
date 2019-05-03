from solid import circle, polygon, square, union
from solidext import Point


def rounded_cube(size: Point, corner_radius, center=False):
    if isinstance(size, (int, float)):
        size = Point(size, size, size)

    def _corner(self):
        corner = polygon(
            points = [
                # Top Face
                (-corner_radius, -corner_radius,  0),  # 0
                (-corner_radius,  corner_radius,  0),  # 1
                ( 0            ,  corner_radius,  0),  # 2
                ( corner_radius,  0            ,  0),  # 3
                ( corner_radius, -corner_radius,  0),  # 4
            ],
        )
        corner = union()(
            circle(r=corner_radius, segments=32),
            corner,
        )
        return corner

    rc = square((size.x - 4 * corner_radius, size.y), center=True),



    corner_radius = corner_radius
    corner_displacements = (
        size.x / 2 - corner_radius,
        size.y / 2 - corner_radius,
    )
