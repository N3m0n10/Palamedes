# Example file showing a circle moving on screen
import pygame
from ball import ball
from player import player

# pygame setup
pygame.init()
WIDTH, HEIGHT = 1280,720 #largura e altura
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#fps
clock = pygame.time.Clock()
dt = 0

ball1 = ball(screen,'red',40)
player1 = player(screen, 'blue', 50, 600)
player2 = player(screen, 'orange', 50, 120)


running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    #Bola
    ball1.atualize(dt,(WIDTH, HEIGHT))
    player1.atualize(dt,(WIDTH, HEIGHT))
    player2.atualize(dt,(WIDTH, HEIGHT))
   
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()