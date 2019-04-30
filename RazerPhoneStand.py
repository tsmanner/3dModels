import solid

scad_object = solid.intersection()(
    solid.cube(10),
    solid.sphere(5, segments=75),
)

solid.scad_render_to_file(scad_object, "RazerPhoneStand.scad")
