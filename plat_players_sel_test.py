import pygame

pygame.init()

###hand_position
###select card
###append and remove card
###move card

HEIGHT, WIDTH = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
card = pygame.image.load('assets/LAUNCH_CARDS/pirate_boat_plataform_card.png')
clock = pygame.time.Clock()
factor = 0.2


hand_position = (WIDTH*0.3, HEIGHT*0.66)  ###initial card position
card_pos = hand_position
drag = False

class cards:
    def __init__(self, card,):#types #list for positioning
        self.card = card
        self.card_pos = hand_position
        self.factor = factor

    def resize(self):
        pass 

    def position(self):
        pass

    def draw(self):
        screen.blit(pygame.transform.scale_by(self.card, self.factor), self.card_pos)
        

running = True
while running:
    card_rect = card.get_rect(left=card_pos[0], top=card_pos[1])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #for i,j in enumerate cards list --->  use index to select card
        if card_rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                drag = True
            
        if event.type == pygame.MOUSEBUTTONUP:
            drag = False
                
    if card_rect.collidepoint(pygame.mouse.get_pos()):
        if factor < 0.21:
            factor += 0.0003
    else:
        if not drag:
            if factor > 0.2:
                factor -= 0.001
            card_pos = hand_position           

    if drag:
        card_pos = pygame.mouse.get_pos()

    screen.fill((30,30,30))
    screen.blit(pygame.transform.scale_by(card, factor), card_pos)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
