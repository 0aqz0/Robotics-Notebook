from PathPlanning.RRTStarSmart import RRTStarSmartPlanner
from PathPlanning.utils import *

def main():
    map = Map(left=0, right=640, top=480, down=0)
    map.add_obstacle(RectangleObstacle(left=450, right=550, top=220, down=200))
    map.add_obstacle(RectangleObstacle(left=100, right=400, top=300, down=250))
    map.add_obstacle(RectangleObstacle(left=400, right=450, top=400, down=50))
    rrtStarSmartPlanner = RRTStarSmartPlanner(map=map, iterations=1e3, epsilon=0.3, step_size=10)
    start = Point(550, 350)
    end = Point(200, 150)
    while map.is_open:
        rrtStarSmartPlanner.plan(start=start, target=end)
        map.add_geometry(type='point', pos=start.tuple(), size=20, color=(100, 0, 0))
        map.add_geometry(type='point', pos=end.tuple(), size=20, color=(0, 100, 0))
        for i in range(len(rrtStarSmartPlanner.finalPath)-1):
            map.add_geometry(type='line', start=rrtStarSmartPlanner.finalPath[i].tuple(), end=rrtStarSmartPlanner.finalPath[i+1].tuple(), color=(0, 100, 0))
        map.render()

if __name__ == '__main__':
    main()