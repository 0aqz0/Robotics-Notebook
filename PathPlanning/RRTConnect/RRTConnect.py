"""
RRTConnect path planning implementation with python
"""
from PathPlanning.utils import *
import random
import math

class RRTConnectPlanner(PathPlanner):
    """
    Path Planner using RRTConnect algorithm.
    """
    def __init__(self, map, iterations=1e4, epsilon=0.05, stepSize=5):
        PathPlanner.__init__(self)
        self.nodeList1 = []
        self.nodeList2 = []
        self.map = map
        self.iterations = iterations
        self.epsilon = epsilon
        self.stepSize = stepSize

    def plan(self, start, target):
        self.nodeList1 = []
        self.nodeList1.append(Node(start))
        self.nodeList2 = []
        self.nodeList2.append(Node(target))
        for iteration in range(int(self.iterations)):
            if iteration%2 == 0:
                expandList = self.nodeList1
                otherList = self.nodeList2
            else:
                expandList = self.nodeList2
                otherList = self.nodeList1
            # random sample
            randNode = Node(self.randomSample(self.epsilon, target))
            # find the nearest node
            nearestNode = self.findNearestNode(randNode, expandList)
            # expand the tree
            theta = math.atan2(randNode.pos.y - nearestNode.pos.y, randNode.pos.x - nearestNode.pos.x)
            newNode = Node(nearestNode.pos + Vector(self.stepSize * math.cos(theta), self.stepSize * math.sin(theta)), nearestNode)

            # outside the map
            if self.map.out_of_map(newNode.pos):
                continue
            # in the node list
            if self.inNodeList(newNode, expandList):
                continue
            # meet obstacles
            if self.check_obstacle(newNode.pos):
                continue

            expandList.append(newNode)
            checkNode = self.findNearestNode(newNode, otherList)
            if newNode.pos.dist(checkNode.pos) < self.stepSize:
                print("final")
                # path1
                finalPath1 = []
                currentNode = newNode
                finalPath1.append(currentNode.pos)
                while currentNode.parent is not None:
                    finalPath1.append(currentNode.parent.pos)
                    currentNode = currentNode.parent
                finalPath1.reverse()
                # path2
                finalPath2 = []
                currentNode = checkNode
                finalPath2.append(currentNode.pos)
                while currentNode.parent is not None:
                    finalPath2.append(currentNode.parent.pos)
                    currentNode = currentNode.parent

                self.finalPath = finalPath1 + finalPath2
                break

    def findNearestNode(self, node, nodelist):
        minDist = 1e10
        nearestNode = None
        for candidate in nodelist:
            if node.pos.dist(candidate.pos) < minDist:
                minDist = node.pos.dist(candidate.pos)
                nearestNode = candidate
        return nearestNode

    def randomSample(self, epsilon, target):
        if random.random() >= epsilon:
            return Point(self.map.left + self.map.length * random.random(), self.map.down + self.map.width * random.random())
        else:
            return target

    def inNodeList(self, node, nodelist):
        for candidate in nodelist:
            if candidate.pos == node.pos:
                return True
        return False

    def check_obstacle(self, pos):
        for obs in self.map.obstacles:
            if obs.check_collision(pos, 10):
                return True
        return False
