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
