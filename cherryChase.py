from random import randrange
import pygame
pygame.init()
_gameWidth = 500
_gameHeight = 500
score = 0 
win = pygame.display.set_mode((_gameWidth, _gameHeight))
pygame.display.set_caption("Cherry Chase")
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
blue = (0, 0, 100)
playerX = 50
playerY = 50
health = 100
_blockages = []

def removeOldPlayer(playerX, playerY, playerWidth, playerHeight):
    pygame.draw.rect(win, (0, 0, 0), (playerX, playerY, playerWidth, playerHeight))

def collisionCheck(cherries, playerX, playerY, foodWidth, foodHeight):
    if len(cherries) > 0:
        for cherry in cherries:
            cherryX = cherry[0]
            cherryXLowerBound = cherryX - (foodWidth // 2)
            cherryXUpperBound = cherryX + foodWidth
            xCollision = playerX < cherryXUpperBound and playerX >= cherryXLowerBound

            cherryY = cherry[1]
            cherryYLowerBound = cherryY - (foodHeight // 2)
            cherryYUpperBound = cherryY + foodHeight
            yCollision = playerY < cherryYUpperBound and playerY >= cherryYLowerBound
            if xCollision and yCollision:
                pygame.draw.rect(win, (0, 0, 0), (cherryX, cherryY, foodWidth, foodHeight))
                cherries.remove(cherry)
                return True

    return False

def spawnFood(cherries, foodWidth, foodHeight):
    foodX = randrange(_gameWidth-foodWidth)
    foodY = randrange(_gameHeight-foodHeight-10)+10
    pygame.draw.rect(win, red, (foodX, foodY, foodWidth, foodHeight))
    cherries.append((foodX, foodY))

def spawnBlockage():
    x = 0
    y = 10
    for i in range(1000):
        randomBlockageType = randrange(0,25)
        if randomBlockageType > 0 and randomBlockageType < 5:
            spawnLeftCornerBlockage(x, y)
        if  randomBlockageType > 5 and randomBlockageType < 10:
            spawnRightCornerBlockage(x, y)
        if randomBlockageType > 10 and randomBlockageType < 15:
            spawnLongVerticalLineBlockage(x, y)
        if randomBlockageType > 15 and randomBlockageType < 21:
            spawnLongHorizontalLineBlockage(x, y)
        # leaving a gap from 21 -> 25
        
        x += 50
        if x >= _gameWidth:
            x = 0
            y += 50
        if y >= _gameHeight:
            print(i)
            return

def spawnVerticalLineBlockage(x, y):
    global _blockages
    width = 10
    height = 30
    pygame.draw.rect(win, blue, (x, y, width, height))
    _blockages.append((x, y, width, height))

def spawnLongVerticalLineBlockage(x, y):
    spawnVerticalLineBlockage(x, y)
    spawnVerticalLineBlockage(x, y + 30)

def spawnHorizontalLineBlockage(x, y):
    global _blockages
    width = 30
    height = 10
    pygame.draw.rect(win, blue, (x, y, width, height))
    _blockages.append((x, y, width, height))

def spawnLongHorizontalLineBlockage(x, y):
    spawnHorizontalLineBlockage(x, y)
    spawnHorizontalLineBlockage(x + 30, y)

def spawnLeftCornerBlockage(x, y):
    random = randrange(0, 2)
    if random == 0:
        spawnTopLeftCornerBlockage(x, y)
    if random == 1:
        spawnBottomLeftCornerBlockage(x, y)

def spawnTopLeftCornerBlockage(x, y):
    random = randrange(0, 100)
    if random > 0 and random < 20:
        spawnHorizontalLineBlockage(x, y)
        spawnVerticalLineBlockage(x, y)
    if random > 20 and random < 60:
        spawnLongHorizontalLineBlockage(x, y)
        spawnVerticalLineBlockage(x, y)
    if random > 60 and random < 100:
        spawnHorizontalLineBlockage(x, y)
        spawnLongVerticalLineBlockage(x, y)

def spawnBottomLeftCornerBlockage(x, y):
    random = randrange(0, 100)
    if random > 0 and random < 20:
        spawnHorizontalLineBlockage(x, y + 20)
        spawnVerticalLineBlockage(x, y)
    if random > 20 and random < 60:
        spawnLongHorizontalLineBlockage(x, y + 20)
        spawnVerticalLineBlockage(x, y)
    if random > 60 and random < 100:
        spawnHorizontalLineBlockage(x, y + 50)
        spawnLongVerticalLineBlockage(x, y)

def spawnRightCornerBlockage(x, y):
    random = randrange(0, 2)
    if random == 0:
        spawnTopRightCornerBlockage(x, y)
    if random == 1:
        spawnBottomRightCornerBlockage(x, y)

def spawnTopRightCornerBlockage(x, y):
    random = randrange(0, 100)
    if random > 0 and random < 20:
        spawnHorizontalLineBlockage(x, y)
        spawnVerticalLineBlockage(x + 20, y)
    if random > 20 and random < 60:
        spawnLongHorizontalLineBlockage(x, y)
        spawnVerticalLineBlockage(x + 50, y)
    if random > 60 and random < 100:
        spawnHorizontalLineBlockage(x, y)
        spawnLongVerticalLineBlockage(x + 20, y)

def spawnBottomRightCornerBlockage(x, y):
    random = randrange(0, 100)
    if random > 0 and random < 20:
        spawnHorizontalLineBlockage(x, y + 20)
        spawnVerticalLineBlockage(x + 20, y)
    if random > 20 and random < 60:
        spawnLongHorizontalLineBlockage(x, y + 20)
        spawnVerticalLineBlockage(x + 50, y)
    if random > 60 and random < 100:
        spawnHorizontalLineBlockage(x, y + 50)
        spawnLongVerticalLineBlockage(x + 20, y)       

def validMove(playerX, playerY):
    global _blockages
    # globalize player width & height
    playerWidth = 5
    playerHeight = 5 

    # might be better to create a dictionary of blockages. faster look-up
    for blockage in _blockages:
        print("blockage: ", blockage)
        blockageXLowerBound = blockage[0]
        blockageXUpperBound = blockageXLowerBound + blockage[2]
        xCollision = playerX + playerWidth - 1 >= blockageXLowerBound and playerX < blockageXUpperBound
        print("x's lower:%s upper:%s" % (blockageXLowerBound, blockageXUpperBound))
        blockageYLowerBound = blockage[1]
        blockageYUpperBound = blockageYLowerBound + blockage[3]
        yCollision = playerY >= blockageYLowerBound and playerY <= blockageYUpperBound
        print("y's lower:%s upper:%s" % (blockageYLowerBound, blockageYUpperBound))

        if xCollision and yCollision:
            print("should not be able allowed %s,%s" % (playerX, playerY))
            return False
        
    return True

def checkPlayerMovement(cherries, foodWidth, foodHeight, playerWidth, playerHeight):
    global playerX
    global playerY
    global health
    step = 5
    cherryEaten = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if validMove(playerX, playerY - step):
            if playerY > step:
                playerY -= step
                cherryEaten = collisionCheck(cherries, playerX, playerY, foodWidth, foodHeight)
    if keys[pygame.K_DOWN]:
        if validMove(playerX, playerY + step):
            if playerY < _gameHeight - playerHeight:
                playerY += step
                cherryEaten = collisionCheck(cherries, playerX, playerY, foodWidth, foodHeight)
    if keys[pygame.K_LEFT]:
        if validMove(playerX - step, playerY):
            if playerX > step:
                playerX -= step
                cherryEaten = collisionCheck(cherries, playerX, playerY, foodWidth, foodHeight)
    if keys[pygame.K_RIGHT]:
        if validMove(playerX + step, playerY):
            if playerX < _gameWidth - playerWidth:
                playerX += step
                cherryEaten = collisionCheck(cherries, playerX, playerY, foodWidth, foodHeight)        
    if cherryEaten:
        if health < 75:
            health += 25
        else:
            health = 100 
        # speed = speed * 1.1, if this is enabled we need to speed up food drop. Else impossible
    pygame.draw.rect(win, (255, 255, 255), (playerX, playerY, playerWidth, playerHeight))
    
def drawHealthBar():
    global health
    health -= 0.25
    healthBarWidth = 100
    pygame.draw.rect(win, red, (_gameWidth - healthBarWidth, 0, healthBarWidth, 10))
    pygame.draw.rect(win, green, (_gameWidth - healthBarWidth, 0, health, 10)) 

def endGameCheck():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def gameLoop():
    run = True

    global playerX
    global playerY
    global health
    playerWidth = 5
    playerHeight = 5
    foodWidth = 10
    foodHeight = 10
    foodDropWait = 150
    foodDropCountdown = 0
    cherries = []

    spawnBlockage()

    while run:   
        pygame.time.wait(50)
        drawHealthBar()

        run = endGameCheck()

        if foodDropCountdown <= 1:
            foodDropCountdown = foodDropWait
            spawnFood(cherries, foodWidth, foodHeight)
        foodDropCountdown -= 1

        removeOldPlayer(playerX, playerY, playerWidth, playerHeight)
        checkPlayerMovement(cherries, foodWidth, foodHeight, playerWidth, playerHeight)
        
        # draw updates
        pygame.display.update()

gameLoop()
pygame.quit()
quit()

#   TODO:
#       1) (DONE) Change score into health bar
#       2) (DONE) Lower the health as the game runs. So that the player needs to "eat" cherries to survive
#       3) (DONE) Build a blockage type structure
#       4) Place blockages to form a maze type scenario
#       5) Check collision on maze tpye scenario
#       5) Other people also try eat teh cherries
# 
# 
# 
# 
# 
# 
