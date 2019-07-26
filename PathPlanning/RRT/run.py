from PathPlanning.RRT import RRTPlanner
from PathPlanning.utils import Map, Point
import matplotlib.pyplot as plt

def main():
    # create the map
    map = Map(500, 0, 0, 1000)
    # create the path planner
    rrtPlanner = RRTPlanner(map)
    # plan the path
    start = Point(5, 5)
    target = Point(100, 100)
    rrtPlanner.plan(start, target)
    plt.scatter(start.x, start.y, linewidths=16)
    plt.scatter(target.x, target.y, linewidths=16)
    for pos in rrtPlanner.finalPath:
        plt.scatter(pos.x, pos.y)
    plt.show()


if __name__ == '__main__':
    main()
