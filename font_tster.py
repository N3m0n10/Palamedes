import pygame
from utils import Text
from random import randint

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

my_text = Text("Olá, mundo!", (400, 200), "Arial", 48, (255, 255, 255))
#my_text.mode = 'screen_protector'

running = True
my_text.start_typewriter(delay=80)
while running:
    screen.fill((0, 0, 0))
    my_text.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                my_text.enable_mouse_drag()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            my_text.change_color_all((randint(0,255), randint(0,255), randint(0,255)))
            
        if my_text.mouse_drag == True:
            my_text.handle_mouse_event(event)
            

    pygame.display.flip()
    clock.tick(60)

pygame.quit()