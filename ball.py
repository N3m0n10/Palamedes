import pygame
import math
import colorsys

class ball():

    def __init__(self,screen, color, radius):
        self.screen = screen
        self.color = color
        self.radius = radius

        self.ball_vel = 0

        #color
        self.hue = 0
        self.twopi = 2*math.pi #otimizar para nao ficar sempre calculando isso

        self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
   
    
    def atualize(self,dt, tela:tuple):
        keys = pygame.key.get_pressed()

        #otimizar com o 'if key_down'
        if keys[pygame.K_w]:
            self.player_pos.y -= 300 *dt
        if keys[pygame.K_s]:
            self.player_pos.y += 300 *dt
        if keys[pygame.K_a]:
            self.player_pos.x -= 300 *dt
        if keys[pygame.K_d]:
            self.player_pos.x += 300 *dt

        #change color
        if keys[pygame.K_o]:
            self.hue += 0.01
            if self.hue > 360:
                self.hue = 0
            color = colorsys.hsv_to_rgb(self.hue,1,1)
            color2 = (color[0]*255,color[1]*255,color[2]*255)
            self.color = color2
            
            

        if self.player_pos.x <= 0:
            self.player_pos.x = 0 + self.radius
        if self.player_pos.x >= tela[0]:
            self.player_pos.x = tela[0] - self.radius


        if self.player_pos.y <= 0:
            self.player_pos.y = 0 + self.radius
        if self.player_pos.y >= tela[1]:
            self.player_pos.y = tela[1] -  self.radius



        pygame.draw.circle(self.screen,self.color, self.player_pos, self.radius)

        