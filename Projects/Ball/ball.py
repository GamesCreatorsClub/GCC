import pygame, sys, math

GREEN = pygame.Color("green")
pygame.init()


ball_sprite = pygame.image.load("ball.png")

#########################################



####Size####
#  the resolution of the screen and dots   #
size = 512

# function for your dots #

def function(x):
    y = 0
    x = x % size

    y = math.sin(x / 20) * 100
    if y < 0:
        y = -y

    return (x, y)



########################################

screen = pygame.display.set_mode((size, size))

x = 0

while True:
    pygame.time.Clock().tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    coordinates = function(x)
    coordinates = (coordinates[0], size / 2 - coordinates[1] - ball_sprite.get_height())
    x = x + 1

    screen.fill((0, 0, 0))
    # pygame.draw.lines(screen, (0,255,0), False, dots)
    pygame.draw.line(screen, GREEN, (0, size / 2), (size, size / 2), 1)
    screen.blit(ball_sprite, coordinates)
    pygame.display.flip()