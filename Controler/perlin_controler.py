from Perlin import noise_plugin  #https://github.com/caseman/noise/blob/master/_perlin.c

from Statistics import stats

from Controler import seed_controler
from World.Methods import perlin
from Utils.utils_functions import output_in_txt


def perlin_generator(seed, file_path, input_data):
    coord_x, coord_y = seed_controler.process_perlin_seed(int(seed))

    P = perlin.calculate_perlin_values(coord_x, coord_y)
    P = perlin.apply_circle_correction(P)
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