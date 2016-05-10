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
