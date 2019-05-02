import os
from solid import *
from math import radians, cos, sin, tan


class Point(list):
    def __init__(self, x, y, z):
        super().__init__()
        self.append(x)
        self.append(y)
        self.append(z)

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, value):
        self[2] = value

    def __add__(self, other):
        return Point(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )


def phone_stand(length, width, thickness, lean_angle):
    theta = -lean_angle
    theta_rad = radians(theta)

    # Bottom Back
    bb = Point(0, 0, 0)
    # Center Back
    cb = Point(-abs(width/2 * sin(theta_rad)), 0, abs(width/2 * cos(theta_rad)))
    # Bottom Center
    bc = Point(abs(thickness/2 * cos(theta_rad)), 0, abs(thickness/2 * sin(theta_rad)))
    # True Center
    cc = bc + cb
    # Bottom Front
    bf = bc + bc
    # Center Front
    cf = cb + bf
    # Top Back
    tb = cb + cb
    # Top Center
    tc = tb + bc
    # Top Front
    tf = tb + bf

    bb.y = length/2
    cb.y = bb.y
    bc.y = bb.y
    cc.y = bb.y
    bf.y = bb.y
    cf.y = bb.y
    tb.y = bb.y
    tc.y = bb.y
    tf.y = bb.y

    # Construct the Phone
    phone = cube((
        thickness,
        length,
        width,
    ))
    phone = rotate((0, theta, 0))(phone)

    # stand_thickness = 2
    # stand_width = 2 * cb.y
    # stand_length = min(length/2, width)
    # # Construct the Stand Front
    # stand_front = cube((stand_length, stand_width, stand_thickness))
    # stand_front = translate((bc.x, bc.y, bc.z - stand_thickness))(stand_front)

    # stand_base = cube((stand_width, tb.y - bf.y, stand_thickness))
    # stand_base = translate((0, 0, bc.z - stand_thickness))(stand_base)

    # stand_back = cube((stand_length, stand_width, stand_thickness))
    # stand_back = rotate((90-theta, 0, 0))(stand_back)
    # stand_back = translate((bc.x, bc.y + stand_width/2 + stand_thickness, bc.z + stand_thickness))(stand_back)

    both = union()(
        phone,
        # stand_front,
        # stand_base,
        # stand_back,

        translate(cc)(sphere(1, segments=32)),

        translate(tc)(sphere(1, segments=32)),
        translate(bc)(sphere(1, segments=32)),
        translate(cb)(sphere(1, segments=32)),
        translate(cf)(sphere(1, segments=32)),

        translate(bb)(sphere(1, segments=32)),
        translate(bf)(sphere(1, segments=32)),
        translate(tb)(sphere(1, segments=32)),
        translate(tf)(sphere(1, segments=32)),
    )

    return both


scad_render_to_file(
    phone_stand(
        158.5,
        77.7,
        8,
        0,
    ),
    os.path.join(os.path.dirname(__file__), "PhoneStand.scad")
)
