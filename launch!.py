###-------------------------------------
###two plataform
###N entitys of the player crew? and opponents
###individual life for all entitys + physics for pushing from plaaform  and gravity
###Main goal, launch projectiles from the player and hit the opponent 
###win conndition, Depleat lifes or push from plataform
###different weapons and later classes
###phase obstacles
###add roguelike mode
###3D version in future?
###-------------------------------------
import pygame         
from colorsys import hsv_to_rgb

flags = pygame.RESIZABLE | pygame.SCALED   #pygame.OPENGL | 
pygame.display.set_mode((1280, 600), flags, vsync=1, depth=0, display=0)
window_surface = pygame.display.get_surface()
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)  
#pygame.display.list_modes(depth=0, flags=pygame.FULLSCREEN, display=0)  DEBUG
pygame.display.set_caption('LAUNCH!  -  F11 to toggle fullscreen')

####
#background = pygame.image.load('assets/general_images/TODO <NAME>').convert()
play_button = pygame.rect.Rect(540,200,200,100)
options_button = pygame.rect.Rect(540,320,200,100)
exit_button = pygame.rect.Rect(540,440,200,100)

####
#class particle_generator():
#    def __init__(self,time):
#        self.particles = []
#        self.lst_time = time
#
#    def create_particle(self,time):
#        if time == self.lst_time:
#            self.particles.append(particle())
#             use senoidal functions

#pygame.display.update()
clock = pygame.time.Clock()

####
running = True
start_menu = True
mode_menu = False
phase_menu = False
in_phase = False
#pause = False
while running:
    while start_menu:

        window_surface.fill((255,253,208))

        if play_button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(window_surface, (20,175,12), pygame.rect.Rect(535,195,210,110), border_radius=5)
        elif options_button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(window_surface, (20,175,12), pygame.rect.Rect(535,315,210,110), border_radius=5)
        elif exit_button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(window_surface, (20,175,12), pygame.rect.Rect(535,435,210,110), border_radius=5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen() 

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(pygame.mouse.get_pos()):
                    start_menu = False
                    mode_menu = True
                elif options_button.collidepoint(pygame.mouse.get_pos()):
                    start_menu = False
                    phase_menu = True
                elif exit_button.collidepoint(pygame.mouse.get_pos()):
                    exit()


        ###PLAY
        pygame.draw.rect(window_surface, (200,50,12), play_button)
        ###OPTIONS
        pygame.draw.rect(window_surface, (200,50,12), options_button) 
        ###EXIT
        pygame.draw.rect(window_surface, (200,50,12), exit_button)
        #window_surface.blit(background TODO, (0, 0))


        #particles ---> later
        #set random time and pos to spawm
        # the timer will compare to the setted variable
        # add to list
        # destroy if time out of screen 


        
        clock.tick(60)
        pygame.display.flip()

    while mode_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen() 

        clock.tick(60)
        pygame.display.flip()
        

    while phase_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()  

        #phase button generator

        clock.tick(60)
        pygame.display.flip()

    while in_phase:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen() 


        

        clock.tick(60)
        pygame.display.flip()
                

    #pygame.display.update() for portion of the screen
