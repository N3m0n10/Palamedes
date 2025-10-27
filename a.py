import pygame
import colorsys
import os
import sys
import random
from math import cos, sin, pi
from teste_yuri import Yuri
from utils import Text, button

# --- Data from your game_menu.py ---
game_list = ['Pong', 'Invaders', 'Snake', 'Tetris']
icon_size = (250, 140)
srfc_height = 800 # Example value
pos_list = [(x, y) for y in range(80, 500, 180) for x in range(120, 1280 - 120, 390)]

# --- Helper function for image loading ---
base_dir = os.path.dirname(os.path.abspath(__file__))
def load_image_from_subfolder(image_name, subfolder="game_thumb"):
    image_path = os.path.join(base_dir, "assets", subfolder, image_name)
    if os.path.exists(image_path):
        return pygame.image.load(image_path)
    else: # Return a placeholder if image not found
        fallback_surf = pygame.Surface(icon_size)
        fallback_surf.fill((80,80,80))
        return fallback_surf

## PYGAME_SETUP
pygame.init()
WIDTH, HEIGHT = 1280, 720 # These are now the dimensions of our VIRTUAL screen

# SC_SURFACE is the master surface we will draw everything on.
SC_SURFACE = pygame.Surface((WIDTH, HEIGHT))

# The 'screen' is the actual window the user sees, which is resizable.
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption('OGYGIA')
clock = pygame.time.Clock()
running = True

## UNIVERSAL_VAR
menu_font = pygame.font.SysFont('z003', 70)
game_list_font = pygame.font.SysFont('Tahoma', 40)
random_game_font = pygame.font.SysFont('Tahoma', 30)
background = (50, 50, 50)
estagio = 0 # 0: menu, 1: game_menu, 2: fase
hue = 0
thb_img = [] # Thumbnail images list
balls = False

# Scroll variables
scroll_offset = 0
scroll_speed = 20
scroll_limit = (srfc_height) - HEIGHT # Calculate scroll limit based on virtual height

