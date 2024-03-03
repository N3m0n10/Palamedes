import pygame


class player():

    def __init__(self,screen, color, size_x, size_y, posit_x):
        self.screen = screen
        self.color = color
        self.size_x = size_x
        self.size_y = size_y
        self.posit_x = posit_x

        
        #self.player_vel = 0

        self.player_pos = pygame.Vector2(posit_x ,screen.get_height() / 2)


    def atualize(self,dt, tela:tuple):
        keys = pygame.key.get_pressed()

        #otimizar com o 'if key_down'
        if keys[pygame.K_UP]:
            self.player_pos.y -= 300 *dt
        if keys[pygame.K_DOWN]:
            self.player_pos.y += 300 *dt
        if keys[pygame.K_LEFT]:
            self.player_pos.x -= 300 *dt
        if keys[pygame.K_RIGHT]:
            self.player_pos.x += 300 *dt

        
        #BORDAS---------------------------------------
        if self.player_pos.x <= 0 + self.size_x:
            self.player_pos.x = 0 + self.size_x
        if self.player_pos.x >= tela[0] - self.size_x:
            self.player_pos.x = tela[0] - self.size_x


        if self.player_pos.y <= 0 :
            self.player_pos.y = 0 
        if self.player_pos.y >= tela[1] - self.size_y:
            self.player_pos.y = tela[1] - self.size_y



        pygame.draw.rect(self.screen,self.color , [self.player_pos.x, self.player_pos.y , self.size_x, self.size_y])