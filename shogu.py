import pygame
import copy 

pygame.init()
WIDGHT, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDGHT, HEIGHT))
pygame.display.set_caption('SHOGU')
start_font = pygame.font.SysFont('Times New Roman', 40)
start_text = start_font.render("WHITE START", True, "white")
points_font = pygame.font.SysFont('Tahoma', 100)
impossible_move_text = start_font.render("IMPOSSIBLE MOVE", True, "red")
points = [0,0]

if __name__ == "__main__":  #make online
    pygame.display.set_icon(pygame.image.load("assets/general_images/Shogu.ico"))

#######create board 
#four boards, each one a list at the main list
#######passive movement
#any direction (even diagonal) is valid, dont move others pieces
#######atack movement
#cant move two opponents pieces
#######win condition
#win if the opponent lost all pieces IN ANY board

blacks = []
whites = []
boards = []
for i in range(4):
    board = []
    for line in range(4):
        line_list = []
        for col in range(4):
            if line == 0:
                line_list.append("white")
                whites.append([i,line,col])
            elif line == 3:
                line_list.append("black")
                blacks.append([i,line,col])
            else:
                line_list.append("empty")
        board.append(line_list)
    boards.append(board)

initial_pos = copy.deepcopy(boards)  # Use deepcopy here
initial_whites, initial_blacks = copy.deepcopy(whites),copy.deepcopy(blacks)

def passive_movement(piece, destiny):
    global turn, whites, blacks, boards , impossible_move

    # Extract current and destination positions
    current_board, current_row, current_col = piece[2]
    dest_board, dest_row, dest_col = destiny[2]

    # Calculate move delta
    delta_row = dest_row - current_row
    delta_col = dest_col - current_col
    
    if turn[0] == "white":  #check if the right board is choosen
        if piece[2][0] == 2 or piece[2][0] == 3:
            return False
        
    if turn[0] == "black":
        if piece[2][0] == 0 or piece[2][0] == 1:
            return False
    
    possible_pos = 0
    impossible_move = False
    team = blacks if boards[current_board][current_row][current_col] == "black" else whites
    for p in team:
        if -1<p[1]+dest_row < 4  or\
            -1<p[2] + dest_col < 4:
            if attack_movement(["holder",boards[p[0]][p[1]][p[2]],p],[current_board,delta_row,delta_col],test=True):
                possible_pos += 1
    if possible_pos < 1:
        impossible_move = True
        return False  
    
    print(possible_pos)
    # Check if moving on the same board
    if dest_board != current_board:
        return False

    # Check if move exceeds 2 squares in any direction
    if abs(delta_row) > 2 or abs(delta_col) > 2 or abs(delta_row) + abs(delta_col) == 3:
        return False

    # Check if destination is empty
    if boards[dest_board][dest_row][dest_col] != "empty":
        return False

    # Check path for moves larger than 1 square
    steps = max(abs(delta_row), abs(delta_col))
    if steps > 1:
        step_r = delta_row // steps
        step_c = delta_col // steps
        for i in range(1, steps):
            row = current_row + step_r * i
            col = current_col + step_c * i
            if boards[current_board][row][col] != "empty":
                return False



    # Update the board and piece position
    boards[current_board][current_row][current_col] = "empty"
    boards[dest_board][dest_row][dest_col] = piece[1]

    # Update the piece's position in the respective list
    if piece[1] == "white":
        for p in whites:
            if p == [current_board, current_row, current_col]:
                p[1], p[2] = dest_row, dest_col
                break
    elif piece[1] == "black":
        for p in blacks:
            if p == [current_board, current_row, current_col]:
                p[1], p[2] = dest_row, dest_col
                break

    turn = [turn[0], "attack"]
    return [current_board,delta_row,delta_col] 

