import pygame , sys

##PYGAME_SETUP---------------------------------------------
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
##UNI_VAR-------------------------------------------------
in_menu = True
menu_font = pygame.font.SysFont('Comic Sans MS', 70)
texto_menu = menu_font.render('Press Space', True, (90, 100, 240))
background = pygame.image.load('background.jpg').convert()
background = pygame.transform.smoothscale(background, screen.get_size())
stages = [0,1,2]
stages = iter(stages)
estagio = next(stages)
##FUNÇÕES_BASE--------------------------------------------------------
def stage(estagio):
    match estagio:
        case 0 :
            return "menu"    #------->mudar nomes

        case 1 :
            return "fases"
            

        case 3 :
            #return pontuacao
            pass
        case False :
            pass
 



##menu-----------------------------------------
def menu_screen():    #---------De preferência ransformar num objeto, dentro de stage
    screen.blit(background, (0, 0))
    screen.blit(texto_menu, (500,240))


##--------------------------------------------------------------------
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN and stage(estagio) == "menu":  #teste apertar tecla
            if event.key == pygame.K_SPACE:    
                estagio = next(stages)
                print("teste_space")

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("White")
    stage(estagio)

    ##CHAMADAS---------------------------------------------
    if stage(estagio) == "menu": #-----------> mudar
        menu_screen()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()



