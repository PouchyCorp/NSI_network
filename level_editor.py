import pygame as p

p.init()

WIN = p.display.set_mode((1000, 1000))
p.display.set_caption("TAGLIATELE Level Editor")
grid = p.image.load('background.jpg')
rects = []

def wall(x1,y1,x2,y2):
    if x2 > x1 and y2 > y1:
        return p.Rect(x1,y1,abs(x2-x1),abs(y2-y1))
    elif x2 > x1 and y2 < y1:
        return p.Rect(x1,y2,abs(x2-x1),abs(y2-y1))
    elif x2 < x1 and y2 > y1 :
        return p.Rect(x2,y1,abs(x2-x1),abs(y2-y1))
    elif x2 < x1 and y2 < y1 :
        return p.Rect(x2,y2,abs(x2-x1),abs(y2-y1))

def surfacePos(x1:int,y1:int,x2:int,y2:int):
    if x2 > x1 and y2 > y1:
        return x1,y1
    elif x2 > x1 and y2 < y1:
        return x1,y2
    elif x2 < x1 and y2 > y1 :
        return x2,y1
    elif x2 < x1 and y2 < y1 :
        return x2,y2
    return x1,y1
    
    
def draw():
    WIN.blit(grid,(0,0))
    for rect in rects:
        p.draw.rect(WIN,"red",rect)
    p.display.update()
    if clicked:
        WIN.blit(ghostSurface,ghostSurfacePos)

running = True
clicked = False
    
while running :
    
    for event in p.event.get() :

        if event.type == p.QUIT :
            running = False
        if event.type == p.MOUSEBUTTONDOWN:
            button_type = event.button

            if clicked == False :
                x1,y1 = event.pos
                clicked = True
            elif clicked == True :
                x2,y2 = event.pos
                clicked = False
                rects.append(wall(x1,y1,x2,y2))

        if clicked == True:
            try:
                ghostSurfacePos : tuple = surfacePos(x1,y1,p.mouse.get_pos()[0],p.mouse.get_pos()[1])
                ghostSurface = p.Surface((abs(p.mouse.get_pos()[0]-x1),abs(p.mouse.get_pos()[1]-y1)))
                ghostSurface.set_alpha(128)
                ghostSurface.fill('blue')
            except:
                print('owo')
                pass
        
        draw()

            
            
    p.display.update()
