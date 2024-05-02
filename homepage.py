import pygame as p
import tkinter as tk
from time import time


p.init()

WIN = p.display.set_mode((1920,1080))
WINw, WINh = WIN.get_size()
bg = p.image.load('assets/homepage.jpg')
bg = p.transform.scale(bg,(WINw,WINh))
WIN.blit(bg,(0,0))
readybuton = p.image.load('assets/ready.png')
WIN.blit(readybuton,(785,800))
p.display.update()
clicSound = p.mixer.Sound('assets/clic.mp3')
checkSprite = p.image.load('assets/check.png')
                                           
#the different butons to choose your color

colors=["blue","red","green","yellow","pink","orange"]
color_selected = "blue"
ready = False

def drawbuton(color,x,y):
    rect = p.Rect(x,y,100,100)
    p.draw.rect(WIN,color,rect)
    p.display.update()
  
for k in range(len(colors)):
    drawbuton(colors[k],(260*k+260),490)

def main():
    ready = False  
    waiting = True
    while waiting:

        for event in p.event.get() :

            if event.type == p.QUIT :
                run = False
                break
            
            if event.type == p.MOUSEBUTTONDOWN:
                
                #if clicked on a colored rectangle
                for k in range(len(colors)):
                    if (260*k+260) <= event.pos[0] <= (260*k+360) and 490 <= event.pos[1] <= 590:
                        p.mixer.Sound.play(clicSound)
                        color_selected = colors[k]
                        
                #if clicked on the ready buton
                if 785 <= event.pos[0] <= 1135 and 800 <= event.pos[1] <= 900 and ready == False :
                    ready = True
                    countdown = time()
                    p.mixer.Sound.play(clicSound)

                    while time() - countdown < 0.2 :
                        readybuton = p.image.load('assets/ready_clicked.png')
                        WIN.blit(readybuton,(785,800))
                        p.display.update()
                        
                    while 0.2 < time() - countdown < 0.4 :
                        readybuton = p.image.load('assets/ready.png')
                        WIN.blit(readybuton,(785,800))
                        p.display.update()
                    server.send(pickle.dumps({'playercolor' : color_selected,'ready' : True}))
                
                if ready:
                    print("waiting for other players...")
                    
                
                
        p.display.update()


main()
p.quit()
