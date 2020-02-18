"""
collections of common structures
"""
from PathPlanning.geometry import *
from PathPlanning.render import Viewer

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

    def vertex(self):
        return (self.left, self.down), (self.left, self.top), (self.right, self.top), (self.right, self.down)

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


class Map(Viewer):
    def __init__(self, top, down, left, right, refresh=True):
        self.top = max(top, down)
        self.down = min(top, down)
        self.left = min(left, right)
        self.right = max(left, right)
        self.length = math.fabs(left - right)
        self.width = math.fabs(top - down)
        self.refresh = refresh
        Viewer.__init__(self, width=self.length, height=self.width)
        self.obstacles = []

    def out_of_map(self, pos):
        return pos.x < self.left or pos.x > self.right or pos.y < self.down or pos.y > self.top

    def add_obstacle(self, obs):
        self.obstacles.append(obs)

    def check_collision(self, other, avoidDist):
        for obs in self.obstacles:
            if obs.check_collision(other, avoidDist):
                return True
        return False

    def draw(self):
        # draw borders
        # self.draw_line(start=(self.left, self.down), end=(self.left, self.top), lineWidth=5)
        # self.draw_line(start=(self.left, self.top), end=(self.right, self.top), lineWidth=5)
        # self.draw_line(start=(self.right, self.top), end=(self.right, self.down), lineWidth=5)
        # self.draw_line(start=(self.right, self.down), end=(self.left, self.down), lineWidth=5)
        # draw geoms
        for geom in self.geoms:
            geom.render()
        # draw obstacles
        for obs in self.obstacles:
            if obs.type() == 'circle':
                self.draw_circle(pos=obs.pos.tuple(), radius=obs.radius)
            elif obs.type() == 'rectangle':
                self.draw_polygon(points=obs.vertex(), filled=True)
        if self.refresh:
            self.geoms = []


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
