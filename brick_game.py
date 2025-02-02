import pygame
from ball import ball
from player import player
from random import choices , choice

###PYGAME_SETUP
pygame.init()
WIDTH, HEIGHT = 1280,720 #largura e altura
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
###VARS
fases_info = {
    "fase_1" : {
        "fase_name" : "FASE 1",
        "base_time" : 360,
        "normal brick count" : 48,
        "unbreakable brick count" : 0,
        "power up count" : 2,
        "positions" : [(4, 20), (132, 20), (260, 20), (388, 20), (516, 20), (644, 20), (772, 20), (900, 20), (1028, 20), (1156, 20),\
                       (4, 58), (132, 58), (260, 58), (388, 58), (516, 58), (644, 58), (772, 58), (900, 58), (1028, 58), (1156, 58),\
                       (4, 96), (132, 96), (260, 96), (388, 96), (516, 96), (644, 96), (772, 96), (900, 96), (1028, 96), (1156, 96), \
                       (4, 134), (132, 134), (260, 134), (388, 134), (516, 134), (644, 134), (772, 134), (900, 134), (1028, 134), (1156, 134),\
                       (4, 172), (132, 172), (260, 172), (388, 172), (516, 172), (644, 172), (772, 172), (900, 172), (1028, 172), (1156, 172)]
    }
}
print(len(fases_info["fase_1"]["positions"]))
ball_radius = 15
player_size = 150
player_half_size = player_size/2
player1 = player(screen, 'cyan' , player_size, 10 , 180,1,"rect","horizontal",posit_y = 600)
ball_st = ball(screen,'white',ball_radius,fixed_start_speed = True,limit_speed=5,min_speed=3)
ball_st_rect = ball_st.rect ##for collision detection
life = 3
need_build = 1
points = 0
courrent_fase = 1
touch_token = 0
color_list = ["red","orange","yellow","green","blue","purple","pink","white",(35,39,120),(100,12,255)]#make secret black block

###FUNCTIONS
def timer():
    pass

def score():
    pass

def game_over():
    pass

def end_fase():
    clean_blocks()
    pass

def build(fase_info_input):
    blocks = []
    possible_pos = fase_info_input["positions"].copy()
    pwerup_num = fase_info_input["power up count"]
    ubrk_num = fase_info_input["unbreakable brick count"]
    norm_num = fase_info_input["normal brick count"]
    if pwerup_num != None:
        for i in range(pwerup_num):
            pos_i = choice(possible_pos)
            bonus_brick = power_up_brick(pos_i,size_x = 120,size_y = 30)
            pygame.draw.rect(screen, bonus_brick.color, bonus_brick.rect)
            possible_pos.remove(pos_i)
            blocks.append(bonus_brick)
    if ubrk_num != None:
        for i in range(ubrk_num):
            pos_i = choice(possible_pos)
            unbreakable_brick = Unbreakable_brick(pos_i)
            pygame.draw.rect(screen, unbreakable_brick.color, unbreakable_brick.rect)
            possible_pos.remove(pos_i)
            blocks.append(unbreakable_brick)
    if norm_num != None:
        for i in range(norm_num):
            pos_i = choice(possible_pos)
            normal_brick = Normal_brick(pos_i)
            pygame.draw.rect(screen, normal_brick.color, normal_brick.rect)
            possible_pos.remove(pos_i)
            blocks.append(normal_brick)
    return blocks

def restart_pos():
    pass

def collision():
    pass

def positions_maker(): #for later use --> use lambda when multiple call
    pass

def clean_blocks():
    pass
    #when finishing a fase or losing all remaining objects must be deleted

def show_stats():
    pass
    #show life, score, time

###BRICKS
class brick():
    def __init__(self,pos ,size_x = 120,size_y = 30):
        self.pos = pos
        self.size_x = size_x
        self.size_y = size_y
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size_x,self.size_y)

    def atualize(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def __del__(self):
        pass

class Normal_brick(brick):
    def __init__(self,pos,size_x = 120,size_y = 30):
        super().__init__(pos,size_x,size_y)
        self.color = (77,150,99) #making it simple for now
        self.points = 100
        self.destroy = False

    def collided(self):
        self.destroy = True
        return self.points

class power_up_brick(brick):
    def __init__(self,pos,size_x = 120,size_y = 30):
        super().__init__(pos)
        power_list = [multiball, speed_up, slow_down, extend, shrink, shooter, shield, ultimate, invencible, score_up, life_up]
        self.drop = choices(power_list,weights = [10,10,10,10,10,10,10,1,5,10,4]) #thinkng about makeing the colors match the power ups, the bad point is making the game more predictable
        self.color = choice(color_list)
        self.points = 200
        
    def collided(self):
        self.destroy = True
        return self.points
        #return drop #make return a tuple, if [1] is not none them apply power up


class Unbreakable_brick(brick):
    def __init__(self,pos,size_x = 120,size_y = 30):
        super().__init__(pos)
        self.color = "grey"
        self.points = 1000

    def collided(self, Hyperball = False): #to do hyperball
        if Hyperball == True:
            self.destroy = True


class strong_brick(brick):
    def __init__(self,pos,size_x = 120,size_y = 30,life = 3):
        super().__init__(pos)
        self.life = life
        self.points = 500

    def collided(self,list):
        #make the colos lose brightnes upon hit
        self.life -= 1
        if self.life == 0:
            self.destroy = True
            return self.points
        return 0


###POWER UPS
class power_up():
    def __init__(self,center_pos):        
        pass

class multiball(power_up):
    pass

class speed_up(power_up):
    pass

class slow_down(power_up):
    pass

class extend(power_up):
    pass

class shrink(power_up):
    pass

class shooter(power_up):
    pass

class shield(power_up):
    pass

class ultimate(power_up):
    pass

class invencible(power_up):
    pass

class score_up(power_up):
    pass    

class life_up(power_up):

    def effect(self):
        global life
        life += 1


class inviseble(power_up):
    pass

class key(power_up): #later use
    pass
    



#make iter
#case iter reach max --> game beaten --> leaderboard
#create txt file for leaderboard
#points will be time based, completing stages will give extra points, finishing\
# a fase with more then one ball will give extra points
#possible add another win condition later, remember when making end_fase()
#create skin after game beaten (RGB skin)
##//

running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False

    screen.fill("black")

    if need_build == 1:
        blocks_list = build(fases_info["fase_1"])
        need_build = 0
    #reminder --> brick size 120

    ##atualizations
    player1.atualize(0.01, (WIDTH, HEIGHT) , 1 , ball_st.player_pos.y , ball_st.player_pos.x)
    ball_st.atualize(0.02, (WIDTH, HEIGHT))

    if touch_token > 0:
        touch_token -= 1

    if pygame.Rect.colliderect(ball_st.rect, player1.rect) and touch_token == 0:
        ball_st.ball_vel_y *= -1
        touch_token += 1

    
    for i in blocks_list:
        if pygame.Rect.colliderect(ball_st.rect,i.rect):  
            points += i.collided()
            ball_st.ball_vel_y *= -1
            if i.destroy == True:
                blocks_list.remove(i)
        try: 
            i.atualize()
        except:
                            #remember to delete the objects  in further changes
            del i
            #collision sucess

    #ball --> ball fall, if pos < 10 --> restart pos and lifes - 1


    pygame.display.flip()
    clock.tick(60)

pygame.quit()