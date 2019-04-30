from solid import *

PCB_THICKNESS = 1.6


# Corner Radius 3mm
# Mounting Holes # M2.5
corner = polyhedron(
    points = [
        # Top Face
        (-3, -3, PCB_THICKNESS/2),  # 0
        (-3,  3, PCB_THICKNESS/2),  # 1
        ( 0,  3, PCB_THICKNESS/2),  # 2
        ( 3,  0, PCB_THICKNESS/2),  # 3
        ( 3, -3, PCB_THICKNESS/2),  # 4
        # Bottom Face
        (-3, -3, -PCB_THICKNESS/2),  # 5
        (-3,  3, -PCB_THICKNESS/2),  # 6
        ( 0,  3, -PCB_THICKNESS/2),  # 7
        ( 3,  0, -PCB_THICKNESS/2),  # 8
        ( 3, -3, -PCB_THICKNESS/2),  # 9
    ],
    faces = [
        (0, 1, 2, 3, 4),
        (5, 6, 1, 0),
        (6, 7, 2, 1),
        (7, 8, 3, 2),
        (8, 9, 4, 3),
        (9, 5, 0, 4),
        (9, 8, 7, 6, 5),
    ],
)

corner = union()(
    cylinder(r=3, h=PCB_THICKNESS, segments=32, center=True),
    corner,
)

corner = hull()(corner)

corner = difference()(
    corner,
    cylinder(r=1.25, h=PCB_THICKNESS, segments=32, center=True),
)


# PCB Dimensions (mm)
#   65 x 30 x 1.6
pizerow = union()(
    cube((53, 30, PCB_THICKNESS), center=True),
    translate((-29.5, 0, 0))(cube((6, 18, PCB_THICKNESS), center=True)),
    translate(( 29.5, 0, 0))(cube((6, 18, PCB_THICKNESS), center=True)),
    translate(( 29.5,  12, 0))(rotate((0, 0,   0))(corner)),
    translate((-29.5,  12, 0))(rotate((0, 0,  90))(corner)),
    translate((-29.5, -12, 0))(rotate((0, 0, 180))(corner)),
    translate(( 29.5, -12, 0))(rotate((0, 0, 270))(corner)),
)
