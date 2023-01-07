def process_perlin_seed(seed):

    # XXXYYYZZZ
    # => XXX = Scale
    # => YYY = coord X
    # => ZZZ = coord y

    coord_x = None
    coord_y = None

    coord_y = ((seed % 1000000) - (seed % 1000))/1000
    coord_x = seed % 1000

    return int(coord_x), int(coord_y)


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


def process_grammar_seed(seed):

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