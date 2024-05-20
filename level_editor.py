import pygame as p
import tkinter as tk
import pickle 

walls = []

def save():
    fileName = e1.get()
    with open("Maps/"+fileName+'.pkl','wb') as file:
        pickle.dump(walls,file)

def snap(coor,r):
    if coor % r != 0:
        if coor % r < r/2:
            coor -= coor % r
        else:
            coor += (r - (coor % r))
    return int(coor)

def main():
    p.init()
    WIN = p.display.set_mode((1920, 1080))
    p.display.set_caption("TAGLIATELE Level Editor")
    grid = p.image.load('assets/background.jpg')
    WIDTH, HEIGHT = WIN.get_size()
    gridXSize, gridYSize = HEIGHT/50, HEIGHT/50
    
    def wall(x1,y1,x2,y2):
        try:
            if x2 > x1 and y2 > y1:
                return p.Rect(x1,y1,abs(x2-x1),abs(y2-y1))
            elif x2 > x1 and y2 < y1:
                return p.Rect(x1,y2,abs(x2-x1),abs(y2-y1))
            elif x2 < x1 and y2 > y1 :
                return p.Rect(x2,y1,abs(x2-x1),abs(y2-y1))
            elif x2 < x1 and y2 < y1 :
                return p.Rect(x2,y2,abs(x2-x1),abs(y2-y1))
            
        except:
            return False
            
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
        x = 0
        for i in range(100):
            p.draw.line(WIN,(10,10,10),(0+x,0),(0+x,WIDTH))
            x+=gridXSize
        x = 0
        while x<=WIDTH:
            p.draw.line(WIN,(10,10,10),(0,0+x),(WIDTH,0+x))
            x+=gridXSize
        for wall in walls:
            p.draw.rect(WIN,wall["color"],wall["rect"])
        p.display.update()
        if clicked:
            WIN.blit(ghostSurface,ghostSurfacePos)

    running = True
    clicked = False
    color = ""
    color_fill = ""
    r = gridXSize
    while running :
        
        for event in p.event.get() :

            if event.type == p.QUIT :
                running = False
                break
            if event.type == p.MOUSEBUTTONDOWN:

                if clicked == False :
                    button_type = event.button
                    x1,y1 = snap(event.pos[0],r),snap(event.pos[1],r)
                    clicked = True

                elif clicked == True :
                    x2,y2 = snap(event.pos[0],r),snap(event.pos[1],r)
                    clicked = False
                    if wall(x1,y1,x2,y2):
                        walls.append({"rect" : wall(x1,y1,x2,y2), "color" : color})

                if button_type == 1:
                    color, color_fill = "red", "red"
                elif button_type == 3:
                    color, color_fill = "blue", "blue"

            if clicked == True:
                    snappedMouseX, snappedMouseY = snap(p.mouse.get_pos()[0],r) , snap(p.mouse.get_pos()[1],r)
                    ghostSurfacePos : tuple = surfacePos(x1,y1,snappedMouseX,snappedMouseY)
                    
                    ghostSurface = p.Surface((abs(snappedMouseX-x1),abs(snappedMouseY-y1)))
                    ghostSurface.set_alpha(128)
                    ghostSurface.fill(color_fill)

            if event.type == p.KEYDOWN :
                if len(walls) != 0 :
                    del(walls[-1])

            
            draw()

        p.display.update()
    p.quit()

master = tk.Tk()
tk.Label(master, 
         text="Map name").grid(row=0)
tk.Label(master, 
         text="close editor to save",fg='red').grid(row=2)


e1 = tk.Entry(master)

e1.grid(row=0, column=1)

tk.Button(master, text='Quit', command=master.quit).grid(row=4, column=3, sticky=tk.W, pady=4)
tk.Button(master, text='Create map', command=main).grid(row=4, column=1, sticky=tk.W, pady=4)
tk.Button(master, text='Save', command=save).grid(row=4, column=0, sticky=tk.W, pady=4)

tk.mainloop()

