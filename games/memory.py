import pygame
from math import sqrt, ceil
from random import shuffle, randint

# TODO: Create a back image for the cards
# TODO: Create a proper dict with states, color and rcts
# TODO: Create a flip state for the cards

pygame.init()
clock = pygame.time.Clock()

frst_select, scnd_select = None, None

class Memory():
    def __init__(self, cards,card_space=20):
        self.card_space = card_space
        self.create(cards)
        self.assign_colors()

    def create(self, cards):
        if cards % 2 != 0:  # Ensure even number of cards
            cards += 1

        self.num = cards
        self.columns = ceil(sqrt(self.num))  # Better to use ceil to avoid too small grids
        self.rows = ceil(self.num / self.columns)  # Calculate rows based on columns

        # Generate card pairs and shuffle
        self.cards = [i for i in range(cards // 2) for _ in range(2)]
        shuffle(self.cards)

        # Calculate card size and spacing
        screen_width, screen_height = pygame.display.get_window_size()
        card_width = (screen_width * 0.7) // self.columns  
        card_height = (screen_height * 0.7) // self.rows    
        card_size = (card_width, card_height)  

        # Calculate margins to center the grid
        margin_x = (screen_width - (self.columns * card_size[0])) // 2 - self.columns * self.card_space // 2
        margin_y = (screen_height - (self.rows * card_size[1])) // 2 - self.rows * self.card_space // 2

        # Create card rectangles
        self.rects = []
        spacex, spacey = 0,0
        for row in range(self.rows):
            spacey = row * self.card_space
            for col in range(self.columns):
                spacex = col * self.card_space
                index = row * self.columns + col
                if index < len(self.cards):  # Only create rect if card exists
                    x = margin_x + col * card_size[0] + spacex
                    y = margin_y + row * card_size[1] + spacey
                    self.rects.append(pygame.Rect(x, y, card_size[0], card_size[1]))

    def assign_colors(self):
        self.colors = {}
        used_colors = set()
        for i in set(self.cards):
            while True:
                color = (randint(0,255), randint(0,255), randint(0,255))
                if color != (0,0,0) and color not in used_colors:
                    self.colors[i] = color
                    used_colors.add(color)
                    break

    def draw(self, screen, draw_front=True):  # arg is provisory, create fliped state for cards
        if draw_front:
            for i, rect in enumerate(self.rects):
                if i < len(self.cards):  # Only draw if card exists
                    pygame.draw.rect(screen, self.colors[self.cards[i]], rect, border_radius=10)
        else:
            for rect in self.rects:
                #screen.blit(back_image, rect)  # NOTE: create back image when starting
                pass

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Memory Game")
memo = Memory(100)  

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN  :
            for i, rect in enumerate(memo.rects):
                if rect.collidepoint(event.pos):
                    if frst_select is None:
                        frst_select = i
                        # flip card
                    elif scnd_select is None and i != frst_select:
                        scnd_select = i
                        # flip card
                        if memo.cards[frst_select] == memo.cards[scnd_select]:
                            # Correct match logic here
                            pass
                        else:
                            # Reset selections after a short delay
                            pygame.time.delay(1000)
                            frst_select, scnd_select = None, None
                        break

    screen.fill((0, 0, 0))
    memo.draw(screen,True)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
