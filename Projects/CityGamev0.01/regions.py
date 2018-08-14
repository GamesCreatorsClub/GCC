import sys, pygame, random

def print_map(lst):
    print("#######################")
    for line in lst:
        print(line)
    print("#######################")
    
def create_blank_map(mapx,mapy):
    lst = []
    for y in range(mapy):
        lst2 = []
        for x in range(mapx):
            lst2.append(0)
        lst.append(lst2)
    return lst

def pick_start_locations(mapx,mapy,lst,width,height,regions):
    start_location = []
    for row in range(mapy//height):
        for col in range(mapx//width):
            lowerx = width*col
            upperx = (width*(col+1)) - 1
            
            lowery = height*row
            uppery = (height*(row+1)) - 1
            x = random.randint(lowerx,upperx)
            y = random.randint(lowery,uppery)
            xy = (x,y)
            start_location.append(xy)

    for i in range(len(start_location)):
        x = start_location[i][0]
        y = start_location[i][1]
        lst[y][x] = i + 1
    return lst


def change_surrounding(j,i,lst,region,mapx,mapy):
    if (i-1) >= 0 and lst[j][i-1] == 0:
        lst[j][i-1] = (region+1)*100
    if (i+1) < mapx and lst[j][i+1] == 0:
        lst[j][i+1] = (region+1)*100
    if (j-1) >= 0 and lst[j-1][i] == 0:
        lst[j-1][i] = (region+1)*100
    if (j+1) < mapy and lst[j+1][i] == 0:
        lst[j+1][i] = (region+1)*100

def expand_start_locations(mapx,mapy,lst,regions):
    incomplete = True
    k = 0
    while incomplete:
        
        for j in range(mapy):
            for i in range(mapx):
                for region in range(regions):
                    if lst[j][i] == region+1:
                        if random.random() <= 0.7:
                            change_surrounding(j,i,lst,region,mapx,mapy)                   
                    
        for j in range(mapy):
            for i in range(mapx):
                for region in range(regions):
                    if lst[j][i] == (region+1)*100:
                        lst[j][i] = (region+1)

        unassigned_tiles = 0                
        for j in range(mapy):
            for i in range(mapx):
                if lst[j][i] == 0:
                    unassigned_tiles += 1
        if unassigned_tiles == 0:
            incomplete = False
        k +=1
    print(k)
    return lst

def region_generator(mapx,mapy,regions):
    width = 32
    height = 32
    lst = create_blank_map(mapx,mapy)
    lst2 = pick_start_locations(mapx,mapy,lst,width,height,regions)
    lst3 = expand_start_locations(mapx,mapy,lst2,regions)
    print("load successful")
    return lst3
