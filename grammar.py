#from Grammary.Actions import Directions
#from Grammary.Actions import direction_matrix

from enum import IntEnum

from math import sqrt

from stats import perlin_stats


class CellularAutomatonState(IntEnum):
    DEAD = 0
    HALF_RISEN = 1
    FULLY_RISEN = 2


corresp = {
    "0": "85",
    "1": "0[42]0[62]",
    "2": "2[74]",
    "3": "0[12]",
    "4": "53",
    "5": "32",
    "6": "[87][152]",
    "7": "[27][15][236]",
    "8": "81",
    "9": "17",
}

corresp_finition = {
    "1": "100",
    "2": "[0][00]2",
    "3": "[01][00][0]",
    "4": "0100",
    "5": "[00][10][01]",
    "6": "[02][0]2[010]2",
    "7": "[00][00]2",
    "8": "[010][00][00]",
    "9": "002"
}


first_process_correspondance = {
    "1": "23",
    "2": "12",
    "3": "65",
    "4": "36",
    "5": "48",
    "6": "97",
    "7": "49",
    "8": "57",
    "9": "18",
    "0": "07"
}


class Directions(IntEnum):
    LEFT_UP = 0
    UP = 1
    RIGHT_UP = 2
    RIGHT = 3
    RIGHT_DOWN = 4
    DOWN = 5
    LEFT_DOWN = 6
    LEFT = 7


direction_matrix = {
    Directions.LEFT_UP: [-1, -1],
    Directions.UP: [0, -1],
    Directions.RIGHT_UP: [1, -1],
    Directions.RIGHT: [1, 0],
    Directions.RIGHT_DOWN: [1, 1],
    Directions.DOWN: [0, 1],
    Directions.LEFT_DOWN: [-1, 1],
    Directions.LEFT: [-1, 0]
}


def process_seed(seed):

    new_seed = ""
    for letter in seed:
        new_seed += first_process_correspondance[letter]
    seed = new_seed

    for i in range(3): #range(3):#range(4):#range(5):#range(3):
        new_seed = ""
        for letter in seed:
            if letter in ["[", "]"]:
                new_seed += letter
            else:
                new_seed += corresp[letter]
        seed = new_seed

    for k in corresp_finition.keys():
        seed = seed.replace(k, corresp_finition[k])
    #for i in range(2):
    #    for k in corresp_finition.keys():
    #        seed = seed.replace(k, corresp_finition[k])

    return seed


def get_max_branch_number(seed):
    nb_max_branch = 0

    actual_number = 0

    for letter in seed:
        if letter == "[":
            actual_number += 1
            if actual_number > nb_max_branch:
                nb_max_branch = actual_number
        elif letter == "]":
            actual_number -= 1

    return nb_max_branch


