class XY(list):
    def __init__(self, x, y):
        super().__init__()
        self.append(x)
        self.append(y)

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

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return XY(
                self.x + other,
                self.y + other,
            )
        return XY(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return XY(
                self.x - other,
                self.y - other,
            )
        return XY(
            self.x - other.x,
            self.y - other.y,
        )

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return XY(
                self.x / other,
                self.y / other,
            )
        return XY(
            self.x / other.x,
            self.y / other.y,
        )

    def __rshift__(self, amount):
        if amount == 0:
            return self
        if amount < 0:
            return self.__lshift__(-amount)
        return XY(
            self.x,
            self.y,
        ).__rshift__(amount-1)

    def __lshift__(self, amount):
        if amount == 0:
            return self
        if amount < 0:
            return self.__rshift__(-amount)
        return XY(
            self.y,
            self.x,
        ).__lshift__(amount-1)

    def __neg__(self):
        return XY(
            -self.x,
            -self.y
        )


class XYZ(XY):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.append(z)

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, value):
        self[2] = value

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return XYZ(
                self.x + other,
                self.y + other,
                self.z + other,
            )
        return XYZ(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return XYZ(
                self.x - other,
                self.y - other,
                self.z - other,
            )
        return XYZ(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return XYZ(
                self.x / other,
                self.y / other,
                self.z / other,
            )
        return XYZ(
            self.x / other.x,
            self.y / other.y,
            self.z / other.z,
        )

    def __rshift__(self, amount):
        if amount == 0:
            return self
        if amount < 0:
            return self.__lshift__(-amount)
        return XYZ(
            self.z,
            self.x,
            self.y,
        ).__rshift__(amount-1)

    def __lshift__(self, amount):
        if amount == 0:
            return self
        if amount < 0:
            return self.__rshift__(-amount)
        return XYZ(
            self.y,
            self.z,
            self.x,
        ).__lshift__(amount-1)

    def __neg__(self):
        return XYZ(
            -self.x,
            -self.y,
            -self.z
        )


Point = XYZ
