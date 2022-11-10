
def print_sprite(sprite_path, palette_path):
    print(str(get_rgb_bytes(sprite_path, palette_path)))

def get_rgb_bytes(sprite_path, palette_path):
    from graphics.palette_file import PaletteFile
    from graphics.sprite_file import SpriteFile
    from graphics.poses import CHARACTER
    palette = PaletteFile(palette_path)

    sprite = SpriteFile(sprite_path, palette)

    return sprite.rgb_data(CHARACTER[1])

if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("sprite_path", help = "Path to sprite pal file to print")
    parser.add_argument("palette_path", help = "Path to palette pal file to print")

    args = parser.parse_args()
    print_sprite(args.sprite_path, args.palette_path)
