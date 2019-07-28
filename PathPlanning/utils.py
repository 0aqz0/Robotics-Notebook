"""
collections of common structures
"""
import math
import pyglet

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


class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mod(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))


class Node(object):
    def __init__(self, pos, parent=None, cost=0):
        self.pos = pos
        self.parent = parent
        self.cost = cost

    def dist(self, node):
        return self.pos.dist(node.pos)


class Obstacle(object):
    def __init__(self, pos):
        self.pos = pos

    def type(self):
        raise  NotImplementedError

    def dist(self, other):
        raise NotImplementedError

    def check_collision(self, other, avoidDist):
        raise NotImplementedError


class CircleObstacle(Obstacle):
    def __init__(self, pos, radius):
        Obstacle.__init__(self, pos)
        self.radius = radius

    def type(self):
        return "circle"

    def dist(self, other):
        return max(self.pos.dist(other) - self.radius, 0)

    def check_collision(self, other, avoidDist):
        return self.dist(other) <= avoidDist


class RectangleObstacle(Obstacle):
    def __init__(self, top, down, left, right):
        self.top = max(top, down)
        self.down = min(top, down)
        self.left = min(left, right)
        self.right = max(left, right)
        self.length = math.fabs(left - right)
        self.width = math.fabs(top - down)
        Obstacle.__init__(self, Point((left+right)/2, (top+down)/2))

    def type(self):
        return "rectangle"

    def dist(self, other):
        if other.x < self.left:
            if other.y > self.top:
                return other.dist(Point(self.left, self.top))
            elif other.y < self.down:
                return other.dist(Point(self.left, self.down))
            else:
                return math.fabs(other.x - self.left)
        elif other.x > self.right:
            if other.y > self.top:
                return other.dist(Point(self.right, self.top))
            elif other.y < self.down:
                return other.dist(Point(self.right, self.down))
            else:
                return math.fabs(other.x - self.right)
        else:
            if other.y > self.top:
                return math.fabs(other.y - self.top)
            elif other.y < self.down:
                return math.fabs(other.y - self.down)
            else:
                return  0

    def check_collision(self, other, avoidDist):
        return self.dist(other) <= avoidDist


class Map(object):
    def __init__(self, top, down, left, right):
        self.top = max(top, down)
        self.down = min(top, down)
        self.left = min(left, right)
        self.right = max(left, right)
        self.length = math.fabs(left - right)
        self.width = math.fabs(top - down)
        self.obstacles = []

    def out_of_map(self, pos):
        return pos.x < self.left or pos.x > self.right or pos.y < self.down or pos.y > self.top

    def check_collision(self, other, avoidDist):
        for obs in self.obstacles:
            if obs.check_collision(other, avoidDist):
                return True
        return False


class GridMap(Map):
    def __init__(self, top, down, left, right, gridSize):
        Map.__init__(top=top, down=down, left=left, right=right)
        self.gridSize = gridSize


class Viewer(object):
    def __init__(self, width, height, display=None):
        self.width = width
        self.height = height
        self.window = pyglet.window.Window(width=width, height=height, display=display)

    def close(self):
        self.window.close()

    def render(self):
        pass

    def draw_circle(self):
        pass

    def draw_polygon(self):
        pass

    def draw_line(self):
        pass

    def draw_obstacle(self):
        pass


class PathPlanner(object):
    """
    superclass for path planning algorithms.
    """
    def __init__(self):
        self.finalPath = []

    def plan(self, start, target):
        """
        Plans the path.
        """
        raise NotImplementedError
