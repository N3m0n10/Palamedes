""" One of those games where you haver to grab things that are falling using mouse movement"""
import pygame

class Colectable(pygame.sprite.Surface):
    def __init__(self,spawm:tuple,speed:tuple):
        super.__init__(spawm)
        self.speed = pygame.math.Vector2(speed)

    def update(self,screen):
        pass

# TODO: add points as a parameter, and add visual indicator to points value
class Good_food(Colectable):
    def __init__(self,spawm:tuple):
        super.__init__(spawm)
        pass

    def action(self,player):
        player.points += 500
        player.stamina += 0.2 #add life when 1

class Money(Colectable):
    def __init__(self,spawm:tuple):
        super.__init__(spawm)

    def action(self,player):
        player.points += 2000

    def update(): # Custom move
        pass

class Candy(Colectable):
    def __init__(self,spawm:tuple):
        super.__init__(spawm)
        pass

    def action(self,player):
        player.points += 100
        player.caries += 0.1

class Tooth_brusher(Colectable):
    def __init__(self,spawm:tuple):
        super.__init__(spawm)
        pass

    def action(self,player):
        player.caries -= 0.1 if player.caries > 0 else 0

class Bad_food(Colectable):
    def __init__(self,spawm:tuple):
        super.__init__(spawm)
        pass

    def action(self,player):
        player.points -= 500

class Dirt(Colectable):
    def __init__(self,spawm:tuple):
        super.__init__(spawm)
        pass

    def action(self,player):
        player.points -= 100
        player.cough(1000) #milliseconds

class Bomb(Colectable):
    def __init__(self,spawm:tuple):
        super.__init__(spawm)
        pass

    def action(self,player):
        player.life -= 1

class Grab:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

        fases = {}

    def update(self,screen):
        pass

    def run(self,screen):
        pass