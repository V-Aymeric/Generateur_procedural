from World.Methods import poisson
from Utils.utils_functions import output_in_txt
from World.world import World


def poisson_points_generator(seed, file_path, input_data):

    world_data = poisson.poisson_disc_sampling(seed)
    s = poisson.poisson_to_str(world_data)
    output_in_txt(file_path, s)

    return s
