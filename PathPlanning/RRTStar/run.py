from PathPlanning.RRTStar import RRTStarPlanner
from PathPlanning.utils import Map, Point, RectangleObstacle
import matplotlib.pyplot as plt

def main():
    # create the map
    map = Map(500, 0, 0, 500)
    map.obstacles.append(RectangleObstacle(300, 0, 100, 150))
    map.obstacles.append(RectangleObstacle(500, 200, 300, 350))
    plt.plot([100, 100, 150, 150, 100], [0, 300, 300, 0, 0])
    plt.plot([300, 300, 350, 350, 300], [200, 500, 500, 200, 200])
    plt.plot([0, 0, 500, 500, 0], [0, 500, 500, 0, 0])
    # create the path planner
    rrtPlanner = RRTStarPlanner(map, epsilon=0.01, stepSize=20)
    # plan the pat0
    start = Point(5, 5)
    target = Point(490, 500)
    rrtPlanner.plan(start, target)
    plt.scatter(start.x, start.y, linewidths=16)
    plt.scatter(target.x, target.y, linewidths=16)
    for pos in rrtPlanner.finalPath:
        plt.scatter(pos.x, pos.y)
    plt.show()


if __name__ == '__main__':
    main()
