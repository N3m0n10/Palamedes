import pygame
from ball import ball
from player import player
import placar

###pygame setup
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 1280,720 #largura e altura
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mixer.init() #sound function
coll_snd = pygame.mixer.Sound("collide_pong.mp3")#collision sound file  
lose = pygame.mixer.Sound('lose.mp3') 
victory= pygame.mixer.Sound('victory.mp3')
p_snd = True  #limitate sound playtime
#fps
clock = pygame.time.Clock()
dt = 0
pontos_1, pontos_2 = 0 , 0
#------------
touch_token = 0
ball_max_speed_y = 20
ball_radius = 20
player_size = 150  #y_side
player_half_size = player_size/2
player1 = player(screen, 'blue' , 20, player_size , 180,1,"rect")
ball1 = ball(screen,'red',ball_radius)
ball1_rect = ball1.rect

def win(pontos_1,pontos_2, played_snd):
        match(pontos_1):
            case 3:
                if played_snd == True:
                    victory.play()
                return "PLAYER 1 WINS",True
        match(pontos_2):
            case 3:
                if players == 0:
                    if played_snd == True:
                        lose.play()
                    return "BOT WINS",True
                if played_snd == True:
                    victory.play()
                return "PLAYER 2 WINS",True
        return '' , False

win_font = pygame.font.SysFont('Comic Sans MS', 70)    #----->fazer função cria texto
finish_text = win_font.render("Press SPACE to EXIT", True, (90, 100, 240))
finish_text_ln_2 = win_font.render("Press BACKSPACE to RESTART", True, (90, 100, 240))
choose_player_text = win_font.render("Press 0 for 1p or 1 for 2p", True, (90, 100, 240))
#--------------------
running = True
choose_player = True
game = False
while running:
    while choose_player:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                choose_player = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    players = 0
                    opponent = player(screen, 'White' , 20, player_size , 1100,0,"rect")
                    choose_player = False
                    game = True
                elif event.key == pygame.K_1:
                    players = 1
                    opponent = player(screen, 'orange' , 20, player_size , 1100,2,"rect")
                    choose_player = False
                    game = True

        screen.fill("black")
        screen.blit(choose_player_text, (50,240))
        pygame.display.flip()
        clock.tick(60)
        
      
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game = False    
            elif win(pontos_1,pontos_2, p_snd)[1] and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                    game = False
                elif event.key == pygame.K_BACKSPACE:
                    game = False
                    pontos_1, pontos_2 = 0 , 0
                    choose_player = True

                
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")      

        

        if not win(pontos_1,pontos_2,p_snd )[1]:
            #Bola
            ball1.atualize(dt, (WIDTH, HEIGHT))
            #jogadores e BOT - ATUALIZE
            player1.atualize(dt, (WIDTH, HEIGHT) , 1 , ball1.player_pos.y , ball1.player_pos.x)
            if players == 0:
                opponent.atualize(dt, (WIDTH, HEIGHT) , 0 , ball1.player_pos.y , ball1.player_pos.x,) #bot
            if players == 1:
                opponent.atualize(dt, (WIDTH, HEIGHT) , 2 , ball1.player_pos.y , ball1.player_pos.x) #player 2
            #colisão
            if pygame.Rect.colliderect(ball1_rect, player1.rect) and touch_token == 0:
                if abs(abs(player1.player_pos.y) - abs(ball1.player_pos.y)) >= player_half_size + ball_radius + 5:
                    if ball1.player_pos.y > player1.player_pos.y and ball1.ball_vel_y < 0\
                    or ball1.player_pos.y < player1.player_pos.y and ball1.ball_vel_y > 0:
                        ball1.ball_vel_y *= -1
                if player1.player_pos.y > last_player1_pos or player1.player_pos.y < last_player1_pos :
                    ball1.ball_vel_y +=  player1.player_pos.y - last_player1_pos
                ball1.ball_vel_x *= -1
                touch_token = 15
                coll_snd.play() #play collision sound
            if pygame.Rect.colliderect(ball1_rect, opponent.rect) and touch_token == 0: 
                if abs(abs(opponent.player_pos.y) - abs(ball1.player_pos.y)) >= player_half_size + ball_radius + 5:
                    if ball1.player_pos.y > opponent.player_pos.y and ball1.ball_vel_y > 0\
                    or ball1.player_pos.y < opponent.player_pos.y and ball1.ball_vel_y < 0:
                        ball1.ball_vel_y *= -1
                if opponent.player_pos.y > last_opponent_pos or opponent.player_pos.y < last_opponent_pos:
                    ball1.ball_vel_y +=  opponent.player_pos.y > last_opponent_pos
                ball1.ball_vel_x *= -1
                touch_token = 15
                coll_snd.play()  #play collision sound


            if touch_token > 0:
                touch_token -= 1

            #pontuação
            if ball1.player_pos.x >= 1280 - ball_radius:
                pontos_1 += 1   
            if ball1.player_pos.x <=  ball_radius:
                pontos_2 += 1    
            placar.placar(screen , pontos_1, pontos_2)
            #guarda a posição anterior, usado na colisão
            last_player1_pos = player1.player_pos.y 
            last_opponent_pos = opponent.player_pos.y

        #win
        if win(pontos_1,pontos_2, p_snd)[1]:
            win_text = win_font.render(win(pontos_1, pontos_2, p_snd)[0], True, (90, 100, 240))
            screen.blit(win_text, (50,240))
            screen.blit(finish_text, (50,440))
            screen.blit(finish_text_ln_2, (50,540))
            p_snd = False
        # flip() adiciona os programa à tela
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()