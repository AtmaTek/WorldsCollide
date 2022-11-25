def get_sprites():
    from graphics.sprites.sprites import id_sprite
    return id_sprite

if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

    import json
    from graphics.sprites.sprites import id_sprite
    from api.get_sprite_palette_bytes import get_sprite_palette_bytes
    
    sprites = [{
        'id': sprite_id,
        'key': key,
    } for ((sprite_id, key)) in id_sprite.items()]
    print(json.dumps(sprites))
