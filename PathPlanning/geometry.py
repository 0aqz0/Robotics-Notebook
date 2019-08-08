"""
geometry elements
"""
import math

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def dist(self, other):
        return math.sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))

    def dir(self, other):
        return math.atan2(other.y - self.y, other.x - self.x)


class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mod(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))


def Polar2Vector(dist, theta):
    return Vector(dist*math.cos(theta), dist*math.sin(theta))