def draw(seed):
    origin = 249

    world = {}
    i = 0
    j = 0

    nb_max_branches = get_max_branch_number(seed)
    print("nb max branches = " + str(get_max_branch_number(seed)))
    branch_index = 0
    direction = Directions.UP
    last_direction = direction

    world[i] = {}
    world[i][j] = 1

    print("drawing the form")
    for index in range(len(seed)):
        if seed[index] == "0":
            for v in range(2):
                i += direction_matrix[direction][1]
                j += direction_matrix[direction][0]
                if i not in world.keys():
                    world[i] = {}
                #world[i][j] = 1
                world = paint_at(world, i, j, nb_max_branches, branch_index)
        elif seed[index] == "1":
            direction = (direction + 1) % 8
            for v in range(2):
                i += direction_matrix[direction][1]
                j += direction_matrix[direction][0]
                if i not in world.keys():
                    world[i] = {}
                #world[i][j] = 1
                world = paint_at(world, i, j, nb_max_branches, branch_index)
        elif seed[index] == "2":
            direction = (direction - 1) % 8
            for v in range(2):
                i += direction_matrix[direction][1]
                j += direction_matrix[direction][0]
                if i not in world.keys():
                    world[i] = {}
                #world[i][j] = 1
                world = paint_at(world, i, j, nb_max_branches, branch_index)
        elif seed[index] == "[":
            world, index, last_direction = branche(world, i, j, last_direction, index, seed, nb_max_branches, branch_index+1)
        if index % 50 == 0:
            print(str(index) + "/" + str(len(seed)))

    print("positionning the form")
    max_x = 0
    min_x = 0
    max_y = max(world.keys())
    min_y = min(world.keys())

    print("max_x = " + str(max_x))
    print("max_y = " + str(max_y))

    for y in world.keys():
        for x in world[y].keys():
            if x > max_x:
                max_x = x
            if x < min_x:
                min_x = x

    print("max_x = " + str(max_x))
    print("max_y = " + str(max_y))

    origin_x = int((max_x + min_x) / 2)
    origin_y = int((max_y + min_y) / 2)

    final_world = []
    for i in range(500):
        final_world.append([])
        for j in range(500):
            final_world[i].append(0)

    #try :
    min_bli = 600
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if x in world[y].keys():
                bli = x + (origin - origin_x)
                if bli < min_bli: min_bli = bli
                try:
                    final_world[y + (origin - origin_y)][bli] = world[y][x]
                except Exception:
                    pass
                    #break

    #final_world = correction_cellular_automaton(final_world)
    ##final_world = circular_correction(final_world)
    #final_world = moyenne_correction(final_world)

    #for y in range(len(final_world)):
    #    for x in range(len(final_world[y])):
    #        final_world[y][x] *= 100

    return final_world


def polynomeA(x):
    return float(
        (-0.01*x*x) + 3
    )
    #return float(
    #    cos(x)
    #    - (0.15*x*x)
    #    + 8
    #    + ((1/(abs(x)+1))*2)
    #)


def polynomeB(x):
    return float(
        #(-0.0015*(x*x))+3
        (-0.0015 * (x * x)) + 2.5
    )


def polynomeC(x):
    return float(
        #(-0.0006*(x*x))+3
        (-0.0003 * (x * x)) + 2
    )


def polynomeD(x):
    return float(
        #(-0.0006*(x*x))+3
        (-0.00005 * (x * x)) + 1.5
    )


def paint_at(world, i, j, max_branch_index, branch_index):
    """
    Paints a 12x12, 40x40, 80x80 and 320x320 dots around a point at
    given coordinates
    """

    # Radius of differents dots
    #if branch_index != 0:
    #    if branch_index % 2 == 0:
    #        radiusA = int(6/int(branch_index/2))
    #        radiusB = int(20/int(branch_index/2))
    #        radiusC = int(40/int(branch_index/2))
    #        radiusD = int(160/(branch_index/2)) #80 #240
    #    else:
    #        radiusA = int(6 / (int(branch_index / 2)+1))
    #        radiusB = int(20 / (int(branch_index / 2)+1))
    #        radiusC = int(40 / (int(branch_index / 2)+1))
    #        radiusD = int(160 / (int(branch_index / 2)+1))  # 80 #240
    #else:
    radiusA = 6
    radiusB = 20
    radiusC = 40
    radiusD = 160 #80 #240

    for y in range(-radiusD, radiusD + 1):
        #for x in range(-radiusD, radiusD + 1):
        for x in range(-int(sqrt((radiusD*radiusD)-(y*y))), int(sqrt((radiusD*radiusD)-(y*y))) + 1):
            distance = sqrt((x * x) + (y * y))
            if i + y not in world.keys():
                world[i + y] = {}
            if j + x not in world[i + y].keys():
                world[i + y][j + x] = 0

            if radiusC < distance:
                try:
                    world[i + y][j + x] += (polynomeD(
                        distance)*(max_branch_index/(max_branch_index+branch_index)))
                except Exception:
                    pass
            elif radiusB < distance:
                try:
                    world[i + y][j + x] += (polynomeC(
                        distance)*(max_branch_index/(max_branch_index+(branch_index*100))))
                except Exception:
                    pass
            elif radiusA < distance:
                try:
                    world[i + y][j + x] += (polynomeB(
                        distance)*(max_branch_index/(max_branch_index+(branch_index*100))))
                except Exception:
                    pass
            else:
                try:
                    world[i + y][j + x] += (polynomeA(distance)*(max_branch_index/(max_branch_index+(branch_index*100))))
                except Exception:
                    pass

    return world


