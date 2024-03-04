# Example file showing a circle moving on screen
import pygame
from ball import ball
import colorsys

# pygame setup
pygame.init()
WIDTH, HEIGHT = 1280,720 #largura e altura
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#fps
clock = pygame.time.Clock()
dt = 0


spriteBalls = pygame.sprite.Group()

ball1 = ball(screen,'red',50)
ball2 = ball(screen,'blue',50)
ball3 = ball(screen,'green',35)
ball4 = ball(screen,'yellow',35)
spriteBalls.add(ball2)
spriteBalls.add(ball3)
spriteBalls.add(ball4)

running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    if pygame.sprite.collide_circle(ball1,ball2):
        ball1.changeColor() 

    #Bola
    ball1.atualize(dt,(WIDTH, HEIGHT))
    ball2.atualize(dt,(WIDTH,HEIGHT))
    #ball3.atualize(dt,(WIDTH,HEIGHT))
    #ball4.atualize(dt,(WIDTH,HEIGHT))


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()