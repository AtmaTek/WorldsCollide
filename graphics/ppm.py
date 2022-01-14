def write_ppm6(width, height, bits_per_value, values, output_file):
    max_value = (1 << bits_per_value) - 1

    header = f"P6 {width} {height} {max_value}\n"
    with open(output_file, "wb") as output:
        output.write(header.encode("ascii"))
        output.write(bytes(values))
