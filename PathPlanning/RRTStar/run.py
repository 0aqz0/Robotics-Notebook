from PathPlanning.RRTStar import RRTStarPlanner
from PathPlanning.utils import *

def main():
    map = Map(480, 0, 0, 640)
    map.add_obstacle(CircleObstacle(pos=Point(400, 300), radius=50))
    map.add_obstacle(RectangleObstacle(top=200, down=100, left=100, right=300))
    rrtPlanner = RRTStarPlanner(map, epsilon=0.2, stepSize=10)
    start = Point(0, 0)
    end = Point(640, 480)
    while map.is_open:
        rrtPlanner.plan(start=start, target=end)
        map.add_geometry(type='point', pos=start.tuple(), size=30, color=(100, 0, 0))
        map.add_geometry(type='point', pos=end.tuple(), size=30, color=(0, 100, 0))
        for node in rrtPlanner.nodeList:
            map.add_geometry(type='point', pos=node.pos.tuple())
            if node.parent is not None:
                map.add_geometry(type='line', start=node.parent.pos.tuple(), end=node.pos.tuple())
        for i in range(len(rrtPlanner.finalPath)-1):
            map.add_geometry(type='line', start=rrtPlanner.finalPath[i].tuple(), end=rrtPlanner.finalPath[i+1].tuple(), color=(0, 100, 0))
        map.render()


if __name__ == '__main__':
    main()