def branche(world, i, j, direction, index_seed, seed, max_branch_index, branch_index):
    direction = (direction + 1) % 8
    last_direction = direction
    index_seed += 1
    for branch_index in range(index_seed, len(seed)):
        if seed[branch_index] == "[":
            world, index_seed, last_direction = branche(world, i, j, last_direction, index_seed, seed, max_branch_index, branch_index+1)
        elif seed[branch_index] == "]":
            return world, index_seed, direction
        elif seed[branch_index] == "0":
            for v in range(int(branch_index/2) + (branch_index % 2)):#2):
                i += direction_matrix[direction][1]
                j += direction_matrix[direction][0]
                if i not in world.keys():
                    world[i] = {}
                #world[i][j] = 1
                world = paint_at(world, i, j, max_branch_index, branch_index)
        elif seed[branch_index] == "1":
            direction = (direction + 1) % 8
            for v in range(int(branch_index/2) + (branch_index % 2)):#2):
                i += direction_matrix[direction][1]
                j += direction_matrix[direction][0]
                if i not in world.keys():
                    world[i] = {}
                #world[i][j] = 1
                world = paint_at(world, i, j, max_branch_index, branch_index)
        elif seed[branch_index] == "2":
            direction = (direction - 1) % 8
            for v in range(int(branch_index/2) + (branch_index % 2)):#2):
                i += direction_matrix[direction][1]
                j += direction_matrix[direction][0]
                if i not in world.keys():
                    world[i] = {}
                #world[i][j] = 1
                world = paint_at(world, i, j, max_branch_index, branch_index)


def get_distance(x, y):
    return sqrt((x*x)+(y*y))


def lambda_plain(min, max):
    return lambda x: int(max >= x > min)

def lambda_water(max):
    return lambda x: int(max >= x)

def lambda_mountain(min):
    return lambda x: int(min < x)

