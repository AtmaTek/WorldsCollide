def get_sprites():
    from graphics.sprites.sprites import id_sprite
    return id_sprite

if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

    import json
    from graphics.palettes.palettes import id_palette
    from api.get_palette_bytes import get_palette_bytes
    palettes = [{
        'id': palette_id,
        'key': key,
        'palette': get_palette_bytes(palette_id)
    } for ((palette_id, key)) in id_palette.items()]
    print(json.dumps(palettes))
