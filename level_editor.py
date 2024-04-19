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
            coor += coor % r
    return coor

def main():
    p.init()
    WIN = p.display.set_mode((1000, 1000))
    p.display.set_caption("TAGLIATELE Level Editor")
    grid = p.image.load('assets/background.jpg')
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
        for wall in walls:
            p.draw.rect(WIN,wall["color"],wall["rect"])
        p.display.update()
        if clicked:
            WIN.blit(ghostSurface,ghostSurfacePos)

    running = True
    clicked = False
    color = ""
    color_fill = ""
    r = 6
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
                
                    ghostSurfacePos : tuple = surfacePos(x1,y1,p.mouse.get_pos()[0],p.mouse.get_pos()[1])
                    ghostSurface = p.Surface((abs(p.mouse.get_pos()[0]-x1),abs(p.mouse.get_pos()[1]-y1)))
                    ghostSurface.set_alpha(128)
                    ghostSurface.fill(color_fill)

            
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

