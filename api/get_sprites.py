def get_sprites():
    from graphics.sprites.sprites import id_sprite
    return id_sprite

if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

    import json
    from graphics.sprites.sprites import id_sprite
    print(json.dumps(id_sprite))
