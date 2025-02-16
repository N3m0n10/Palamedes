import pygame
from math import sqrt
pygame.init()

screen = pygame.display.set_mode((1024, 720))
clock = pygame.time.Clock()
reset_ball = False
gravity = 3  #Has inclination
reset_pos = (500,500)
horizontal_relative_center = 700
#screen.blit(gabinete_surface, (0, -scroll_offset))

def reflect_and_draw():
    polygons = [[(400, 5), (450, 5), (400, 50)]]
    #tuples = []
    for polygon in polygons:
        pygame.draw.polygon(screen, (255, 0, 0), polygon)
        #pygame.transform.flip(poly, True, False) use later
        #new list
        tuples = []
        for tuplee in polygon:
            if tuplee[0] > horizontal_relative_center:
                tuplee = (horizontal_relative_center - (tuplee[0] - horizontal_relative_center), tuplee[1])
            else:
                tuplee = (tuplee[0] + (horizontal_relative_center - tuplee[0])*2, tuplee[1])
            tuples.append(tuplee)
        pygame.draw.polygon(screen, (255, 0, 0), tuples)
    #return tuples   ----> pygame.draw.polygon(screen, (255, 0, 0), tuples) make for different colors
        
    

class Display():
    def __init__(self):
        pass

class Pins(pygame.sprite.Sprite):
    pass

class Bumper(pygame.sprite.Sprite):
    pass

class Flipper(pygame.sprite.Sprite):
    def __init__(self, image_path, screen_pivot, local_pivot, angle=0):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        
        self.screen_pivot = screen_pivot
        self.local_pivot = local_pivot
        self.offset = pygame.math.Vector2(local_pivot)/5 - pygame.math.Vector2(self.rect.center)/5
        
        self.angle = angle
        self.rotate(angle)

    def rotate(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle,0.2)
        self.mask = pygame.mask.from_surface(self.image)
        rotated_offset = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center=self.screen_pivot + rotated_offset)
        ##make angle progressive

    def check_collisions(ball, flippers):
        collisions = pygame.sprite.spritecollide(
            ball, flippers, False, pygame.sprite.collide_mask
        )
        
        if collisions:
            # Simplified bounce effect
            ball.velocity.y *= -0.8
            # Add horizontal force based on flipper direction
            #TODO calculate distance from pivot to ball

class ball(pygame.sprite.Sprite):
    def __init__(self, radius,image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (radius*2, radius*2))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (500,500)
        self.radius = radius
        self.velocity = pygame.math.Vector2(0, 0)

    def actualize(self,_dt):
        global reset_ball
        if not reset_ball:
            self.velocity.y = self.velocity.y + gravity*_dt  #upwards = negative
            self.rect.center += self.velocity
        else:
            self.velocity = pygame.math.Vector2(0, 0)


    def launch(self):
        self.velocity = pygame.math.Vector2(0, -10)
        global reset_ball
        reset_ball = False


            
class box():
    def __init__(self,x1,x2,y,y2):
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.y2 = y2
        self.lines = [(x1,y),(x1,y2),(x2,y2),(x2,y)]

    def autualize(self,ball_obj,_screen):
        if ball_obj.rect.centerx < self.x1 or ball_obj.rect.centerx > self.x2:
            ball_obj.velocity.x = -ball_obj.velocity.x
        if ball_obj.rect.centery < self.y:
            ball_obj.velocity.y = -ball_obj.velocity.y
        if ball_obj.rect.centery > self.y2:
            global reset_ball
            reset_ball = True
            ball_obj.rect.center = reset_pos
        pygame.draw.lines(_screen, (255, 0, 0), True, self.lines)


            


# Create flippers
local_pivot = (215, 80)  
left_flipper = Flipper("assets/sprites/pinball/flipper.png", (640, 631), local_pivot)  #change for flipping the image later
right_flipper = Flipper("assets/sprites/pinball/flipper.png", (760, 630), local_pivot) #they aren't simetrical right now, one need to be mirrored horizontally
ball_1 = ball(5,"assets/sprites/pinball/ball.png")

all_sprites = pygame.sprite.Group(left_flipper, right_flipper,ball_1)
boxe = box(400,1000,5,700)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        left_flipper.rotate(39)  # Rotate left flipper up
    else:
        left_flipper.rotate(59)
    if keys[pygame.K_d]:
        right_flipper.rotate(-130)  # Rotate right flipper up
    else:
        right_flipper.rotate(-150)
    if keys[pygame.K_SPACE]:
        ball_1.launch()

    screen.fill((0, 0, 0))

    boxe.autualize(ball_1,screen)
    ball_1.actualize(0.02)
    all_sprites.draw(screen)
    reflect_and_draw()

    pygame.display.flip()
    clock.tick(60)
    

pygame.quit()

#todo:
#add a score system
#add a timer
#draw box
#add obstacles
#add collision for obstacles, using surface normal
#LATER --> minigames
#LATER --> add sounds