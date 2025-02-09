import pygame
import math

# Inicializa o Pygame
pygame.init()

# Tamanho inicial da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
x = 0
y = 1
reverse = 1
# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:  # Evento de redimensionamento
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            #resize_coeficient = (screen_width / 800, screen_height / 600)

    # Preenche a tela com uma cor (opcional)
    screen.fill((30, 30, 30))
    pos = ((10)*y*math.cos(x) + screen_width/2, (10)*y*math.sin(x) + screen_height/2)
    x += 0.1
    y += 0.1*reverse
    pygame.draw.circle(screen, (255, 0, 0), pos, 5)
    if y > 13*math.pi:
        reverse = -1
    elif y < 0:
        reverse = 1
    if x > 2*math.pi:
        x = 0
   
    

    # Atualiza a tela
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Encerra o Pygame
pygame.quit()
