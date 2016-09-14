#here we import pygame and sys
import pygame, sys, random, math

PLAYER_SPEED = 4
ENEMY_SPEED = 2
BULLET_SPEED = 4
GUN_COOLDOWN = 40
NEXT_ENEMY_TIME_MIN = 130
NEXT_ENEMY_TIME_MAX = 190

GAME_STATE_MENU = 0
GAME_STATE_GAME = 1
GAME_STATE_END = 2

pygame.init()
clock = pygame.time.Clock()

smallFont = pygame.font.SysFont("apple casual", 32)
bigFont = pygame.font.SysFont("apple casual", 48)

#here we have the variables
screenRect = pygame.Rect(0, 0, 480, 768)
screen = pygame.display.set_mode(screenRect.size)

playerSprite = pygame.image.load("player.png")
enemySprite = pygame.image.load("enemy.png")
bulletSprite = pygame.image.load("bullet.png")

starSprite1 = pygame.image.load("star1.png")
starSprite2 = pygame.image.load("star2.png")
starSprite3 = pygame.image.load("star3.png")
starSprite4 = pygame.image.load("star4.png")

playerPosition = pygame.Rect(playerSprite.get_rect())
playerPosition.move_ip(screenRect.width / 2, screenRect.height - playerSprite.get_height())
player = {
    "pos" : playerPosition,
    "sprite" : playerSprite
}

key = []

bullets = []
enemies = []
background = []

level = 1
score = 0
highScore = 0
gun_heat = 0
time_to_next_enemy = NEXT_ENEMY_TIME_MIN


scoreRect = pygame.Rect(screenRect.width - 180, 5, 64, 64)
highScoreRect = pygame.Rect(20, 5, 64, 64)
levelRect = pygame.Rect(screenRect.width / 2 - 100, screenRect.top / 2 - 15, 64, 64)

game_state = GAME_STATE_MENU

def resetGame():
    global gun_heat, game_state, score

    bullets.clear()
    enemies.clear()
    playerPosition = pygame.Rect(playerSprite.get_rect())
    playerPosition.move_ip(screenRect.width / 2, screenRect.height - playerSprite.get_height())
    player["pos"] = playerPosition
    gun_heat = 10
    game_state = GAME_STATE_GAME
    scone = 0

def drawTextBig(s, x, y):
    global bigFont
    text = bigFont.render(s, 1, (255, 255, 255))
    screen.blit(text, pygame.Rect(x, y, 0, 0))

def drawTextSmall(s, x, y):
    global smallFont
    text = smallFont.render(s, 1, (255, 255, 255))
    screen.blit(text, pygame.Rect(x, y, 0, 0))


def drawScore():
    global smallFont, score, screen, scoreRect, highScoreRect
    text = smallFont.render("High Score: " + str(highScore), 1, (255, 255, 255))
    screen.blit(text, highScoreRect)
    text = smallFont.render("Score: " + str(score), 1, (255, 255, 255))
    screen.blit(text, scoreRect)

def drawLevel():
    global bigFont, level, screen, levelRect, highScoreRect
    text = bigFont.render("Level " + str(level), 1, (255, 255, 255))
    screen.blit(text, levelRect)

def drawObject(o):
    screen.blit(o["sprite"], o["pos"])

def drawObjects(a):
    for o in a:
        drawObject(o)

def createBackgrond():
    for i in range(100):
        r = random.randint(0, 20)
        if r < 14:
            sprite = starSprite1
        elif r < 17:
            sprite = starSprite2
        elif r < 19:
            sprite = starSprite4
        else:
            sprite = starSprite3

        x = random.randint(0, screenRect.width)
        y = random.randint(0, screenRect.height)
        rect = pygame.Rect(x, y, 16, 16)
        speedDistribution = random.randint(0, 10)
        if (speedDistribution < 6):
            speed = (0, 1)
        elif (speedDistribution < 9):
            speed = (0, 2)
        else:
            speed = (0, 3)

        backgroundObject = {
            'sprite': sprite,
            'pos': rect,
            'speed': speed
        }
        background.append(backgroundObject)


