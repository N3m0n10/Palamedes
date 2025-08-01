import pygame
import colorsys

class player():

    def __init__(self,screen, color, size_x, size_y, posit_x, player_num,format,move_type = "vertical",posit_y = None):  #plan to change for format = "rect"
        ##VAR
        self.move_type = move_type
        self.format = format
        self.screen = screen
        self.color = color
        self.size_x = size_x
        self.size_y = size_y
        self.posit_x = posit_x
        self.player_num = player_num
        self.movement_keys = [[None],\
                              [pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d], \
                              [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT]]
        if posit_y == None:
            self.player_pos = pygame.Vector2(posit_x ,screen.get_height() / 2)
        else:
            self.player_pos = pygame.Vector2(posit_x ,posit_y)
        self.rect = pygame.Rect(self.player_pos.x,self.player_pos.y,size_x,size_y)
    ##FUNÇÂO DE MOVIMENTO----> MODIFICAR PARA ADEQUAR O BOT
    
    def move(self, movement_keys ,  keys, dt, player_num, ball_pos_y, ball_pos_x,predicted_pos_y = None): 

        ##BOT config --- FOLLOW BALL 
        if player_num == 0:
           
            if ball_pos_y > self.player_pos.y :
                self.player_pos.y += 900 *dt
            elif ball_pos_y < self.player_pos.y :
                self.player_pos.y -= 900 *dt
        
        ##PLAYERS MOVE --- RESTRICTED TO VERTICAL    
        else:
            if self.move_type == "vertical":
                if keys[movement_keys[0]]:
                    self.player_pos.y -= 900 *dt
                if keys[movement_keys[1]]:
                    self.player_pos.y += 900 *dt
            elif self.move_type == "horizontal":
                if keys[movement_keys[2]]:
                    self.player_pos.x -= 600 *dt
                if keys[movement_keys[3]]:
                    self.player_pos.x += 600 *dt
            elif self.move_type == "full":
                if keys[movement_keys[0]]:
                    self.player_pos.y -= 900 *dt
                if keys[movement_keys[1]]:
                    self.player_pos.y += 900 *dt
                if keys[movement_keys[2]]:
                    self.player_pos.x -= 600 *dt
                if keys[movement_keys[3]]:
                    self.player_pos.x += 600 *dt
    
    def atualize(self,dt, tela:tuple,player_num ,ball_pos_y = None , ball_pos_x = None):
        keys = pygame.key.get_pressed()

        if self.format == "rect":  ## TODO: Problably tried using for arc_pong, check and delete
            self.move( self.movement_keys[self.player_num], keys, dt, player_num, ball_pos_y, ball_pos_x )
        
        #BORDAS_X
        if self.player_pos.x <= 0 :
            self.player_pos.x = 0 
        if self.player_pos.x >= tela[0] - self.size_x:
            self.player_pos.x = tela[0] - self.size_x
        #BORDAS_Y
        if self.player_pos.y <= 0 :
            self.player_pos.y = 0 
        if self.player_pos.y >= tela[1] - self.size_y:
            self.player_pos.y = tela[1] - self.size_y
        #para a colisão
        self.rect.x = self.player_pos.x
        self.rect.y = self.player_pos.y
        #DESENHA O PLAYER
        if self.format == "rect":
            pygame.draw.rect(self.screen,self.color , self.rect)

    def change_size(self, size_x, size_y):
        self.rect.width = size_x   #inflate() and other methods # -> https://www.pygame.org/docs/ref/rect.html
        self.rect.height = size_y
        self.size_x = size_x
        self.size_y = size_y

    def change_color(self, color_chng_input):
        self.color = color_chng_input

    def Glowing(self):
        self.hue += 0.05
        if self.hue > 1:
            self.hue = 0
        color = colorsys.hsv_to_rgb(self.hue,1,1)
        color2 = (color[0]*255,color[1]*255,color[2]*255)
        self.color = color2

    def set_pos(self,x,y):
        self.player_pos.x = x
        self.player_pos.y = y
        