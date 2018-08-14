import sys, pygame

def draw_borders(border_image_list, tile_list, screen, zoom, mapx, mapy):
    x = y = 0
    for row in tile_list:
        for tile in row:
            if x-1 >= 0:
                if tile.region != tile_list[y][x-1].region:
                    screen.blit(border_image_list[3][zoom], tile.rect)
            if x+1 <= mapx-1:
                if tile.region != tile_list[y][x+1].region:
                    screen.blit(border_image_list[1][zoom], tile.rect)
            if y-1 >= 0:
                if tile.region != tile_list[y-1][x].region:
                    screen.blit(border_image_list[0][zoom], tile.rect)
            if y+1 <= mapy-1:
                if tile.region != tile_list[y+1][x].region:
                    screen.blit(border_image_list[2][zoom], tile.rect)   
            x += 1
        y += 1
        x = 0

def check_if_in_view(screen, rect):
    screen_rect = pygame.Rect(0,0,screen.get_width(),screen.get_height())
    if rect.colliderect(screen_rect):
        return True
    else:
        return False

def draw_tiles(screen, tile_list, image_dict, zoom):
    for col in tile_list:
        for tile in col:                
            if check_if_in_view(screen, tile.rect):
                screen.blit(image_dict[tile.tile_type][zoom], tile.rect)
                if tile.layer00 != "none":
                    screen.blit(image_dict[tile.layer00][zoom], tile.rect)

def draw_buildings(screen, building_list, image_dict, zoom):
    for item in building_list:
        if check_if_in_view(screen, item.rect):
            screen.blit(image_dict[item.building_type][zoom], item.rect)

def draw_zoning(screen, tile_list, image_dict, zoom):
    for col in tile_list:
        for tile in col:
            if check_if_in_view(screen, tile.rect):
                if tile.fertility == 0:
                    screen.blit(image_dict["zone00"][zoom], tile.rect)
                elif tile.fertility == 1:
                    screen.blit(image_dict["zone01"][zoom], tile.rect)
                else:
                    screen.blit(image_dict["zone02"][zoom], tile.rect)

def draw_region(screen, tile_list, region_colour):
    for team in range(len(region_colour)):
        for col in tile_list:
            for tile in col:
                if check_if_in_view(screen, tile.rect):
                    if tile.region == team+1:
                        screen.fill(region_colour[team], tile.rect)
        
def draw_building_ui(screen, mouse, UI_element_list, selected_ui_element):
    for button in UI_element_list:
        if button.rect.collidepoint(mouse.pos):
            screen.fill((255,0,0),button.rect)
        elif button.name == selected_ui_element:
            screen.fill((0,0,255),button.rect)
        else:
            screen.fill((255,255,150),button.rect)
        screen.blit(button.image,button.rect)
        
## NOT UPDATED YET
def draw_particle():
    if mouse.pos[0] < screen.get_width() - 128:
        rect = mouse.grid_brush()
        pixel_size = Tile.width[zoom]/10
        half_pixel = pixel_size/2
        total_time = 1000
        t = current_time() % total_time
        distance = Tile.width[zoom]*building_ref[selected_ui_element]["size"][0] - half_pixel
        tpos = (distance* t) / total_time
        rect1 = pygame.Rect(rect.left - half_pixel + tpos, rect.top - half_pixel, pixel_size, pixel_size)
        rect2 = pygame.Rect(rect.right + half_pixel - pixel_size, rect.top + tpos, pixel_size, pixel_size)
        rect3 = pygame.Rect(rect.right + half_pixel - pixel_size - tpos, rect.bottom + half_pixel - pixel_size, pixel_size, pixel_size)
        rect4 = pygame.Rect(rect.left - half_pixel, rect.bottom + half_pixel - pixel_size - tpos, pixel_size, pixel_size)
        pygame.draw.rect(screen, (255,255,255), rect1)
        pygame.draw.rect(screen, (255,255,255), rect2)
        pygame.draw.rect(screen, (255,255,255), rect3)
        pygame.draw.rect(screen, (255,255,255), rect4)
        
def draw_cursor(screen, cursor00, mouse, building_ref, selected_ui_element, zoom, Tile):
    if mouse.pos[0] < screen.get_width() - 128:       
        cursor01 = pygame.transform.scale(cursor00, (building_ref[selected_ui_element]["size"][0]*Tile.width[zoom], building_ref[selected_ui_element]["size"][1]*Tile.height[zoom]))
        screen.blit(cursor01, mouse.grid_brush()) 
            
def draw_turn_bar(screen, turn_bar, current_time, turn_length):
    background_rect = pygame.Rect(0,0,turn_bar.get_width(),turn_bar.get_height())
    background_rect.x = screen.get_width() / 2 - (background_rect.width/2)
    progress_rect = pygame.Rect(background_rect.x+5, background_rect.y+5, (turn_bar.get_width()-10)/10 , turn_bar.get_height() -10)
    
    color = (0,0,255)
    
    time = current_time()
    tenth_of_turn = turn_length / 100
    time_this_turn = time % turn_length
    
    increment = time_this_turn // tenth_of_turn
    new_color = (0+increment*2,0,(color[2]-(increment)))
    progress_rect.width = 2.46*increment
    
    screen.blit(turn_bar, background_rect)
    screen.fill(new_color,progress_rect)

def draw_inventory_dislay(screen, invent_font, inventory_display):
    i = j = 0
    xoffset = 5
    for j in range(len(inventory_display)):
        for i in range(len(inventory_display[j])):
            if j == 0:
                screen.fill((48,48,48), inventory_display[j][0][0])
            else:
                text = invent_font.render(inventory_display[j][i][1],1,(255,255,255))
                text_height = text.get_height()
                text_width = text.get_width()
                rect = inventory_display[j][i][0]
                drawx = rect.x + rect.width/2 - text_width/2
                drawy = rect.y + rect.height/2 - text_height/2
                location = (drawx, drawy)

                screen.fill((128,128,128), rect)
                pygame.draw.rect(screen, (192,192,192), rect, 2)
                screen.blit(text, location)
                i += 1
        j += 1
        i = 0
