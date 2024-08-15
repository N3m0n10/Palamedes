import pygame 
import colorsys
from game_menu import excell, surface_size , game_list, icon_size, srfc_height, pos_list
import subprocess

#run game_menu.py as a subprocess
subprocess.run(['python', 'game_menu.py'])
##PYGAME_SETUP---------------------------------------------
pygame.init()
pygame.font.init()
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
stages = [0,1,2,3]
stages = iter(stages)
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
            return "menu"    #------->mudar nomes
        ##--------------->create select game ---> new vers == new gamemodes
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
        for i, item in enumerate(game_list):
            recta = pygame.Rect(pos_list[i], icon_size)
            pygame.draw.rect(game_menu_surface, 'white' ,recta)
    screen.blit(game_menu_surface, (0, -scroll_offset))
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
            elif event.key == pygame.K_1:
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
           
        
        
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("White")
    stage(estagio)
    
    ##CHAMADAS---------------------------------------------
    
    if stage(estagio) == "menu": #-----------> mudar
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
        with open("teste_nemo.py", "r") as file:  #to be done: f'{game}.py
            exec(file.read(), {"__name__": ""})

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()