def attack_movement(piece, destiny,test = False):
    global turn, whites, blacks, boards

    #Can't move on the same board
    if piece[2][0] == destiny[0]:
        print("same board")
        return False
    
    #out of the board
    if 0 > destiny[1] + piece[2][1] or 0 > destiny[2] + piece[2][2] or 3 < destiny[1] + piece[2][1] or 3 < destiny[2] + piece[2][2]:
        print("out of the board")
        return False
    
    
    #Checking variables
    if piece[1] == "white":
        op_color = "black"
    else:
        op_color = "white"
    current_board, current_row, current_col = piece[2]
    dest_board, dest_row, dest_col = destiny  #this is the deslocament and previous board (NOT DESTINY)

    #check vars 2 
    checking = boards[current_board][current_row + dest_row][current_col + dest_col]
    ot_checking = boards[current_board][current_row + int(dest_row/2)][current_col + int(dest_col/2)]
    col_coef = 1 if dest_col > 0 else -1 
    row_coef = 1 if dest_row > 0 else -1
    if dest_row == 0:
        row_coef = 0
    if dest_col == 0: 
        col_coef = 0
        
    #Can't move 2 pieces 
    if checking == op_color and ot_checking == op_color and (int(dest_row/2),int(dest_col/2)) != (0,0): #or (checking == op_color or ot_checking == op_color)\
        print("two pieces")
        return False

    #2 pieces, posterior piece case
    if 0 <= (current_row + dest_row + row_coef) \
            and (current_row + dest_row + row_coef) <= 3\
            and 0 <= (current_col + dest_col + col_coef)\
            and (current_col + dest_col + col_coef) <= 3: 
        print(boards[current_board][current_row + dest_row + row_coef][current_col + dest_col + col_coef])
        if (checking != "empty" or (ot_checking != "empty" and ((int(dest_row/2), int(dest_col/2)) != (0,0)))) \
           and boards[current_board][current_row + dest_row + row_coef][current_col + dest_col + col_coef] != "empty":
            print("two pieces, posterior piece case")
            return False
        
    #can't move same color
    if checking == piece[1] or (ot_checking == piece[1] and (abs(dest_row) == 2 or abs(dest_col) == 2)):
        print("same color")
        return False

    if not test:
        if checking == op_color:  #peça no local de destino
            checking = "empty"
            print("in the spot")
            op_team = blacks if piece[1] == "white" else whites
            if 0 > (current_row + dest_row + row_coef) \
                or (current_row + dest_row + row_coef) > 3\
                or 0 > (current_col + dest_col + col_coef)\
                or (current_col + dest_col + col_coef) > 3:   #cheeck if the position thepiece is pushed exceeds the board
                if op_team == whites:
                    for k in whites:
                        if k == [current_board, dest_row + current_row, dest_col + current_col]:#atualiza a lista op_team --> condição de vitória
                            whites.remove(k) #piece out of board
                            break
                else:
                    for k in blacks:
                        if k == [current_board, dest_row + current_row, dest_col + current_col]:#atualiza a lista op_team --> condição de vitória
                            blacks.remove(k) #piece out of board
                            break
            else:
                if op_team == whites:
                    for k in whites:
                        if k == [current_board, dest_row + current_row, dest_col + current_col]:
                            k[1], k[2] = current_row + dest_row + row_coef, current_col + dest_col + col_coef
                            break
                else:
                    for k in blacks:
                        if k == [current_board, dest_row + current_row, dest_col + current_col]:
                            k[1], k[2] = current_row + dest_row + row_coef, current_col + dest_col + col_coef
                            break
                boards[current_board][dest_row + current_row + row_coef][dest_col + current_col + col_coef] = op_color #push piece
            print(op_team)
        elif ot_checking == op_color and ((int(dest_row/2),int(dest_col/2)) != (0,0)): #em caso de movimento de duas casas -> peça na primeira casa
            ot_checking = "empty"  #RESET
            print("before the spot")
            op_team = blacks if piece[1] == "white" else whites
            if 0 > (current_row + dest_row + row_coef) \
                or (current_row + dest_row + row_coef) > 3\
                or 0 > (current_col + dest_col + col_coef)\
                or (current_col + dest_col + col_coef) > 3:   #cheeck if the piece is pushed exceeds the board
                if op_team == whites:
                    for k in whites:
                        if k == [current_board,current_row + int(dest_row/2),current_col + int(dest_col/2)]:#atualiza a lista op_team --> condição de vitória
                            whites.remove(k) #piece out of board
                            break
                else:
                    for k in blacks:
                        if k == [current_board,current_row + int(dest_row/2),current_col + int(dest_col/2)]:#atualiza a lista op_team --> condição de vitória
                            blacks.remove(k) #piece out of board
                            break
            else:
                print("push")
                if op_team == whites:   
                    for bk in whites:
                        if bk == [current_board,current_row + int(dest_row/2),current_col + int(dest_col/2)]:
                            bk[1], bk[2] = current_row + dest_row + row_coef, current_col + dest_col + col_coef
                            break
                else:
                    for bk in blacks:
                        if bk == [current_board,current_row + int(dest_row/2),current_col + int(dest_col/2)]:
                            bk[1], bk[2] = current_row + dest_row + row_coef, current_col + dest_col + col_coef
                            break
                boards[current_board][dest_row + current_row + row_coef][dest_col + current_col + col_coef] = op_color #push
            boards[current_board][current_row + int(dest_row/2)][current_col + int(dest_col/2)] = "empty"  #place of piece in the 1st mov empty
        print(ot_checking)
        # Update the piece's position in the respective list
        team = whites if piece[1] == "white" else blacks #clean exsecive variables later
        for p in team:
            if p == [current_board, current_row, current_col]:
                p[1], p[2] = current_row + dest_row, current_col + dest_col
                break

        #atualize board position
        boards[current_board][current_row][current_col] = "empty"
        boards[current_board][dest_row + current_row][dest_col + current_col] = piece[1]
        turn = ["black" if turn[0] == "white" else "white", "passive"]
    return True



