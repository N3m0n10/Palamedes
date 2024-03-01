import pygame


class ball():
    def __init__(self,screen, color, radius):
        self.screen = screen
        self.color = color
        self.radius = radius

        self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    def atualize(self,dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_pos.y -= 300 *dt
        if keys[pygame.K_s]:
            self.player_pos.y += 300 *dt
        if keys[pygame.K_a]:
            self.player_pos.x -= 300 *dt
        if keys[pygame.K_d]:
            self.player_pos.x += 300 *dt


        pygame.draw.circle(self.screen,self.color, self.player_pos, self.radius)
