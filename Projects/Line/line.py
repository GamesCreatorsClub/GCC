import pygame, sys, math
pygame.init()


#########################################

####Size####
#  the resolution of the screen and dots   #
size = 512

# function for your dots #

def function(x):
    return 0

########################################

screen = pygame.display.set_mode((size, size))

dots = []
for x in range(0, size, 1):
    dots.append([x, (size / 2) + function(x)])

dots.append([size, (size / 2) + function(size)])

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    pygame.draw.lines(screen, (0,255,0), False, dots)
    pygame.display.flip()