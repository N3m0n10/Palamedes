import pygame

screen = pygame.display.set_mode((800, 600))

class Plunger(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, mass, k, damping):
        # Spring properties
        self.original_image = pygame.Surface((width, height))#pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.equilibrium_y = y  # Resting position
        self.mass = mass
        self.k = k  # Spring constant (stiffness)
        self.damping = damping  # Energy loss factor (0.0-1.0)
        self.rect.x = x
        self.rect.y = y

        # State variables
        self.velocity = 0
        self.displacement = 0  # x in Hooke's Law
        self.is_pulling = False

    def update(self, keys, dt):
        # Holding SPACE: Pull the plunger
        if keys[pygame.K_SPACE]:
            if not self.is_pulling:
                self.is_pulling = True
            # Accumulate displacement (cap at max pull)
            self.displacement = min(self.displacement + 5, 300)  # Max pull = 300 pixels
        else:
            if self.is_pulling:
                # Release: Apply spring force
                self.velocity = -self.displacement * (self.k / self.mass)  # Initial velocity
                self.is_pulling = False
            # Physics when released
            if abs(self.velocity) > 0.001:  # Prevent micro-jitter
                # Spring force (Hooke's Law)
                force = -self.k * self.displacement
                # Damping (energy loss)
                force -= self.velocity * self.damping
                # Newton's Second Law
                acceleration = force / self.mass
                # Update velocity and displacement
                self.velocity += acceleration * dt
                self.displacement += self.velocity * dt
            else:
                # Reset to equilibrium
                self.velocity = 0
                self.displacement = 0
        if self.displacement < -50:
            self.displacement = -50

        # Update plunger position
        self.rect.y = self.equilibrium_y + self.displacement

    def draw(self, surface):
        # Draw plunger
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

    def collide_plunger(self, other):
        # Check for collision with other sprite
        if self.rect.colliderect(other.rect):
            # Apply collision response
            other.velocity = self.velocity //200

    


class ball(pygame.sprite.Sprite):
    def __init__(self, radius):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        print(self.rect)
        print(self.rect.center)
        self.radius = radius
        self.velocity = 0
    def actualize(self):
        self.rect.centery += self.velocity
        pygame.draw.circle(screen, (255, 0, 0), self.rect.center, self.radius)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.center = (100,230)

# Example usage in game loop
plunger = Plunger(
    x=100, y=200, width=20, height=7,
    mass=1.0, k=7, damping=0.5
)

ball_1 = ball(10)



#ball = 
#balls_sprites = pygame.SpriteGroup(ball)
#scenary_sprites = pygame.sprite.Group()
#flipper_sprites = pygame.sprite.Group()



clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))
    keys = pygame.key.get_pressed()
    plunger.collide_plunger(ball_1)
    plunger.update(keys, dt)
    ball_1.move(keys)
    ball_1.actualize()
    plunger.draw(screen)
    pygame.display.flip()
    if ball_1.rect.center[1] < 20:
        ball_1.velocity = 0
    print(ball_1.rect.center)

    # Draw plunger and ball here...
pygame.quit()