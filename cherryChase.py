from random import randrange
import pygame
import numpy as np

pygame.init()
_gameWidth = 500
_gameHeight = 500
win = pygame.display.set_mode((_gameWidth, _gameHeight))
pygame.display.set_caption("Cherry Chase")
_grid = np.zeros(250000).reshape(500, 500)

red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
blue = (0, 0, 100)

_playerX = 0
_playerY = 0
_health = 100
_blockage = 1
_cherries = []
_cherryWidth = 10
_cherryHeight = 10


def removeOldPlayer(playerX, playerY, playerWidth, playerHeight):
    pygame.draw.rect(win, (0, 0, 0), (playerX, playerY,
                     playerWidth, playerHeight))


def collisionCheck():
    global _cherries
    global _playerX
    global _playerY
    global _cherryWidth
    global _cherryHeight

    if len(_cherries) > 0:
        for cherry in _cherries:
            cherryX = cherry[0]
            cherryXLowerBound = cherryX - (_cherryWidth // 2)
            cherryXUpperBound = cherryX + _cherryWidth
            xCollision = _playerX < cherryXUpperBound and _playerX >= cherryXLowerBound

            cherryY = cherry[1]
            cherryYLowerBound = cherryY - (_cherryHeight // 2)
            cherryYUpperBound = cherryY + _cherryHeight
            yCollision = _playerY < cherryYUpperBound and _playerY >= cherryYLowerBound
            if xCollision and yCollision:
                pygame.draw.rect(
                    win, (0, 0, 0), (cherryX, cherryY, _cherryWidth, _cherryHeight))
                _cherries.remove(cherry)
                return True

    return False


def spawnCherry():
    global _cherries
    cherryWidth = 10
    cherryHeight = 10
    cherryX = randrange(_gameWidth-cherryWidth)
    cherryY = randrange(_gameHeight-cherryHeight-10)+10

    if validCherry(cherryX, cherryY, cherryWidth, cherryHeight):
        pygame.draw.rect(win, red, (cherryX, cherryY,
                         cherryWidth, cherryHeight))
        _cherries.append((cherryX, cherryY))
    else:
        spawnCherry()


def validCherry(cherryX, cherryY, cherryWidth, cherryHeight):
    for i in range(cherryWidth):
        for j in range(cherryHeight):
            if _grid[cherryX + i][cherryY + j] != 0:
                return False
    return True


def addItemToGrid(x, y, width, height, item):
    for i in range(width):
        if x + i < _gameWidth:
            for j in range(height):
                if y + j < _gameHeight:
                    _grid[x+i][y+j] = item


def spawnBlockage():
    x = 0
    y = 10
    for i in range(1000):
        randomBlockageType = randrange(0, 25)
        if randomBlockageType > 0 and randomBlockageType < 5:
            spawnLeftCornerBlockage(x, y)
        if randomBlockageType > 5 and randomBlockageType < 10:
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
            return


def spawnVerticalLineBlockage(x, y):
    global _blockage
    width = 10
    height = 30
    pygame.draw.rect(win, blue, (x, y, width, height))
    addItemToGrid(x, y, width, height, _blockage)


def spawnLongVerticalLineBlockage(x, y):
    spawnVerticalLineBlockage(x, y)
    spawnVerticalLineBlockage(x, y + 30)


def spawnHorizontalLineBlockage(x, y):
    global _blockage
    width = 30
    height = 10
    pygame.draw.rect(win, blue, (x, y, width, height))
    addItemToGrid(x, y, width, height, _blockage)


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
    global _grid
    return _grid[playerX][playerY] == 0


def checkPlayerMovement(playerWidth, playerHeight):
    global _playerX
    global _playerY
    global _health
    step = 5
    cherryEaten = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if validMove(_playerX, _playerY - step):
            if _playerY > step:
                _playerY -= step
                cherryEaten = collisionCheck()
    if keys[pygame.K_DOWN]:
        if validMove(_playerX, _playerY + step):
            if _playerY < _gameHeight - playerHeight:
                _playerY += step
                cherryEaten = collisionCheck()
    if keys[pygame.K_LEFT]:
        if validMove(_playerX - step, _playerY):
            if _playerX > step:
                _playerX -= step
                cherryEaten = collisionCheck()
    if keys[pygame.K_RIGHT]:
        if validMove(_playerX + step, _playerY):
            if _playerX < _gameWidth - playerWidth:
                _playerX += step
                cherryEaten = collisionCheck()
    if cherryEaten:
        if _health < 75:
            _health += 25
        else:
            _health = 100
        # speed = speed * 1.1, if this is enabled we need to speed up food drop. Else impossible
    pygame.draw.rect(win, (255, 255, 255), (_playerX,
                     _playerY, playerWidth, playerHeight))


def drawHealthBar():
    global _health
    _health -= 0.25
    healthBarWidth = 100
    pygame.draw.rect(
        win, red, (_gameWidth - healthBarWidth, 0, healthBarWidth, 10))
    pygame.draw.rect(win, green, (_gameWidth - healthBarWidth, 0, _health, 10))


def endGameCheck():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def gameLoop():
    run = True

    global _playerX
    global _playerY
    global _health
    playerWidth = 5
    playerHeight = 5
    foodDropWait = 150
    foodDropCountdown = 0

    spawnBlockage()

    while run:
        pygame.time.wait(50)
        drawHealthBar()

        run = endGameCheck()

        if foodDropCountdown <= 1:
            foodDropCountdown = foodDropWait
            spawnCherry()
        foodDropCountdown -= 1

        removeOldPlayer(_playerX, _playerY, playerWidth, playerHeight)
        checkPlayerMovement(playerWidth, playerHeight)

        # draw updates
        pygame.display.update()


gameLoop()
pygame.quit()
quit()
