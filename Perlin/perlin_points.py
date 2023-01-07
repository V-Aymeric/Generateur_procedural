def perlin_points(perlin_tab):
    final_tab = []
    i = 0
    s = ""
    for row in perlin_tab:
        final_tab.append([])
        for value in row:
            if int(value) % 5 == 0:
                final_tab[i].append("∩")
                s += "∩"
            else:
                final_tab[i].append("▲")
                s += "▲"
        s += "\n"

    return s

#def perlin_points_to_str(perlin_points_tab):
