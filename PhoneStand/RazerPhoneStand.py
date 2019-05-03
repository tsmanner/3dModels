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

    def __sub__(self, other):
        return Point(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )


def phone_stand(phone_length, phone_width, phone_thickness, lean_angle):
    theta = -lean_angle
    theta_rad = radians(theta)

    # Bottom Back
    bb = Point(0, 0, 0)
    # Center Back
    cb = Point(-abs(phone_width/2 * sin(theta_rad)), 0, abs(phone_width/2 * cos(theta_rad)))
    # Bottom Center
    bc = Point(abs(phone_thickness/2 * cos(theta_rad)), 0, abs(phone_thickness/2 * sin(theta_rad)))
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

    bb.y = phone_length/2
    cb.y = bb.y
    bc.y = bb.y
    cc.y = bb.y
    bf.y = bb.y
    cf.y = bb.y
    tb.y = bb.y
    tc.y = bb.y
    tf.y = bb.y

    refs = union()(
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

    # Construct the Phone
    phone = cube((
        phone_thickness,
        phone_length,
        phone_width,
    ))
    phone = rotate((0, theta, 0))(phone)

    thickness = 2

    width = min(phone_length/2, phone_width)
    length = bf.x
    stand_base = cube((length, width, thickness))
    stand_base = translate(bb - Point(0, width/2, thickness))(stand_base)

    width = 20
    length = max(-tb.x, 0)
    stand_support = cube((length, width, thickness))
    stand_support = translate(bb - Point(length, width/2, thickness))(stand_support)

    length = phone_width/2
    stand_back = cube((thickness, width, length))
    stand_back = rotate((0, theta, 0))(stand_back)
    stand_back = translate(bb - Point(thickness * cos(theta_rad), width/2, -thickness * sin(theta_rad)))(stand_back)

    width = min(phone_length/2, phone_width)
    length = thickness + bf.z + 1
    stand_front = cube((thickness, width, length))
    stand_front = translate(bb - Point(-bf.x, width/2, thickness))(stand_front)

    stand = union()(
        stand_base,
        stand_support,
        stand_back,
        stand_front,
    )

    return union()(
        # phone,
        # refs,
        stand,
    )


filename = os.path.join(os.path.dirname(__file__), "PhoneStand.scad")


scad_render_to_file(
    phone_stand(158.5, 77.7, 8, 20),
    filename
)