def addBullet(where):
    global gun_heat

    bullet = {
        "pos": pygame.Rect(
            where.x + (where.width - bulletSprite.get_width()) / 2,
            where.y,
            bulletSprite.get_width(), bulletSprite.get_width()),
        "sprite" : bulletSprite,
        "direction": (0, -BULLET_SPEED)
    }
    bullets.append(bullet)
    gun_heat = GUN_COOLDOWN

def addEnemy():
    x = random.randint(0, screenRect.width - enemySprite.get_width())
    enemy = {
        "pos" : pygame.Rect(x, 0, enemySprite.get_width(), enemySprite.get_height()),
        "sprite" : enemySprite
    }
    enemies.append(enemy)

def movePlayer():
    global game_state, highScore

    if key[pygame.K_LEFT] and player["pos"].left > 0:
        player["pos"].move_ip(-PLAYER_SPEED, 0)
    if key[pygame.K_RIGHT] and player["pos"].right < screen.get_width() - 1:
        player["pos"].move_ip(PLAYER_SPEED, 0)
    if key[pygame.K_SPACE] and gun_heat == 0:
        addBullet(player["pos"])

    e = collideWithEnemies(player["pos"])
    if e >= 0:
        if highScore < score:
            highScore = score
        game_state = GAME_STATE_END

def moveBackground():
    for backgroundObject in background:
        s = backgroundObject["speed"]
        backgroundObject["pos"].move_ip(s)
        if not screenRect.colliderect(backgroundObject["pos"]):
            backgroundObject["pos"].y = -backgroundObject["sprite"].get_height()

def enemyFunction(x, y):

    y = y + 1


    return (x, y)



def moveEnemies():
    for i in range(len(enemies) - 1, -1, -1):
        enemy = enemies[i]
        nextPosition = enemyFunction(enemy["pos"].x, enemy["pos"].y)
        enemy["pos"].x = nextPosition[0]
        enemy["pos"].y = nextPosition[1]

def collideWithEnemies(r):
    i = 0
    for e in enemies:
        if e["pos"].colliderect(r):
            return i
        i = i + 1
    return -1

def moveBullets():
    global score

    for i in range(len(bullets) - 1, -1, -1):
        b = bullets[i]
        b["pos"].move_ip(b["direction"])
        if not screenRect.colliderect(b["pos"]):
            del bullets[i]
        else:
            e = collideWithEnemies(b["pos"])
            if e >= 0:
                del enemies[e]
                del bullets[i]
                score = score + 50

resetGame()
createBackgrond()
game_state = GAME_STATE_MENU

while True:
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()

    key = pygame.key.get_pressed() 
    if key[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    if game_state == GAME_STATE_GAME:

        if gun_heat > 0:
            gun_heat = gun_heat - 1

        if time_to_next_enemy <= 0:
            addEnemy()
            time_to_next_enemy = random.randint(NEXT_ENEMY_TIME_MIN, NEXT_ENEMY_TIME_MAX)

        time_to_next_enemy = time_to_next_enemy - 1

        movePlayer()
        moveEnemies()
        moveBullets()
    else:
        if key[pygame.K_SPACE]:
            resetGame()


    moveBackground()

    screen.fill((0, 0, 0))
    drawScore()

    drawObjects(background)
    drawObject(player)
    drawObjects(enemies)
    drawObjects(bullets)

    if game_state == GAME_STATE_MENU or game_state == GAME_STATE_END:
        if game_state == GAME_STATE_END:
            drawTextBig("Oh, no, you've lost!", 80, screenRect.height / 2 - 100)

        drawTextBig("Press SPACE to start", 80, screenRect.height / 2)


    pygame.display.flip()

    clock.tick(60)
    

