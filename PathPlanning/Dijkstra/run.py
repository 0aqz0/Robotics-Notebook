from PathPlanning.Dijkstra import DijkstraPlanner
from PathPlanning.utils import *

def main():
    map = Map(top=480, down=0, left=0, right=640)
    map.add_obstacle(CircleObstacle(pos=Point(400, 300), radius=80))
    map.add_obstacle(CircleObstacle(pos=Point(300, 100), radius=30))
    map.add_obstacle(RectangleObstacle(top=150, down=100, left=0, right=200))
    dijkstraPlanner = DijkstraPlanner(map=map, step_size=30)
    start = Point(0, 0)
    end = Point(640, 480)
    while map.is_open:
        dijkstraPlanner.plan(start=start, target=end)
        map.add_geometry(type='point', pos=start.tuple(), size=30, color=(100, 0, 0))
        map.add_geometry(type='point', pos=end.tuple(), size = 30, color=(0, 100, 0))
        for i in range(len(dijkstraPlanner.finalPath)-1):
            map.add_geometry(type='line', start=dijkstraPlanner.finalPath[i].tuple(), end=dijkstraPlanner.finalPath[i+1].tuple(), color=(0, 100, 0))
        map.render()

if __name__ == '__main__':
    main()