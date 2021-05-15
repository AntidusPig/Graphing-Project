import pygame
from math import sqrt
from ui import Notification
# ----------objs-----------
class prevImages:
    def __init__(self,initImage,maxLen=20):
        self.maxLen = maxLen
        if maxLen <=0:
            self.maxLen = 20
        self.images = [initImage]+[None]*(maxLen-1)
        self.curpos = 0
    def update_cur_image(self,nwimage):
        self.images[self.curpos] = nwimage
    def add_new(self,nwimage):
        if self.curpos < self.maxLen-1:
            self.curpos += 1
            self.images[self.curpos] = nwimage
        else: # self.curpos = self.maxLen
            self.images.pop(0)
            self.images.append(nwimage)
    def roll_back(self): # TODO: this part is still malfunctioning (a little bit)
        if self.curpos > 0:
            self.curpos -= 1
    def roll_forward(self):
        if self.curpos < self.maxLen-1 and self.images[self.curpos+1]!=None:
            self.curpos += 1
    def get(self):
        return self.images[self.curpos]

class Canvas:
    def __init__(self,images,pos,zoom):
        self.images = images # class prevImages
        self.pos = pos
        self.zoom = zoom
    def get(self):
        return self.images.get()
    def zoom(self): # TODO: zoom in to part of the canvas
        pass
    def move_canvas(self):
        pass

class Brush:
    def __init__(self):
        self.width = 5
        self.color = (0, 0, 0, 255)
        self.style = 'circle'  # brush type,patterns（images） and so on
        self.transition_quality = 0.2  # The distance to draw a point as a percentage of width
        self.drawing = False
        self.lastpoint = None
        self.paper = None

    def start_draw(self, paper, canvasPos,canvasZoom):
        '''
        :param paper: class Surface,referenced by value
        '''
        self.drawing = True
        self.lastpoint = (int((pygame.mouse.get_pos()[0]-canvasPos[0])/canvasZoom),
                          int((pygame.mouse.get_pos()[1]-canvasPos[1])/canvasZoom))
        self.paper = paper.copy()

    def end_draw(self):
        self.drawing = False
        return self.paper

    def draw(self,canvasPos,canvasZoom):
        '''
        draw is called repeatedly by the main function with linear interpolation
        '''
        realmp = pygame.mouse.get_pos()
        mp = (int((realmp[0] - canvasPos[0]) / canvasZoom), int((realmp[1] - canvasPos[1]) / canvasZoom))
        x, y = mp[0]-self.lastpoint[0], mp[1]-self.lastpoint[1]
        l = sqrt(x ** 2 + y ** 2)
        if l!=0:
            dx = self.width * self.transition_quality / l * x
            dy = self.width * self.transition_quality / l * y
            n = int(l / (self.width * self.transition_quality))
            for i in range(n):
                pygame.draw.circle(self.paper, self.color, (int(self.lastpoint[0]+dx*i), int(self.lastpoint[1]+dy*i)),
                                   self.width)
            pygame.draw.circle(self.paper, self.color, mp, self.width)
        self.lastpoint = mp
        return self.paper
    def change_clr(self,newclr):
        self.color = newclr
    def change_width(self,width):
        self.width = width
    def change_style(self,newstyle): #TODO:add style for brush
        pass
    def change_quality(self,newquality):
        self.transition_quality = newquality

class Selector:
    def __init__(self):
        self.linecolor = (0,0,255,255)
        self.dashedline = True
        self.fillcolor = (0,0,255,50)
        self.selecstartpos = None # position on the canvas, not the real position
        self.selecendpos = None
        self.selected = False
        self.dragstartpos = None
        self.dragendpos = None
    def start_select(self,realmp,canvasPos,canvasZoom):
        self.selecstartpos = (int((realmp[0]-canvasPos[0])/canvasZoom), int((realmp[1]-canvasPos[1])/canvasZoom))
    def end_select(self,realmp,canvasPos,canvasZoom):
        self.selecendpos = (int((realmp[0]-canvasPos[0])/canvasZoom), int((realmp[1]-canvasPos[1])/canvasZoom))
    def start_drag(self, realmp, canvasPos, canvasZoom):
        self.dragstartpos = (
        int((realmp[0] - canvasPos[0]) / canvasZoom), int((realmp[1] - canvasPos[1]) / canvasZoom))
    def end_drag(self, realmp, canvasPos, canvasZoom):
        self.dragendpos = (int((realmp[0] - canvasPos[0]) / canvasZoom), int((realmp[1] - canvasPos[1]) / canvasZoom))
    def draw_selec_area(self,paper): # TODO:dashed line
        pass

class Tool:
    def __init__(self):
        self.__tools = ["pen","select","eraser","magnifier","canvasDragger"]
        self.lasttool = "selector"
        self.tool = "selector"
    def t(self):
        return self.tool
    def change(self,nwtool): #change tool with whatever method
        if nwtool in self.__tools:
            self.tool = nwtool
        else:raise Exception(f"Tool name {nwtool} is illegal")
    def switch(self):  # just like in C4D, spacebar switches it
        self.tool,self.lasttool = self.lasttool,self.tool