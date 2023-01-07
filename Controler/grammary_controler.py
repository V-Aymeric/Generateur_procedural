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