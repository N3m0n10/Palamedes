import pygame

def pontuacao(ball_x_pos, screen_limit):
    pontos_1 ,pontos_2 = 0 , 0
    if ball_x_pos <= screen_limit[0]:
        pontos_1 += 1                #pontos player 1
    if ball_x_pos >= screen_limit[1]:
        pontos_2 += 1                #pontos player 2 / BOT
    return pontos_1 , pontos_2

def placar(screen, pontos_1 , pontos_2):
    text_placar_font = pygame.font.SysFont('tahoma', 100) 
    text_placar1 = text_placar_font.render(f'{pontos_1}', True, ('White'))
    text_placar2 = text_placar_font.render(f'{pontos_2}', True, ('White'))
    screen.blit(text_placar1, (380,100))
    screen.blit(text_placar2, (900,100))