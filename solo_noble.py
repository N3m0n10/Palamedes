import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))

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

positions = initial_positions.copy()

def move_piece(fst,scd):
    global positions
    global selected_piece
    global second_selected_piece
    fst_x, fst_y = (fst[0]-44)//80, (fst[1]-44)//80
    scd_x, scd_y = (scd[0]-44)//80 , (scd[1]-44)//80
    print(fst_x, fst_y, scd_x, scd_y)
    if positions[scd_x][scd_y] or positions[fst_x][fst_y] != ["empty"]:
        print("eaaaaaaaaaaaaaaaaaaa")
        if (fst_x == scd_x) and (fst_y == scd_y + 1):
            if scd_y  > 0:
                print("abbbbbbbbbbbb")
                if positions[scd_x][scd_y-1] == ["empty"]:
                    positions[fst_x][fst_y] = ["empty"]
                    positions[scd_x][scd_y] = ["empty"]
                    positions[scd_x][scd_y-1] = ["occupied"]
                    print("a")
        elif (fst_x == scd_x) and (fst_y == scd_y - 1):
            if scd_y  < 6:
                if positions[scd_x][scd_y+1] == ["empty"]:
                    positions[fst_x][fst_y] = ["empty"]
                    positions[scd_x][scd_y] = ["empty"]
                    positions[scd_x][scd_y+1] = ["occupied"]
        elif (fst_x == scd_x + 1) and (fst_y == scd_y):
            if scd_x < 6:
                if positions[scd_x-1][scd_y] == ["empty"]:
                    positions[fst_x][fst_y] = ["empty"]
                    positions[scd_x][scd_y] = ["empty"]
                    positions[scd_x-1][scd_y] = ["occupied"]
        elif (fst_x == scd_x - 1) and (fst_y == scd_y):
            if scd_x > 0:
                if positions[scd_x+1][scd_y] == ["empty"]:
                    positions[fst_x][fst_y] = ["empty"]
                    positions[scd_x][scd_y] = ["empty"]
                    positions[scd_x+1][scd_y] = ["occupied"]
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
    pygame.draw.circle(screen, (0, 50, 190), (300, 300), 290)

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
                        print("selected")
                    elif selected_piece == rect:
                        selected_piece = None
                        print("unselected")
                    elif selected_piece is not None:
                        second_selected_piece = rect
                        print("second selected")
                        move_piece(selected_piece, second_selected_piece)
                        print(selected_piece,second_selected_piece)
            if button.collidepoint(pygame.mouse.get_pos()):
                print("reset")
                second_selected_piece = None
                selected_piece = None
                positions = initial_positions.copy() ###TODO
                print(positions)

##################################################################events

    
    pygame.draw.circle(screen, "orange", button.center, 15)
    if selected_piece is not None:
        pygame.draw.circle(screen, "green", selected_piece.center, 17,1)
    if second_selected_piece is not None:
        pygame.draw.circle(screen, "green", second_selected_piece.center, 17,1)
    
    #for a in initial_positions:


    pygame.display.flip()
    clock.tick(60)
    rects = []

pygame.quit()



        