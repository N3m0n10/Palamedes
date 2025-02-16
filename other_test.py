import pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Game states
reset_ball = True
scroll_offset = 0
gravity = 0.5

class Flipper(pygame.sprite.Sprite):
    def __init__(self, pos, is_right=False):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=pos)
        self.base_angle = -30 if is_right else 30
        self.angle = self.base_angle

    def update(self, active):
        self.angle = self.base_angle * 0.6 if active else self.base_angle
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = rotated_image.get_rect(center=self.rect.center)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (15, 15), 15)
        self.rect = self.image.get_rect(center=(500, 500))
        self.velocity = pygame.math.Vector2(0, 0)
        self.world_y = 500

    def update(self, dt):
        global scroll_offset, reset_ball
        
        if not reset_ball:
            self.velocity.y += gravity
            self.world_y += self.velocity.y
            self.rect.centery = self.world_y - scroll_offset
            
            # Keep ball in view
            if self.rect.centery < SCREEN_HEIGHT * 0.3:
                scroll_offset -= SCREEN_HEIGHT * 0.3 - self.rect.centery
            elif self.rect.centery > SCREEN_HEIGHT * 0.7:
                scroll_offset += self.rect.centery - SCREEN_HEIGHT * 0.7
                
            # Basic floor collision
            if self.world_y > 2500:
                reset_ball = True
                self.velocity = pygame.math.Vector2(0, 0)
                self.world_y = 500
                self.rect.center = (500, 500)
        else:
            self.rect.center = (500, 500 - scroll_offset)

# Game setup
flippers = pygame.sprite.Group(
    Flipper((350, 600)),
    Flipper((674, 600), is_right=True)
)
ball = Ball()

running = True
while running:
    dt = clock.tick(60) / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if reset_ball:
                reset_ball = False
                ball.velocity = pygame.math.Vector2(0, -15)

    keys = pygame.key.get_pressed()
    for flipper in flippers:
        flipper.update(keys[pygame.K_a] or keys[pygame.K_d])

    screen.fill((0, 0, 0))
    
    # Draw game elements
    ball.update(dt)
    flippers.draw(screen)
    screen.blit(ball.image, ball.rect)
    
    pygame.display.flip()

pygame.quit()