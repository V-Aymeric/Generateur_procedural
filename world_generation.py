import sys
import os
import time

#TODO: Check why I made this file and where it is used

grammary_dict = {
    "A": "ABAAABB",
    "B": "ABBAB",
    "C": "B",
    "D": "BBA",
    "E": "BA",
    "F": "ABA",
    "G": "BBAB",
    "H": "AABA",
    "I": "BABA",
    "J": "AA",
    "K": "BB",
    "L": "BAAB",
    "M": "ABBA",
    "N": "BAB",
    "O": "AAB",
    "P": "AAA",
    "Q": "BBB",
    "R": "BBAA",
    "S": "ABAA",
    "T": "A",
    "U": "BAB",
    "V": "AAB",
    "W": "B",
    "X": "AA",
    "Y": "BB",
    "Z": "BABAB"
}

grammary_dict_2 = {
    "A": "B",
    "B": "H",
    "C": "F",
    "D": "B",
    "E": "D",
    "F": "D",
    "G": "H",
    "H": "B",
    "I": "F",
    "J": "F",
    "K": "H",
    "L": "B",
    "M": "C",
    "N": "E",
    "O": "A",
    "P": "E",
    "Q": "E",
    "R": "A",
    "S": "C",
    "T": "A",
    "U": "B",
    "V": "G",
    "W": "G",
    "X": "H",
    "Y": "G",
    "Z": "E"
}

movement_dict = {
    "A": [-1, -1],
    "B": [-1, 0],
    "C": [-1, 1],
    "D": [0, 1],
    "E": [1, 1],
    "F": [1, 0],
    "G": [1, -1],
    "H": [0, -1]
}


def generate_grammary(arg_str):
    tmp_str = ""
    for i in range(3):
        for c in arg_str:
            tmp_str += grammary_dict[c]
        arg_str = tmp_str
        tmp_str = ""

    return arg_str


def generate_grammary_2(arg_str):
    tmp_str = ""
    for i in range(4):
        for c in arg_str:
            tmp_str += grammary_dict_2[c]
        arg_str = tmp_str
        tmp_str = ""

    return arg_str


def draw_2(arg_str):
    array_size_f = 40
    array_size = array_size_f + 1
    final_array = []

    for i in range(array_size):
        tmp = []
        for j in range(array_size):
            tmp.append('-')
        final_array.append(tmp)

    index_x = round(array_size_f / 2)
    index_y = round(array_size_f / 2)
    final_array[index_y][index_x] = 'O'

    for c in arg_str:
        try:
            tmp_movmt = movement_dict[c]
        except Exception:
            pass
        try:
            if (index_x + tmp_movmt[1] in range(array_size)
                    and index_y + tmp_movmt[0] in range(array_size)):
                index_y = index_y + tmp_movmt[0]
                index_x = index_x + tmp_movmt[1]
                final_array[index_y][index_x] = 'O'
        except Exception:
            pass

    display_array(final_array)


def draw_with_grammary(arg_str):
    array_size = 20

    world_map = []
    for i in range(20):
        tmp = []
        for j in range(20):
            tmp.append('-')
        world_map.append(tmp)

    for wm in world_map:
        print(str(wm))

    print()
    print()

    x = 0
    y = 0
    for c in arg_str:
        if c == "A":

            world_map[x][y] = "O"
            if y + 1 != 20:
                y += 1
            pass

        elif c == "B":

            world_map[x][y] = "O"
            if x + 1 != 20:
                x += 1
            pass

    for wm in world_map:
        print(str(wm))

    print()
    print()
    #print(str(world_map))


def display_array(arg_array):

    final_str = ""
    for y in range(len(arg_array)):
        for x in range(len(arg_array[y])):
            final_str += arg_array[y][x]
        final_str += "\n"

    print()
    print()
    print(final_str)


    #############

def __isAlive(arg_array, x, y):
    somme = 0
    for a in [y-1, y, y+1]:
        for b in [x - 1, x, x + 1]:
            if arg_array[a][b] == "O":
                somme += 1

    if somme not in [2, 3]:
        return "-"
    else:
        return "O"


def __isNotBorn(arg_array, x, y):
    somme = 0
    for a in [y - 1, y, y + 1]:
        for b in [x - 1, x, x + 1]:
            if arg_array[a][b] == "O":
                somme += 1

    if somme == 3:
        return "-"
    else:
        return "O"


def iteration_life_game(arg_array=[]):
    array_copy = []

    for y in range(0, len(arg_array)):
        array_copy.append([])
        for x in range(0, len(arg_array[y])):
            if arg_array[y][x] == "-":
                array_copy[y].append(__isNotBorn(arg_array, x, y))
            elif arg_array[y][x] == "O":
                array_copy[y].append(__isAlive(arg_array, x, y))
