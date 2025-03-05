
#direction = (mouse point - char_origin) --> vect / abs(mouse point - char_origin) --> unit vect
#launch = force * unit vect   #--> force is a module

import pygame as p
import math

class character():  #make sprite
    def __init__(self,mass,x,y):
        self.color = ("green")
        self.mass = mass
        self.x = x
        self.y = y
        self.origin = (self.x,self.y)
        self.char = p.draw.circle(screen,self.color,(self.x,self.y),10)  #for now

    @staticmethod
    def launch(self,mouse_x,mouse_y,origin):
        vector = (mouse_x - origin[0],mouse_y - origin[1])
        direction = [vector[0]/math.sqrt(vector[0]**2 + vector[1]**2),vector[1]/math.sqrt(vector[0]**2 + vector[1]**2)]      #math.sqrt(vector[0]**2 + vector[1]**2)  
        speed_module = math.sqrt(vector[0]**2 + vector[1]**2)**1.5
        speed = [speed_module*direction[0],speed_module*direction[1]]
        projectile.append((speed,direction,origin))    #type,force,direction

touch_token = 0
gravity = 20000
square_launch_radius = 9000

projectile = list()
p.init()
screen = p.display.set_mode((800,600))
clock = p.time.Clock()
run = True
while run:
    for event in p.event.get():
        if event.type == p.QUIT:
            run = False 

    screen.fill((0,0,0))

    char = character(1,400,300)
    

    if 0 < len(projectile) :  #if there is a projectile and max 10
        for projec in projectile:
            projec[2][0] += projec[0][0]*dt
            projec[0][1] += (gravity*dt**2)/2
            projec[2][1] += projec[0][1]*dt 
            p.draw.circle(screen,(255,255,255),(projec[2][0],projec[2][1]),10)
            if projec[2][1] > 600 or projec[2][0] > 800 or projec[2][0] < 0:
                projectile.remove(projec)
                del projec

    if len(projectile) < 10:
        mouse_x,mouse_y = p.mouse.get_pos()
        if  abs((mouse_x - char.x)**2 + (char.y - mouse_y)**2) < square_launch_radius:  #mouse limit in a circle
            p.draw.line(screen,(255,0,0),(mouse_x,mouse_y),(char.x,char.y))
            p.draw.circle(screen,(255,255,255),(char.x,char.y),math.sqrt(square_launch_radius),2)
            if p.mouse.get_pressed()[0] and touch_token == 0:
                touch_token = 50
                char.launch(char,mouse_x,mouse_y,[char.x,char.y])

    if touch_token > 0:
        touch_token -= 1


        
    
    dt = clock.tick(60) / 1000
    p.display.flip()

p.quit()