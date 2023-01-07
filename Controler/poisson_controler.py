from World.Methods import poisson
from Utils.utils_functions import output_in_txt


def poisson_points_generator(seed, file_path, input_data):
    P = poisson.poisson_disc_sampling(seed)
    s = poisson.poisson_to_str(P)
    output_in_txt(file_path, s)

    return s
