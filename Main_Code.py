import pygame, random, sys
from pygame.locals import *

# Setting globals.
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
BLACKTEXT = (0, 0, 0)
WHITEBACKGROUND = (255, 255, 255)
FPS = 40
BLOCKMINSIZE = 11 
BLOCKMAXSIZE = 40
BLOCKMINSPEED = 1
BLOCKMAXSPEED = 7
ADDNEWBLOCKRATE = 10
PLAYERMOVERATE = 5
BULLETSPEED = 15
FIRINGRATE = 10
BULLETPOWER = 8

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing escape quits
                    terminate()
                if event.key == K_SPACE:
                    return

def ifBulletHitBlock(bulletRect, blocks):
    for i in blocks:
        if bulletRect.colliderect(i['rect']):
            i['rect'].size = (i['rect'].size[0] - BULLETPOWER, i['rect'].size[1] - BULLETPOWER) # Resize the block
            (i['rect'].x, i['rect'].y) = (i['rect'].x + (BULLETPOWER / 2), i['rect'].y + (BULLETPOWER / 2))  # Re-center the block
            if i['rect'].size > (15,  15): # If the block is bigger than 15x15 pixels:
                i['surface'] = pygame.transform.scale(blockImage, (i['rect'].size[0] - 8, i['rect'].size[1] - 8)) # Update the image of the block
                                                                                                                  # to the correct pixel size.     
            else: # Else the block is too small to be shoot at accurately
                blocks.remove(i) # Remove the rock from the list this would cause the rock to disappear from the screen
                
def playerHasHitBlock(playerRect, blocks):
    for i in blocks:
        if playerRect.colliderect(i['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, BLACKTEXT)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def drawCenteredText(text, font, surface, x, y):
    textobj = font.render(text, 1, BLACKTEXT)
    textrect = textobj.get_rect()
    x = (x - textrect.width) / 2
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Set up pygame, the window.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Falling Blocks')

# Set up fonts.
bigFont = pygame.font.SysFont(None, 48)
smallFont = pygame.font.SysFont(None, 30)

# Set up images.
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
blockImage = pygame.image.load('block.png')
bulletImage = pygame.image.load('bullet.png')

# Show the "Start" screen.
windowSurface.fill(WHITEBACKGROUND)
drawCenteredText('Falling Blocks:', bigFont, windowSurface, (WINDOWWIDTH), (WINDOWHEIGHT / 3))
drawCenteredText('Use arrow keys to move', smallFont, windowSurface, (WINDOWWIDTH), (WINDOWHEIGHT / 3) + 40)
drawCenteredText('Shooting blocks will make them smaller', smallFont, windowSurface, (WINDOWWIDTH), (WINDOWHEIGHT / 3) + 70)
drawCenteredText('Press SPACE to start...', smallFont, windowSurface, (WINDOWWIDTH), (WINDOWHEIGHT / 3) + 100)
pygame.display.update()
waitForPlayerToPressKey()


inFile = open("topScore.txt", "r")
topScore = inFile.readline().strip()
topScore = int(topScore)
inFile.close()

while True:
    # Set up the start of the game.
    blocks = []
    bullets = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 300)
    moveLeft = moveRight = moveUp = moveDown = False
    blockAddCounter = 0
    bulletCounter = 0
    timeCounter = 0

    while True: # the game loop runs while the game part is playing
        score += 1 # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    moveLeft = True
                if event.key == K_RIGHT:
                    moveRight = True
                if event.key == K_UP:
                    moveUp = True
                if event.key == K_DOWN:
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False

        # Add new rocks at the top of the screen, if needed.
        blockAddCounter += 1
        timeCounter += 1  
        if blockAddCounter >= ADDNEWBLOCKRATE:
            blockAddCounter = 0
            blockSize = random.randint(BLOCKMINSIZE, BLOCKMAXSIZE)
            newblock = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - blockSize), 0 - blockSize, blockSize, blockSize),
                        'speed': random.randint(BLOCKMINSPEED, BLOCKMAXSPEED),
                        'surface': pygame.transform.scale(blockImage, (blockSize, blockSize)),
                        }

            blocks.append(newblock)
            
        # Increase rock speed and spawn rate every 5 seconds.
        # Also increases FIRINGRATE to help player survival rate.
        if timeCounter == FPS * 5:
            timeCounter = 0
            BLOCKMINSPEED += 1
            BLOCKMAXSPEED += 1
            BLOCKMINSIZE += 5
            BLOCKMAXSIZE += 5
            if ADDNEWBLOCKRATE > 2:
                ADDNEWBLOCKRATE -= 1
            if FIRINGRATE > 5:
                FIRINGRATE -= 1
        
        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Make new bullets constantly.
        bulletCounter += 1
        if bulletCounter >= FIRINGRATE:
            bulletCounter = 0
            newBullet = {'rect': pygame.Rect(playerRect.left + 8, playerRect.top, 4, 12),
                         'speed': BULLETSPEED,
                         'surface': pygame.transform.scale(bulletImage, (4, 12)),
                        }
            bullets.append(newBullet)
        
        # Move blocks down.
        for i in blocks:
            i['rect'].move_ip(0, i['speed'])

        # Fire bullets.
        for bullet in bullets:
            bullet['rect'].move_ip(0, -bullet['speed'])

        # Delete rocks that have fallen past the bottom.
        for b in blocks[:]:
            if i['rect'].top > WINDOWHEIGHT:
                rocks.remove(i)

        # Delete bullets that reaches the top of screen
        for bullet in bullets[:]:
            if bullet['rect'].bottom < 0:
                bullets.remove(bullet)

        # Draw the game world on the window.
        windowSurface.fill(WHITEBACKGROUND)

        # Draw the score and top score.
        drawText('Score: %s' % (score), bigFont, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), bigFont, windowSurface, 10, 40)

        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

        # Draw each block
        for i in blocks:
            windowSurface.blit(i['surface'], i['rect'])

        # Draw bullets
        for bullet in bullets:
            windowSurface.blit(bullet['surface'], bullet['rect'])
            
        pygame.display.update()

        # Check if bullet hit blocks
        for bullet in bullets:
            ifBulletHitBlock(bullet['rect'], blocks)

        # Check if any of the blocks have hit the player.
        if playerHasHitBlock(playerRect, blocks):
            if score > topScore:
                topScore = score # set new top score
                outFile = open("topScore.txt", "w")
                print(topScore, file = outFile)
                outFile.close()
            break           
            
        pygame.display.update()
        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    windowSurface.fill(WHITEBACKGROUND)
    drawCenteredText('GAME OVER', bigFont, windowSurface, WINDOWWIDTH, (WINDOWHEIGHT / 3))
    drawCenteredText('Your score is: %s' % score, bigFont, windowSurface, WINDOWWIDTH, (WINDOWHEIGHT / 3) + 35)
    drawCenteredText('Press SPACE to play again', smallFont, windowSurface, WINDOWWIDTH, (WINDOWHEIGHT / 3) + 70)
    drawCenteredText('Press ESC to quit', smallFont, windowSurface, WINDOWWIDTH, (WINDOWHEIGHT / 3) + 95)
    pygame.display.update()
    waitForPlayerToPressKey()

    # Resets globals before new game
    timeCounter = 0
    BLOCKMINSIZE = 10
    BLOCKMAXSIZE = 40
    BLOCKMINSPEED = 1
    BLOCKMAXSPEED = 7
    ADDNEWBLOCKRATE = 10
    FIRINGRATE = 10
