import pygame 
import colorsys
from game_menu import excell, surface_size , game_list, icon_size, srfc_height, pos_list
#import subprocess  ###will be used later
import os
import itertools

base_dir = os.path.dirname(os.path.abspath(__file__)) # Get the directory of the current script
def load_image_from_subfolder(image_name, subfolder="game_thumb"): #fix the error alert
    # Build the full path to the image based on the base_dir
    image_path = os.path.join(base_dir, "images", subfolder, image_name)
    if os.path.exists(image_path):
        return pygame.image.load(image_path)
    else:
        raise FileNotFoundError(f"Image not found: {image_path}")

#subprocess.run(['python', 'game_menu.py','--subprocess'])#run game_menu.py as a subprocess
                                          #read  and arrange games for menu

##PYGAME_SETUP---------------------------------------------
pygame.init()
#screen setup
screen = pygame.display.set_mode((1280, 720))
game_menu_surface = pygame.Surface((1280, srfc_height)) ###excell is calculated in game_menu.py
#running and windw sets
pygame.display.set_caption('PONG')
clock = pygame.time.Clock()
running = True
icon_name = pygame.image.load('icon_name.jfif').convert()   
pygame.display.set_icon(icon_name)  #----> criar icône 
##UNIVERSAL_VAR-------------------------------------------------
in_menu = True
menu_font = pygame.font.SysFont('Comic Sans MS', 70)    #----->fazer função cria texto
texto_selectplayer = menu_font.render('Press 0 for 1p or 1 for 2p', True, (90, 40, 240))
background = pygame.image.load('background.png').convert()
background = pygame.transform.smoothscale(background, screen.get_size())
stages_list = [0,1,2,3]
stages = itertools.cycle(stages_list)
estagio = next(stages)
players = -1
hue = 0 
run= 0
#vars for game_menu  #translate to english
# Variável de deslocamento para a rolagem
scroll_offset = 0
# Limite de rolagem (o máximo que a superfície pode rolar)
scroll_limit = (srfc_height) - 720 
# Velocidade de rolagem
scroll_speed = 20
##BASE_FUNCTIONS---------------------------------------------
def stage(estagio):
    match estagio:
        case 0 :
            return "menu"    

        case 1 :
            return "game_menu"

        case 2 :
            return "select_player"
            
        case 3 :
            return "fase"

        case False :
            pass
 

##menu-----------------------------------------
def menu_screen(color):    #---------De preferência ransformar num objeto, dentro de stage
    texto_menu = menu_font.render('Press Space', True, color)
    screen.blit(background, (0, 0))
    screen.blit(texto_menu, (450,600))

def select_player_screen():
    screen.blit(texto_selectplayer, (100,240))

def changeColor(hue):
        color = colorsys.hsv_to_rgb(hue,1,1)
        return (color[0]*255,color[1]*255,color[2]*255)


##game_menu-----------------------------------------

def game_menu_screen(game_list, pos_list,icon_size, excell, srfc_height,run):  #exclude unused vars
    if run == 0:
        thb_img = []
        for i, item in enumerate(game_list): 
            recta = pygame.Rect(pos_list[i], icon_size)
            pygame.draw.rect(game_menu_surface, 'white' ,recta)
            thb_img.append(load_image_from_subfolder(f'{item}_thumb_image.png'))
    screen.blit(game_menu_surface, (0, -scroll_offset))
    for i in range(len(game_list)):
        image_pos = (pos_list[i][0], pos_list[i][1] - scroll_offset)
        screen.blit(thb_img[i], image_pos) #print the image in the rectangle
        #FIX OFFSET FOR IMAGES
##On click event must be created in #main #events
#create  game icons --> clickable rectangle 
    run = 1
##--------------------------------------------------------------------
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN and stage(estagio) == "select_player":  #usar pygamr.key.get_pressed()
            if event.key == pygame.K_0:
                players = 0
                estagio = next(stages)
            if event.key == pygame.K_1:
                players = 1
                estagio = next(stages)

        elif event.type == pygame.KEYDOWN and stage(estagio) == "menu":  #usar pygame.key.get_pressed()
            if event.key == pygame.K_SPACE:    
                estagio = next(stages)

        # Controle da rolagem usando as setas para cima e para baixo  ##not working ----> need to fix
        elif event.type == pygame.MOUSEWHEEL:
            if event.y < 0:  # Scroll para baixo
                scroll_offset = min(scroll_offset + scroll_speed, scroll_limit)
            elif event.y > 0:  # Scroll para cima
                scroll_offset = max(scroll_offset - scroll_speed, 0)
        
        elif event.type == pygame.MOUSEBUTTONDOWN and stage(estagio) == "game_menu":
            for i, item in enumerate(game_list):
                if pygame.Rect(pos_list[i], icon_size).collidepoint(pygame.mouse.get_pos()):
                    game = game_list[i]
                    estagio = next(stages)

        
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("White")
    stage(estagio)
    
    ##CHAMADAS---------------------------------------------
    
    if stage(estagio) == "menu": 
        if hue > 1:
            hue = 0
        hue += 0.005
        cor = changeColor(hue)
        menu_screen(cor)

    if stage(estagio) == "game_menu": 
        game_menu_screen(game_list, pos_list,icon_size, excell, srfc_height, run)

    if stage(estagio) == "select_player": #error -------> repetindo #will berelocated to each game 
        select_player_screen()

    if stage(estagio) == "fase": #will be renamed and triggered by game_menu
        try:
            with open(f"{game}.py", "r") as file:  #change to import lib ---> change pong for no self imports
                exec(file.read(), {"__name__": ""})  ##"__name__": ""
                ruunning = False
        except: 
            print('error - game does not exist')
            running = False

    # flip() the display to put your work on screen
    pygame.display.flip()  #main seens to continue running, CHECK <---

    clock.tick(60)  # limits FPS to 60

pygame.quit()



