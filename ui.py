# user interface for the project
import pygame
from pygame.locals import *
from time import time

def available_fonts():
    return '\n      '.join(pygame.font.get_fonts())

class ToolChangeButton:
    def __init__(self, pos, width, height, text, textclr, font, font_size, pic_idle_path, pic_active_path, pic_pressed_path, tool_type):
        self.pos = pos
        self.dime = (width,height)
        self.text = text
        self.textclr = textclr
        try:
            self.font = pygame.font.SysFont(font,font_size)
        except FileNotFoundError:
            print(f"Current font \"{font}\" is unavailable, try the follows or install others:\n{available_fonts()}")  # TODO:change to message box
            self.text = None
        self.pressed = False
        self.pic_idle = pygame.Surface(self.dime,SRCALPHA,32)
        self.pic_active = pygame.Surface(self.dime,SRCALPHA,32)
        self.pic_pressed = pygame.Surface(self.dime,SRCALPHA,32)
        pygame.transform.scale(pygame.image.load(pic_idle_path),(width,height),self.pic_idle)
        pygame.transform.scale(pygame.image.load(pic_active_path),(width,height),self.pic_active)
        pygame.transform.scale(pygame.image.load(pic_pressed_path),(width,height),self.pic_pressed)
        self.toolType = tool_type
        self.pressed = False
    def mouse_inside(self):
        x,y = pygame.mouse.get_pos()
        if self.pos[0] < x < self.pos[0]+self.dime[0] and self.pos[1] < y < self.pos[1]+self.dime[1]:
            return True
        else: return False
    def clicked(self,toolObj): # ensure mouse_inside() is true
        self.pressed = True
        toolObj.change(self.toolType)
        # if self.func_press:  # TODO: is it possible to pass arguments to these functions?
        #     return self.func_press()
    def declicked(self):
        self.pressed = False
        # if self.func_release:
        #     return self.func_release()
    def show(self,window):
        if self.pressed: # if pressed, it is inside
            window.blit(self.pic_pressed,self.pos)
        elif self.mouse_inside():
            window.blit(self.pic_active,self.pos)
        else:
            window.blit(self.pic_idle,self.pos)
        if self.text:
            window.blit(self.font.render(self.text,True,self.textclr),self.pos) # TODO 居中文字

class Notification:
    def __init__(self,text,textclr=(0,0,0,255),font="dejavuserif",fontsize=50,pos=(1000,40),width=340,height=170,rectclr=(128,128,128,128),boarder_radius=30,life=2500):
        self.text = text
        self.textclr = textclr
        self.pos = pos
        self.boarder_radius = boarder_radius
        try:
            self.font = pygame.font.SysFont(font,fontsize)
        except FileNotFoundError:
            print(f"Current font \"{font}\" is unavailable, try the follows or install others:\n{available_fonts()}")
            exit(1)
        self.rectclr = rectclr
        self.size = (width,height)
        self.life = life
        self.borntime = time()
        self.alive = True
    def show(self,window):
        pygame.draw.rect(window,self.rectclr,pygame.Rect(self.pos,self.size),border_radius=self.boarder_radius)
        window.blit(self.font.render(self.text,True,self.textclr),self.pos)
        if self.life <= time()-self.borntime:
            self.alive = False