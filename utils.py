""" Reuseable pieces if code"""
## TODO: add player, ball here. Struture all game files and this in a diferent folder then main                                                         # n3m0n10
import pygame

class button():
    def __init__(self,x,y,size:tuple,color,width = 0, border_radius = 0, text = None, font = 'Arial', font_size = 10,text_color = 'White'):
        # TODO: add multiple pos and size input option

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
            if mouse_pos is not None:
                if self.obj.collidepoint(mouse_pos):
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

class Text():
    """Each line (for starter) will be dvivided into each character with"""
    """it's own surface. That way text can be easely moved, transformed """
    """and turned into a object of the game, adding astistic enphase or """
    """game design liberty"""
    def __init__(self,text,pos:tuple,font,font_size,color,mouse_drag = False):
        self.text = text
        self.init_pos = pos
        self.font = font
        self.font_size = font_size
        self.color = color
        self.mode = None
        self.mouse_drag = mouse_drag
        self.sp_vel_x, self.sp_vel_y = 5,5

        self.create()

    def create(self):  # Also works as a HARD RESET
        self.letters = []  
        font_obj = pygame.font.SysFont(self.font, self.font_size)

        # 1. Calcular largura total do texto
        total_width = 0
        surfaces = []
        for char in self.text:
            surface = font_obj.render(char, True, self.color)
            surfaces.append((char, surface))
            total_width += surface.get_width()

        # 2. Reposicionar início com base no centro
        start_x = self.init_pos[0] - total_width // 2
        x_offset = 0

        # 3. Criar letras com posição ajustada
        for char, surface in surfaces:
            rect = surface.get_rect(topleft=(start_x + x_offset, self.init_pos[1]))
            self.letters.append({'char': char, 'surf': surface, 'rect': rect})
            x_offset += surface.get_width()

    def draw(self, screen):
        count = self.visible_letters if hasattr(self, 'typing_mode') and self.typing_mode else len(self.letters)
        for letter in self.letters[:count]:
            screen.blit(letter['surf'], letter['rect'])

    def update(self,screen):
        if self.mode == "inerte":
            self._inerte_mode()
        elif self.mode == "screen_protector":
            self._screen_protector_mode(screen)
        elif self.mode == "pong":
            self._pong_mode()
        if hasattr(self, 'typing_mode') and self.typing_mode:
            self._typewriter_mode()
        self.draw(screen)

    def move_all(self, dx, dy):
        for letter in self.letters:
            letter['rect'].x += dx
            letter['rect'].y += dy

    def move(self, move_function, letter_index):
        if 0 <= letter_index < len(self.letters):
            rect = self.letters[letter_index]['rect']
            move_function(rect)

    def change_color_all(self, color):
        font_obj = pygame.font.SysFont(self.font, self.font_size)
        self.color = color
        for letter in self.letters:
            surface = font_obj.render(letter['char'], True, color)
            rect = letter['rect']
            letter['surf'] = surface
            letter['rect'] = surface.get_rect(topleft=(rect.x, rect.y))

    def change_color(self,letter_index,color):
        if 0 <= letter_index < len(self.letters):
            font_obj = pygame.font.SysFont(self.font, self.font_size)
            char = self.letters[letter_index]['char']
            surface = font_obj.render(char, True, color)
            rect = self.letters[letter_index]['rect']
            self.letters[letter_index]['surf'] = surface
            self.letters[letter_index]['rect'] = surface.get_rect(topleft=(rect.x, rect.y))

    def enable_mouse_drag(self):
        self.mouse_drag = not self.mouse_drag
        self.dragging = False

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for letter in self.letters:
                if letter['rect'].collidepoint(event.pos):
                    self.dragging = True
                    self.drag_offset = (letter['rect'].x - event.pos[0], letter['rect'].y - event.pos[1])
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            dx, dy = event.rel
            self.move_all(dx, dy) #TODO: thats trick, I might wan't to move just a single letter sometimes --> elaborate this function

    def events_handler(self,event):
        """Call in events"""
        pass

    def change_mode(self):
        """update will have conditionals to handle this"""
        pass

    def _inerte_mode(self):
        pass

    def _screen_protector_mode(self,screen):
        for letter in self.letters:
            rect = letter['rect']
            rect.x += self.sp_vel_x
            rect.y += self.sp_vel_y
            # rebater nas bordas
            if rect.right > screen.get_size()[0] or rect.left < 0:
                self.sp_vel_x *= -1
            if rect.bottom > screen.get_size()[1] or rect.top < 0:
                self.sp_vel_y *= -1

    def start_typewriter(self, delay=100):
        """Inicia o efeito de digitação. 'delay' em ms entre letras"""
        self.typing_mode = True
        self.visible_letters = 0
        self.last_typing_time = pygame.time.get_ticks()
        self.typing_delay = delay

    def _typewriter_mode(self):
        """Atualiza o número de letras visíveis"""
        now = pygame.time.get_ticks()
        if self.visible_letters < len(self.letters) and now - self.last_typing_time >= self.typing_delay:
            self.visible_letters += 1
            self.last_typing_time = now

    def _pong_mode(self):
        pass

    def _choose_letter(self, letter_char):
        for i, letter in enumerate(self.letters):
            if letter['char'] == letter_char:
                return i
        return -1
                                                                                                                                                                                                                 # n3m0n10

class TextStatic:
    def __init__(self, text, center_pos: tuple, font, font_size, color):
        self.text = text
        self.color = color
        self.font_obj = pygame.font.SysFont(font, font_size)
        self.surface = self.font_obj.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center=center_pos)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def change_color(self, color):
        self.color = color
        self.surface = self.font_obj.render(self.text, True, self.color)

class Text_sprite(pygame.sprite.Sprite):
    def __init__(self,image,pos,scale):
        pygame.sprite.Sprite.__init__(self)
        pass