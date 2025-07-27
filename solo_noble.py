import pygame
import copy

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Peg Solitaire')
general_font = pygame.font.SysFont('Times New Roman', 25)
win_text = general_font.render("WIN!", True, (90, 100, 240))
reset_text = general_font.render("RESET", True, "orange")
move_error_text = general_font.render("Select the piece to move and the piece jumped!", True, "orange")

move_error = False
initial_positions = []
for i in range(7):
    line = []
    for j in range(7):
        if i in [0,1,5,6] and j in [0,1,5,6]:
            line.append([ "blocked"])
        elif i == 3 and j == 3:
            line.append([ "empty"])
        else:
            line.append([ "occupied"])
    initial_positions.append(line)

positions = copy.deepcopy(initial_positions)

def move_piece(fst,scd):
    global positions
    global selected_piece
    global second_selected_piece
    global move_error
    fst_x, fst_y = (fst[0]-44)//80, (fst[1]-44)//80
    scd_x, scd_y = (scd[0]-44)//80 , (scd[1]-44)//80
    if positions[scd_x][scd_y] or positions[fst_x][fst_y] != ["empty"]:
        if (fst_x == scd_x) and (fst_y == (scd_y + 1)):
            if scd_y  > 0:
                if positions[scd_x][scd_y-1] == ["empty"]:
                    positions[fst_x][fst_y] = ["empty"]
                    positions[scd_x][scd_y] = ["empty"]
                    positions[scd_x][scd_y-1] = ["occupied"]
                else: move_error = True
        elif (fst_x == scd_x) and (fst_y == (scd_y - 1)):
            if scd_y  < 6:
                if positions[scd_x][scd_y+1] == ["empty"]:
                    positions[fst_x][fst_y] = ["empty"]
                    positions[scd_x][scd_y] = ["empty"]
                    positions[scd_x][scd_y+1] = ["occupied"]
                else: move_error = True
        elif (fst_x == (scd_x + 1)) and (fst_y == scd_y):
            if scd_x > 0:
                if positions[scd_x-1][scd_y] == ["empty"]:
                    positions[fst_x][fst_y] = ["empty"]
                    positions[scd_x][scd_y] = ["empty"]
                    positions[scd_x-1][scd_y] = ["occupied"]
                else: move_error = True
        elif (fst_x == (scd_x - 1)) and (fst_y == scd_y):
            if scd_x <6:
                if positions[scd_x+1][scd_y] == ["empty"]:
                    positions[fst_x][fst_y] = ["empty"]
                    positions[scd_x][scd_y] = ["empty"]
                    positions[scd_x+1][scd_y] = ["occupied"]
                else: move_error = True
    selected_piece = None
    second_selected_piece = None

clock = pygame.time.Clock()
running = True
selected_piece = None
second_selected_piece = None
button = pygame.rect.Rect(0,0,50,50)
    
rects = [] #for mouse hover
while running:

    screen.fill((30,30,30))
    pygame.draw.circle(screen, (0, 50, 190), (300, 300), 290) #draw board
    

    occupied_count = 0
    for j,line in enumerate(positions):
        for k, piece in enumerate(line): 
            match piece:
                case ["blocked"]:
                    pass
                case ["empty"]:
                    a = pygame.draw.circle(screen, (0, 0, 0), (j * 80 + 60, k * 80 + 60), 15)
                    rects.append(a)
                case ["occupied"]:
                    b = pygame.draw.circle(screen, "brown", (j * 80 + 60, k * 80 + 60), 16)
                    rects.append(b)
                    occupied_count += 1

    if occupied_count == 1:
        screen.blit(win_text, (500,10))
    
    for rect in rects:
        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.circle(screen, "yellow", rect.center, 17,1)
##################################################################events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect in rects:
                if rect.collidepoint(pygame.mouse.get_pos()):
                    if selected_piece is None:
                        selected_piece = rect
                    elif selected_piece == rect:
                        selected_piece = None
                    elif selected_piece is not None:
                        second_selected_piece = rect
                        move_piece(selected_piece, second_selected_piece)
            if button.collidepoint(pygame.mouse.get_pos()):
                second_selected_piece = None
                selected_piece = None
                del positions
                positions = copy.deepcopy(initial_positions) 

##################################################################events

    
    pygame.draw.circle(screen, "orange", button.center, 15)
    screen.blit(reset_text, (45,10))
    if selected_piece is not None:
        pygame.draw.circle(screen, "green", selected_piece.center, 17,1)
    if second_selected_piece is not None:
        pygame.draw.circle(screen, "green", second_selected_piece.center, 17,1)
    if move_error:
        screen.blit(move_error_text, (45,250))

    pygame.display.flip()
    clock.tick(60)
    rects = []

pygame.quit()        