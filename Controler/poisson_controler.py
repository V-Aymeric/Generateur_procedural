def poisson_points_generator(seed, file_path, input_data):
    P = poisson_disk.poisson_disc_sampling(seed)
    s = poisson_disk.poisson_to_str(P)
    output_in_txt(file_path, s)

    return s