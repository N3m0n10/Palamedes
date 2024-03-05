import pygame
import math
import colorsys
import random
class ball(pygame.sprite.Sprite):

    def __init__(self,screen, color, radius):

        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.color = color
        self.radius = radius

        self.ball_vel_x = random.randint(6,20)
        self.ball_vel_y = random.randint(6,20) 

        #color
        self.hue = 0
        self.twopi = 2*math.pi #otimizar para nao ficar sempre calculando isso
        
        self.player_pos = pygame.Vector2(random.randint(0,screen.get_width()),random.randint(0,screen.get_width()))
        #self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

        #pra area estar no mesmo lugar do desenho
        self.rect = pygame.Rect(self.player_pos.x,self.player_pos.y,radius,radius)

    
    def atualize(self,dt, tela:tuple):
        
        #mobilidade
        self.player_pos.x += self.ball_vel_x
        self.player_pos.y += self.ball_vel_y
        
        #por enquanto só ta sendo utilizado agora para alterar a cor da bola com um botão
        #keys = pygame.key.get_pressed()
        
        #change color
       

        if self.player_pos.x <= 0:
            self.player_pos.x = 0 + self.radius
            self.ball_vel_x =   self.ball_vel_x * -1

            self.ball_vel_x =   self.ball_vel_x * -1

        if self.player_pos.x >= tela[0]:
            self.player_pos.x = tela[0] - self.radius
            self.ball_vel_x = self.ball_vel_x * -1
            self.ball_vel_x = self.ball_vel_x * -1


        if self.player_pos.y <= 0:
            self.player_pos.y = 0 + self.radius
            self.ball_vel_y = self.ball_vel_y * -1

            self.ball_vel_y = self.ball_vel_y * -1

        if self.player_pos.y >= tela[1]:
            self.player_pos.y = tela[1] -  self.radius
            self.ball_vel_y = self.ball_vel_y * -1

        
        #to utilizando o rect para testar colizao   
        self.rect.x = self.player_pos.x
        self.rect.y = self.player_pos.y

        pygame.draw.circle(self.screen,self.color, self.player_pos, self.radius)

        
    def changeColor(self):
        self.hue += 0.05
        if self.hue > 1:
            self.hue = 0
        color = colorsys.hsv_to_rgb(self.hue,1,1)
        color2 = (color[0]*255,color[1]*255,color[2]*255)
        self.color = color2
        

    def colide(self):
        self.ball_vel_x *= -1
        self.ball_vel_y *= -1