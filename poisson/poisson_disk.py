from math import pi
from math import sqrt
from math import cos
from math import sin

from World.world import World
from World.world import WORLD_SIZE
from poisson.queue import PoissonQueue
from poisson.point import PoissonPoint

from  hashlib import sha256

INNER_RANGE = 50
OUTER_RANGE = INNER_RANGE * 2


def poisson_disc_sampling(seed):
    #http://extremelearning.com.au/an-improved-version-of-bridsons-algorithm-n-for-poisson-disc-sampling/
    #https://bl.ocks.org/mbostock/dbb02448b0f93e4c82c3
    #https://observablehq.com/@mbostock/poisson-disc-distribution
    #https://observablehq.com/@techsparx/an-improvement-on-bridsons-algorithm-for-poisson-disc-samp/2
    epsilon = 0.0000001
    seed = int(seed)
    new_seed = seed / 1000000
    k = 50

    parent_y = int((seed % 1000) / 2)
    parent_x = int(((seed - parent_y) / 1000) / 2)
    #print(parent_x)
    #print(parent_y)

    world = World()
    queue = PoissonQueue()

    #world.set_point(250, 250)
    tmp_x = int(sha256(str(seed).encode('utf-8')).hexdigest(), base=16) % 500
    tmp_y = int(sha256(str(tmp_x).encode('utf-8')).hexdigest(), base=16) % 500
    world.set_point(tmp_x, tmp_y)
    queue.add_coord_to_queue(tmp_x, tmp_y)

    nbr_of_points = 1
    u = parent_x / 1000
    v = parent_y / 1000

    #print(queue.is_empty())
    while(not queue.is_empty()):
        #print('ici')
        parent = queue.get_next()
        j = 0

        while j < k:

            x = WORLD_SIZE
            y = WORLD_SIZE

            while not (0 <= x < WORLD_SIZE and 0 <= y < WORLD_SIZE):
                u = (int(sha256(str(u).encode('utf-8')).hexdigest(), base=16) % 10000) / 1000
                v = (int(sha256(str(v).encode('utf-8')).hexdigest(), base=16) % 10000) / 1000
                theta = 2 * pi * u

                r = sqrt(INNER_RANGE**2 + v*(OUTER_RANGE**2 - INNER_RANGE**2))

                dist = poisson_distance_square(x, y)

                x = int(parent.x + r * cos(theta))
                y = int(parent.y + r * sin(theta))

            if 0 <= x < WORLD_SIZE and 0 <= y < WORLD_SIZE:
                point = PoissonPoint(int(x), int(y))

                j += 1
                if poisson_check_if_not_in_range(world, point):
                    queue.add_to_queue(point)
                    world.set_point(point.x, point.y)
                    j = 0
                    nbr_of_points += 1

        queue.pop_first()

    print (nbr_of_points)
    return world


def poisson_check_if_not_in_range(world, point):
    for j in range(-INNER_RANGE, INNER_RANGE):
        for i in range(int(-sqrt(INNER_RANGE*INNER_RANGE - j*j)),
                       int(sqrt(INNER_RANGE*INNER_RANGE - j*j))):
            try:
                if world.is_point(point.x + i, point.y + j):
                    return False
            except Exception:
                pass
    return True


def poisson_distance_square(x, y):
    return sqrt((x*x)+(y*y))


def poisson_to_str(world):
    s = ""

    for x in range(WORLD_SIZE):
        for y in range(WORLD_SIZE):
            if world.is_point(x, y):
                s += "▲"
            else:
                s += "˵"
        s += "\n"

    return s