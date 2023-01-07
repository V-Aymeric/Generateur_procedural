import noise
import stats
from Statistics.maths_functions import lambda_polynome


def calculate_perlin_values(coord_x=0, coord_y=0):

    print("coord X : " + str(coord_x))
    print("coord Y : " + str(coord_y))
    coord_x = int(coord_x * 1000)
    coord_y = int(coord_y * 1000)
    shape = (500+coord_x, 500+coord_y)
    scale = 100.0
    octaves = 100
    persistence = 0.5
    lacunarity = 2.0

    # world = [[0] * shape[0]] * shape[1]
    world = []
    # print(len(world))
    # print(len(world[0]))

    for i in range(int(coord_x), int(shape[0])):
        world.append([])
        for j in range(int(coord_y), int(shape[1])):
            world[-1].append(noise.pnoise2(
                (i+coord_x)/scale,
                (j+coord_y)/scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=shape[0],
                repeaty=shape[1],
                base=0
            ))

    return world


def apply_circle_correction(perlin, percentage_ext=10, percentage_sommet=70):
    #https://www.mathwarehouse.com/geometry/circle/images/equation-of-circle/example-2-equation-of-circle.webp
    statistiques = stats.perlin_stats(perlin)
    radius = 240
    radius_carre = radius*radius
    O = [250, 250]

    # Determination facteurs polynome
    val_ext = statistiques.get_val_at_percentage(percentage_ext)
    val_sommet = statistiques.get_val_at_percentage(percentage_sommet)
    sommet = int(len(perlin)/2)

    a = None
    b = None
    c = None

    c = val_sommet
    b = 0
    a = (val_ext-val_sommet)/(O[0]*O[0])

    polynome = lambda_polynome(a, b, c)

    # Application correction
    for i in range(len(perlin)):
        for j in range(len(perlin[i])):
            distance_2_O = int(sqrt(((i-O[0])*(i-O[0])) + ((j-O[1])*(j-O[1]))))
            if perlin[i][j] + polynome(distance_2_O)*2 >= statistiques.valeur_min:
                perlin[i][j] += (polynome(distance_2_O)*2)
            else:
                perlin[i][j] = statistiques.valeur_min
    return perlin