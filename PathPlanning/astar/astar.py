# author: 0aqz0
# date: 2018/11/20
"""
A* path planning implementation with python
"""
import math
from collections import deque
import matplotlib.pyplot as plt

grid_size = 1.0      # grid resolution
robot_size = 1.0     # robot size
obstacle_x = []      # coordinate x of obstacles
obstacle_y = []      # coordinate y of obstacles
motions = [
    [1,0,1],                # right          cost: 1
    [0,1,1],                # up             cost: 1
    [-1,0,1],               # left           cost: 1
    [0,-1,1],               # down           cost: 1
    [-1,-1,math.sqrt(2)],   # left and down  cost: 2^0.5
    [-1,1,math.sqrt(2)],    # left and up    cost: 2^0.5
    [1,-1,math.sqrt(2)],    # right and down cost: 2^0.5
    [1,1,math.sqrt(2)],     # right and up   cost: 2^0.5
]

class Node:
    """
    smallest unit of the grid map
    """
    def __init__(self, x, y, cost, parent):
        self.x = x
        self.y = y
        self.cost = cost
        self.parent = parent

def generate_final_path():
    """
    generate the final path from the goal
    """
    pass

def calculate_heuristic(node1, node2):
    """
    calculate the heuristic evaluation from node1 to node2
    :param node1: start node
    :param node2: goal node
    :return: the heuristic evaluation
    """
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)

def a_star_planning(start_x, start_y, goal_x, goal_y, obstacle_x, obstacle_y):
    """

    :param start_x:
    :param start_y:
    :param goal_x:
    :param goal_y:
    :param obstacle_x:
    :param obstacle_y:
    :return:
    """
    # extract the index of start node, goal node and obstacles
    start = Node(round(start_x/grid_size), round(start_y/grid_size), 0.0, -1)
    goal = Node(round(goal_x/grid_size), round(goal_y/grid_size), 0.0, -1)
    obstacle_x = [round(obs_x/grid_size) for obs_x in obstacle_x]
    obstacle_y = [round(obs_y/grid_size) for obs_y in obstacle_y]

    obstacles = [[obstacle_x[i],obstacle_y[i]] for i in range(len(obstacle_x))]

    # plot the obstacles
    for obs in obstacles:
        plt.plot(obs[0],obs[1],"b")

    # create the open list and close list to store nodes
    openset, closeset = deque(), deque()
    openset.append(start)

    # while True:
    #     # find out the min f node to explore
    #     current_id = min(openset,
    #                      key=lambda i: openset[i].cost + calculate_heuristic(openset[i],goal))
    #     current_node = openset[current_id]

if __name__ == '__main__':
    start_x = 10.0
    start_y = 10.0
    goal_x = 50.0
    goal_y = 50.0

    for i in range(60):
        obstacle_x.append(i)
        obstacle_y.append(0.0)
    for i in range(60):
        obstacle_x.append(60.0)
        obstacle_y.append(i)
    for i in range(61):
        obstacle_x.append(i)
        obstacle_y.append(60.0)
    for i in range(61):
        obstacle_x.append(0.0)
        obstacle_y.append(i)
    for i in range(40):
        obstacle_x.append(20.0)
        obstacle_y.append(i)
    for i in range(40):
        obstacle_x.append(40.0)
        obstacle_y.append(60.0-i)

    obstacle_x = [round(obs_x / grid_size) for obs_x in obstacle_x]
    obstacle_y = [round(obs_y / grid_size) for obs_y in obstacle_y]

    obstacles = [[obstacle_x[i], obstacle_y[i]] for i in range(len(obstacle_x))]

    # plot the obstacles
    for obs in obstacles:
        plt.plot(obs[0], obs[1], "b")