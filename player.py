import pygame


class player():

    def __init__(self,screen, color, size_x, size_y, posit_x, player_num):
        #VAR___________________________________________________________________________
        self.screen = screen
        self.color = color
        self.size_x = size_x
        self.size_y = size_y
        self.posit_x = posit_x
        self.player_num = player_num
        self.player_speed = 0
        self.movement_keys = [[pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d], \
                              [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT]]
        self.player_pos = pygame.Vector2(posit_x ,screen.get_height() / 2)
        #_______________________________________________________________________________
    #FUNÇÂO DE MOVIMENTO----> MODIFICAR PARA ADEQUAR O BOT
    def move(self, movement_keys ,  keys, dt, player_num, ball_pos_y , ball_speed_y): 
        if player_num == 0:
            if self.player_pos.y != ball_pos_y:
                self.player_speed = ball_speed_y
        else:
            if keys[movement_keys[0]]:
                self.player_pos.y -= 300 *dt
            if keys[movement_keys[1]]:
                self.player_pos.y += 300 *dt
            if keys[movement_keys[2]]:
                self.player_pos.x -= 300 *dt
            if keys[movement_keys[3]]:
                self.player_pos.x += 300 *dt
    
    def atualize(self,dt, tela:tuple,player_num ,ball_pos_y , ball_speed_y):
        keys = pygame.key.get_pressed()

        self.move( self.movement_keys[self.player_num], keys, dt, player_num, ball_pos_y , ball_speed_y)
        
        #MOVIMENTO BOT
        self.player_pos.y += self.player_speed
        
        #BORDAS_X
        if self.player_pos.x <= 0 :
            self.player_pos.x = 0 
        if self.player_pos.x >= tela[0] - self.size_x:
            self.player_pos.x = tela[0] - self.size_x
        #BORDAS_X
        if self.player_pos.y <= 0 :
            self.player_pos.y = 0 
        if self.player_pos.y >= tela[1] - self.size_y:
            self.player_pos.y = tela[1] - self.size_y
        #DESENHA O PLAYER
        pygame.draw.rect(self.screen,self.color , [self.player_pos.x, self.player_pos.y , self.size_x, self.size_y])