import pygame

pygame.init()

screen = pygame.display.set_mode((600,600))

frameclock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (100, 100, 100), (20, 20, 250, 250))

    screen.blit(boxes[0],(0,0))

    pygame.display.flip()

    frameclock.tick(30)