
import pygame
import math
import random

class Galaxy():
    def __init__(self, screen):
        self.angle = 0
        self.screen = screen
        # Gera alguns blocos em 3D
        self.blocks = []
        for _ in range(20):
            x = random.randint(-200, 200)
            y = random.randint(-200, 200)
            z = random.randint(-50, 50)
            self.blocks.append([x, y, z])

    # Função de projeção isométrica
    def iso_projection(self,x, y, z):
        X = x - y
        Y = (x + y) / 2 - z
        return int(pygame.display.get_window_size()[0]//2 + X), int(pygame.display.get_window_size()[1]//2 + Y)  # centraliza na tela

    def run(self):
        self.screen.fill((10, 20, 40))  # fundo azulado estilo PS2
        self.angle += 0.01

        for b in self.blocks:
            x, y, z = b
            # Pequena rotação para dar vida
            rx = x * math.cos(self.angle) - y * math.sin(self.angle)
            ry = x * math.sin(self.angle) + y * math.cos(self.angle)
            
            X, Y = self.iso_projection(rx, ry, z)
            size = max(5, 20 - z)  # tamanho muda levemente com a profundidade 
            color = (100, 150, 255, 80)
            
            pygame.draw.rect(self.screen, color, (X, Y, size, size))


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    galax = Galaxy(screen)


    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        galax.run()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
