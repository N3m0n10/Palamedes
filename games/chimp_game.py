import pygame
from random import randint

"""Using a multi-if esctructure to simplify"""

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chimp Game")

numbers = ['1','2','3','4','5','6','7','8','9']
rect_size = 50
button = pygame.Rect(30, 650, 50, 50)

font_size = 50
font = pygame.font.SysFont('Arial', font_size, bold=True) 
num_texts = []
for i in range(len(numbers)):
    text_surf = font.render(numbers[i], True, (255, 255, 255)) 
    text_obj = text_surf.get_rect()
    num_texts.append([text_obj,text_surf])

fail = False
create_number = True
show_numbers = False
choose_places = False
running = True
rects = []

while running:

    if create_number:

        clicked = [False] * len(numbers)
        rects.clear() 

        for i in range(len(numbers)):
            while True:
                x = randint(0, WIDTH - rect_size)
                y = randint(0, HEIGHT - rect_size)
                new_rect = pygame.Rect(x, y, rect_size, rect_size)

                if not any(new_rect.colliderect(r) for r in rects) or new_rect.colliderect(button):
                    num_texts[i][0].center = new_rect.center
                    break
            rects.append(new_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    create_number = False
                    choose_places = True

        screen.fill((30,30,30))

        pygame.draw.rect(screen, (255, 255, 255), button, border_radius=45)

        pygame.display.flip()
        clock.tick(60)

    if choose_places:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for d in range(len(num_texts)):
                if event.type == pygame.MOUSEBUTTONDOWN and num_texts[d][0].collidepoint(event.pos):
                    clicked[d] = True
                    if d == clicked.count(True) - 1:
                        pass
                    else:
                        # fail sound
                        #pygame.mixer.Sound('NOTE:find_this_later.mp3').play()
                        fail = True
                        choose_places = False
                        create_number = True

        screen.fill((30,30,30))

        if set(clicked) == {False}:
            for j in num_texts:
                screen.blit(j[1], j[0].topleft)

        else:
            for l in range(len(numbers)):
                if not clicked[l]:
                    pygame.draw.rect(screen, (255, 255, 255), rects[l])

            if set(clicked) == {True}:
                
                if not fail:
                    # win sound
                    #pygame.mixer.Sound('NOTE:find_this_later.mp3').play()
                    fail = False

                create_number = True
                choose_places = False

        pygame.display.flip()
        clock.tick(60)

pygame.quit()