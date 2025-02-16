import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))

initial_positions = []
for i in range(7):
    for j in range(7):
        if i in [0,1,5,6] and j in [0,1,5,6]:
            initial_positions.append([i, j, "blocked"])
        elif i == 3 and j == 3:
            initial_positions.append([i, j, "empty"])
        else:
            initial_positions.append([i, j, "occupied"])

def move_piece(fst,scd):
    pass

clock = pygame.time.Clock()
running = True
selected_piece = None
second_selected_piece = None

    
rects = [] #for mouse hover
while running:

    screen.fill((30,30,30))
    pygame.draw.circle(screen, (0, 50, 190), (300, 300), 290)

    for k in initial_positions:
        match k[2]:
            case "blocked":
                pass
            case "empty":
                a = pygame.draw.circle(screen, (0, 0, 0), (k[0] * 80 + 60, k[1] * 80 + 60), 15)
                rects.append(a)
            case "occupied":
                b = pygame.draw.circle(screen, "brown", (k[0] * 80 + 60, k[1] * 80 + 60), 16)
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

##################################################################events

    
    
    if selected_piece is not None:
        pygame.draw.circle(screen, "green", selected_piece.center, 17,1)
    if second_selected_piece is not None:
        pygame.draw.circle(screen, "green", second_selected_piece.center, 17,1)
    
                


    pygame.display.flip()
    clock.tick(60)
    rects = []

pygame.quit()



        