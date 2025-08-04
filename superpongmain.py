import pygame 
import colorsys
from game_menu import game_list, icon_size, srfc_height, pos_list
import os
import sys
import random
from teste_yuri import Yuri
from utils import Text, button
from math import cos, sin, pi

base_dir = os.path.dirname(os.path.abspath(__file__)) # Get the directory of the current script
def load_image_from_subfolder(image_name, subfolder="game_thumb"): #fix the error alert
    # Build the full path to the image based on the base_dir
    image_path = os.path.join(base_dir, "assets", subfolder, image_name)
    if os.path.exists(image_path):
        return pygame.image.load(image_path)
    else:
        raise FileNotFoundError(f"Image not found: {image_path}")
    

##PYGAME_SETUP---------------------------------------------
WIDTH, HEIGHT = 1280, 720 
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_menu_surface = pygame.Surface((WIDTH, srfc_height)) ###excell is calculated in game_menu.py
#running and windw sets
pygame.display.set_caption('PONG')
clock = pygame.time.Clock()
running = True
icon_name = pygame.image.load('icon_name.jfif').convert()   
pygame.display.set_icon(icon_name)  #----> criar icône 
##UNIVERSAL_VAR-------------------------------------------------
#print(pygame.font.get_fonts()) see fonts
menu_font = pygame.font.SysFont('z003', 70)    #----->fazer função cria texto
game_list_font = pygame.font.SysFont('Tahoma', 40)
random_game_font = pygame.font.SysFont('Tahoma', 30)
background = (50,50,50)
TITLE = 'OGYGIA'
stages_list = [0,1,2]
estagio = 0
players = -1
hue = 0 
run= 0 
balls = False
#vars for game_menu # Scroll variables
scroll_offset = 0
scroll_limit = (srfc_height) - 720 
scroll_speed = 20
##Main_objects
yuri = Yuri(screen, WIDTH, HEIGHT)
title = Text(TITLE,(WIDTH//2,HEIGHT//2),'Arial',200,(240,240,240))
balls_b = button(20,20,(50,50),(125,125,0),0,45,'BALLS',font_size=10,text_color=(0,25,183))
##BASE_FUNCTIONS---------------------------------------------
def stage(estagio):
    match estagio:
        case 0 :
            return "menu"    

        case 1 :
            return "game_menu"
            
        case 2 :
            return "fase"

        case False :
            pass
##menu-----------------------------------------
def menu_screen(color):    #---------De preferência ransformar num objeto, dentro de stage
    texto_menu = menu_font.render('PRESS SPACE', True, color)
    screen.fill(background)  #screen.blit(background_main_menu, (0, 0)) if image
    title.update(screen)
    return texto_menu.get_rect(center=(screen.get_width()//2, screen.get_height()*(7/8))) , texto_menu  # Center the text on the screen

def changeColor(hue):
        color = colorsys.hsv_to_rgb(hue,1,1)
        return (color[0]*255,color[1]*255,color[2]*255)

def change_balls():
    global balls
    balls = not balls
##game_menu-----------------------------------------

def game_menu_screen(game_list, pos_list,icon_size,run):  #exclude unused vars
    if run == 0:
        thb_img = []
        for i, item in enumerate(game_list): 
            recta = pygame.Rect(pos_list[i], icon_size)
            pygame.draw.rect(game_menu_surface, 'white' ,recta)  ##EMPTY SPOTS FOR GAME IMAGES
            thb_img.append(load_image_from_subfolder(f'{item}_thumb_image.png'))
    screen.blit(game_menu_surface, (0, -scroll_offset))
    #randon button
    random_rect = pygame.Rect(790 , 5 - scroll_offset, 165, 50)
    pygame.draw.rect(screen, 'orange' ,random_rect)
    random_text = random_game_font.render("RANDOM", True, 'black')
    screen.blit(random_text, (814, 10 - scroll_offset))
    #Draw images
    for i in range(len(game_list)):
        image_pos = (pos_list[i][0], pos_list[i][1] - scroll_offset)
        screen.blit(thb_img[i], image_pos) #print the image in the rectangle
    _text = game_list_font.render("You can Scroll!!", True, 'white')
    screen.blit(_text, (10, 5 - scroll_offset))
    run = 1  #Mounting rects occours once
##--------------------------------------------------------------------
title.start_typewriter(delay=400) #runs once
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False        

        elif event.type == pygame.KEYDOWN and stage(estagio) == "menu":  #usar pygame.key.get_pressed()
            if event.key == pygame.K_SPACE:    
                estagio = 1

            elif event.key == pygame.K_d:
                title.enable_mouse_drag()

            elif event.key == pygame.K_BACKSPACE:
                title.create()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            title.change_color_all((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            if balls_b.obj.collidepoint(event.pos[0],event.pos[1]):
                change_balls()
            
        if title.mouse_drag == True:
            title.handle_mouse_event(event)

        # Controle da rolagem usando as setas para cima e para baixo  ##not working ----> need to fix
        elif stage(estagio) == "game_menu":
            game_menu_surface.fill('black')
            if event.type == pygame.MOUSEWHEEL:
                if event.y < 0:  # Scroll para baixo
                    scroll_offset = min(scroll_offset + scroll_speed, scroll_limit)
                elif event.y > 0:  # Scroll para cima
                    scroll_offset = max(scroll_offset - scroll_speed, 0)

            for i, item in enumerate(game_list): #green selection
                    if pygame.Rect((pos_list[i][0], pos_list[i][1] - scroll_offset), icon_size).collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(game_menu_surface, 'green' ,pygame.Rect((pos_list[i][0] - 5 , pos_list[i][1] - 5), (icon_size[0] + 10,icon_size[1] + 10)),border_radius=5)

            if pygame.Rect(790, 5 - scroll_offset , 165, 50).collidepoint(pygame.mouse.get_pos()): #green selection
                pygame.draw.rect(game_menu_surface, 'green' ,pygame.Rect((785 , 0 ), (175,60)),border_radius=5)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, item in enumerate(game_list):
                    if pygame.Rect((pos_list[i][0], pos_list[i][1] - scroll_offset), icon_size).collidepoint(pygame.mouse.get_pos()):# NOTE:triggering on scroll --> FIX
                        game = game_list[i]
                        estagio = 2
                    elif pygame.Rect(790, 5 - scroll_offset , 165, 50).collidepoint(pygame.mouse.get_pos()): #random button collision 
                        game = random.choice(game_list)
                        estagio = 2
                        
    
    stage(estagio)
    
    ##CHAMADAS---------------------------------------------
    
    if stage(estagio) == "menu": 
        if hue > 1:
            hue = 0
        hue += 0.005
        cor = changeColor(hue)
        start_rect, press_start = menu_screen(cor)  
        if balls: yuri.run(clock)
        #balls_b.move((WIDTH*hue,100*cos(hue*2*pi)))
        balls_b.update(screen,True)
        screen.blit(press_start, start_rect)

    if stage(estagio) == "game_menu": 
        game_menu_screen(game_list, pos_list,icon_size, run)
        pygame.display.flip()

    if stage(estagio) == "fase": #will be renamed and triggered by game_menu
        ruunning = False
        print(game)
        try:
            with open(f"{game}.py", "r") as file:  #change to import lib ---> change pong for no self imports
                exec(file.read())  ##"__name__": ""
        except: 
            print('error - game does not exist')
            #raise FileNotFoundError("Game not found")     
        pygame.quit()
        sys.exit()
              

    pygame.display.flip()
    clock.tick(60) 
    
pygame.quit()
sys.exit()