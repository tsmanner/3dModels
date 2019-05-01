import os
from solid import *
from PiZeroW import *


bed = cube(
    (
        PIZW_LENGTH + 6,
        PIZW_WIDTH + 6,
        1
    ),
    center=True,
)

bed = translate((0, 0, -2))(bed)


model = union()(
    pizerow,
    # bed,
)


scad_render_to_file(model, os.path.join(os.path.dirname(__file__), "PaPirusZeroCase.scad"))