## Main_objects
yuri = Yuri(SC_SURFACE, WIDTH, HEIGHT)
title = Text('OGYGIA', (WIDTH // 2, HEIGHT // 2), 'p052', 200, (240, 240, 240))
balls_b = button(20,20,(50,50),(125,125,0),0,45,'BALLS',font_size=10,text_color=(0,25,183))

## BASE_FUNCTIONS
def stage(estagio):
    return {0: "menu", 1: "game_menu", 2: "fase"}.get(estagio)

def changeColor(hue):
    color = colorsys.hsv_to_rgb(hue, 1, 1)
    return (color[0] * 255, color[1] * 255, color[2] * 255)

def map_mouse_to_surface():
    """
    Translates the window's mouse position to the SC_SURFACE's coordinates.
    This is the KEY to making interactions work on a scaled surface.
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    window_width, window_height = screen.get_size()
    
    scale_x = window_width / WIDTH
    scale_y = window_height / HEIGHT
    scale = min(scale_x, scale_y) # Use the smaller scale factor to maintain aspect ratio

    # Calculate the position of the scaled surface on the window
    scaled_width = WIDTH * scale
    scaled_height = HEIGHT * scale
    offset_x = (window_width - scaled_width) / 2
    offset_y = (window_height - scaled_height) / 2
    
    # Reverse the calculation to find the mouse position on the virtual surface
    if scale == 0: return None
    surface_x = (mouse_x - offset_x) / scale
    surface_y = (mouse_y - offset_y) / scale

    # Make sure the mapped coordinates are within the virtual screen bounds
    if 0 <= surface_x < WIDTH and 0 <= surface_y < HEIGHT:
        return int(surface_x), int(surface_y)
    return None # Return None if the mouse is in the black bars (letterbox)

## Load assets once
for item in game_list:
    thb_img.append(load_image_from_subfolder(f'{item}_thumb_image.png'))

title.start_typewriter(delay=400)

### MAIN LOOP ###
while running:
    # Get mouse position mapped to the virtual surface for this frame
    virtual_mouse_pos = map_mouse_to_surface()

    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- MENU STAGE EVENTS ---
        if stage(estagio) == "menu":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                estagio = 1
            if event.type == pygame.MOUSEBUTTONDOWN and virtual_mouse_pos:
                if balls_b.obj.collidepoint(virtual_mouse_pos):
                    balls = not balls

        # --- GAME MENU STAGE EVENTS ---
        elif stage(estagio) == "game_menu":
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset -= event.y * scroll_speed
                scroll_offset = max(0, min(scroll_offset, scroll_limit)) # Clamp scrolling

            if event.type == pygame.MOUSEBUTTONDOWN and virtual_mouse_pos:
                # Check for clicks on game thumbnails
                for i, item in enumerate(game_list):
                    rect = pygame.Rect(pos_list[i], icon_size)
                    # We must adjust the rect for scrolling before checking collision
                    if rect.move(0, -scroll_offset).collidepoint(virtual_mouse_pos):
                        game = game_list[i]
                        estagio = 2
                        break # Exit loop once a selection is made
                
                # Check for click on random button
                random_rect = pygame.Rect(790, 5, 165, 50)
                if random_rect.move(0, -scroll_offset).collidepoint(virtual_mouse_pos):
                    game = random.choice(game_list)
                    estagio = 2

    # DRAWING LOGIC (Always draw to SC_SURFACE)
    # ---------------------------------------------

    # --- MENU STAGE DRAWING ---
    if stage(estagio) == "menu":
        SC_SURFACE.fill(background)
        hue = (hue + 0.005) % 1
        color = changeColor(hue)
        
        title.update(SC_SURFACE)
        if balls: yuri.run(clock)
        balls_b.update(SC_SURFACE, True)
        
        texto_menu = menu_font.render('PRESS SPACE', True, color)
        rect_menu = texto_menu.get_rect(center=(WIDTH // 2, HEIGHT * (7/8)))
        SC_SURFACE.blit(texto_menu, rect_menu)
        
    # --- GAME MENU STAGE DRAWING ---
    elif stage(estagio) == "game_menu":
        SC_SURFACE.fill('black')
        
        # Draw game thumbnails
        for i in range(len(game_list)):
            image_pos = (pos_list[i][0], pos_list[i][1] - scroll_offset)
            # Hover effect
            rect = pygame.Rect(image_pos, icon_size)
            if virtual_mouse_pos and rect.collidepoint(virtual_mouse_pos):
                pygame.draw.rect(SC_SURFACE, 'green', rect.inflate(10, 10), border_radius=5)
            
            SC_SURFACE.blit(thb_img[i], image_pos)

        # Draw random button
        random_rect = pygame.Rect(790, 5 - scroll_offset, 165, 50)
        # Hover effect
        if virtual_mouse_pos and random_rect.collidepoint(virtual_mouse_pos):
             pygame.draw.rect(SC_SURFACE, 'green', random_rect.inflate(10, 10), border_radius=5)
        pygame.draw.rect(SC_SURFACE, 'orange', random_rect)
        random_text = random_game_font.render("RANDOM", True, 'black')
        SC_SURFACE.blit(random_text, random_text.get_rect(center=random_rect.center))

    # --- LAUNCH STAGE ---
    elif stage(estagio) == "fase":
        print(f"Launching game: {game}")
        # IMPORTANT: exec(file.read()) is very unsafe.
        # A better approach is to use a dictionary of functions or importlib.
        # For this example, we'll just quit.
        # try:
        #     with open(f"{game}.py", "r") as file:
        #         exec(file.read())
        # except FileNotFoundError:
        #     print('Error - game does not exist')
        running = False # Exit the main loop to "launch" the game

    # FINAL RENDERING STEP
    # ---------------------------------------------
    # Now, take the final SC_SURFACE and scale it to the actual window.
    
    window_size = screen.get_size()
    scale = min(window_size[0] / WIDTH, window_size[1] / HEIGHT)
    scaled_size = (int(WIDTH * scale), int(HEIGHT * scale))
    scaled_surface = pygame.transform.smoothscale(SC_SURFACE, scaled_size)
    
    # Calculate the centered position
    pos = ((window_size[0] - scaled_size[0]) // 2, (window_size[1] - scaled_size[1]) // 2)

    screen.fill((0, 0, 0)) # Fill window with black for letterboxing
    screen.blit(scaled_surface, pos)
    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()
sys.exit()