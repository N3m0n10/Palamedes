#create game list
game_list = ["pong_game", "circle_pong", "breakout_game", 'bomber_brick', 'solid_pong_game',
              'solo_noble', 'bottles_game', 'chimp_game','8']  
num_games = len(game_list )-1 #desconsider the easter egg
#set icons size and position
icon_size = (300, 200)
first_pos = (90, 100)
#create pos list with first pos
pos_list = []
pos_list.append(first_pos)
#create positions
pointer = pos_list[0]
for a in range(len(game_list) - 2):
    next_pos = (pos_list[a][0] + 400 , pointer[1])
    if next_pos[0] > 1280 - 300:    #When the next element goes off the screen, it starts on the next line
        old_pointer = pointer
        pointer = (90, old_pointer[1] + 250) #pointer fixed on first of each line (when the line is being coumposed)
        next_pos = pointer
        pos_list.append(next_pos)
    else: pos_list.append(next_pos)    
#create excell
if pos_list[-1][1] > 720:
    excell = pos_list[-1][1] + 1800
else:
    excell = 1800
#not so secret easter egg position
pos_list.append((790, excell - 250))

#create screen size based on games number -> num will be used on main-> game_menu function
surface_size = (1280, excell)

#Define surface height  
srfc_height = excell

#create random mode <----------------