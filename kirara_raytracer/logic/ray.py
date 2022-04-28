from glm import vec3, c_float


class Ray:
    origin: vec3
    direction: vec3

    def __init__(self, origin: vec3 = None, direction: vec3 = None):
        self.origin = origin or vec3()
        self.direction = direction or vec3()

    def at(self, t: c_float):
        return self.origin + t * self.direction


if __name__ == '__main__':
    pass