def cellular_2(world, input_data):

    minimal_percentage_plains = input_data.get_water_percentage() #get_beach_percentage()  # 50
    maximal_percentage_plains = input_data.get_plain_percentage()  # 90

    corrected_world = world

    for iteration in range(1):#range(50):#range(5):
        stats = perlin_stats(world)
        value_minimal_percentage_plains = stats.get_val_at_percentage(
            minimal_percentage_plains)
        value_maximal_percentage_plains = stats.get_val_at_percentage(
            maximal_percentage_plains)

        is_plain = lambda_plain(value_minimal_percentage_plains, value_maximal_percentage_plains)
        is_water = lambda_water(value_minimal_percentage_plains)
        is_mountain = lambda_mountain(value_maximal_percentage_plains)

        #Correction des pixels vengeurs
        for y in range(1, len(world)-1):
            for x in range(1, len(world[y])-1):
                sum_plain = is_plain(world[y-1][x-1]) + \
                    is_plain(world[y-1][x]) + \
                    is_plain(world[y-1][x+1]) + \
                    is_plain(world[y][x-1]) + \
                    is_plain(world[y][x+1]) + \
                    is_plain(world[y+1][x-1]) + \
                    is_plain(world[y+1][x]) + \
                    is_plain(world[y+1][x+1])

                sum_surround = world[y-1][x-1] + \
                               world[y-1][x] + \
                               world[y-1][x+1] + \
                               world[y][x-1] + \
                               world[y][x+1] + \
                               world[y+1][x-1] + \
                               world[y+1][x-1] + \
                               world[y+1][x-1]

                sum_water = is_water(world[y - 1][x - 1]) + \
                            is_water(world[y - 1][x]) + \
                            is_water(world[y - 1][x + 1]) + \
                            is_water(world[y][x - 1]) + \
                            is_water(world[y][x + 1]) + \
                            is_water(world[y + 1][x - 1]) + \
                            is_water(world[y + 1][x]) + \
                            is_water(world[y + 1][x + 1])

                sum_mountain = is_mountain(world[y - 1][x - 1]) + \
                            is_mountain(world[y - 1][x]) + \
                            is_mountain(world[y - 1][x + 1]) + \
                            is_mountain(world[y][x - 1]) + \
                            is_mountain(world[y][x + 1]) + \
                            is_mountain(world[y + 1][x - 1]) + \
                            is_mountain(world[y + 1][x]) + \
                            is_mountain(world[y + 1][x + 1])

                if (is_plain(world[y][x]) and sum_plain < 3 ) \
                        or (is_mountain(world[y][x]) and sum_mountain < 3) :
                    world[y][x] = sum_surround / 8

    corrected_world = world
    for iteration in range(10):#range(25):

        stats = perlin_stats(world)
        value_minimal_percentage_plains = stats.get_val_at_percentage(
            minimal_percentage_plains)
        value_maximal_percentage_plains = stats.get_val_at_percentage(
            maximal_percentage_plains)

        is_plain = lambda_plain(value_minimal_percentage_plains,
                                value_maximal_percentage_plains)
        is_water = lambda_water(value_minimal_percentage_plains)
        is_mountain = lambda_mountain(value_maximal_percentage_plains)

        for y in range(1, len(world)-1):
            for x in range(1, len(world[y])-1):
                sum_plain = is_plain(world[y-1][x-1]) + \
                    is_plain(world[y-1][x]) + \
                    is_plain(world[y-1][x+1]) + \
                    is_plain(world[y][x-1]) + \
                    is_plain(world[y][x+1]) + \
                    is_plain(world[y+1][x-1]) + \
                    is_plain(world[y+1][x]) + \
                    is_plain(world[y+1][x+1])

                sum_surround = world[y-1][x-1] + \
                               world[y-1][x] + \
                               world[y-1][x+1] + \
                               world[y][x-1] + \
                               world[y][x+1] + \
                               world[y+1][x-1] + \
                               world[y+1][x-1] + \
                               world[y+1][x-1]

                sum_water = is_water(world[y - 1][x - 1]) + \
                            is_water(world[y - 1][x]) + \
                            is_water(world[y - 1][x + 1]) + \
                            is_water(world[y][x - 1]) + \
                            is_water(world[y][x + 1]) + \
                            is_water(world[y + 1][x - 1]) + \
                            is_water(world[y + 1][x]) + \
                            is_water(world[y + 1][x + 1])

                sum_mountain = is_mountain(world[y - 1][x - 1]) + \
                            is_mountain(world[y - 1][x]) + \
                            is_mountain(world[y - 1][x + 1]) + \
                            is_mountain(world[y][x - 1]) + \
                            is_mountain(world[y][x + 1]) + \
                            is_mountain(world[y + 1][x - 1]) + \
                            is_mountain(world[y + 1][x]) + \
                            is_mountain(world[y + 1][x + 1])

                if (is_water(world[y][x]) and 0 < sum_plain <= 3):
                    corrected_world[y][x] += (abs(world[y][x] - (sum_surround/8)))/2

                else:
                    corrected_world[y][x] += (abs(
                        world[y][x] - (sum_surround / 8))) / 4

        world = corrected_world

    return world


