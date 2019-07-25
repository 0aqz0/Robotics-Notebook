"""
collections of common structures
"""
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def dist(self, point):
        """
        Distance to another point
        :param point: another point
        :return: dist to another point
        """
        return math.sqrt(pow(self.x - point.x, 2) + pow(self.y - point.y, 2))


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Node:
    def __init__(self, pos, parent=None, cost=0):
        self.pos = pos
        self.parent = parent
        self.cost = cost

    def dist(self, node):
        """
        Distance to another node
        :param node: another node
        :return: dist to another node
        """
        return self.pos.dist(node.pos)


class Map:
    def __init__(self, top, down, left, right):
        self.top = max(top, down)
        self.down = min(top, down)
        self.left = min(left, right)
        self.right = max(left, right)
        self.length = math.fabs(left - right)
        self.width = math.fabs(top - down)

    def outOfMap(self, pos):
        return pos.x < self.left or pos.x > self.right or pos.y < self.down or pos.y > self.top


class GridMap(Map):
    def __init__(self, top, down, left, right, gridSize):
        Map.__init__(top=top, down=down, left=left, right=right)
        self.gridSize = gridSize


class PathPlanner:
    """
    superclass for path planning algorithms.
    """
    def __init__(self):
        self.finalPath = []

    def plan(self):
        """
        planning function.
        :return:
        """
        pass
