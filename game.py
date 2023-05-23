# import modules
import pygame
import sys
import random
import math
from pygame import mixer

# initialise pygame
pygame.init()

# create game screen
screen = pygame.display.set_mode((800,600))

# screen title and icon
pygame.display.set_caption('SPACE INVADERS')
icon = pygame.image.load('F:\\Vinaya\\Python Projects\\Space Invaders\media\\icon.png')
pygame.display.set_icon(icon)

# screen background
BackgroundImg = pygame.image.load('F:\\Vinaya\\Python Projects\\Space Invaders\\media\\background.png')

# background music
mixer.music.load('F:\\Vinaya\\Python Projects\\Space Invaders\\media\\background.wav')
mixer.music.play(-1)

BulletSound = mixer.Sound('F:\\Vinaya\\Python Projects\\Space Invaders\\media\\laser.wav')
CollisionSound = mixer.Sound('F:\\Vinaya\\Python Projects\\Space Invaders\\media\\explosion.wav')

# player
PlayerImg = pygame.image.load('F:\\Vinaya\\Python Projects\\Space Invaders\\media\\player.png')
PlayerX = 370
PlayerY = 480
PlayerChangeX = 0
PlayerChangeY = 0

def player(x,y):
    screen.blit(PlayerImg, (x,y))

# enemy
NumEnemy = 6

EnemyImg = pygame.image.load('F:\\Vinaya\\Python Projects\\Space Invaders\\media\\enemy.png')
EnemyX = []
EnemyY = []
EnemyChangeX = []
EnemyChangeY = []

for x in range(NumEnemy):
    EnemyX.append(random.randint(0,736))
    EnemyY.append(random.randint(10, 50))
    EnemyChangeX.append(4)
    EnemyChangeY.append(40)

def enemy(x,y):
    screen.blit(EnemyImg, (x,y))

# bullet
BulletImg = pygame.image.load('F:\\Vinaya\\Python Projects\\Space Invaders\\media\\bullet.png')
BulletX = 0
BulletY = 480
BulletChangeX = 0
BulletChangeY = 10

# when BulletState = False, bullet not visible on screen
# when BulletState = True, bullet visible on screen
BulletState = False 

def bullet(x,y):
    screen.blit(BulletImg, (x + 16, y + 10))

# score

score_font = pygame.font.Font('freesansbold.ttf', 32)

score_val = 0

ScoreX = 10
ScoreY = 10

def ShowScore(x,y):
    score = score_font.render('SCORE :'+str(score_val), True, (255, 255, 255))
    screen.blit(score, (x,y))
    
# collision betn bullet and enemy
def collision(Ex, Ey, Bx, By):
    for i in range(NumEnemy):
        dist = math.hypot(Ex - Bx, Ey - By)
        if dist < 27:
            return True
        else:
            return False

# game over

OverX = 200
OverY = 250

over_font = pygame.font.Font('freesansbold.ttf', 64)
GameOver = over_font.render('GAME OVER', True, (225, 0, 0))

def DispGameOver(x,y):
    screen.blit(GameOver, (x,y))
# main loop
while True:

    # check event
    for event in pygame.event.get():
        
        # loop exit condition
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
        if event.type == pygame.KEYDOWN:
            
            # player key press
            if event.key == pygame.K_LEFT:
                PlayerChangeX = -5
            elif event.key == pygame.K_RIGHT:
                PlayerChangeX = 5
                
            # bullet key press
            if event.key == pygame.K_SPACE:

                if not BulletState: 

                    BulletX = PlayerX
                    BulletState = True

                    BulletSound.play()
                            
    # screen background solid
    screen.fill((70, 130, 180))

    #screen background image
    screen.blit(BackgroundImg, (0,0))

    # player movement
    PlayerX += PlayerChangeX

    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736

    # enemy movement
    for i in range(NumEnemy):

        # game over
        if EnemyY[i] > 440:
            for j in range(NumEnemy):
                EnemyY[j] = 2000
                
            DispGameOver(OverX, OverY)
                        
            break
        
        EnemyX[i] += EnemyChangeX[i]
    
        if EnemyX[i] <= 0:
            EnemyChangeX[i] = 4
            EnemyY[i] += EnemyChangeY[i]
            
        elif EnemyX[i] >= 736:
            EnemyChangeX[i] = -4
            EnemyY[i] += EnemyChangeY[i]

        # collision betn bullet and enemy
        collide = collision(EnemyX[i], EnemyY[i], BulletX, BulletY)
    
        if collide:
            CollisionSound.play()
        
            BulletState = False
            BulletX = 0
            BulletY = 480

            EnemyX[i] = random.randint(0,736)
            EnemyY[i] = random.randint(10, 50)

            score_val += 1

        # call enemy
        enemy(EnemyX[i], EnemyY[i])

    # bullet movement
    if BulletState:
        bullet(BulletX, BulletY)
        BulletY -= BulletChangeY

    if BulletY <= 0:
        BulletState = False
        BulletX = 0
        BulletY = 480

    # call player
    player(PlayerX, PlayerY)

    # display score
    ShowScore(ScoreX, ScoreY)

    # screen update
    pygame.display.update()
