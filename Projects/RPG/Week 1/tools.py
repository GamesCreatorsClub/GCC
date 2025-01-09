import pygame


def create_scaled_tile_sheet(tile_sheet, pixel_size, scale):
    sheet_width, sheet_height = tile_sheet.get_size()

    columns = int(sheet_width / pixel_size)
    rows = int(sheet_height / pixel_size)

    number_of_tiles = columns * rows

    tiles = []

    for y in range(rows):
        for x in range(columns):
            rect = pygame.Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size)
            tiles.append(tile_sheet.subsurface(rect))

    new_pixel_size = pixel_size * scale
    scaled_tiles = []
    for tile in tiles:
        scaled_tiles.append(pygame.transform.scale(tile, (new_pixel_size, new_pixel_size)))
        
    return scaled_tiles
        

def scale_image(image, pixel_size, scale):
    new_pixel_size = pixel_size * scale
    scaled_image = pygame.transform.scale(image, (new_pixel_size, new_pixel_size))
    return scaled_image
