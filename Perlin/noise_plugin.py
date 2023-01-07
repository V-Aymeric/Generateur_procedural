import noise
import stats
from Statistics.maths_functions import lambda_polynome

from math import sqrt
#from main import taille_tableau

taille_tableau = 500


def process_seed(seed):

    # XXXYYYZZZ
    # => XXX = Scale
    # => YYY = coord X
    # => ZZZ = coord y

    coord_x = None
    coord_y = None

    coord_y = ((seed % 1000000) - (seed % 1000))/1000
    coord_x = seed % 1000

    return int(coord_x), int(coord_y)


def convert_values_to_string(P, data):
    perlin_lettres = [
        "˵",
        "ᴖ",
        "∩",
        "▲",
    ]

    perlin_correspondance = {
        "˵": data["water"],
        "ᴖ": data['beach'],
        "∩": data["plains"],
        "▲": data["mountain"] + 1
    }

    s = ""
    for P_row in P:
        for P_data in P_row:
            # P_data = (P_data + 1) * 0.5 * 255
            P_data = (P_data) * 100
            tmp = "-"
            for lettre in perlin_lettres:
                try:
                    if P_data <= perlin_correspondance[lettre]:
                        tmp = lettre
                        break
                except Exception:
                    pass
            if tmp == "-":
                print("P_data = {0}  corresp = {1}".format(str(P_data), str(perlin_correspondance["▲"])))
            s += tmp
        s += "\n"

    return s


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


def apply_factor_correction(perlin):
    facteur = 2
    perlin=[[y*facteur for y in x] for x in perlin]
    return perlin


def apply_circle_correction(perlin, percentage_ext=10, percentage_sommet=70):
    #https://www.mathwarehouse.com/geometry/circle/images/equation-of-circle/example-2-equation-of-circle.webp
    statistiques = stats.perlin_stats(perlin)
    radius = 240
    radius_carre = radius*radius
    O = [250, 250]

    # Determination facteurs polynome
    val_ext = statistiques.get_val_at_percentage(percentage_ext) #statistiques.get_val_at_percentage(50)
    val_sommet = statistiques.get_val_at_percentage(percentage_sommet)#statistiques.get_val_at_percentage(70)
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