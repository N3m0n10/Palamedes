import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280,720))
dados_font = pygame.font.SysFont('Arial', 70)
button = pygame.Rect(200,300,100,100)
counting = True

rect = [pygame.Rect(100*i,100,100,200) for i in range(3)]
for item in rect:
    pygame.draw.rect(screen,"white",item)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(pygame.mouse.get_pos()):
                counting = not counting
                try:
                    del value
                except:
                    pass
    screen.fill((30,30,30))
    pygame.draw.rect(screen,"white",button)
    if counting:
        for i in range(3):
            text = dados_font.render(str(random.randint(1,6)),True,"white")
            screen.blit(text,(rect[i].x + 15,rect[i].y))
    else:
        try:
            for i in range(3):
                text = dados_font.render(value[i],True,"white")
                screen.blit(text,(rect[i].x + 15,rect[i].y))
        except:
            value = list()
            for i in range(3):  
                value.append(str(random.randint(1,6)))
    pygame.display.flip()
pygame.quit()

