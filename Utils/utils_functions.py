def output_in_txt(arg_path, arg_str):
    file = open(arg_path, "w", encoding="utf-8")
    file.write(arg_str)
    file.close()