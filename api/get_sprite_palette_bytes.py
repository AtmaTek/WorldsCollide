def get_sprite_palette_bytes(sprite_id, palette_id, pose_id):
    from graphics.sprites.sprites import get_path as get_sprite_path
    from graphics.palettes.palettes import get_path as get_palette_path
    from graphics.palette_file import PaletteFile
    from graphics.sprite_file import SpriteFile
    from graphics.poses import CHARACTER
    
    palette = PaletteFile(get_palette_path(palette_id))
    sprite = SpriteFile(get_sprite_path(sprite_id), palette)
    
    palette_bytes = [(color.red, color.green, color.blue) for color in palette.colors]
    sprite_bytes = [item for sublist in sprite.tile_matrix(CHARACTER[pose_id]) for item in sublist]
    
    return (sprite_bytes, palette_bytes)
