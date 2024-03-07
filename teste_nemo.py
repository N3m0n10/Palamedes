# Example file showing a circle moving on screen
import pygame
from ball import ball
from player import player
from superpongmain import players
import placar
# pygame setup
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 1280,720 #largura e altura
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#fps
clock = pygame.time.Clock()
dt = 0
pontos_1, pontos_2 = 0 , 0
#------------
ball_radius = 20
player_size = 150
ball1 = ball(screen,'red',ball_radius)
ball1_rect = ball1.rect
player1 = player(screen, 'blue' , 20, player_size , 180,1)
if players == 0:
    opponent = player(screen, 'White' , 20, player_size , 1100,0)
elif players == 1:
    opponent = player(screen, 'orange' , 20, player_size , 1100,2) 
#--------------------
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
    #jogadores e BOT - ATUALIZE
    player1.atualize(dt, (WIDTH, HEIGHT) , 1 , ball1.player_pos.y )
    if players == 0:
        opponent.atualize(dt, (WIDTH, HEIGHT) , 0 , ball1.player_pos.y ) #bot
    if players == 1:
        opponent.atualize(dt, (WIDTH, HEIGHT) , 2 , ball1.player_pos.y ) #player 2
    
    #colisão
    if pygame.Rect.colliderect(ball1_rect, player1.rect) \
    or pygame.Rect.colliderect(ball1_rect, opponent.rect):
        if ball1.ball_vel_x > 0: #adicionar velocidade a bola pela velocidade do jogador
            pass
        if ball1.ball_vel_x < 0: 
            pass
        ball1.ball_vel_x *= -1
            
    #pontuação
    if ball1.player_pos.x >= 1280 - ball_radius:
        pontos_1 += 1   
    if ball1.player_pos.x <=  ball_radius:
        pontos_2 += 1    
    placar.placar(screen , pontos_1, pontos_2)
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()