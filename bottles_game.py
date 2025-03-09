import pygame
from random import randint,sample
import math

pygame.init()
WIDGHT,HEIGHT = 800,600
MINWIDTH ,MINHEIGHT = 400,300
widght,height = WIDGHT,HEIGHT  
sc = pygame.display.set_mode((WIDGHT,HEIGHT), pygame.RESIZABLE) 
pygame.display.set_caption('let me move the bottles!')
clock = pygame.time.Clock()

difficult = 1
pointer = 0 
pointer_2 = 0
checking = False
right_number = 0


start_text_font = pygame.font.Font(None, 36)
start_text = start_text_font.render('Press SPACE or click to start', True, (255, 255, 255))
start_text_rect = start_text.get_rect(center=(400, 300))
r_num_text = start_text_font.render(f'{right_number}', True, (255, 255, 255))
help_text = start_text_font.render('Use A and D to move the first hand and LEFT and RIGHT to move the second hand', True, (255, 255, 255))
help_text_2nd = start_text_font.render('Press SPACE to change the bottles and RIGHT ENTER to check', True, (255, 255, 255))
win_text = start_text_font.render('You win! Press SPACE to continue', True, (255, 255, 255))
win_text_2nd = start_text_font.render('Press BACKSPACE to exit', True, (255, 255, 255))



class Bottle:  
    color_list = [i for i in range(9 + difficult)]
    def __init__(self, id):
        self.id = id
        self.color = Bottle.color_list[id]
        self.image = pygame.image.load(f'assets/general_images/bottle_{self.color}.png')
        self.processed_image = pygame.transform.smoothscale_by(self.image, 0.2)
        self.rect = self.image.get_rect()

    def atualize(self,pos):
        pygame.draw(self.image, center = pos)

    def process_image(self, width, height):
        self.processed_image = pygame.transform.scale(self.image, (width, height))

def enemy(_bottles, _sequence):
    choose = 0
    drop_a_coin = randint(0, 1)
    match drop_a_coin:  
        case 0:
            for b in range(len(_bottles)):
                if _bottles[b].color == _sequence[b]:
                    choose = 1
                    pointer = b
                    pointer_2 = randint(0, 9 + difficult)
                    while pointer_2 == pointer:
                        pointer_2 = randint(0, 9 + difficult)
                    break
            if choose == 0:
                pointer, pointer_2 = randint(0, 9+difficult), randint(0, 9+difficult)
                while pointer_2 == pointer:
                    pointer_2 = randint(0, 9+difficult)
        case 1:
            pointer, pointer_2 = randint(0, 9+difficult), randint(0, 9+difficult)
            while pointer_2 == pointer:
                pointer_2 = randint(0, 9+difficult)
    return pointer, pointer_2
                


    


running = True
menu = True
phase = False
interlude = False
finish_screen = False
while running:
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False
            if event.type == pygame.VIDEORESIZE:
                widght = max(MINWIDTH, event.w)
                height = max(MINHEIGHT, event.h)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False
                    phase = True
            if start_text_rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    menu = False
                    phase = True
        
        if start_text_rect.collidepoint(pygame.mouse.get_pos()):
                start_text_font = pygame.font.Font(None, 36 + int(math.sin(pygame.time.get_ticks() / 150) * 10))
                start_text = start_text_font.render('Press SPACE or click to start', True, (255, 255, 255))
                start_text_rect = start_text.get_rect(center=(widght/2, height/2))
        
        sc.fill((0, 0, 0))
        sc.blit(start_text, start_text_rect)
        pygame.display.flip()  # when fullscreened the using flip fix update bugs
        #pygame.display.update(start_text_rect)
        dt = clock.tick(60) / 1000

    while phase:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                phase = False
            if event.type == pygame.VIDEORESIZE:
                widght = max(MINWIDTH, event.w)
                height = max(MINHEIGHT, event.h)
                sc = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                ###transform bottle images
            if event.type == pygame.KEYDOWN:
                if not checking:
                    if event.key == pygame.K_SPACE:
                        old_in_pos = bottles[pointer]
                        bottles[pointer] = bottles[pointer_2]
                        bottles[pointer_2] = old_in_pos
                    if event.key == pygame.K_KP_ENTER:
                        checking = True
                        print("checking")
                    if event.key == pygame.K_d:
                        if pointer < 8 + difficult:
                            pointer += 1
                    if event.key == pygame.K_a:
                        if pointer > 0:
                            pointer -= 1
                    if event.key == pygame.K_RIGHT:
                        if pointer_2 < 8 + difficult:
                            pointer_2 += 1
                    if event.key == pygame.K_LEFT:
                        if pointer_2 > 0:
                            pointer_2 -= 1
                if event.key == pygame.K_m:
                    list_bot = []
                    for i, bottle in enumerate(bottles):
                        list_bot.append(bottle.id)
                    print(list_bot)
                    print(sequence)
            #if event.type == pygame.MOUSEBUTTONDOWN:

        if checking:
            try:
                run
            except NameError:
                run = 0
            try:
                wait_time
            except NameError:
                wait_time = pygame.time.get_ticks()
            try:
                count
            except NameError:
                right_number = 0
                for i in range(9 + difficult):
                    if bottles[i].id == sequence[i]:
                        right_number += 1
                count = True
            if pygame.time.get_ticks() - wait_time > 3000:
                run += 1
                enemy(bottles, sequence)
                old_in_pos = bottles[pointer]
                bottles[pointer] = bottles[pointer_2]
                bottles[pointer_2] = old_in_pos
                right_number = 0
                for i in range(9 + difficult):
                    if bottles[i].id == sequence[i]:
                        right_number += 1
                if difficult - run == 0:
                    checking = False
                    run = 0
                del wait_time
                del count
            r_num_text = start_text_font.render(f'{right_number}', True, (255, 255, 255))

        if right_number == 9 + difficult:
            checking = False
            finish_screen = True
            phase = False
            del bottles
            del sequence
            del right_number
            del count
              
        try:  #create the bottles and the sequence
            bottles  
        except NameError:
            bottles = [Bottle(i) for i in range(9 + difficult)]
            sequence = sample(range((9 + difficult)), k=(9 + difficult))

        sc.fill((0, 0, 0))
        for i, bottle in enumerate(bottles):
            sc.blit(bottle.image, (i*widght/WIDGHT*60 - 40, 0))
        sc.blit(pygame.image.load('assets/general_images/hand.png'), (pointer*widght/WIDGHT*60, height*0.5))  #TODO resize images
        sc.blit(pygame.image.load('assets/general_images/hand.png'), (pointer_2*widght/WIDGHT*60, height*0.55))  #TODO resize images
        sc.blit(r_num_text, (0, 0))
        sc.blit(help_text, (0, height*0.95))
        sc.blit(help_text_2nd, (0, height*0.90))
        pygame.display.update()  #update only a rect, most of the screen is not updated

        clock.tick(60)

    while finish_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                widght = max(MINWIDTH, event.w)
                height = max(MINHEIGHT, event.h)
                sc = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if difficult < 5:
                        finish_screen = False
                        phase = True
                        difficult += 1
                if event.key == pygame.K_BACKSPACE:
                    finish_screen = False
                    running = False
                    
        

        sc.fill((30,30,30))
        sc.blit(win_text, (0, height*0.5))
        sc.blit(win_text_2nd, (0, height*0.55))
        pygame.display.update()
        clock.tick(60)
        
        


pygame.quit()