def correction_cellular_automaton(world, input_data):

    stats = perlin_stats(world)
    minimal_percentage_plains = input_data.get_beach_percentage()#50
    maximal_percentage_plains = input_data.get_plain_percentage()#90
    value_minimal_percentage_plains = stats.get_val_at_percentage(
        minimal_percentage_plains)
    value_maximal_percentage_plains = stats.get_val_at_percentage(
        maximal_percentage_plains)
    corrected_world = world

    for nb_of_iteration_for_correction in range(5): #range(10):#range(50):#range(25):

        value_minimal_percentage_plains = stats.get_val_at_percentage(
            minimal_percentage_plains)
        value_maximal_percentage_plains = stats.get_val_at_percentage(
            maximal_percentage_plains)

        world_state = {}
        for y in range(1, len(world)-1):
            if y not in world_state.keys():
                world_state[y] = {}
            for x in range(1, len(world[y])-1):
                if x not in world_state[y].keys():
                    world_state[y][x] = CellularAutomatonState.DEAD
                sum_plain = 0
                sum_plain_value = 0
                sum_water = 0
                sum_mountain = 0
                tmp_list = [world[y+1][x-1],
                    world[y+1][x],
                    world[y+1][x+1],
                    world[y-1][x-1],
                    world[y-1][x],
                    world[y-1][x+1],
                    world[y][x-1],
                    world[y][x+1],
                ]
                sum_water = sum(1 for n in tmp_list if n <= value_minimal_percentage_plains)
                sum_plain = sum(1 for n in tmp_list if value_minimal_percentage_plains < n <= value_maximal_percentage_plains)
                sum_plain_value = sum(n for n in tmp_list if value_minimal_percentage_plains < n <= value_maximal_percentage_plains)
                sum_mountain = 8 - (sum_water + sum_plain)
                sum_total = sum(tmp_list)

                #  NORMAL

                #if sum_plain in [3, 4, 5] and world[y][x] < value_minimal_percentage_plains:
                #    corrected_world[y][x] = (sum_plain_value / sum_plain)
                #    #for j in range(-1, 2):
                #    #    for i in range(-1, 2):
                #    #        corrected_world[y + j][x + i] = (sum_plain_value / sum_plain)/(get_distance(i, j)+1) #world[y+j][x+i] + (sum_plain_value / sum_plain)/(get_distance(i, j)+1)
                #elif sum_water == 8 and world[y][x] >= value_minimal_percentage_plains:
                #    corrected_world[y][x] = sum_total/8
                #elif sum_plain <= 2 and sum_mountain == 0:
                #    corrected_world[y][x] = world[y][x] - (world[y][x]/10)

                #  AVEC ETATS

                if sum_plain in [3, 4, 5] and world[y][x] < value_minimal_percentage_plains:
                    #corrected_world[y][x] = (sum_plain_value / sum_plain)
                    for j in range(-1, 2):
                        if y+j not in world_state.keys():
                            world_state[y+j] = {}
                        for i in range(-1, 2):
                            if get_distance(i, j) <= 1:
                                if x+i not in world_state[y+j].keys():
                                    world_state[y+j][x+i] = CellularAutomatonState.DEAD
                                if world_state[y+j][x+i] == CellularAutomatonState.DEAD:  # < CellularAutomatonState.FULLY_RISEN:
                                    corrected_world[y + j][x + i] = (sum_plain_value / sum_plain)/(get_distance(i, j)+1) #world[y+j][x+i] + (sum_plain_value / sum_plain)/(get_distance(i, j)+1)
                                    world_state[y + j][x + i] += 1
                                if [i, j] == [0, 0]:
                                    world_state[y+j][x+i] = CellularAutomatonState.FULLY_RISEN


                #elif sum_water == 8 and world[y][x] >= value_minimal_percentage_plains:
                #    corrected_world[y][x] = sum_total/8
                #    world_state[y][x] = CellularAutomatonState.FULLY_RISEN
                #elif sum_plain <= 2 and sum_mountain == 0:
                #    corrected_world[y][x] = world[y][x] - (world[y][x]/10)
                #    world_state[y][x] = CellularAutomatonState.HALF_RISEN

                #  ALTERNATIF

                #if (sum_plain == 3 and world[y][x] <= value_minimal_percentage_plains) \
                #    or (sum_plain in [5, 8] and sum_mountain == 0 and world[y][x] <= value_minimal_percentage_plains) :
                #    #print("LA")
                #    moy_plain_value = sum_plain_value/sum_plain
                #    corrected_world[y][x] = moy_plain_value
                #    #corrected_world = correction_cell_autom_at(corrected_world, x, y, moy_plain_value)
                #    #corrected_world[y][x] +=
                #elif (sum_plain == 4 and sum_mountain == 0) :#or sum_water == 1:
                #    #print("PTET")
                #    corrected_world[y][x] = world[y][x]/2
                #elif sum_plain == 5 and world[y][x] <= value_maximal_percentage_plains and sum_mountain == 0:
                #    corrected_world[y][x] = world[y][x] / 2
                #elif sum_water == 2 :
                #    if corrected_world[y][x] != 0:
                #        corrected_world[y][x] = corrected_world[y][x] / 2
                #    else :
                #        corrected_world[y][x] = world[y][x] / 2

        world = corrected_world
    return corrected_world


