import pygame, random
import sys

global background_image_path
background_image_path = "images/background.png"

screen = pygame.display.set_mode((800,600))

# Your code here

global zoom
global tile_list, building_list, UI_element_list
global click_delay, building_ref, cursor01
global mapx, mapy
global inventory_font

grass00 = pygame.image.load("images/grass01.png").convert_alpha()
dirt00 = pygame.image.load("images/dirt.png").convert_alpha()
water00 = pygame.image.load("images/water00.png").convert_alpha()

cursor00 = pygame.image.load("images/tile_select.png").convert_alpha()
cursor01 = cursor00
cross00 = pygame.image.load("images/cross00.png").convert_alpha()

townhall00 = pygame.image.load("images/townhall00.png").convert_alpha()
house00 = pygame.image.load("images/house00.png").convert_alpha()
house01 = pygame.image.load("images/house01.png").convert_alpha()
path00 = pygame.image.load("images/path00.png").convert_alpha()
tree00 = pygame.image.load("images/tree01.png").convert_alpha()
rock00 = pygame.image.load("images/rock00.png").convert_alpha()
field00 = pygame.image.load("images/field00.png").convert_alpha()
city00 = pygame.image.load("images/city00.png").convert_alpha()
shop00 = pygame.image.load("images/shop00.png").convert_alpha()
zone00 = pygame.image.load("images/zone00.png").convert_alpha()
zone01 = pygame.image.load("images/zone01.png").convert_alpha()
zone02 = pygame.image.load("images/zone03.png").convert_alpha()

def create_image_dict():
    global image_dict
    image_dict = {
        "grass00": scaled_images(grass00),
        "dirt00": scaled_images(dirt00), 
        "water00": scaled_images(water00),
        "townhall00": scaled_images(townhall00, building_ref["townhall00"]["size"][0], building_ref["townhall00"]["size"][1]),
        "house00": scaled_images(house00, building_ref["house00"]["size"][0], building_ref["house00"]["size"][1]),
        "house01": scaled_images(house01, building_ref["house01"]["size"][0], building_ref["house01"]["size"][1]),
        "path00": scaled_images(path00, building_ref["path00"]["size"][0], building_ref["path00"]["size"][1]),
        "tree00": scaled_images(tree00),
        "rock00": scaled_images(rock00),
        "city00": scaled_images(city00),
        "shop00": scaled_images(shop00, building_ref["shop00"]["size"][0], building_ref["shop00"]["size"][1]),
        "field00": scaled_images(field00, building_ref["field00"]["size"][0], building_ref["field00"]["size"][1]),
        "cursor00": scaled_images(cursor00),
        "zone00": scaled_images(zone00),
        "zone01": scaled_images(zone01),
        "zone02": scaled_images(zone02)
        }

turn_bar = pygame.image.load("images/turn_bar.png").convert_alpha()
inventory_font = "fonts/CAESAR.ttf"

zoom = 2
image_dict = {}

mapx = 64
mapy = 64

selected_ui_element = "none"
click_delay = 0
tile_list = []
building_list = []
UI_element_list = []

class Tile(object):
    height = [2, 16, 32, 64, 128]
    width = [2, 16, 32, 64, 128]

    def __init__(self, x, y, tile_type):
        self.init_pos = [
            (x*Tile.width[0],y*Tile.height[0]),
            (x*Tile.width[1],y*Tile.height[1]),
            (x*Tile.width[2],y*Tile.height[2]),
            (x*Tile.width[1],y*Tile.height[3]),
            (x*Tile.width[1],y*Tile.height[4])
            ]
        self.init_rects = [
            pygame.Rect(x*Tile.width[0], y*Tile.height[0], Tile.width[0], Tile.height[0]),
            pygame.Rect(x*Tile.width[1], y*Tile.height[1], Tile.width[1], Tile.height[1]),
            pygame.Rect(x*Tile.width[2], y*Tile.height[2], Tile.width[2], Tile.height[2]),
            pygame.Rect(x*Tile.width[3], y*Tile.height[3], Tile.width[3], Tile.height[3]),
            pygame.Rect(x*Tile.width[4], y*Tile.height[4], Tile.width[4], Tile.height[4])
            ]
        self.rect = self.init_rects[zoom]
        
        self.coord = (x, y)
        self.x = x
        self.y = y
        self.tile_type = tile_type      
        self.layer00 = "none"
        rand = random.random()
        if rand < 0.1:
            self.fertility = 0
        elif rand < 0.5:
            self.fertility = 1
        else:
            self.fertility = 2
        if self.tile_type == "water00":
            self.fertility = 0
        self.built = False
        self.region = 0
        self.owner = 0

