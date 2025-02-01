import pygame

def placar(screen, pontos_1 , pontos_2, pos_1 = (380,100), pos_2 = (900,100)): #make arg
    text_placar_font = pygame.font.SysFont('tahoma', 100) 
    text_placar1 = text_placar_font.render(f'{pontos_1}', True, ('White'))
    text_placar2 = text_placar_font.render(f'{pontos_2}', True, ('White'))
    screen.blit(text_placar1,pos_1)
    screen.blit(text_placar2,pos_2) #make an arg when replication is needed