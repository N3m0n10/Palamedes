import pygame
import math
import colorsys
import random

class ball():

    def __init__(self,screen, color, radius):

        self.screen = screen
        self.color = color
        self.radius = radius

        self.ball_vel_x = random.randint(6,20)
        self.ball_vel_y = random.randint(6,20) 

        self.ball_max_speed = 20

        #color
        self.hue = 0
        self.twopi = 2*math.pi #otimizar para nao ficar sempre calculando isso
        
        #self.player_pos = pygame.Vector2(random.randint(0,screen.get_width()),random.randint(0,screen.get_width())) 
        self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

        #pra area estar no mesmo lugar do desenho
        self.rect = pygame.Rect(self.player_pos.x,self.player_pos.y,radius,radius)
    
    def atualize(self,dt, tela:tuple):
        
        #mobilidade
        self.player_pos.x += self.ball_vel_x
        self.player_pos.y += self.ball_vel_y

        if self.player_pos.x <= 0 + self.radius:
            self.player_pos.x = 0 + self.radius
            self.ball_vel_x =   self.ball_vel_x * -1

        if self.player_pos.x >= tela[0] - self.radius:
            self.player_pos.x = tela[0] - self.radius
            self.ball_vel_x = self.ball_vel_x * -1

        if self.player_pos.y <= 0 + self.radius:
            self.player_pos.y = 0 + self.radius
            self.ball_vel_y = self.ball_vel_y * -1

        if self.player_pos.y >= tela[1] - self.radius:
            self.player_pos.y = tela[1] - self.radius
            self.ball_vel_y = self.ball_vel_y * -1

        #to utilizando o rect para testar colisao   
        self.rect.x = self.player_pos.x
        self.rect.y = self.player_pos.y

        pygame.draw.circle(self.screen,self.color, self.player_pos, self.radius)
        #limite de velocidade da bola
        if abs(self.ball_vel_y) > self.ball_max_speed:
            if self.ball_vel_y > 0:
                self.ball_vel_y = self.ball_max_speed
            else: self.ball_vel_y = self.ball_max_speed* - 1


    def changeColor(self):
        self.hue += 0.05
        if self.hue > 1:
            self.hue = 0
        color = colorsys.hsv_to_rgb(self.hue,1,1)
        color2 = (color[0]*255,color[1]*255,color[2]*255)
        self.color = color2