import pygame
import random
import math
from pygame import mixer

# Initializing the game
pygame.init()

# Create screen (x axis, y axis)
screen = pygame.display.set_mode((800, 600))

# Background image
background = pygame.image.load('pngegg.png')

# Background music
mixer.music.load('background_music.wav')
mixer.music.play(-1)

# Title screen and icon
pygame.display.set_caption("Furiosa's Space Kitten Battle!")
icon = pygame.image.load('player_image.png')
pygame.display.set_icon(icon)

# Player - defining image and location on the screen
player_img = pygame.image.load('player_image.png')
player_x = 370
player_y = 480
player_x_change = 0

# Enemy - defining image and location on the screen
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change =[]
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('cat.png'))
    enemy_x.append(random.randint(0, 730))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(.3)
    enemy_y_change.append(40)



# Bullet - defining image and location on the screen
bullet_img = pygame.image.load('cucumber.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 2
# Ready (can't see bullet)
# Fire (bullet is moving)
bullet_state = 'ready'

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = game_over_font.render('GAME OVER ', True, (0, 255, 0))
    screen.blit(over_text, (250, 250))

# Draw the player's image on screen
def player(x, y):
    screen.blit(player_img, (x, y))

# Draw the enemy's image on screen
def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:

    # color of background
    screen.fill((0, 0, 0))

    # background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  

        # If a keystroke is pressed it checks to see if left or right
        # KEYDOWN is when any key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:                
                player_x_change = -1
            if event.key == pygame.K_RIGHT:
                player_x_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound = mixer.Sound('bullet_sound.mp3')
                    bullet_sound.play()
                    # Getting x coordinate of player
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        
        # Keystroke is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0          

    # Move player in x axis
    player_x += player_x_change

    # Set boundaries for the player referencing the pixels
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(num_of_enemies):

        # Game Over
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            
            game_over_text()
            break

        # Move enemy in x axis
        enemy_x[i] += enemy_x_change[i]

        # Set boundaries and move parameters for enemy
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 1
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -1
            enemy_y[i] += enemy_y_change[i]
        
        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound('meow.wav')
            explosion_sound.play()
            bullet_y = 480
            bullet_state = 'ready'
            score_value += 1
            print(score_value)
            enemy_x[i] = random.randint(0, 800)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)
        
    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change


    player(player_x, player_y)
    show_score(text_x, text_y)    
    pygame.display.update()


