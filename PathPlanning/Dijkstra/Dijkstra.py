"""
Dijkstra path planning implementation with python
"""
from PathPlanning.utils import *

class DijkstraPlanner(PathPlanner):
    def __init__(self, map, iterations=1e4, step_size=10):
        PathPlanner.__init__(self)
        self.map = map
        self.iterations = iterations
        self.step_size = step_size
        self.motions = [
            Vector(1, 0),  # right          cost: 1
            Vector(0, 1),  # up             cost: 1
            Vector(-1, 0),  # left           cost: 1
            Vector(0, -1),  # down           cost: 1
            Vector(-1, -1),  # left and down  cost: 2^0.5
            Vector(-1, 1),  # left and up    cost: 2^0.5
            Vector(1, -1),  # right and down cost: 2^0.5
            Vector(1, 1),  # right and up   cost: 2^0.5
        ]
        self.open_list = []
        self.close_list = []

    def plan(self, start, target):
        self.open_list = []
        self.close_list = []
        self.open_list.append(Node(start))

        for iteration in range(int(self.iterations)):
            current_node = min(self.open_list,
                               key=lambda node: node.cost)

            if current_node.pos.dist(target) < self.step_size:
                print("final")
                finalNode = Node(pos=target, parent=current_node,
                                 cost=current_node.cost + current_node.pos.dist(target))
                self.close_list.append(finalNode)
                self.generate_final_path()
                break

            # remove from open list
            self.open_list.remove(current_node)
            # add to close list
            self.close_list.append(current_node)
            # explore
            for motion in self.motions:
                newNode = Node(pos=current_node.pos + motion * self.step_size, parent=current_node,
                               cost=current_node.cost + motion.mod() * self.step_size)

                # in close list
                if self.find_in_close_list(newNode):
                    continue
                # outside the map
                if self.map.out_of_map(newNode.pos):
                    continue
                # meet obstacle
                if self.check_obstacle(newNode.pos):
                    continue

                # add to open list
                if self.find_in_open_list(newNode):
                    sameNode = self.find_in_open_list(newNode)
                    if sameNode.cost > newNode.cost:
                        sameNode = newNode
                else:
                    self.open_list.append(newNode)

    def find_in_close_list(self, node):
        for candidate in self.close_list:
            if candidate.pos == node.pos:
                return candidate
        return None

    def find_in_open_list(self, node):
        for candidate in self.open_list:
            if candidate.pos == node.pos:
                return candidate
        return None

    def check_obstacle(self, pos):
        for obs in self.map.obstacles:
            if obs.check_collision(pos, 10):
                return True
        return False

    def generate_final_path(self):
        self.finalPath = []
        self.finalPath.append(self.close_list[-1].pos)
        currentNode = self.close_list[-1]
        while currentNode.parent is not None:
            currentNode = currentNode.parent
            self.finalPath.append(currentNode.pos)
        self.finalPath.reverse()