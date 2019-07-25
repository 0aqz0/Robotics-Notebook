# author: 0aqz0
# date: 2018/11/24
"""
RRT path planning implementation with python
"""
from ..utils import PathPlanner, Point, Node, Vector
import random
import math

class RRTPlanner(PathPlanner):
    """
    Path Planner using RRT algorithm.
    """
    def __init__(self, start, target, map, iterations=1e5, epsilon=0.05, stepSize=5):
        PathPlanner.__init__(self)
        self.nodeList = []
        self.start = start
        self.target = target
        self.map = map
        self.iterations = iterations
        self.epsilon = epsilon
        self.stepSize = stepSize

    def plan(self):
        self.nodeList = []
        self.nodeList.append(Node(self.start))
        for iter in range(self.iterations):
            # random sample
            randNode = Node(self.randomSample(self.epsilon, self.target))
            # find the nearest node
            nearestNode = self.findNearestNode(randNode)
            # expand the tree
            theta = math.atan2(randNode.pos.y - nearestNode.pos.y, randNode.pos.x - nearestNode.pos.x)
            newNode = Node(nearestNode.pos + Vector(self.stepSize * math.cos(theta), self.stepSize * math.sin(theta)), nearestNode)

            # outside the map
            if self.map.outOfMap(newNode.pos):
                continue
            # in the node list
            if self.inNodeList(newNode):
                continue
            # meet obstacles
            if False:
                continue

            self.nodeList.append(newNode)
            if newNode.pos.dist(self.target) < self.stepSize:
                print("final")
                self.finalPath = []
                self.finalPath.append(self.target)
                currentNode = self.nodeList[-1]
                self.finalPath.append(currentNode.pos)
                while currentNode.parent is not None:
                    self.finalPath.append(currentNode.parent.pos)
                    currentNode = currentNode.parent


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

    def inNodeList(self, node):
        for candidate in self.nodeList:
            if candidate.pos == node.pos:
                return True
        return False