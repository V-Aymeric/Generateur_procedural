from Perlin import noise_plugin
from Perlin import perlin_points
from poisson import poisson_disk
import stats
import grammar

caracters = [
        "˵",
        "ᴖ",
        "∩",
        "▲",
]

def output_in_txt(arg_path, arg_str):
    file = open(arg_path, "w", encoding="utf-8")
    file.write(arg_str)
    file.close()


def perlin_generator(seed, file_path, input_data):
    #https://github.com/caseman/noise/blob/master/_perlin.c
    coord_x, coord_y = noise_plugin.process_seed(int(seed))


    P = noise_plugin.calculate_perlin_values(coord_x, coord_y)
    P = noise_plugin.apply_circle_correction(P)
    statistiques = stats.perlin_stats(P)


    data_slider = {
        "water": int(statistiques.get_val_at_percentage(
            input_data.get_water_percentage())*100
        ),  # 0,
        "beach": int(statistiques.get_val_at_percentage(
            input_data.get_beach_percentage()) * 100
        ),  # 25,
        "plains": int(statistiques.get_val_at_percentage(
            input_data.get_plain_percentage()) * 100
        ),  # 25,
        "mountain": int(statistiques.get_val_at_percentage(
            input_data.get_mountain_percentage()) * 100
        )  # 1000 get_mountain_percentage
    }
    s = noise_plugin.convert_values_to_string(P, data_slider)
    output_in_txt(file_path, s)
    print("Generation Perlin OK")
    return s


def grammary_generator(seed, file_path, input_data):
    print("input_data.get_water_percentage() = " + str(input_data.get_water_percentage()))
    print("input_data.get_beach_percentage() = " + str(input_data.get_beach_percentage()))
    print("input_data.get_plain_percentage() = " + str(input_data.get_plain_percentage()))
    print("input_data.get_mountain_percentage() = " + str(
        input_data.get_mountain_percentage()))
    print("processing seed")
    seed_new = grammar.process_seed(str(seed))
    #print(seed_new)
    print("drawing map ...")
    G = grammar.draw(seed_new)  # Grammar.draw(seed)
    print("statistics")

    print("Corrections : cellular")
    #G = grammar.cellular_2(G, input_data)
    print("Corrections : polynom")
    #G = grammar.circular_correction(G, input_data)
    #G = grammar.correction_cellular_automaton(G, input_data)
    print("preparing string")

    statistiques = stats.perlin_stats(G)

    statistiques.debug_percentages()
    data_slider = {
        "water": float(statistiques.get_val_at_percentage(
            input_data.get_water_percentage())),  # 0,
        "beach": float(statistiques.get_val_at_percentage(
            input_data.get_beach_percentage())),  # 25,
        "plains": float(statistiques.get_val_at_percentage(
            input_data.get_plain_percentage())),  # 25,
        "mountain": float(statistiques.get_val_at_percentage(
            input_data.get_mountain_percentage()))
        # 1000
    }

    s = grammar.to_str(G, data_slider)
    print("writing file")
    output_in_txt(file_path, s)
    print("Generation Grammaire OK")

    return s


def poisson_points_generator(seed, file_path, input_data):
    P = poisson_disk.poisson_disc_sampling(seed)
    s = poisson_disk.poisson_to_str(P)
    output_in_txt(file_path, s)

    return s


def str_to_tab(s):
    s_lines = s.split("\n")
    y = 0
    world = []
    for line in s_lines:
        world.append([])
        for letter in line:
            world[y].append(letter)
        y += 1

    return world