turn = ["white","passive"]
clock = pygame.time.Clock()
running = True
selected_piece = None
selected_destination = None
first_move = True
impossible_move = False
while running:
    

    screen.fill((113,113,113))

    

    #Draw boards and divisory
    pygame.draw.rect(screen, "brown", (340,40,300,300), border_radius=30)
    pygame.draw.rect(screen, (239,173,100), (680,40,300,300), border_radius=30)
    pygame.draw.rect(screen, "brown", (340,380,300,300), border_radius=30)
    pygame.draw.rect(screen, (239,173,100), (680,380,300,300), border_radius=30)
    pygame.draw.line(screen, "black", (320,HEIGHT/2),(1000,HEIGHT/2), width=10)
    pygame.draw.rect(screen, (10,10,10), (1040,210,150,300), border_radius=30)
    points_text1 = points_font.render(str(points[0]), True, (250,250,250))
    points_text2 = points_font.render("_", True, (250,250,250))
    points_text3 = points_font.render(str(points[1]), True, (250,250,250))
    screen.blit(points_text1,(1085,220))
    screen.blit(points_text2,(1085,250))
    screen.blit(points_text3,(1085,370))
    #points text

    for i in range(1,4):
        pygame.draw.line(screen, (25,15,5), (i*80 + 330,50 ),(i*80 + 330, 330), width=10)
        pygame.draw.line(screen, (25,15,5), (i*80 + 670,50),(i*80 + 670,330), width=10) 
        pygame.draw.line(screen, (25,15,5), (i*80 + 330,390 ),(i*80 + 330, HEIGHT - 50), width=10)
        pygame.draw.line(screen, (25,15,5), (i*80 + 670,390),(i*80 + 670,HEIGHT - 50), width=10)
        pygame.draw.line(screen, (25,15,5), (350,i*80 + 30),(630,i*80 + 30), width=10) 
        pygame.draw.line(screen, (25,15,5), (350,i*80 + 370),(630,i*80 + 370), width=10)
        pygame.draw.line(screen, (25,15,5), (690,i*80 + 30),(960,i*80 + 30), width=10)
        pygame.draw.line(screen, (25,15,5), (690,i*80 + 370),(960,i*80 + 370), width=10)

    pieces_rects = []
    only_pieces_rects = []  #for win condition  ########unnecessary  #TODO fix this
    for j in range(4):
        for k in range(4):
            if boards[0][j][k] != "empty":
                pygame.draw.circle(screen, boards[0][j][k], (k*80 + 370,j*80 + 70), 25)
                only_pieces_rects.append([pygame.Rect(k*80 + 345,j*80 + 45, 50, 50),boards[0][j][k],[0,j,k]])
            pieces_rects.append([pygame.Rect(k*80 + 345,j*80 + 45, 50, 50),boards[0][j][k],[0,j,k]])
            if boards[1][j][k] != "empty":
                pygame.draw.circle(screen, boards[1][j][k], (k*80 + 710,j*80 + 70), 25)
                only_pieces_rects.append([pygame.Rect(k*80 + 345,j*80 + 45, 50, 50),boards[1][j][k],[1,j,k]])
            pieces_rects.append([pygame.Rect(k*80 + 685,j*80 + 45, 50, 50),boards[1][j][k],[1,j,k]])
            if boards[2][j][k] != "empty":
                pygame.draw.circle(screen, boards[2][j][k], (k*80 + 370,j*80 + 410), 25)
                only_pieces_rects.append([pygame.Rect(k*80 + 345,j*80 + 385, 50, 50),boards[2][j][k],[2,j,k]])
            pieces_rects.append([pygame.Rect(k*80 + 345,j*80 + 385, 50, 50),boards[2][j][k],[2,j,k]])
            if boards[3][j][k] != "empty":
                pygame.draw.circle(screen, boards[3][j][k], (k*80 + 710,j*80 + 410), 25)
                only_pieces_rects.append([pygame.Rect(k*80 + 345,j*80 + 385, 50, 50),boards[3][j][k],[3,j,k]])
            pieces_rects.append([pygame.Rect(k*80 + 685,j*80 + 385, 50, 50),boards[3][j][k],[3,j,k]])
            

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for rect in pieces_rects:
                if rect[0].collidepoint(pygame.mouse.get_pos()):
                    first_move = False
                    if turn[0] == "white" and pieces_rects[pieces_rects.index(rect)][1] == "white": #select the piece in passive
                        if selected_piece == rect:
                            selected_piece = None
                        else:
                            selected_piece = rect
                        if turn[1] == "attack": #attack movement
                            destination = [pas[0],pas[1],pas[2]]
                            at = attack_movement(selected_piece,destination)
                            print(at)
                            if at:
                                del at
                                del pas
                            selected_piece = None
                    elif turn[0] == "black" and pieces_rects[pieces_rects.index(rect)][1] == "black":
                        if selected_piece == rect:
                            selected_piece = None
                        else:
                            selected_piece = rect
                        if turn[1] == "attack":
                            destination = [pas[0],pas[1],pas[2]]
                            at = attack_movement(selected_piece,destination)
                            if at:
                                del at
                                del pas
                            selected_piece = None
                    #select the destination of passive movement 
                    elif (selected_piece is not None) and (pieces_rects[pieces_rects.index(rect)][1] == "empty") and turn[1] == "passive":
                        selected_destination = rect
                        pas = passive_movement(selected_piece,selected_destination)
                        selected_piece = None
                        selected_destination = None
                    
    
    for rect in pieces_rects:
        if rect[0].collidepoint(pygame.mouse.get_pos()):
            pygame.draw.circle(screen, "blue", rect[0].center, 27,3)

    if selected_piece is not None:
        pygame.draw.circle(screen, "green", selected_piece[0].center, 27,3)

    if first_move:
        screen.blit(start_text, (50,10))

    if impossible_move:
        screen.blit(impossible_move_text, (10,5))
    
    for z in range(4):
        count = 0
        for wi in whites:
            if wi[0] == z:
                count += 1
        if count == 0: #BLACKS WIN
            boards = initial_pos.copy()
            whites, blacks = initial_whites.copy(),initial_blacks.copy()
            points[1] += 1
            selected_piece = None
            selected_destination = None
            first_move = True
            impossible_move = False
            turn = ["white","passive"]
            #checkar e resetar todas as variáveis
            #mostrar texto de vitória (temporizado ou até o primeira movimento)
        count = 0
        for bc in blacks:
            if bc[0] == z:
                count+= 1
        if count == 0:  #WHITES WIN
            boards = copy.deepcopy(initial_pos)
            whites, blacks = copy.deepcopy(initial_whites),copy.deepcopy(initial_blacks)
            points[0] += 1
            selected_piece = None
            selected_destination = None
            first_move = True
            impossible_move = False
            turn = ["white","passive"]

    pygame.display.update()

    clock.tick(60)

pygame.quit()