# this is my DBZ inspired game 
from multiprocessing import Event
import pygame
import os

pygame.init()

# static vars
WIDTH, HEIGHT = 1000, 700
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
FPS = 60 # fps of game
VEL = 4 # speed of players
GBLAST_VEL = 5 # speed of goku blasts
VBLAST_VEL = 8 # speed of vegeta blasts
FONT = pygame.font.SysFont('comicsans', 40) # font used for text 
BORDER = pygame.Rect(WIDTH/2 - 5,0,10,HEIGHT) # border dividing players

# assets
background_img = pygame.image.load("arena.png")
goku = pygame.transform.scale(pygame.image.load("goku.png"), (150,150))
vegeta = pygame.transform.scale(pygame.image.load("vegeta.png"), (150,150))
gAttack = pygame.transform.scale(pygame.image.load("goku_attack.png"), (100,100))
vAttack = pygame.transform.scale(pygame.image.load("vegeta_attack.png"), (60,60))

pygame.display.set_caption("FIGHT!")

# lists of attacks of each character 
gokuBlasts = []
vegetaBlasts = []
MAX_BLASTS = 3 # each player can only fire 3 bullets at a time 


# when a character gets hit 
GOKU_HIT = pygame.USEREVENT + 1
VEGETA_HIT = pygame.USEREVENT + 2

# main game loop
def main():
    p1 = pygame.Rect(WIDTH/6, HEIGHT/3, 150, 150) # goku's rectangle
    p2 = pygame.Rect(WIDTH/1.5, HEIGHT/3, 150, 150) # vegeta's rectangle

    # player health values 
    GOKU_H = 10
    VEGETA_H = 10

    clock = pygame.time.Clock() # how often the game updates 
    run = True 

    while run == True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # check if game is quit
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(gokuBlasts) <= MAX_BLASTS:
                    blast = pygame.Rect(p1.x + p1.width, p1.y + p1.height/2, 100, 100)
                    gokuBlasts.append(blast)
                if event.key == pygame.K_COMMA and len(vegetaBlasts) <= MAX_BLASTS * 2:
                    blast = pygame.Rect(p2.x - p2.width, p2.y + p2.height/2, 60,60)
                    vegetaBlasts.append(blast)
            
            if event.type == GOKU_HIT:
                GOKU_H -= 1
            if event.type == VEGETA_HIT:
                VEGETA_H -= 1
        
        winner_text = ""
        if (GOKU_H <= 0):
            winner_text = "Vegeta wins"
            drawWinner(winner_text)
        if (VEGETA_H <= 0):
            winner_text = "Goku wins"
            drawWinner(winner_text)

        # movement detection
        keys_pressed = pygame.key.get_pressed() # gets the keys currently being pressed
        charMovement(keys_pressed, p1, p2)
        blastMovement(p1,p2)
        draw_window(p1, p2, GOKU_H, VEGETA_H)

    pygame.quit()

# draws the window every tick 
def draw_window(p1, p2, GOKU_H, VEGETA_H):
    WINDOW.blit(background_img,[0,0])
    pygame.draw.rect(WINDOW, (0,0,0), BORDER) # draw the border 

    VEGETA_TXT = FONT.render("Health: " + str(VEGETA_H), 1, (0,0,0))
    GOKU_TXT = FONT.render("Health: " + str(GOKU_H), 1, (0,0,0))

    WINDOW.blit(VEGETA_TXT, (WIDTH - VEGETA_TXT.get_width() - 10, 20))
    WINDOW.blit(GOKU_TXT, (10, 20))

    WINDOW.blit(goku, (p1.x, p1.y))
    WINDOW.blit(vegeta, (p2.x, p2.y))
    for blast in gokuBlasts:
        WINDOW.blit(gAttack, (blast.x, blast.y))
    for blast in vegetaBlasts:
        WINDOW.blit(vAttack, (blast.x, blast.y))
    pygame.display.update()

# draws winner text 
def drawWinner(text):
    draw_text = FONT.render(text,1, (0,0,0))
    WINDOW.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()


# moves characters 
def charMovement(keys_pressed, p1, p2):
    if keys_pressed[pygame.K_a] and p1.x - VEL > 0: # player 1 left 
        p1.x -= VEL
    if keys_pressed[pygame.K_d] and p1.x + VEL < BORDER.x - p1.width: # player 1 right 
        p1.x += VEL
    if keys_pressed[pygame.K_w] and p1.y - VEL > 0: # player 1 up 
        p1.y -= VEL
    if keys_pressed[pygame.K_s] and p1.y + VEL < HEIGHT - p1.height: # player 1 down 
        p1.y += VEL
    if keys_pressed[pygame.K_LEFT] and p2.x + VEL > BORDER.x: # player 2 left 
        p2.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and p2.x + VEL + p2.width < WIDTH: # player 2 right 
        p2.x += VEL
    if keys_pressed[pygame.K_UP] and p2.y - VEL > 0: # player 2 up 
        p2.y -= VEL
    if keys_pressed[pygame.K_DOWN] and p2.y + VEL < HEIGHT - p2.height: # player 2 down 
        p2.y += VEL

# moves blasts 
def blastMovement(p1,p2):
    for blast in gokuBlasts:
        blast.x += GBLAST_VEL
        if p2.colliderect(blast):
            gokuBlasts.remove(blast)
            pygame.event.post(pygame.event.Event(VEGETA_HIT))
        if blast.x >= WIDTH:
            gokuBlasts.remove(blast)
    for blast in vegetaBlasts:
        blast.x -= VBLAST_VEL
        if p1.colliderect(blast):
            vegetaBlasts.remove(blast)
            pygame.event.post(pygame.event.Event(GOKU_HIT))
        if blast.x <= 0:
            vegetaBlasts.remove(blast)

# run game while file is run
if __name__ == "__main__":
    main()


