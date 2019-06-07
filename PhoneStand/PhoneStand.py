from functools import lru_cache
import os
from solid import *
from solidext import XY, Point, rounded_cube, minkowski_rounded_cube, rounded_triangle_prism, triangle_prism
from math import radians, cos, sin, tan


class Phone:
    def __init__(self, phone_length, phone_width, phone_thickness, lean_angle, corner_radius=None, corner_segments=32, offset=None):
        self.phone_length = phone_length
        self.phone_width = phone_width
        self.phone_thickness = phone_thickness
        self.lean_angle = lean_angle
        self.corner_radius = corner_radius
        self.corner_segments = corner_segments
        self.offset = offset if offset is not None else Point(0, self.phone_length/2, 0)

        theta = -lean_angle
        theta_rad = radians(theta)

        # Bottom Back
        self.bb = self.offset
        # Center Back
        self.cb = Point(-abs(self.phone_width/2 * sin(theta_rad)), 0, abs(self.phone_width/2 * cos(theta_rad)))
        # Bottom Center
        self.bc = Point(abs(self.phone_thickness/2 * cos(theta_rad)), 0, abs(self.phone_thickness/2 * sin(theta_rad)))
        # True Center
        self.cc = self.bc + self.cb
        # Bottom Front
        self.bf = self.bc + self.bc
        # Center Front
        self.cf = self.cb + self.bf
        # Top Back
        self.tb = self.cb + self.cb
        # Top Center
        self.tc = self.tb + self.bc
        # Top Front
        self.tf = self.tb + self.bf

        self.bb.y = self.phone_length/2 if self.offset is None else self.offset.y
        self.cb.y = self.bb.y
        self.bc.y = self.bb.y
        self.cc.y = self.bb.y
        self.bf.y = self.bb.y
        self.cf.y = self.bb.y
        self.tb.y = self.bb.y
        self.tc.y = self.bb.y
        self.tf.y = self.bb.y

        self.refs = union()(
            translate(self.cc)(sphere(1, segments=32)),

            translate(self.tc)(sphere(1, segments=32)),
            translate(self.bc)(sphere(1, segments=32)),
            translate(self.cb)(sphere(1, segments=32)),
            translate(self.cf)(sphere(1, segments=32)),

            translate(self.bb)(sphere(1, segments=32)),
            translate(self.bf)(sphere(1, segments=32)),
            translate(self.tb)(sphere(1, segments=32)),
            translate(self.tf)(sphere(1, segments=32)),
        )

        # Construct the Phone
        if self.corner_radius is not None:
            self.geometry = minkowski_rounded_cube((
                self.phone_thickness,
                self.phone_length,
                self.phone_width,
            ), self.corner_radius, self.corner_segments)
        else:
            self.geometry = cube((
                self.phone_thickness,
                self.phone_length,
                self.phone_width,
            ))
        self.geometry = rotate((0, theta, 0))(translate(self.offset + Point(0, -self.phone_length/2, 0))(self.geometry))


def phone_stand(phone_length, phone_width, phone_thickness, lean_angle, corner_radius=None, corner_segments=32):
    landscape_phone = Phone(phone_length, phone_width, phone_thickness, lean_angle, corner_radius, corner_segments)
    portrait_phone = Phone(phone_width, phone_length, phone_thickness, lean_angle, corner_radius, corner_segments, Point(0, phone_length/2, 0))

    theta = -lean_angle
    theta_rad = radians(theta)

    thickness = 2
    mkrad = 0.75
    corner_segments = 32

    # Generate geometry for the bottom of the front section
    width = min(phone_length/2, phone_width)
    length = landscape_phone.bf.x
    translate_point = Point(mkrad, width/2, thickness)
    stand_base = rounded_cube((length + 3 * mkrad, width, thickness), mkrad, corner_segments)
    stand_base = translate(landscape_phone.bb - translate_point)(stand_base)

    # Generate geometry for the front of the front section
    length = thickness + landscape_phone.bf.z + 2
    translate_point = Point(-landscape_phone.bf.x, width/2, thickness)
    stand_front = rounded_cube((thickness, width, length), mkrad, corner_segments)
    stand_front = translate(landscape_phone.bb - translate_point)(stand_front)

    # Generate geometry for the bottom of the support section
    width = 20
    length = max(-portrait_phone.tb.x, 0)
    stand_support = rounded_cube((length + 2 * mkrad, width, thickness), mkrad, corner_segments)
    stand_support = translate(landscape_phone.bb - Point(length, width/2, thickness))(stand_support)

    # Generate geometry for the support that holds the phone up
    length = min(phone_length, phone_width, max(phone_length * 3/8, phone_width/2))
    translate_point = Point(
        thickness * cos(theta_rad) + mkrad * 2 * sin(theta_rad),
        width/2,
        -thickness * sin(theta_rad) + mkrad * 2 * cos(theta_rad)
    )
    stand_back = rounded_cube((thickness, width, length + 2 * mkrad), mkrad, corner_segments)
    stand_back = rotate((0, theta, 0))(stand_back)
    stand_back = translate(landscape_phone.bb - translate_point)(stand_back)

    # Generate geometry for additional support fin for the back
    length = length / 3
    translate_point = Point(
        (landscape_phone.cb.x - landscape_phone.bb.x - 2*mkrad),
        (thickness - 2 * mkrad) / 2,
        0
    )
    stand_support_fin = rounded_triangle_prism(
        XY(0, 0),
        XY(-landscape_phone.cb.x, 0),
        XY(0, landscape_phone.cb.z),
        thickness,
        mkrad,
        corner_radius
    )
    stand_support_fin = rotate((90, 0, 0))(stand_support_fin)
    stand_support_fin = translate(landscape_phone.bb + translate_point)(stand_support_fin)

    stand = union()(
        stand_base,
        stand_front,
        stand_support,
        stand_back,
        stand_support_fin,
    )

    return union()(
        # landscape_phone.geometry,
        # landscape_phone.refs,
        # portrait_phone.geometry,
        # portrait_phone.refs,
        stand,
    )


def main():
    filename = os.path.join(os.path.dirname(__file__), "PhoneStand.scad")
    length = 158.5
    width = 77.7
    thickness = 8
    lean_angle = 30
    scad_render_to_file(
        phone_stand(length, width, thickness, lean_angle, 1, 48),
        filename
    )


if __name__ == "__main__":
    main()