def correction_cell_autom_at(world, x, y, val_max):
    radius = 5
    poly = polynome_lambda(((val_max * 1 / 4) - val_max) / (radius * radius), 0,
                           val_max)
    for j in range(-radius, radius+1):
        for i in range(-radius, radius+1):
            if 0 <= j+y <= 499 and 0 <= i+x <= 499:
                distance = sqrt(
                    ((i)*(i))
                    +((j)*(j))
                )
                if distance <= radius:
                    if world[y+j][x+i] < poly(distance):
                        print("ICI")
                        world[y+j][x+i] += poly(distance)
    return world


def moyenne_correction(world):
    corrected_world = world
    print("moyenne correction")
    for nbr_iteration in range(1):
        for y in range(len(world)):
            for x in range(len(world[y])):
                sum_value = 0
                nbr_value = 0
                for j in range(-1, 2):
                    for i in range(-1, 2):
                        if [i, j] != [0, 0]:
                            try:
                                sum_value += world[y+j][x+i]
                                nbr_value += 1
                            except Exception:
                                pass

                corrected_world[y][x] += sum_value/nbr_value
        world = corrected_world

    return world
            #sum += world[y-1][x-1]
            #sum += world[y-1][x]
            #sum += world[y-1][x+1]
            #sum += world[y][x-1]
            #sum += world[y][x+1]
            #sum += world[y+1][x-1]
            #sum += world[y+1][x]
            #sum += world[y+1][x+1]


def polynome_lambda(a, b, c):
    return lambda x: (a*x*x)+(b*x*x)+c


def circular_correction(world, input_data):

    stats = perlin_stats(world)
    perc_min = input_data.get_water_percentage()  # 40 par defaut
    perc_max = input_data.get_plain_percentage()  # 90 par defaut
    origin = int(len(world)/2)
    val_min = stats.get_val_at_percentage(perc_min)
    val_max = stats.get_val_at_percentage(perc_max)

    #print("val_min = " + str(val_min))
    #print("val_max = " + str(val_max))

    #print("a = " + str((val_min-val_max)/(origin*origin)))
    #print("b = " + str(0))
    #print("c = " + str(val_min))

    poly = polynome_lambda((val_min-val_max)/(origin*origin), 0, val_min)
    for y in range(len(world)):
        for x in range(len(world[y])):
            distance = sqrt(
                ((x-origin)*(x-origin))
                + ((y-origin)*(y-origin))
            )
            world[y][x] += (poly(distance)/4)
            #world[y][x] += (world[y][x]/10)

    return world


def to_str(G, data):
    grammary_lettres = [
        "˵",
        "ᴖ",
        "∩",
        "▲",
    ]

    grammary_correspondance = {
        "˵": data["water"],
        "ᴖ": data['beach'],
        "∩": data["plains"],
        "▲": data["mountain"] + 1
    }

    s = ""
    for G_row in G:
        for G_data in G_row:
            tmp = "-"
            for lettre in grammary_lettres:
                try:
                    if G_data <= grammary_correspondance[lettre]:
                        tmp = lettre
                        break
                except Exception:
                    pass
            if tmp == "-":
                #print("P_data = {0}  corresp = {1}".format(str(G_data), str(grammary_correspondance["▲"])))
                tmp = "▲"
            s += tmp
        s += "\n"

    return s