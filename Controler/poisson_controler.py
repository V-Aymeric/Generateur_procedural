from World.Methods import poisson
from Utils.utils_functions import output_in_txt
from World.world import World


def poisson_points_generator(seed, file_path, input_data):

    # Points definition
    world_data = poisson.poisson_disc_sampling(seed)


    #TODO: Definition zone des points
    #   Determiner zone via voronoi
    # https://en.wikipedia.org/wiki/Voronoi_diagram
    #TODO: Definition elevation des zones
    # Elevation via nombre entier (0 = niveau de l'eau; + = terre)
    #TODO: lissage elevation

    s = poisson.poisson_to_str(world_data)
    output_in_txt(file_path, s)

    return s
