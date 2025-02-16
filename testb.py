import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite from Surface Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Create a custom sprite class
class CustomSprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        # Create a Surface for the sprite
        self.image = pygame.Surface([width, height])
        self.image.fill(color)  # Fill the surface with a color

        # Set the rect (position and size) of the sprite
        self.rect = self.image.get_rect()

        # Set initial position
        self.rect.x = random.randint(0, WIDTH - width)
        self.rect.y = random.randint(0, HEIGHT - height)

        # Set initial velocity
        self.dx = random.choice([-3, -2, 2, 3])
        self.dy = random.choice([-3, -2, 2, 3])

    def update(self):
        # Move the sprite
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off the edges of the screen
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1

# Create a sprite group
all_sprites = pygame.sprite.Group()

# Create multiple sprites
for _ in range(10):
    sprite = CustomSprite(RED, 50, 50)  # Create a 50x50 red sprite
    all_sprites.add(sprite)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    all_sprites.update()

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()