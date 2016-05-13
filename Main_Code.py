import pygame, random, sys
from pygame.locals import *

# Setting globals.
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0 , 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
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
                                if event.key == K_ESCAPE:
                                        terminate()
                                if event.key == K_SPACE:
                                        return

def ifBulletHitBlock(bulletRect, blocks):
        for b in blocks:
                if bulletRect.colliderect(b['rect']):
                        b['rect'].size = (b['rect'].size[0] - BULLETPOWER, b['rect'].size[1] - BULLETPOWER) # Resize the block
                        (b['rect'].x, b['rect'].y) = (b['rect'].x + (BULLETPOWER / 2), b['rect'].y + (BULLETPOWER / 2)) # Re-center the block
                if b['rect'].size > (15,  15): # If the block is bigger than 15x15 pixels:
                        b['surface'] = pygame.transform.scale(blockImage, (b['rect'].size[0] - 8, b['rect'].size[1] - 8)) # Update the image of the block
                                                                                                                          # to the correct pixel size.     
                else: # Else the block is too small to be shoot at accurately
                        blocks.remove(b) # Remove the rock from the list this would cause the rock to disappear from the screen
 
def playerHasHitBlock(playerRect, blocks):
        for b in blocks:
                if playerRect.colliderect(b['rect']):
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

# Add new blocks at the top of the screen, if needed.
        blockAddCounter += 1
        timeCounter += 1
        if blockAddCounter >= ADDNEWBLOCKRATE:
                blockAddCounter = 0
                blockSize = random.randint(BLOCKMINSIZE, BLOCKMAXSIZE)
                newBlock = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - blockSize), 0 - blockSize, blockSize, blockSize),
                        'speed': random.randint(BLOCKMINSPEED, BLOCKMAXSPEED),
                        'surface': pygame.transform.scale(blockImage, (blockSize, blockSize)),
                        }
                blocks.append(newBlock)
            
            
                
        # Increase block speed and spawn rate every 5 seconds.
        # Also increases FIRINGRATE to help survival rate
        if timeCounter == FPS * 5:
                timeCounter = 0
                BLOCKMINSPEED += 1
                BLOCKMAXSPEED += 1
                BLOCKMINSPEED += 5
                BLOCKMAXSPEED += 5
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
            
        # Move the blocks down.
        for b in blocks:
            b['rect'].move_ip(0, b['speed'])
            
        # Delete blocks that have fallen past the bottom.
        for b in blocks[:]:
            if b['rect'].top > WINDOWHEIGHT:
                blocks.remove(b)
