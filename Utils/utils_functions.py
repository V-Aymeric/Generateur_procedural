def output_in_txt(arg_path, arg_str):
    file = open(arg_path, "w", encoding="utf-8")
    file.write(arg_str)
    file.close()


caracters = [
        "˵",
        "ᴖ",
        "∩",
        "▲",
]


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