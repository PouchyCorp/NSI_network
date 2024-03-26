from socket import socket
from time import sleep
import pygame as pg
from random import randint
import pickle
from player import Player

print('trying to connect to server')
server = socket()
server.connect( ('127.0.0.1', 16384) )
############

WIN = pg.display.set_mode((500,500))

run = True
def mainLoop():
    global run
    localPlayer = pickle.loads(server.recv(2048))
    while run:
        localPlayer.move()
        localPlayer.updateValues()
        server.send(pickle.dumps(localPlayer))

        player2 : Player = pickle.loads(server.recv(2048))
        
       # if serverMessage:
       #     otherPlayer = Player()


        WIN.fill('black')
        pg.draw.rect(WIN, "blue", localPlayer.rect)
        pg.draw.rect(WIN, "red", player2.rect)
        pg.display.update()

        for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    return

mainLoop()
server.close()
pg.quit()
