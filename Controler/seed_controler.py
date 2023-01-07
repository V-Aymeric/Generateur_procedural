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