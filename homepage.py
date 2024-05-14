import pygame as p
import tkinter as tk
from time import time
import socket
import player as Player
import pickle
import sys

class Button:
    def __init__(self, color, x, y):
        self.color = color
        self.clicked = False
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.rect = p.Rect(self.x,self.y,self.width,self.height)
        self.color = color

    def check_clicked(self) -> bool:
        if self.rect.collidepoint(p.mouse.get_pos()[0],p.mouse.get_pos()[1]):
            return self
        else:
            return None
    
    def draw(self, WIN : p.Surface, checkSprite, clicked_button):
        if self == clicked_button:
            p.draw.rect(WIN,self.color,self.rect)
            WIN.blit(checkSprite,self.rect)
        else:
            p.draw.rect(WIN,self.color,self.rect)
            




def main(ip, port, name):
    p.init()

    IP = ip
    PORT = port

    print(f'trying to connect to server with port : {PORT} and ip : {IP}')
    server = socket.socket()
    server.connect((IP, PORT))
    print('connected')

    WIN = p.display.set_mode((0,0), p.FULLSREEN)
    WINw, WINh = WIN.get_size()
    bg = p.image.load('assets/homepage.jpg')
    bg = p.transform.scale(bg,(WINw,WINh))
    WIN.blit(bg,(0,0))
    ready_button = p.image.load('assets/ready.png')
    not_ready_button = p.image.load('assets/not_ready.png')
    actual_ready_texture = not_ready_button
    readyButtonRect = actual_ready_texture.get_rect()
    readyButtonRect.x , readyButtonRect.y = 830, 780
    clicSound = p.mixer.Sound('assets/clic.mp3')
    checkSprite = p.image.load('assets/Check3.png')
    playerFaceSprite = p.image.load('assets/playerFace.png')
    playerGreyScaleSprite = p.image.load('assets/playerGreyScale.png')
    playerFaceSprite = p.transform.scale(playerFaceSprite,(100,100))
    playerGreyScaleSprite = p.transform.scale(playerGreyScaleSprite,(100,100))


                                            
    #the different butons to choose your color

    colors=["blue","red","green","yellow","pink","orange"]
    color_selected = "red"
    clicked_button = None
    buttons : list[Button] = []
    ready = False
    
    for k in range(len(colors)):
        buttons.append(Button(colors[k],260*(k+1),652))
    
    ready = False  
    waiting = True
    run = True
    while waiting and run:

        
        if server.recv(1) == b'1':
            waiting = False
            break
        else:
            waiting = True

        for event in p.event.get() :
            if event.type == p.QUIT :
                run = False
                break
            
            if event.type == p.MOUSEBUTTONDOWN:
                mousePos = p.mouse.get_pos()

                #if clicked on a colored rectangle
                for button in buttons:
                    check_clicked = button.check_clicked()
                    if check_clicked != None:
                        clicked_button = check_clicked
                        color_selected = clicked_button.color
                        
                #if clicked on the ready button
                if readyButtonRect.collidepoint(mousePos[0],mousePos[1]):
                    ready = not ready
                    p.mixer.Sound.play(clicSound)
                    actual_ready_texture = ready_button if ready else not_ready_button

        
        msg = ('1' if ready else '0')+'/'+color_selected
        server.send(msg.encode())
        WIN.blit(actual_ready_texture, readyButtonRect)
        for button in buttons:
            button.draw(WIN,checkSprite,clicked_button)
        p.display.update()

    if not run:
        return
    else:
        return server 
    
p.quit()
