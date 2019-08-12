from PathPlanning.PotentialField import PotentialFieldPlanner
from PathPlanning.utils import *

def main():
    map = Map(left=0, right=640, top=480, down=0)
    map.add_obstacle(CircleObstacle(pos=Point(200, 200), radius=50))
    map.add_obstacle(CircleObstacle(pos=Point(350, 250), radius=30))
    map.add_obstacle(CircleObstacle(pos=Point(450, 400), radius=80))
    potentialFieldPlanner = PotentialFieldPlanner(map=map, iterations=1e4, step_size=2, ka=1, kr=1e4, da=10, dr=100)
    start = Point(0, 0)
    end = Point(640, 480)
    while map.is_open:
        potentialFieldPlanner.plan(start=start, target=end)
        map.add_geometry(type='point', pos=start.tuple(), size=30, color=(100, 0, 0))
        map.add_geometry(type='point', pos=end.tuple(), size=30, color=(0, 100, 0))
        for i in range(len(potentialFieldPlanner.finalPath)-1):
            map.add_geometry(type='line', start=potentialFieldPlanner.finalPath[i].tuple(), end=potentialFieldPlanner.finalPath[i+1].tuple(), color=(0, 100, 0))
        map.render()

if __name__ == '__main__':
    main()