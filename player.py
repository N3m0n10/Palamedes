import pygame


class player():

<<<<<<< HEAD
    def __init__(self,screen, color, radius, posit_y):
=======
    def __init__(self,screen, color, radius, posit_x):
>>>>>>> Player
        self.screen = screen
        self.color = color
        self.radius = radius

        self.player_vel = 0


<<<<<<< HEAD
        self.player_pos = pygame.Vector2(screen.get_width() / 2, posit_y)
=======
        self.player_pos = pygame.Vector2(posit_x ,screen.get_height() / 2)
>>>>>>> Player

    def atualize(self,dt, tela:tuple):
        keys = pygame.key.get_pressed()

        #otimizar com o 'if key_down'
<<<<<<< HEAD
        #if keys[pygame.K_UP]:
        #    self.player_pos.y -= 300 *dt
        #if keys[pygame.K_DOWN]:
        #    self.player_pos.y += 300 *dt
=======
        if keys[pygame.K_UP]:
            self.player_pos.y -= 300 *dt
        if keys[pygame.K_DOWN]:
            self.player_pos.y += 300 *dt
>>>>>>> Player
        if keys[pygame.K_LEFT]:
            self.player_pos.x -= 300 *dt
        if keys[pygame.K_RIGHT]:
            self.player_pos.x += 300 *dt

        
   
        if self.player_pos.x <= 0 + self.radius:
            self.player_pos.x = 0 + self.radius
        if self.player_pos.x >= tela[0] - self.radius:
            self.player_pos.x = tela[0] - self.radius


<<<<<<< HEAD
        #if self.player_pos.y <= 0 + self.radius:
        #    self.player_pos.y = 0 + self.radius
        #if self.player_pos.y >= tela[1] - self.radius:
        #    self.player_pos.y = tela[1] - self.radius
=======
        if self.player_pos.y <= 0 + self.radius:
            self.player_pos.y = 0 + self.radius
        if self.player_pos.y >= tela[1] - self.radius:
            self.player_pos.y = tela[1] - self.radius
>>>>>>> Player



        pygame.draw.circle(self.screen,self.color, self.player_pos, self.radius)