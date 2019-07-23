# author: 0aqz0
# date: 2018/11/24
"""
RRT path planning implementation with python
"""
from ..utils import PathPlanner, Point
import random

class RRTPlanner(PathPlanner):
    """
    Path Planner using RRT algorithm.
    """
    def __init__(self, target, map, iterations=1e5, epsilon=0.05):
        PathPlanner.__init__(self)
        self.nodeList = []
        self.target = target
        self.map = map
        self.iterations = iterations
        self.epsilon = epsilon

    def plan(self):
        for iter in range(self.iterations):
            pass

    def findNearestNode(self, node):
        minDist = 1e10
        nearestNode = None
        for candidate in self.nodeList:
            if node.pos.dist(candidate.pos) < minDist:
                minDist = node.pos.dist(candidate.pos)
                nearestNode = candidate
        return nearestNode

    def randomSample(self, epsilon, target):
        if random.random() >= epsilon:
            return Point(self.map.left + self.map.length * random.random(), self.map.down + self.map.width * random.random())
        else:
            return target

    def inNodeList(self):
        pass