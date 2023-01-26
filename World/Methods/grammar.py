from enum import IntEnum

from math import sqrt

#from stats import perlin_stats
from World.world import World

from Utils.constansts import WORLD_SIZE_RANGE
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
    print("seed length = ", len(seed))
    print("seed  = ", seed)
    for index in range(len(seed)):
        print("seed[", index, "] = ", seed[index])
        if seed[index] == "0":
            for v in range(2):
                i += direction_matrix[direction][1]
                j += direction_matrix[direction][0]
                if i not in world.keys():
                    world[i] = {}
                world = paint_at(world, i, j, nb_max_branches, branch_index)
        elif seed[index] == "1":
            direction = (direction + 1) % 8
            for v in range(2):
                i += direction_matrix[direction][1]
                j += direction_matrix[direction][0]
                if i not in world.keys():
                    world[i] = {}
                world = paint_at(world, i, j, nb_max_branches, branch_index)
        elif seed[index] == "2":
            direction = (direction - 1) % 8
            for v in range(2):
                i += direction_matrix[direction][1]
                j += direction_matrix[direction][0]
                if i not in world.keys():
                    world[i] = {}
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

    final_world = World()

    min_bli = 600
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if x in world[y].keys():
                bli = x + (origin - origin_x)
                if bli < min_bli:
                    min_bli = bli
                try:
                    # final_world[y + (origin - origin_y)][bli] = world[y][x]
                    final_world.set(bli, y + (origin - origin_y), world[y][x])
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


def paint_at(world, i, j, max_branch_index, branch_index):
    """
    Paints a 12x12, 40x40, 80x80 and 320x320 dots around a point at
    given coordinates
    """

    # Radius of differents dots
    # if branch_index != 0:
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
    radiusD = 100 #160 #80 #240

    branch_index_result = max_branch_index/(max_branch_index+branch_index)
    branch_index_result_scaled = max_branch_index/(max_branch_index+(branch_index*100))
    for y in range(-radiusD, radiusD + 1):
        # for x in range(-radiusD, radiusD + 1):
        for x in range(-int(sqrt((radiusD*radiusD)-(y*y))), int(sqrt((radiusD*radiusD)-(y*y))) + 1):
            distance = sqrt((x * x) + (y * y))
            if i + y not in world.keys():
                world[i + y] = {}
            if j + x not in world[i + y].keys():
                world[i + y][j + x] = 0

            if radiusC < distance:
                try:
                    world[i + y][j + x] += \
                        (polynomeD(distance)*branch_index_result)
                except Exception:
                    pass
            elif radiusB < distance:
                try:
                    world[i + y][j + x] += \
                        (polynomeC(distance)*branch_index_result_scaled)
                except Exception:
                    pass
            elif radiusA < distance:
                try:
                    world[i + y][j + x] += \
                        (polynomeB(distance)*branch_index_result_scaled)
                except Exception:
                    pass
            else:
                try:
                    world[i + y][j + x] += \
                        (polynomeA(distance)*branch_index_result_scaled)
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
            for v in range(int(branch_index/2) + (branch_index % 2)):  # 2):
                i += direction_matrix[direction][1]
                j += direction_matrix[direction][0]
                if i not in world.keys():
                    world[i] = {}
                world = paint_at(world, i, j, max_branch_index, branch_index)
        elif seed[branch_index] == "1":
            direction = (direction + 1) % 8
            for v in range(int(branch_index/2) + (branch_index % 2)):  # 2):
                i += direction_matrix[direction][1]
                j += direction_matrix[direction][0]
                if i not in world.keys():
                    world[i] = {}
                world = paint_at(world, i, j, max_branch_index, branch_index)
        elif seed[branch_index] == "2":
            direction = (direction - 1) % 8
            for v in range(int(branch_index/2) + (branch_index % 2)):  # 2):
                i += direction_matrix[direction][1]
                j += direction_matrix[direction][0]
                if i not in world.keys():
                    world[i] = {}
                world = paint_at(world, i, j, max_branch_index, branch_index)


def to_str(world_data, data):
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
    # for G_row in G:
    #    for G_data in G_row:
    for x in WORLD_SIZE_RANGE:
        for y in WORLD_SIZE_RANGE:
            tmp = "-"
            for lettre in grammary_lettres:
                try:
                    if world_data.get(x, y).value <= grammary_correspondance[lettre]:
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
