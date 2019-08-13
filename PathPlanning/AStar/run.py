from PathPlanning.AStar import AStarPlanner
from PathPlanning.utils import *

def main():
    map = Map(top=480, down=0, left=0, right=640)
    map.add_obstacle(CircleObstacle(pos=Point(500, 300), radius=50))
    map.add_obstacle(CircleObstacle(pos=Point(100, 100), radius=45))
    map.add_obstacle(RectangleObstacle(top=480, down=200, left=300, right=350))
    astarPlanner = AStarPlanner(map=map, step_size=30, heuristic_dist='Euclidean')
    start = Point(0, 0)
    end = Point(640, 480)
    while map.is_open:
        astarPlanner.plan(start=start, target=end)
        map.add_geometry(type='point', pos=start.tuple(), size=30, color=(100, 0, 0))
        map.add_geometry(type='point', pos=end.tuple(), size = 30, color=(0, 100, 0))
        for i in range(len(astarPlanner.finalPath)-1):
            map.add_geometry(type='line', start=astarPlanner.finalPath[i].tuple(), end=astarPlanner.finalPath[i+1].tuple(), color=(0, 100, 0))
        map.render()

if __name__ == '__main__':
    main()