import pygame
from utils import button

pygame.init()
screen = pygame.display.set_mode((800,600))
start = button(20,400,(100,30),(125,125,0),0,30,'START',font_size=20,text_color=(0,25,183))
hold = False

running = True
while running:

    screen.fill((0,0,0))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and start.obj.collidepoint(mouse_pos):
            start.action(print,start.text)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                hold = not hold

    if hold:
        start.move(mouse_pos)

    start.update(screen,True,mouse_pos=mouse_pos)
    pygame.display.update()

pygame.quit()