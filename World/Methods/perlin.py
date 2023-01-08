import noise

from math import sqrt

from Statistics import stats
from World.world import World

from Statistics.maths_functions import lambda_polynome

from Utils.constansts import WORLD_SIZE
from Utils.constansts import WORLD_SIZE_RANGE


def calculate_perlin_values(coord_x=0, coord_y=0):

    print("coord X : " + str(coord_x))
    print("coord Y : " + str(coord_y))
    coord_x = int(coord_x * 1000)
    coord_y = int(coord_y * 1000)
    shape = (WORLD_SIZE + coord_x, WORLD_SIZE + coord_y)
    scale = 100.0
    octaves = 100
    persistence = 0.5
    lacunarity = 2.0

    # world = [[0] * shape[0]] * shape[1]
    # world = []
    world_data = World()

    # print(len(world))
    # print(len(world[0]))

    print('coord_x=' + str(coord_x))
    print('shape[0]=' + str(shape[0]))
    for i in range(int(coord_x), int(shape[0])):

        #world.append([])
        for j in range(int(coord_y), int(shape[1])):
            # print("x = ", i-coord_x, "y = ", j-coord_y)
            world_data.set(i-coord_x, j-coord_y, noise.pnoise2(
                (i+coord_x)/scale,
                (j+coord_y)/scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=shape[0],
                repeaty=shape[1],
                base=0
            ))
            #world[-1].append(noise.pnoise2(
            #    (i+coord_x)/scale,
            #    (j+coord_y)/scale,
            #    octaves=octaves,
            #    persistence=persistence,
            #    lacunarity=lacunarity,
            #    repeatx=shape[0],
            #    repeaty=shape[1],
            #    base=0
            #))

    return world_data


def apply_circle_correction(perlin, percentage_ext=10, percentage_sommet=70):
    # https://www.mathwarehouse.com/geometry/circle/images/equation-of-circle/example-2-equation-of-circle.webp
    statistiques = stats.perlin_stats(perlin)
    radius = 240
    radius_carre = radius*radius
    O = [250, 250]

    # Determination facteurs polynome
    val_ext = statistiques.get_val_at_percentage(percentage_ext)
    val_sommet = statistiques.get_val_at_percentage(percentage_sommet)
    # sommet = int(WORLD_SIZE/2)

    c = val_sommet
    b = 0
    a = (val_ext-val_sommet)/(O[0]*O[0])

    polynome = lambda_polynome(a, b, c)

    # Application correction
    for i in WORLD_SIZE_RANGE:
        for j in WORLD_SIZE_RANGE:
            distance_2_O = int(sqrt(((i-O[0])*(i-O[0])) + ((j-O[1])*(j-O[1]))))
            poly_dist = polynome(distance_2_O)*2
            if perlin.get(i, j).value + poly_dist >= statistiques.valeur_min:
                perlin.set(i, j,
                           perlin.get(i, j).value + poly_dist)
            else:
                perlin.set(i, j,
                           perlin.get(i, j).value + statistiques.valeur_min)
    return perlin
