# Example file showing a circle moving on screen
import pygame
from ball import ball
from player import player
from superpongmain import players
# pygame setup
pygame.init()
WIDTH, HEIGHT = 1280,720 #largura e altura
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#fps
clock = pygame.time.Clock()
dt = 0
#pontuação
pontos1 = 0
pontos2 = 0

ball1 = ball(screen,'red',40)
player1 = player(screen, 'blue' , 20, 70 , 180,0,)
if players == 1:
    player2 = player(screen, 'orange' , 20, 70 , 1100,1)
if players == 0:
    bot = player(screen, 'orange' , 20, 70 , 1100,0)

running = True
while running:
    #SAI COM O "X" DE FECHAR A JANELA
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")      

    #Bola
    ball1.atualize(dt, (WIDTH, HEIGHT))
    if players == 0:
        bot.atualize(dt, (WIDTH, HEIGHT) , 0 , ball1.player_pos.y )
    player1.atualize(dt, (WIDTH, HEIGHT) , 1 , ball1.player_pos.y )
    if players == 1:
        player2.atualize(dt, (WIDTH, HEIGHT) , 2 , ball1.player_pos.y )
   
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()