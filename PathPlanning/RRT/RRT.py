"""
RRT path planning implementation with python
"""
from PathPlanning.utils import *
import random
import math

class RRTPlanner(PathPlanner):
    """
    Path Planner using RRT algorithm.
    """
    def __init__(self, map, iterations=1e4, epsilon=0.05, stepSize=5):
        PathPlanner.__init__(self)
        self.nodeList = []
        self.map = map
        self.iterations = iterations
        self.epsilon = epsilon
        self.stepSize = stepSize

    def plan(self, start, target):
        self.nodeList = []
        self.nodeList.append(Node(start))
        for iteration in range(int(self.iterations)):
            # random sample
            randNode = Node(self.randomSample(self.epsilon, target))
            # find the nearest node
            nearestNode = self.findNearestNode(randNode)
            # expand the tree
            theta = math.atan2(randNode.pos.y - nearestNode.pos.y, randNode.pos.x - nearestNode.pos.x)
            newNode = Node(nearestNode.pos + Vector(self.stepSize * math.cos(theta), self.stepSize * math.sin(theta)), nearestNode)

            # outside the map
            if self.map.out_of_map(newNode.pos):
                continue
            # in the node list
            if self.inNodeList(newNode):
                continue
            # meet obstacles
            if self.check_obstacle(newNode.pos):
                continue

            self.nodeList.append(newNode)
            if newNode.pos.dist(target) < self.stepSize:
                print("final")
                self.finalPath = []
                self.finalPath.append(target)
                currentNode = self.nodeList[-1]
                self.finalPath.append(currentNode.pos)
                while currentNode.parent is not None:
                    self.finalPath.append(currentNode.parent.pos)
                    currentNode = currentNode.parent
                self.finalPath.reverse()
                break

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

    def check_obstacle(self, pos):
        for obs in self.map.obstacles:
            if obs.check_collision(pos, 10):
                return True
        return False
