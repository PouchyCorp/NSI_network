import pygame as p
import tkinter as tk
from time import time
import socket
import player as Player
import pickle
import sys

def main(ip, port, name):
    p.init()

    IP = str(ip)
    PORT = int(port)

    print(f'trying to connect to server with port : {PORT} and ip : {IP}')
    server = socket.socket()
    server.connect((IP, PORT))
    print('connected')

    WIN = p.display.set_mode((1920,1080))
    WINw, WINh = WIN.get_size()
    bg = p.image.load('assets/homepage.jpg')
    bg = p.transform.scale(bg,(WINw,WINh))
    WIN.blit(bg,(0,0))
    readybuton = p.image.load('assets/ready.png')
    WIN.blit(readybuton,(785,650))
    readyButtonRect = readybuton.get_rect()
    clicSound = p.mixer.Sound('assets/clic.mp3')
    checkSprite = p.image.load('assets/check.png')
    playerFaceSprite = p.image.load('assets/playerFace.png')
    playerGreyScaleSprite = p.image.load('assets/playerGreyScale.png')
    playerFaceSprite = p.transform.scale(playerFaceSprite,(100,100))
    playerGreyScaleSprite = p.transform.scale(playerGreyScaleSprite,(100,100))


                                            
    #the different butons to choose your color

    colors=["blue","red","green","yellow","pink","orange"]
    color_selected = "blue"
    ready = False

    def draw():
        WIN.blit(readybuton,readyButtonRect)

    def drawbuton(color,x,y):
        
        playerGreyScaleSprite = p.image.load('assets/playerGreyScale.png')
        playerGreyScaleSprite = p.transform.scale(playerGreyScaleSprite,(100,100))
        butoncolor = p.Surface(playerGreyScaleSprite.get_size()).convert_alpha()
        butoncolor.fill(color)
        playerGreyScaleSprite.blit(butoncolor, (0,0), special_flags = p.BLEND_RGBA_MULT)

        
        WIN.blit(playerGreyScaleSprite,(x,y))
        
        
        WIN.blit(playerFaceSprite,(x,y))
        p.display.update()
    
    for k in range(len(colors)):
        drawbuton(colors[k],260*(k+1),500)
    WIN.blit(checkSprite,(335,505))
    
    ready = False  
    waiting = True
    while waiting:

        server.recv(1)

        for event in p.event.get() :
            if event.type == p.QUIT :
                run = False
                break
            
            if event.type == p.MOUSEBUTTONDOWN:
                mousePos = p.mouse.get_pos()

                #if clicked on a colored rectangle
                for k in range(len(colors)):
                    if 260*(k+1) <= event.pos[0] <= (260*k+360) and 500 <= event.pos[1] <= 600:
                        p.mixer.Sound.play(clicSound)
                        color_selected = colors[k]
                        
                        WIN.blit(checkSprite,((260*k+335),505))
                        
                        for j in range(len(colors)):
                            if j != k:
                                drawbuton(colors[j],260*(j+1),500)
                        
                #if clicked on the ready buton
                if readyButtonRect.collidepoint(mousePos[0],mousePos[1]) and not ready:
                    ready = True
                    countdown = time()
                    p.mixer.Sound.play(clicSound)

                    while time() - countdown < 0.2 :
                        readybuton = p.image.load('assets/ready_clicked.png')
                        WIN.blit(readybuton,(785,650))
                        p.display.update()
                    while 0.2 < time() - countdown < 0.4 :
                        readybuton = p.image.load('assets/ready.png')
                        WIN.blit(readybuton,(785,650))
                        p.display.update()
                
                if ready:
                    print("waiting for other players...")
        
        server.send(b'0' if ready else b'0')
        draw()
        p.display.update()

    return server
 

p.quit()
