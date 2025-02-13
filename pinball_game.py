import pygame
pygame.init()

screen = pygame.display.set_mode((1024, 720))
clock = pygame.time.Clock()

class Flipper(pygame.sprite.Sprite):
    def __init__(self, image_path, screen_pivot, local_pivot, angle=0):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        self.screen_pivot = screen_pivot
        self.local_pivot = local_pivot
        self.offset = pygame.math.Vector2(local_pivot)/2 - pygame.math.Vector2(self.rect.center)/2
        
        self.angle = angle
        self.rotate(angle)

    def rotate(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle,0.5)
        rotated_offset = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center=self.screen_pivot + rotated_offset)

class ball(pygame.sprite.Sprite):
    def __init__(self, radius):
        super().__init__()
        self.image = pygame.surface((10, 10))
        self.rect = self.image.get_rect()
        self.radius = radius

    def actualize(self):
        pygame.draw.circle(screen, (255, 0, 0), self.rect.center, self.radius)

# Create flippers
local_pivot = (215, 80)  
left_flipper = Flipper("assets/sprites/pinball/flipper.png", (350, 504), local_pivot)  #change for flipping the image later
right_flipper = Flipper("assets/sprites/pinball/flipper.png", (650, 500), local_pivot)

all_sprites = pygame.sprite.Group(left_flipper, right_flipper)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        left_flipper.rotate(20)  # Rotate left flipper up
    else:
        left_flipper.rotate(40)
    if keys[pygame.K_d]:
        right_flipper.rotate(-110)  # Rotate right flipper up
    else:
        right_flipper.rotate(-130)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()