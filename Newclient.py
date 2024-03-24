from socket import socket
from time import sleep
import pygame as pg
from random import randint

print('starting')
server = socket()
server.connect( ('127.0.0.1', 16384) )
############

WIN = pg.display.set_mode((500,500))


def draw():
    WIN.fill('black')
    

class Player():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rect = (x,y,20,20)

    def draw(self):
        pg.draw.rect(WIN, "red", self.rect)

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.x -= 1
        if keys[pg.K_RIGHT]:
            self.x += 1
        if keys[pg.K_DOWN]:
            self.y += 1
        if keys[pg.K_UP]:
            self.y -= 1
    def updateValues(self):
        self.rect = (self.x,self.y,20,20)

localPlayer = Player(50,50)

run = True
def mainLoop():
    global run
    global localPlayer
    while run:
        localPlayer.move()

        localPlayer.updateValues()
        response = str("PlayerX:"+str(localPlayer.x)+"/"+"PlayerY:"+str(localPlayer.y))
        server.send(response.encode())

        serverMessage = server.recv(1000).decode()
       # if serverMessage:
       #     otherPlayer = Player()


        draw()
        localPlayer.draw()
        pg.display.update()

        for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    return

mainLoop()
server.close()
pg.quit()
