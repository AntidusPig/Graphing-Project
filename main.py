from os import getcwd
from os.path import join
from ui import *
from objects import *

# -----------Startup------------
WINSIZE = (1920,1080)
top = pygame.display.set_mode(WINSIZE,NOFRAME|RESIZABLE,32)
pygame.init()
# -----------loading------------
PIC_RESOURCES_PATH = join(getcwd(),"pic_resources")
ICONS = {"PEN_TOOL":{"idle":pygame.image.load(join(PIC_RESOURCES_PATH,"pen_tool_idle.png")).convert_alpha(),
            "using":pygame.image.load(join(PIC_RESOURCES_PATH, "pen_tool_using.png")).convert_alpha()},
         "ERASER":{"idle":pygame.image.load(join(PIC_RESOURCES_PATH,"eraser_idle.png")).convert_alpha(),
            "using":pygame.image.load(join(PIC_RESOURCES_PATH,"eraser_using.png")).convert_alpha()}
         }
# -----------control-vars------------
imagesize = (810,540)# TODO:ui ask the user about it
images = prevImages(pygame.Surface(imagesize,SRCALPHA,32).convert_alpha(),20)  # previous(and current) images
canvas = Canvas(images,(396,216),1.2)
tool = Tool()
BUTTON_TEXT_CLR = (0,0,0,255)
pen = Brush()
pen_button = ToolChangeButton((50,50),150,42,"Pen",BUTTON_TEXT_CLR,"dejavuserif",40,"pic_resources/grey-bg.png","pic_resources/white-bg.png","pic_resources/grey-bg.png","pen")
eraser = Brush()
eraser.change_clr((0,0,0,0))
eraser_button = ToolChangeButton((50,100),150,42,"Eraser",BUTTON_TEXT_CLR,"dejavuserif",40,"pic_resources/grey-bg.png","pic_resources/white-bg.png","pic_resources/grey-bg.png","eraser")
buttons = (pen_button,eraser_button)
shift = False
ctrl = False
alt = False
clock = pygame.time.Clock()
notificationQueue = []
# -----------controlling-functions------------
def zoomSurface(surface,scale):
    x,y=surface.get_size()
    size=(int(x*scale),int(y*scale))
    surface2 = pygame.Surface(size,SRCALPHA,32)
    pygame.transform.smoothscale(surface,size,surface2)
    return surface2

def show_background(window,canvas,div=40): # div is for the number of black/white blocks horizontally
    cw,ch = int(canvas.images.get().get_width()*canvas.zoom),int(canvas.images.get().get_height()*canvas.zoom)
    pygame.draw.rect(window,(128,128,128,255),pygame.Rect(0,0,*window.get_size())) # Grey bg
    pygame.draw.rect(window,(255,0,0,255),pygame.Rect(*canvas.pos,cw,ch),width=5)
    pygame.draw.rect(window,(250,250,250,255),pygame.Rect(*canvas.pos,cw,ch)) # TODO: use white and black array to show its transparency

def show_canvas(window,canvas):
    window.blit(zoomSurface(canvas.images.get(),canvas.zoom),canvas.pos,)

def show_cursor(window):
    if tool.t() == "pen":
        if pen.drawing == True:
            window.blit(ICONS["PEN_TOOL"]["using"],pygame.mouse.get_pos())
        else:
            window.blit(ICONS["PEN_TOOL"]["idle"],pygame.mouse.get_pos())
    elif tool.t() == "eraser":
        if eraser.drawing == True:
            window.blit(ICONS["ERASER"]["using"],pygame.mouse.get_pos())
        else:
            window.blit(ICONS["ERASER"]["idle"],pygame.mouse.get_pos())

def show_button(window):
    for b in buttons:
        b.show(window)

def show_notification(window,nq):
    # nq == notification queue
    if nq:
        for i in range(len(nq)):
            nq[i].show(window)
        return [n for n in nq if n.alive]
    return []



def save_image(image,notiQue,path=None):
    '''
    :param image:  class Surface
    '''
    try:
        if path:
            pygame.image.save(image,path)
        else:
            path = join(getcwd(), "unamed.png")
            pygame.image.save(image, path) # TODO:make file saving better
        notiQue.append(Notification("Saved succefffully at "+str(path),))
        return True
    except FileNotFoundError:
        notiQue.append(Notification("File path is not valid",))
        return False

# -----------main------------
while True:
    show_background(top,canvas)
    for i in range(3): # Smooth the drawing, but no need for video output so high
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == K_LSHIFT or event.key == K_RSHIFT:
                    shift = True
                elif event.key == K_LCTRL or event.key == K_RCTRL:
                    ctrl = True
                elif event.key == K_LALT or event.key == K_RALT:
                    alt = True
                elif ctrl == True and shift == True and event.key == K_z:  # notice those with more conditions comes first
                    canvas.images.roll_forward()
                elif ctrl == True and shift == True and event.key == K_s:
                    save_image(canvas.images.get(),notificationQueue) # TODO: I need an input box and enter file name
                elif ctrl==True and event.key == K_z:
                    canvas.images.roll_back()
                elif event.key == K_b:
                    tool.change('pen')
                elif shift == True and event.key == K_e:
                    tool.change('eraser')
                elif event.key == K_v:
                    tool.change('select')
                elif event.key == K_SPACE:
                    tool.switch()
            elif event.type == KEYUP:
                if event.key == K_LSHIFT or event.key == K_RSHIFT:
                    shift = False
                elif event.key == K_LCTRL or event.key == K_RCTRL:
                    ctrl = False
                elif event.key == K_LALT or event.key == K_RALT:
                    alt = False
            elif event.type == MOUSEBUTTONDOWN:
                for b in buttons:
                    if b.mouse_inside():
                        b.clicked(tool)
                        continue
                if tool.t()=='pen':
                    pen.start_draw(canvas.images.get(),canvas.pos,canvas.zoom)
                elif tool.t()=='eraser':
                    eraser.start_draw(canvas.images.get(),canvas.pos,canvas.zoom)
                elif tool.t()=='select': # TODO: Select
                    pass
            elif event.type == MOUSEBUTTONUP:
                for b in buttons:
                    if b.mouse_inside():
                        b.declicked()
                        continue
                if tool.t()=='pen':
                    canvas.images.add_new(pen.end_draw())
                elif tool.t()=='eraser':
                    canvas.images.add_new(eraser.end_draw())
                elif tool == 'select':
                    pass
        if tool.t()=="pen":
            if pen.drawing == True:
                canvas.images.update_cur_image(pen.draw(canvas.pos,canvas.zoom))
        elif tool.t()=="eraser":
            if eraser.drawing == True:
                canvas.images.update_cur_image(eraser.draw(canvas.pos,canvas.zoom))
    show_canvas(top,canvas)
    show_button(top)
    notificationQueue = show_notification(top,notificationQueue)
    show_cursor(top)
    clock.tick(60)
    pygame.display.update()

#TODO: ui controller can scale as I resize the window
