import pygame, sys, math

GREEN = pygame.Color(26, 79, 85)
pygame.init()


ball_sprite = pygame.image.load("menu.png")

time = 0
max_time = 160

#########################################


####Size####
#  the resolution of the screen and dots   #
size = 512
menu_width = 418

# function for your dots #

def function(t):
    x = t / max_time




    return x * menu_width



########################################

screen = pygame.display.set_mode((size, size))

menuVisible = False
noEvents = True

while True:
    pygame.time.Clock().tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if noEvents:
                noEvents = False
                menuVisible = not menuVisible
        else:
            noEvents = True

    x = function(time) - menu_width

    if menuVisible and time < max_time:
        if x < 0:
            time = time + 1
    if not menuVisible and time > 0:
        if x > -menu_width:
            time = time - 1

    screen.fill((26, 79, 85))
    # pygame.draw.lines(screen, (0,255,0), False, dots)
    pygame.draw.line(screen, GREEN, (0, size / 2), (size, size / 2), 1)
    screen.blit(ball_sprite, (x, 0))
    pygame.display.flip()