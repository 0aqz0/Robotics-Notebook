from PathPlanning.PotentialField import PotentialFieldPlanner
from PathPlanning.utils import *

def main():
    map = Map(left=0, right=640, top=480, down=0, refresh=False)
    map.add_obstacle(CircleObstacle(pos=Point(200, 200), radius=50))
    map.add_obstacle(CircleObstacle(pos=Point(400, 300), radius=40))
    # map.add_obstacle(CircleObstacle(pos=Point(450, 400), radius=80))
    potentialFieldPlanner = PotentialFieldPlanner(map=map, iterations=1e4, step_size=2, ka=1, kr=1e7, da=10, dr=50)
    start = Point(100, 100)
    end = Point(500, 250)
    potentialFieldPlanner.plan(start=start, target=end)
    map.add_geometry(type='point', pos=start.tuple(), size=10, color=(100, 0, 0))
    map.add_geometry(type='point', pos=end.tuple(), size=10, color=(0, 100, 0))
    for i in range(len(potentialFieldPlanner.finalPath)-1):
        map.add_geometry(type='line', start=potentialFieldPlanner.finalPath[i].tuple(), end=potentialFieldPlanner.finalPath[i+1].tuple(), color=(0, 100, 0))
    # draw potential force
    for x in range(0, map.right+1, 10):
        for y in range(0, map.top+1, 10):
            force = potentialFieldPlanner.calculate_potential_force(Point(x, y), end)
            force_start = Point(x, y)
            force_end = force_start + Polar2Vector(5, force.dir())
            # map.add_geometry(type='point', pos=(x,y), size=3, color=(0, 0, 100))
            map.add_geometry(type='line', start=force_start.tuple(), end=force_end.tuple(), width=2, color=(120,50,80))
    # draw potential line
    potential_lines = [i for i in range(0, 20000, 1000)]
    for x in range(0, map.right+1, 1):
        for y in range(0, map.top+1, 1):
            valid = True
            for obs in map.obstacles:
                if obs.dist(Point(x, y)) <= 32:
                    valid = False

            if valid:
                offset = 20
            else:
                offset = 100
            potential = potentialFieldPlanner.calculate_attractive_potential(Point(x, y), end) + potentialFieldPlanner.calculate_repulsive_potential(Point(x, y))
            # print(potential, potentialFieldPlanner.calculate_attractive_potential(Point(x, y), end))
            for p in potential_lines:
                if math.fabs(potential-p) < offset:
                    map.add_geometry(type='point', pos=(x,y), size=1, color=(0, 0, 100))

    while map.is_open:
        map.render()

if __name__ == '__main__':
    main()