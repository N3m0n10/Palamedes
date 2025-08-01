""" Reuseable pieces if code"""
## TODO: add player, ball here. Struture all game files and this in a diferent folder then main
import pygame

class button():
    def __init__(self,x,y,size:tuple,color,width = 0, border_radius = 0, text = None, font = 'Arial', font_size = 10,text_color = 'White'):
        # TODO: add multiple pos and size input option
        pygame.init()

        self.color = color
        self.start_pos = (x,y) 
        self.start_size = size
        self.width = width
        self.border_radius = border_radius
        self.obj = pygame.Rect((x,y),size) # https://www.pygame.org/docs/ref/rect.html?highlight=rect#pygame.Rect

        self.text = text
        if self.text is not None:
            pygame.font.init()
            self.font = pygame.font.SysFont(font, font_size) 
            self.text_surf = self.font.render(text, True, text_color) 
            self.text_obj = self.text_surf.get_rect()
            self.text_obj.center = self.obj.center

    def update(self,screen, on_pass = False, on_pass_color = (255,0,0) ,mouse_pos = None):
        color = self.color
        if on_pass:
            if self.obj.collidepoint(mouse_pos) and mouse_pos is not None:
                color = on_pass_color
                ## or self.animation(self)
        pygame.draw.rect(screen, color,self.obj,self.width,self.border_radius)
        screen.blit(self.text_surf, self.text_obj)
        #screen.update(self.obj) if needed

    def move(self,pos):
        self.obj.x , self.obj.y = pos[0], pos[1]
        self.text_obj.center = self.obj.center

    def action(self,func,*kwargs): 
        """ Call in the right event, handle event outside"""
        func(*kwargs)

    def animation(self):
        pass    

    def rewrite(self, font, font_size, text, text_color):
        self.font = pygame.font.SysFont(font, font_size)
        self.text_surf = self.font.render(text,True,text_color)
        self.text_obj = self.text_surf.get_rect()
        self.text_obj.center = self.obj.center
        
class Sprite_button(pygame.sprite.Sprite):
    def __init__(self,image,pos,scale):
        pygame.sprite.Sprite.__init__(self)
        pass