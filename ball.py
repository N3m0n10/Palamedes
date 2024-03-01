import pygame


class ball():

    def __init__(self,screen, color, radius):
        self.screen = screen
        self.color = color
        self.radius = radius

        self.ball_vel = 0


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
            self.color = 'green'
   
        if self.player_pos.x <= 0:
            self.player_pos.x = 0 + self.radius
        if self.player_pos.x >= tela[0]:
            self.player_pos.x = tela[0] - self.radius


        if self.player_pos.y <= 0:
            self.player_pos.y = 0 + self.radius
        if self.player_pos.y >= tela[1]:
            self.player_pos.y = tela[1] -  self.radius



        pygame.draw.circle(self.screen,self.color, self.player_pos, self.radius)
