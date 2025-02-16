import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pinball Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Ball properties
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 5 * random.choice([-1, 1])
ball_dy = 5 * random.choice([-1, 1])

# Flipper properties
flipper_width = 100
flipper_height = 20
left_flipper_x = 100
right_flipper_x = WIDTH - 100 - flipper_width
flipper_y = HEIGHT - 50
flipper_speed = 10

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses
    keys = pygame.key.get_pressed()

    # Move flippers
    if keys[pygame.K_LEFT]:
        left_flipper_x -= flipper_speed
    if keys[pygame.K_RIGHT]:
        right_flipper_x += flipper_speed
    if keys[pygame.K_UP]:
        right_flipper_x -= flipper_speed
    if keys[pygame.K_DOWN]:
        left_flipper_x += flipper_speed

    # Ball movement
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with walls
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_dx *= -1
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
        ball_dy *= -1

    # Ball collision with flippers
    if (ball_y + ball_radius >= flipper_y and
        (left_flipper_x <= ball_x <= left_flipper_x + flipper_width or
         right_flipper_x <= ball_x <= right_flipper_x + flipper_width)):
        ball_dy *= -1

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    pygame.draw.rect(screen, GREEN, (left_flipper_x, flipper_y, flipper_width, flipper_height))
    pygame.draw.rect(screen, GREEN, (right_flipper_x, flipper_y, flipper_width, flipper_height))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()