class Building(object):
    def __init__(self, x, y, building):
        self.coord = (x, y)

        self.building = building
        self.xsize = building_ref[building]["size"][0]
        self.ysize = building_ref[building]["size"][1]
                
        self.init_rects = [
            pygame.Rect(x*Tile.width[0], y*Tile.height[0], Tile.width[0]*self.xsize, Tile.height[0]*self.ysize),
            pygame.Rect(x*Tile.width[1], y*Tile.height[1], Tile.width[1]*self.xsize, Tile.height[1]*self.ysize),
            pygame.Rect(x*Tile.width[2], y*Tile.height[2], Tile.width[2]*self.xsize, Tile.height[2]*self.ysize),
            pygame.Rect(x*Tile.width[3], y*Tile.height[3], Tile.width[3]*self.xsize, Tile.height[3]*self.ysize),
            pygame.Rect(x*Tile.width[4], y*Tile.height[4], Tile.width[4]*self.xsize, Tile.height[4]*self.ysize)
            ]
        self.rect = self.init_rects[zoom]

# This class is going to deal with all mouse input and use
class Mouse(object):
    def __init__(self):
        self.pos = pygame.mouse.get_pos()
        
    def xcoord(self):
        x = ((self.pos[0] - xshift) // Tile.width[zoom])
        return x
    
    def ycoord(self):
        y = ((self.pos[1] - yshift) // Tile.height[zoom])
        return y
    
    def coord(self):
        x = ((self.pos[0] - xshift) // Tile.width[zoom])
        y = ((self.pos[1] - yshift) // Tile.height[zoom])
        return (x,y)

    def grid_brush(self):
        x = self.pos[0] // Tile.width[zoom]
        y = self.pos[1] // Tile.height[zoom]  
        
        if selected_ui_element == "none":
            rectx = x*Tile.width[zoom]
            recty = y*Tile.height[zoom]
            xsize = 1
            ysize = 1
        else:
            xsize = building_ref[selected_ui_element]["size"][0]
            ysize = building_ref[selected_ui_element]["size"][1]
            if xsize % 2 == 0:
                dx = mouse.pos[0] % Tile.width[zoom]
                if dx <= Tile.width[zoom]/2:
                    x -= 1
            else:
                x -= xsize // 2
            if ysize % 2 == 0:
                dy = mouse.pos[1] % Tile.height[zoom]
                if dy <= Tile.height[zoom]/2:
                    y -= 1
            else:
                y -= ysize // 2
                
        rectx = x*Tile.width[zoom]
        recty = y*Tile.height[zoom]
        rect = pygame.Rect(rectx, recty, Tile.width[zoom]*xsize, Tile.height[zoom]*ysize)
        return rect

    def left_mouse_click(self):
        if pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

# This class is for creating build buttons that will be clickable
class UI_element(object):
    def __init__(self,x,y, height, width, image, name):
        self.image = image
        self.name = name
        self.rect = pygame.Rect(x,y,height,width)

#### CAMERA RELATED FUNCTIONS #####################
def camera_control(speed):
    global xshift, yshift
    if keys[pygame.K_RIGHT]:
        xshift -= speed
    elif keys[pygame.K_LEFT]:
        xshift += speed
    if keys[pygame.K_UP]:
        yshift += speed
    elif keys[pygame.K_DOWN]:
        yshift -= speed

def camera_move():
    global xshift, yshift
    global tile_list
    for col in tile_list:
        for tile in col:
            x = tile.coord[0]*Tile.width[zoom]
            y = tile.coord[1]*Tile.height[zoom]
            tile.rect[0] = x + xshift
            tile.rect[1] = y + yshift
    
    for building in building_list:
        x = building.coord[0]*Tile.width[zoom]
        y = building.coord[1]*Tile.height[zoom]
        building.rect[0] = x + xshift
        building.rect[1] = y + yshift

# This functions detects a single input of the plus or minus keys and then increments the global zoom        
def change_zoom():
    global zoom
    global tile_list
    global xshift, yshift
    last_zoom = zoom
    if keys[pygame.K_KP_MINUS] and(keys[pygame.K_KP_MINUS] != last_keys[pygame.K_KP_MINUS]) and zoom > 0:
        zoom -= 1
    if keys[pygame.K_KP_PLUS] and(keys[pygame.K_KP_PLUS] != last_keys[pygame.K_KP_PLUS]) and zoom < len(Tile.height)-1:
        zoom += 1
    if zoom != last_zoom:
        for col in tile_list:
            for tile in col:
                tile.rect = tile.init_rects[zoom]
        for building in building_list:
            building.rect = building.init_rects[zoom]
            
        midx = (screen.get_width()/Tile.width[zoom]) // 2
        midy = (screen.get_height()/Tile.height[zoom]) // 2
        
        xshift = Tile.width[zoom]*midx - Tile.width[zoom]*(mapx//2) 
        yshift = Tile.height[zoom]*midy - Tile.height[zoom]*(mapy//2)

#### GAME INIT FUNCTIONS #####################
# This function populates the tile_list to create a map
def create_map():
    global tile_list
    tile_list = []
    row_list = []
    x = y = 0
    xcoord = ycoord = 0
    
    for col in range(mapy):
        row_list = []
        for tile in range(mapx):
            tile = Tile(x,y,"grass00")
            if x == 0 or x == mapx - 1 or y == 0 or y == mapy - 1:
                tile = Tile(x,y,"water00")
            if x == 1 or x == mapx - 2 or y == 1 or y == mapy - 2:
                if random.random() < 0.6:
                    tile = Tile(x,y,"water00")
            if x == 2 or x == mapx - 3 or y == 2 or y == mapy - 3:
                if random.random() < 0.3:
                    tile = Tile(x,y,"water00")
            row_list.append(tile)
            x += 1
        tile_list.append(row_list)
        y += 1
        x = 0

    forest_num = 30
    k = 0
    while k < forest_num:
        i = iref = random.randint(0,mapx-10)
        j = jref = random.randint(0,mapx-10)
        maxi = i + 8
        maxj = j + 9
        while j <= maxj:
            while i <= maxi:
                if random.random() < 0.9:
                    tile_list[j][i].layer00 = "tree00"
                i += 1
            j += 1
            i = iref
        k += 1

    for col in tile_list:
        for tile in col:
            if random.random() < 0.1:
                tile.layer00 = "rock00"
            elif random.random() < 0.3:
                tile.layer00 = "tree00"
            if tile.tile_type == "water00":
                tile.layer00 = "none"        
    
def create_UI_element_list():
    global UI_element_list
    image = [house00, house01, path00, field00, city00, shop00, field00, house00]
    name = ["house00", "house01", "path00", "field00", "city00", "shop00", "field00", "house00"]
    x = screen.get_width() - 128
    y = index = 0
    for button in range(8):
        rect = UI_element(x, y, 128, 128, image[index], name[index])
        UI_element_list.append(rect)
        index += 1
        y += 128+8
        
# This function takes a single image and creates multiple scaled versions and returns them in a list
def scaled_images(image,xsize = 1,ysize = 1):
    scaled_list = [
            pygame.transform.scale(image,(int(Tile.width[0]*xsize),int(Tile.height[0]*ysize))),
            pygame.transform.scale(image,(int(Tile.width[1]*xsize),int(Tile.height[1]*ysize))),
            pygame.transform.scale(image,(int(Tile.width[2]*xsize),int(Tile.height[2]*ysize))),
            pygame.transform.scale(image,(int(Tile.width[3]*xsize),int(Tile.height[3]*ysize))),
            pygame.transform.scale(image,(int(Tile.width[4]*xsize),int(Tile.height[4]*ysize)))
            ]
    return scaled_list

resource_list = [
    {"name": "population",  "type": "pop",      "value": 0},
    {"name": "grain",       "type": "food",     "value": 10},
    {"name": "wood",        "type": "cons_mat", "value": 20},
    {"name": "stone",       "type": "cons_mat", "value": 30},
    {"name": "clay",        "type": "raw_mat",  "value": 15},
    {"name": "pottery",     "type": "lux_mat",  "value": 50},
    ]

building_ref = {
    "none": {"bulding_type": "none", "size": (1,1)},
    "house00": {"bulding_type": "house", "size": (2,2), "cost": 50},
    "house01": {"bulding_type": "house", "size": (3,3), "cost": 200},
    "path00": {"bulding_type": "road", "size": (1,1), "cost": 5},
    "shop00": {"bulding_type": "market", "size": (2,2), "cost": 100},
    "field00": {"bulding_type": "farm", "size": (2,2), "cost": 15, "grain_p": 5},
    "townhall00": {"bulding_type": "civic", "size": (3,4), "cost": 500, "grain_p": 10, "gold_p": 10},
    } 

# Name, stored, prod, cons, net
inventory = [
    ["Population", 10, 0, 0, 0],
    ["Gold", 20, 0, 0, 0],
    ["Grain", 20, 0, 0, 0],
    ["Wood", 20, 0, 0, 0],
    ["Stone", 0, 0, 0, 0],
    ["Clay", 0, 0, 0, 0],
    ["Pottery", 0, 0, 0, 0]
    ]

# Look up the resource list to create a series of rects that will be used to display a cities inventory
def create_inventory_display(xpix,ypix):
    global inventory_display
    inventory_display = []
    temp_list = []
    headings = ["Resource","Storage","Production","Consumption", "Net"]
    num_row = len(inventory)+1
    num_col = len(inventory[0])
    gap = 4

    i = j = 0
    width = 120
    height = 30
    background_width = width * num_col + gap * (num_col + 1) 
    background_height = height * num_row + gap * (num_row + 1)

    # Remove this to use arguments to assign location
    ypix = screen.get_height() - background_height

    item1 = pygame.Rect(xpix,ypix, background_width, background_height)
    item2 = "hello"
    temp_list.append([item1,item2])
    inventory_display.append(temp_list)
    
    temp_list = []

    for i in range(num_col):
        item3 = pygame.Rect(xpix+((i+1)*gap) +(i*width),ypix+gap, width, height)
        item4 = headings[i]
        temp_list.append([item3,item4])
    inventory_display.append(temp_list)

    for j in range(num_row-1):
        temp_list = []
        for i in range(num_col):
            item5 = pygame.Rect(xpix + ((i+1)*gap) + (i*width),ypix + ((j+2)*gap) + ((j+1)*height), width, height)
            item6 = inventory[j][i]
            item6 = str(item6)
            temp_list.append([item5,item6])
        inventory_display.append(temp_list)

    return inventory_display

def update_inventory():
    global inventory
    # Test case of calculating production/consumption THIS WILL NEED TO CHANGE
    grain_prod = 0
    for building in building_list:
        if building.building == "field00":
            grain_prod += building_ref["field00"]["grain_p"]
    inventory[2][2] = grain_prod
    # Calculate the net values
    for i in range(len(inventory)):
        inventory[i][4] = inventory[i][2] + inventory[i][3]
        
def apply_income():
    for i in range(len(inventory)):
        inventory[i][1] += inventory[i][4]

def current_time():
    time = pygame.time.get_ticks() - start_time
    return time

def end_of_turn():
    global last_turn
    current_turn = current_time() // turn_length
    # This code makes all of the changes that happen at the end of a turn. Calculating inventory/pop change etc.
    if current_turn != last_turn:
        update_inventory()
        create_inventory_display(0,0)
        apply_income()
        # This statement should be the last change to be made
        last_turn = current_turn   
    
def debug_text2(text1,text2,text3):
    text_1 = debug_font.render(text1,1,(255,255,255))
    text_2 = debug_font.render(text2,1,(255,255,255))
    text_3 = debug_font.render(text3,1,(255,255,255))
    screen.blit(text_1, (0,0))
    screen.blit(text_2, (0,40))
    screen.blit(text_3, (0,80))
    
#### GAME RUNNING FUNCTIONS #####################
def check_build_area_clear():
    for col in tile_list:
        for tile in col:
            if tile.rect.colliderect(mouse.grid_brush()):
                if tile.built == True:
                    return False
    return True

def create_new_building(x,y):
    rect = mouse.grid_brush()
    xrect = rect.x - xshift
    yrect = rect.y - yshift
    x = xrect/Tile.width[zoom]
    y = yrect/Tile.height[zoom]
    building = Building(x,y, selected_ui_element)
    return building

def convert_build_area():
    for col in tile_list:
        for tile in col:
            if tile.rect.colliderect(mouse.grid_brush()):
                tile.built = True
                tile.layer00 = "none"
                tile.tile_type = "grass00"
                
###################################################################################################################################################################################################################################               
#### DRAW FUNCTIONS #####################
def draw_tiles():
    for col in tile_list:
        for tile in col:
            if (tile.rect.x < screen.get_width() - 128) and (tile.rect.x >= 0) and (tile.rect.y >=0) and (tile.rect.y < screen.get_height()):
                screen.blit(image_dict[tile.tile_type][zoom], tile.rect)
                if tile.layer00 != "none":
                    screen.blit(image_dict[tile.layer00][zoom], tile.rect)

def draw_buildings():
    for item in building_list:
        screen.blit(image_dict[item.building][zoom], item.rect)

def draw_zoning():
    for col in tile_list:
        for tile in col:
            if tile.fertility == 0:
                screen.blit(image_dict["zone00"][zoom], tile.rect)
            elif tile.fertility == 1:
                screen.blit(image_dict["zone01"][zoom], tile.rect)
            else:
                screen.blit(image_dict["zone02"][zoom], tile.rect)

def draw_mouse_brush():
    global mouse
    if selected_ui_element != "none" and mouse.pos[0] < screen.get_width() - 128:
        if check_build_area_clear():
            if current_time()% 1400 < 1200:
                screen.blit(image_dict[selected_ui_element][zoom], mouse.grid_brush())
        else:
            cross = pygame.transform.scale(cross00, (building_ref[selected_ui_element]["size"][0]*Tile.width[zoom], building_ref[selected_ui_element]["size"][1]*Tile.height[zoom]))
            screen.blit(cross, mouse.grid_brush())
        
def draw_building_ui():
    for button in UI_element_list:
        if button.rect.collidepoint(mouse.pos):
            screen.fill((255,0,0),button.rect)
        elif button.name == selected_ui_element:
            screen.fill((0,0,255),button.rect)
        else:
            screen.fill((255,255,150),button.rect)
        screen.blit(button.image,button.rect)

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
        
def draw_cursor():
    if mouse.pos[0] < screen.get_width() - 128:       
        cursor01 = pygame.transform.scale(cursor00, (building_ref[selected_ui_element]["size"][0]*Tile.width[zoom], building_ref[selected_ui_element]["size"][1]*Tile.height[zoom]))
        screen.blit(cursor01, mouse.grid_brush()) 
            
def draw_turn_bar():
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

def draw_inventory_dislay():
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

def draw_text():
    debug_text(str(mouse.coord()),str(xshift/Tile.width[zoom]),str(yshift))
    
#### TEXT FUNCTIONS #####################
def debug_text(text1,text2,text3):
    text_1 = debug_font.render(text1,1,(255,255,255))
    text_2 = debug_font.render(text2,1,(255,255,255))
    text_3 = debug_font.render(text3,1,(255,255,255))
    screen.blit(text_1, (0,0))
    screen.blit(text_2, (0,40))
    screen.blit(text_3, (0,80))

######################################################################################################################################################
        #Special Functions
######################################################################################################################################################
def custom_game_init():
    """
    Perform one-time initialisation here
    This is only called once when the game is first run
    """
    global title_font, level_font, debug_font, invent_font
    global tile_list, UI_element_list
    global mouse
    global xshift, yshift
    global last_turn
    global turn_length

    ######################### GAME CONSTANTS ###############################
    turn_length = 10000
    ########################################################################
    
    ######################### IMAGES #######################################
    global tile_cursor, tree
    create_image_dict()
    ########################################################################

    xshift = yshift = 0
    last_turn = 0
    
    mouse = Mouse()
    create_map()

    # Randomly place the start town hall (THIS IS TEMPORARY IT NEEDS IMPROVING)
    startx = random.randint(5,mapx-8)
    starty = random.randint(5,mapy-8)
    start_building = Building(startx,starty, "townhall00")
    building_list.append(start_building)

    for j in range(4):
        for i in range(3):
            for col in tile_list:
                for tile in col:
                    if tile.coord == (startx+i,starty+j):
                        tile.built = True
                        tile.layer00 = "none"
                        tile.tile_type = "grass00"
    ####################################################################


    
    create_UI_element_list()

    title_font = pygame.font.SysFont("ariel", 50)
    level_font = pygame.font.SysFont("ariel", 32)
    debug_font = pygame.font.SysFont("ariel", 32)
    invent_font = pygame.font.SysFont("ariel", 26)

    create_inventory_display(0,0)
    
    add_game_state("start", "update_game_start", "draw_game_start")
    add_game_state("running", "update_game_running", "draw_game_running")
    set_game_state("start")
    return
    
def custom_game_reset():
    global start_time
    """
    Reset any game values here before starting a game-running type game-state
    You will typically call this function many times during a game session
    """
    start_time = pygame.time.get_ticks()
    return 

def update_game_running():
    global keys
    global zoom
    global click_delay
    global mouse, tile_list, building_list, building_ref
    global selected_ui_element

    mouse = Mouse()

    # UI control of the construction buttons on right side of screen
    if mouse.left_mouse_click():
        if mouse.pos[0] > screen.get_width() - 128:
            for button in UI_element_list:
                if button.rect.collidepoint(mouse.pos):
                    if button.name == selected_ui_element:
                        selected_ui_element = "none"                    
                    else:
                        selected_ui_element = button.name

        # If mouse is on board then buildings can be built at the cursor brush location
        else:
            if selected_ui_element != "none":
                for col in tile_list:
                    for tile in col:
                        if tile.x == mouse.xcoord() and tile.y == mouse.ycoord():
                            if check_build_area_clear():
                                building_list.append(create_new_building(mouse.xcoord(),mouse.ycoord()))
                                convert_build_area()
                                
    if keys[pygame.K_r]:
        create_map()

    if keys[pygame.K_ESCAPE]:
        custom_game_reset()
        set_game_state("start")
    if keys[pygame.K_w]:
        pygame.quit()
        sys.exit()
        
    change_zoom()
    camera_control(Tile.width[zoom])
    camera_move()
    end_of_turn()
    
    if click_delay > 0:
        click_delay -= 1   
    return

def draw_game_running():
    global screen
    global background_surface

    # Draw background star image
    screen.blit(background_surface, (0,0))

    # Draws the tile then the layer00 on top
    draw_tiles()

    if keys[pygame.K_z]:
        draw_zoning()
    
    # Draws the buildings from the building list
    draw_buildings()

    # Draw an image of the selected building at the mouses location, this will be where the building will be built on clicking left mouse button
    draw_mouse_brush()
    
    # Icon to show which tile mouse is currently over
    #draw_particle()
    draw_cursor()

    # Draws the construction bar on the right hand side of the screen
    draw_building_ui()

    # Draws the turn timer bar at the top of the screen
    draw_turn_bar()

    # Draws the inventory if 'i' is pressed
    if keys[pygame.K_i]:
        draw_inventory_dislay()

    # Draws text on screen
    draw_text()
    return

def update_game_start():
    global keys
    
    if keys[pygame.K_SPACE]:
        custom_game_reset()
        set_game_state("running")
    return

def draw_game_start():
    global title_font
    global screen

    rendered_text = title_font.render("Press Space to Start", 1, (255,255,255))
    shadow_text = title_font.render("Press Space to Start", 1, (0, 0, 0))

    position = rendered_text.get_rect()
    position.center = screen.get_rect().center
    screen.blit(shadow_text, position.move((5,5)))
    screen.blit(rendered_text, position)
    return

####################################################
#   Game 'Engine'
#   -----------
#
#   Reusable code for lots of basic games
#
#   YOU DON'T NEED TO CHANGE ANYTHING AFTER HERE
#
#   BUT DO READ IT :)
#
####################################################


def game_init():
    """
    Perform global initialisation
    """
    global screen
    global clock
    global keys, last_keys
    global game_state_dict
    global current_game_state
    global background_surface

    # Initialise pygame
    pygame.init()
    
    # Screen
    # Size according to a background image or explicit size if 
    # specified as globals already
    if "background_image_path" in globals():
        background_surface = pygame.image.load(background_image_path)
        screen = pygame.display.set_mode(background_surface.get_size(), pygame.FULLSCREEN)
    elif "screen_size" in globals():
        screen = pygame.display.set_mode(screen_size)
    else:
        screen = pygame.display.set_mode((960,540))
    
    # Take a copy of the initial key states
    # and store it for comparison later in the update function
    keys = pygame.key.get_pressed()
    last_keys = keys

    # Clock is used to regulate game speed
    clock = pygame.time.Clock()

    # Iniatialise the gamestates lookup data
    game_state_dict = {}
    current_game_state = {}

    # If a custom init function has been defined, call it now
    if "custom_game_init" in globals():
        custom_game_init()

    # Right, lets go!
    return game_run()

def game_run():
    """
    The main gameloop cycle
    """
    # Call custom reset function, if defined
    if "custom_game_reset" in globals():
        custom_game_reset()

    # Loop game-state input, update, draw functions 
    while True:
        game_input()
        game_update()
        game_draw()
    return

def game_input():
    """
    Fill the keys list with the
    currently pressed keys
    and check for quit
    """
    global keys
    global last_keys

    last_keys = keys
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    return

def add_game_state(name, update_function_name, draw_function_name):
    """
    Create a new gamestate data entry dictionary
    Add it to the gamestate dictionary using the
    gamestate name as key
    """
    global game_state_dict

    if update_function_name in globals() and draw_function_name in globals():
        game_state = {
            "update_function":update_function_name,
            "draw_function":draw_function_name
        }
        game_state_dict[name] = game_state
        return True
    else:
        print("game state functions do not exist.")
        return False

def set_game_state(state_name):
    """
    Sets the global current_game_state by name
    Return True if successful
    """
    global game_state_dict
    global current_game_state

    if state_name in game_state_dict:
        current_game_state = game_state_dict[state_name]
        return True
    else:
        print("The state name requested could not be found.")
        return False

def game_update():
    """
    Update the game data
    by calling the current game state's
    update function
    """
    global game_state_dict
    global current_game_state

    if current_game_state:
        globals()[current_game_state["update_function"]]()

    return

def game_draw():
    """
    Draw to the screen
    by calling the current game state's
    draw function
    """
    global screen
    global clock
    global game_state_dict
    global current_game_state

    # Clear the screen
    screen.fill([127, 127, 127])

    if current_game_state:
        globals()[current_game_state["draw_function"]]()

    # Update the display to the screen
    pygame.display.flip()

    # Delay until time for next frame
    clock.tick(30)
    return

# Python cleverness to allow this file to
# be used as a module or executed directly
if __name__ == "__main__":
    game_init()
