from solid import *


__all__ = [
    "PCB_THICKNESS",
    "PIZW_LENGTH",
    "PIZW_WIDTH",
    "pizerow",
]


PCB_THICKNESS = 1.6
PIZW_LENGTH = 65
PIZW_WIDTH = 30


class SolidObject:
    def __init__(self, parent=None, coordinate=(0, 0, 0)):
        self.parent = parent
        self.coordinate = coordinate
        self.children = []
        if parent:
            parent.addChild(self)

    def addChild(self, child):
        child.parent = self
        self.children.append(child)

    @property
    def coordinate(self):
        if self.parent:
            return (
                self.parent.coordinate[0] + self._coordinate[0],
                self.parent.coordinate[1] + self._coordinate[1],
                self.parent.coordinate[2] + self._coordinate[2],
            )
        return self._coordinate

    @coordinate.setter
    def coordinate(self, coordinate):
        self._coordinate = coordinate


class PCBMountingHole(SolidObject):
    def __init__(self, radius, thickness, parent=None, coordinate=(0, 0, 0)):
        super().__init__(parent, coordinate)
        self.radius = radius
        self.thickness = thickness

    def geometry(self, parent_geometry=None):
        this_geometry = cylinder(r=self.radius, h=self.thickness, segments=32, center=True)
        this_geometry = translate(self.coordinate)(this_geometry)
        if parent_geometry:
            this_geometry = difference()(
                parent_geometry,
                this_geometry
            )
        return this_geometry


class PCBDevice(SolidObject):
    def __init__(self, geometry, parent=None, coordinate=(0, 0, 0)):
        super().__init__(parent, coordinate)
        self._geometry = geometry

    def geometry(self, parent_geometry=None):
        pass


class PCB(SolidObject):
    def __init__(self, length, width, thickness, corner_radius, parent=None, coordinate=(0, 0, 0)):
        super().__init__(parent, coordinate)
        self.length = length
        self.width = width
        self.thickness = thickness
        self.corner_radius = corner_radius
        self.corner_displacements = (
            self.length / 2 - self.corner_radius,
            self.width / 2 - self.corner_radius,
            0
        )

    def _corner(self):
        corner = polygon(
            points = [
                # Top Face
                (-self.corner_radius, -self.corner_radius,  0),  # 0
                (-self.corner_radius,  self.corner_radius,  0),  # 1
                ( 0                 ,  self.corner_radius,  0),  # 2
                ( self.corner_radius,  0                 ,  0),  # 3
                ( self.corner_radius, -self.corner_radius,  0),  # 4
            ],
        )
        corner = linear_extrude(PCB_THICKNESS, center=True)(corner)
        corner = union()(
            cylinder(r=self.corner_radius, h=self.thickness, segments=32, center=True),
            corner,
        )
        corner = hull()(corner)
        return corner

    def geometry(self, parent_geometry=None):
        this_geometry = union()(
            cube((self.length - 4 * self.corner_radius, self.width, PCB_THICKNESS), center=True),
            translate((-self.corner_displacements[0], 0, 0))(cube((2 * self.corner_radius, self.width - 4 * self.corner_radius, PCB_THICKNESS), center=True)),
            translate(( self.corner_displacements[0], 0, 0))(cube((2 * self.corner_radius, self.width - 4 * self.corner_radius, PCB_THICKNESS), center=True)),
            translate(( self.corner_displacements[0], self.corner_displacements[1], 0))(rotate((0, 0,   0))(self._corner())),
            translate((-self.corner_displacements[0], self.corner_displacements[1], 0))(rotate((0, 0,  90))(self._corner())),
            translate((-self.corner_displacements[0],-self.corner_displacements[1], 0))(rotate((0, 0, 180))(self._corner())),
            translate(( self.corner_displacements[0],-self.corner_displacements[1], 0))(rotate((0, 0, 270))(self._corner())),
        )
        this_geometry = hull()(this_geometry)
        this_geometry = translate(self.coordinate)(this_geometry)
        if parent_geometry:
            this_geometry = union()(
                parent_geometry,
                this_geometry
            )
        for child in self.children:
            this_geometry = child.geometry(this_geometry)
        return this_geometry


# PCB Dimensions (mm)
#   65 x 30 x 1.6
# Corner Radius 3mm
# Mounting Holes # M2.5
pizw = PCB(65, 30, PCB_THICKNESS, 3)
PCBMountingHole(1.25, PCB_THICKNESS, coordinate=( pizw.corner_displacements[0], pizw.corner_displacements[1], 0), parent=pizw)
PCBMountingHole(1.25, PCB_THICKNESS, coordinate=(-pizw.corner_displacements[0], pizw.corner_displacements[1], 0), parent=pizw)
PCBMountingHole(1.25, PCB_THICKNESS, coordinate=(-pizw.corner_displacements[0],-pizw.corner_displacements[1], 0), parent=pizw)
PCBMountingHole(1.25, PCB_THICKNESS, coordinate=( pizw.corner_displacements[0],-pizw.corner_displacements[1], 0), parent=pizw)

pizerow = pizw.geometry()
