import pygame
from ball import ball
from player import player
import math

###pygame setup
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 1280,720 #largura e altura
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mixer.init() #sound function
coll_snd = pygame.mixer.Sound('assets/sounds/collide_pong.mp3')#collision sound file  
lose = pygame.mixer.Sound('assets/sounds/lose.mp3') 
victory= pygame.mixer.Sound('assets/sounds/victory.mp3')
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
show_fps = False

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

def placar(screen, pontos_1 , pontos_2, pos_1 = (380,100), pos_2 = (900,100)): #make arg
    text_placar_font = pygame.font.SysFont('tahoma', 100) 
    text_placar1 = text_placar_font.render(f'{pontos_1}', True, ('White'))
    text_placar2 = text_placar_font.render(f'{pontos_2}', True, ('White'))
    screen.blit(text_placar1,pos_1)
    screen.blit(text_placar2,pos_2)
    p1_points_rect = text_placar1.get_rect(topleft = pos_1)
    op_points_rect = text_placar1.get_rect(topleft = pos_2)
    return p1_points_rect , op_points_rect

class FPS:
    def __init__(self,clock):
        self.font = pygame.font.SysFont('arial', 20) 
        self.value = "init"
        self.text = self.font.render(f'{self.value}')
        self.rect = self.text.get_rect(0,20,20,20)
        self.clock = clock

    def display(self,valid,surf):
        if valid:
            self.text = clock.get_fps
            surf.blit(self.text)
            pygame.display.update(self.rect)

class FPS:
    def __init__(self, clock): 
        self.clock = clock
    
    def display(self, valid):
        """Display the FPS counter if show is True"""
        if valid:
            pygame.display.set_caption(f"FPS: {round(clock.get_fps(), 1)}")

fps = FPS(clock)


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
                opponent = player(screen, (255, 255, 255), 20, player_size, 1100, 0, "rect")
                choose_player = False
                game = True
                # Clear everything completely
                screen.fill((0, 0, 0))  # Use RGB tuple for black
                pygame.display.flip()  # Full screen update
                continue  
            elif event.key == pygame.K_1:
                players = 1
                opponent = player(screen, (255, 165, 0), 20, player_size, 1100, 2, "rect")  # Orange
                choose_player = False
                game = True
                # Clear everything completely
                screen.fill((0, 0, 0))
                pygame.display.flip()
                continue

    # Only draw selection screen if still choosing
    if choose_player:
        screen.fill((0, 0, 0))
        screen.blit(choose_player_text, (50, 240))
        pygame.display.flip()  # Or use pygame.display.update(choose_player_text.get_rect(topleft=(50, 240))) for partial update
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    show_fps = not show_fps

                
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")      

        fps.display(show_fps)        

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
            # In your collision detection code:
            if touch_token == 0:
                # Player 1 collision
                if ball1_rect.colliderect(player1.rect):
                    # Calculate relative intersection point (-1 to 1)
                    relative_intersect_y = (player1.rect.centery - ball1_rect.centery) / (player1.rect.height/2)
                    
                    # Calculate bounce angle (limited to 75 degrees)
                    bounce_angle = relative_intersect_y * (5*math.pi/12)
                    
                    # Maintain consistent speed while changing direction
                    current_speed = math.sqrt(ball1.ball_vel_x**2 + ball1.ball_vel_y**2)
                    ball1.ball_vel_x = abs(current_speed * math.cos(bounce_angle))  # Always bounce right
                    ball1.ball_vel_y = -current_speed * math.sin(bounce_angle)
                    
                    # Add paddle velocity influence (dampened)
                    paddle_velocity = (player1.player_pos.y - last_player1_pos) * 0.3
                    ball1.ball_vel_y += paddle_velocity
                    
                    touch_token = 15
                    coll_snd.play()
                
                # Opponent collision (mirrored)
                elif ball1_rect.colliderect(opponent.rect):
                    relative_intersect_y = (opponent.rect.centery - ball1_rect.centery) / (opponent.rect.height/2)
                    bounce_angle = relative_intersect_y * (5*math.pi/12)
                    
                    current_speed = math.sqrt(ball1.ball_vel_x**2 + ball1.ball_vel_y**2)
                    ball1.ball_vel_x = -abs(current_speed * math.cos(bounce_angle))  # Always bounce left
                    ball1.ball_vel_y = -current_speed * math.sin(bounce_angle)
                    
                    paddle_velocity = (opponent.player_pos.y - last_opponent_pos) * 0.3
                    ball1.ball_vel_y += paddle_velocity
                    
                    touch_token = 15
                    coll_snd.play() #play collision sound

            touch_token = max(0, touch_token - 1)

            #pontuação
            if ball1.player_pos.x >= 1280 - ball_radius:
                pontos_1 += 1   
            if ball1.player_pos.x <=  ball_radius:
                pontos_2 += 1    
            rect_score_1 , rect_socre_2 = placar(screen , pontos_1, pontos_2)
            #guarda a posição anterior, usado na colisão
            last_player1_pos = player1.player_pos.y 
            last_opponent_pos = opponent.player_pos.y

            # update elements
            pygame.display.update(rect_score_1)
            pygame.display.update(rect_socre_2)
            #pygame.display.update(ball1.rect.inflate(100,100))
            ball1.update()
            pygame.display.update((player1.posit_x -5,0,player_size + 5, HEIGHT))
            pygame.display.update((opponent.posit_x -5,0,player_size + 5, HEIGHT))

        #win
        if win(pontos_1,pontos_2, p_snd)[1]:
            win_text = win_font.render(win(pontos_1, pontos_2, p_snd)[0], True, (90, 100, 240))
            screen.blit(win_text, (50,240))
            screen.blit(finish_text, (50,440))
            screen.blit(finish_text_ln_2, (50,540))
            pygame.display.flip()
            p_snd = False

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()