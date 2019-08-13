"""
RRT* Smart Path Planning Algorithm
"""
from PathPlanning.utils import *
import random

class RRTStarSmartPlanner(PathPlanner):
    """
        Path Planner using RRT* Smart algorithm.
    """
    def __init__(self, map, iterations=1e3, epsilon=0.2, step_size=10, biasing_radius=50, biasing_ratio=3):
        PathPlanner.__init__(self)
        self.nodeList = []
        self.map = map
        self.iterations = iterations
        self.epsilon = epsilon
        self.step_size = step_size
        self.biasing_radius = biasing_radius
        self.biasing_ratio = biasing_ratio
        self.beacons = []
        self.n = None
        self.cost = float('inf')

    def plan(self, start, target):
        self.nodeList = [Node(start)]
        # self.beacons = []
        # self.n = None
        # self.cost = float('inf')
        for iteration in range(int(self.iterations)):
            # random sample or intelligent sample
            if self.n is not None and (iteration - self.n)%self.biasing_ratio is 0:
                randNode = Node(self.intelligent_sample())
            else:
                randNode = Node(self.randomSample(self.epsilon, target))
            # find the nearest node
            nearestNode = self.findNearestNode(randNode)
            # expand the tree
            theta = math.atan2(randNode.pos.y - nearestNode.pos.y, randNode.pos.x - nearestNode.pos.x)
            newNode = Node(nearestNode.pos + Polar2Vector(self.step_size, theta), nearestNode,
                           nearestNode.cost + self.step_size)

            # outside the map
            if self.map.out_of_map(newNode.pos):
                continue
            # in the node list
            if self.inNodeList(newNode):
                continue
            # meet obstacles
            if self.check_obstacle(newNode.pos):
                continue

            # choose best parent
            radius = 100.0 * math.sqrt(math.log(len(self.nodeList)) / len(self.nodeList))
            self.chooseBestParent(newNode, radius)
            # rewire
            self.rewire(newNode, radius)

            self.nodeList.append(newNode)
            if newNode.pos.dist(target) < self.step_size:
                # generate final path
                finalPath = [target]
                currentNode = self.nodeList[-1]
                finalPath.append(currentNode.pos)
                while currentNode.parent is not None:
                    finalPath.append(currentNode.parent.pos)
                    currentNode = currentNode.parent
                finalPath.reverse()

                # find initial path
                if len(self.finalPath) is 0:
                    self.n = iteration
                # path optimization
                optimized_path, cost = self.path_optimization(finalPath)
                # update beacons
                if cost < self.cost:
                    print("better")
                    self.cost = cost
                    self.finalPath = optimized_path
                    self.beacons = self.finalPath
                # start next path planning
                self.nodeList = [Node(start)]
        print('final')


    def rewire(self, newNode, radius):
        # find near nodes
        nearNodes = [nearNode for nearNode in self.nodeList if newNode.dist(nearNode) < radius]
        # rewire
        for nearNode in nearNodes:
            new_cost = newNode.cost + newNode.dist(nearNode)
            if new_cost < nearNode.cost:
                nearNode.cost = new_cost
                nearNode.parent = newNode

    def chooseBestParent(self, newNode, radius):
        # find near nodes
        nearNodes = [nearNode for nearNode in self.nodeList if newNode.dist(nearNode) < radius]
        # choose best parent
        for nearNode in nearNodes:
            new_cost = nearNode.cost + newNode.dist(nearNode)
            if self.check_line_collision(newNode.pos, nearNode.pos):
                continue
            if new_cost < newNode.cost:
                newNode.cost = new_cost
                newNode.parent = nearNode

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
            return Point(self.map.left + self.map.length * random.random(),
                         self.map.down + self.map.width * random.random())
        else:
            return target

    def intelligent_sample(self):
        samples = random.sample(self.beacons, 1)
        beacon = samples[0]
        return beacon + Polar2Vector(self.biasing_radius * random.random(), random.uniform(0, 2 * math.pi))

    def inNodeList(self, node):
        for candidate in self.nodeList:
            if candidate.pos == node.pos:
                return True
        return False

    def check_obstacle(self, pos):
        for obs in self.map.obstacles:
            if obs.check_collision(pos, 5):
                return True
        return False

    def check_line_collision(self, pos1, pos2):
        testNum = pos1.dist(pos2) / 10
        for i in range(int(testNum) + 1):
            testPos = pos1 + Polar2Vector(i * 10, pos1.dir(pos2))
            if self.check_obstacle(testPos):
                return True
        return False

    def path_optimization(self, finalPath):
        cost = 0
        optimized_path = [finalPath[-1]]
        parent_index = (len(finalPath) - 1) - 1
        while parent_index >= 0:
            if parent_index is 0 or self.check_line_collision(optimized_path[-1], finalPath[parent_index-1]):
                cost = cost + optimized_path[-1].dist(finalPath[parent_index])
                optimized_path.append(finalPath[parent_index])
            parent_index = parent_index - 1
        optimized_path.reverse()
        return optimized_path, cost