import pygame
from random import randint

pygame.init()

#seções
#menu
#saves/start
#inputs
#in_game_menu_UI

tower = []

window1 = pygame.display.set_mode((400, 300), pygame.RESIZABLE)
clock = pygame.time.Clock()
local_4_surface = pygame.Surface((window1.get_width(), window1.get_height()), pygame.SRCALPHA)
local_4_surface.fill((25,255,0,125))

def change_location(actual,next):
    actual = False
    next = True


#1. rects
rects = [pygame.Rect(10,0,30,window1.get_height()),
         pygame.Rect(window1.get_width() - 40,0,30,window1.get_height()),
         pygame.Rect(10,0,window1.get_width()-20,30)]


#set timer after menu

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:  # Evento de redimensionamento
            local_4_surface.set_alpha(randint(1, 255))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()

    
    pygame.display.set_caption(f"D TOWER  FPS: {round(clock.get_fps())}")
    for rect in rects:
        pygame.draw.rect(window1, (255, 0, 0), rect)

    
    pygame.display.flip()

    clock.tick(60)


pygame.quit()
