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
        self.movement_keys = [[None],\
                              [pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d], \
                              [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT]]
        self.player_pos = pygame.Vector2(posit_x ,screen.get_height() / 2)
        self.rect = pygame.Rect(self.player_pos.x,self.player_pos.y,size_x,size_y)
    #FUNÇÂO DE MOVIMENTO----> MODIFICAR PARA ADEQUAR O BOT
    def move(self, movement_keys ,  keys, dt, player_num, ball_pos_y , ball_pos_x ): 
        if player_num == 0:
            if self.player_pos.y > ball_pos_y and ball_pos_x < self.player_pos.x:
                self.player_pos.y -= 900 *dt
            elif self.player_pos.y < ball_pos_y and ball_pos_x < self.player_pos.x:
                self.player_pos.y += 900 *dt
        else:
            if keys[movement_keys[0]]:
                self.player_pos.y -= 900 *dt
            if keys[movement_keys[1]]:
                self.player_pos.y += 900 *dt
            #if keys[movement_keys[2]]:
            #    self.player_pos.x -= 600 *dt
            #if keys[movement_keys[3]]:
            #    self.player_pos.x += 600 *dt
    
    def atualize(self,dt, tela:tuple,player_num ,ball_pos_y , ball_pos_x):
        keys = pygame.key.get_pressed()

        self.move( self.movement_keys[self.player_num], keys, dt, player_num, ball_pos_y, ball_pos_x )
        
        #BORDAS_X
        #if self.player_pos.x <= 0 :
        #    self.player_pos.x = 0 
        #if self.player_pos.x >= tela[0] - self.size_x:
        #    self.player_pos.x = tela[0] - self.size_x
        #BORDAS_X
        if self.player_pos.y <= 0 :
            self.player_pos.y = 0 
        if self.player_pos.y >= tela[1] - self.size_y:
            self.player_pos.y = tela[1] - self.size_y
        #para a colisão
        self.rect.x = self.player_pos.x
        self.rect.y = self.player_pos.y
        #DESENHA O PLAYER
        pygame.draw.rect(self.screen,self.color , [self.player_pos.x, self.player_pos.y , self.size_x, self.size_y])