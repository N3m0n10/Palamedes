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
    
def get_proportion():
    global WIDTH
    global HEIGHT
    size = pygame.display.get_window_size()
    proportion = size / (WIDTH, HEIGHT)
    return proportion

def map_mouse_to_surface():
    """
    Translates the window's mouse position to the SC_SURFACE's coordinates.
    This is the KEY to making interactions work on a scaled surface.
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    window_width, window_height = screen.get_size()
    
    scale_x = window_width / WIDTH
    scale_y = window_height / HEIGHT
    scale = min(scale_x, scale_y) # Use the smaller scale factor to maintain aspect ratio

    # Calculate the position of the scaled surface on the window
    scaled_width = WIDTH * scale
    scaled_height = HEIGHT * scale
    offset_x = (window_width - scaled_width) / 2
    offset_y = (window_height - scaled_height) / 2
    
    # Reverse the calculation to find the mouse position on the virtual surface
    if scale == 0: return None
    surface_x = (mouse_x - offset_x) / scale
    surface_y = (mouse_y - offset_y) / scale

    # Make sure the mapped coordinates are within the virtual screen bounds
    if 0 <= surface_x < WIDTH and 0 <= surface_y < HEIGHT:
        return int(surface_x), int(surface_y)
    return None

## MAIN_GLOBALS
TITLE = 'OGYGIA'
WIDTH, HEIGHT = 1280, 720 
background = (50,50,50)
stages_list = [0,1,2]
estagio = 0
players = -1
hue = 0 
run= 0 
balls = False
running = True

# Scroll variables
scroll_offset = 0
scroll_speed = 20
scroll_limit = (srfc_height) - HEIGHT

##PYGAME_SETUP---------------------------------------------
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption(TITLE)

# windw sets
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
SC_SURFACE = pygame.Surface((WIDTH, HEIGHT))   #TODO: make a master surface who resizes everything!!!
icon_name = pygame.image.load('icon_name.jfif').convert()   
menu_font = pygame.font.SysFont('z003', 70)    
game_list_font = pygame.font.SysFont('Tahoma', 40)
random_game_font = pygame.font.SysFont('Tahoma', 30)

##Main_objects
yuri = Yuri(SC_SURFACE, WIDTH, HEIGHT)       # NOTE: change to screen for test SC_SURFACE
title = Text(TITLE,(WIDTH//2,HEIGHT//2),'p052',200,(240,240,240))
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
def changeColor(hue):
        color = colorsys.hsv_to_rgb(hue,1,1)
        return (color[0]*255,color[1]*255,color[2]*255)
##game_menu-----------------------------------------

def game_menu_screen(game_list, pos_list,icon_size,run):  #exclude unused vars
    SC_SURFACE.fill('black')
    if run == 0:
        thb_img = []
        for i, item in enumerate(game_list): 
            recta = pygame.Rect(pos_list[i], icon_size)
            pygame.draw.rect(SC_SURFACE, 'white' ,recta)  ##EMPTY SPOTS FOR GAME IMAGES
            thb_img.append(load_image_from_subfolder(f'{item}_thumb_image.png'))
    SC_SURFACE.fill('black')
        
    # Draw game thumbnails
    for i in range(len(game_list)):
        image_pos = (pos_list[i][0], pos_list[i][1] - scroll_offset)
        # Hover effect
        rect = pygame.Rect(image_pos, icon_size)
        if virtual_mouse_pos and rect.collidepoint(virtual_mouse_pos):
            pygame.draw.rect(SC_SURFACE, 'green', rect.inflate(10, 10), border_radius=5)
        
        SC_SURFACE.blit(thb_img[i], image_pos)

    # Draw random button
    random_rect = pygame.Rect(790, 5 - scroll_offset, 165, 50)
    # Hover effect
    if virtual_mouse_pos and random_rect.collidepoint(virtual_mouse_pos):
            pygame.draw.rect(SC_SURFACE, 'green', random_rect.inflate(10, 10), border_radius=5)
    pygame.draw.rect(SC_SURFACE, 'orange', random_rect)
    random_text = random_game_font.render("RANDOM", True, 'black')
    SC_SURFACE.blit(random_text, random_text.get_rect(center=random_rect.center))
    run = 1  #Mounting rects occours once
##--------------------------------------------------------------------
title.start_typewriter(delay=400) #runs once
while running:

    virtual_mouse_pos = map_mouse_to_surface()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False        

        # --- MENU STAGE EVENTS ---
        if stage(estagio) == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    estagio = 1
                elif event.key == pygame.K_d:
                    title.enable_mouse_drag()
                elif event.key == pygame.K_BACKSPACE:
                    title.create()
                elif event.key == pygame.K_c:
                    title.change_color_all((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                    
            if event.type == pygame.MOUSEBUTTONDOWN and virtual_mouse_pos:
                if balls_b.obj.collidepoint(virtual_mouse_pos):
                    balls = not balls
            
            if title.mouse_drag == True:
                title.handle_mouse_event(event)

        # Controle da rolagem usando as setas para cima e para baixo  ##not working ----> need to fix
        elif stage(estagio) == "game_menu":
            if event.type == pygame.MOUSEWHEEL:
                if event.y < 0:  # Scroll para baixo
                    scroll_offset = min(scroll_offset + scroll_speed, scroll_limit)
                elif event.y > 0:  # Scroll para cima
                    scroll_offset = max(scroll_offset - scroll_speed, 0)

            for i, item in enumerate(game_list): #green selection
                    if pygame.Rect((pos_list[i][0], pos_list[i][1] - scroll_offset), icon_size).collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(SC_SURFACE, 'green' ,pygame.Rect((pos_list[i][0] - 5 , pos_list[i][1] - 5), (icon_size[0] + 10,icon_size[1] + 10)),border_radius=5)

            if pygame.Rect(790, 5 - scroll_offset , 165, 50).collidepoint(pygame.mouse.get_pos()): #green selection
                pygame.draw.rect(SC_SURFACE, 'green' ,pygame.Rect((785 , 0 ), (175,60)),border_radius=5)

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
        SC_SURFACE.fill(background)
        hue = (hue + 0.005) % 1
        color = changeColor(hue)
        
        title.update(SC_SURFACE)
        if balls: yuri.run(clock)
        balls_b.update(SC_SURFACE, True)
        
        texto_menu = menu_font.render('PRESS SPACE', True, color)
        rect_menu = texto_menu.get_rect(center=(WIDTH // 2, HEIGHT * (7/8)))
        SC_SURFACE.blit(texto_menu, rect_menu)
        

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
              
    window_size = screen.get_size()
    scale = min(window_size[0] / WIDTH, window_size[1] / HEIGHT)
    scaled_size = (int(WIDTH * scale), int(HEIGHT * scale))
    scaled_surface = pygame.transform.smoothscale(SC_SURFACE, scaled_size)
    
    # Calculate the centered position
    pos = ((window_size[0] - scaled_size[0]) // 2, (window_size[1] - scaled_size[1]) // 2)

    screen.fill((0, 0, 0)) # Fill window with black for letterboxing
    screen.blit(scaled_surface, pos)

    pygame.display.flip()
    clock.tick(60) 
    
pygame.quit()
sys.exit()