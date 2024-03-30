from socket import socket
from time import sleep
import pygame as pg
from random import randint
import pickle
from player import Player

print('trying to connect to server')
server = socket()
server.connect( ('127.0.0.1', 16384) )
print('connected')

WIN = pg.display.set_mode((500,500))

OtherPlayers : dict[int, Player] = {}

run = True
def mainLoop():
    global run
    localPlayer : Player = pickle.loads(server.recv(2048))
    while run:
        localPlayer.move()
        localPlayer.updateValues()

        server.send(pickle.dumps(localPlayer))
        print('player sent to server')

        msg = server.recv(20480)
        if msg != b'0':
            data : dict[int,Player] = pickle.loads(msg)
            print(data)
            for player in data.values():
                print(player)
                OtherPlayers[player.num] = player
            print('players recieved from server')
        else : 
            print('no other player from server')
        
        
       # if serverMessage:
       #     otherPlayer = Player()


        WIN.fill('black')
        pg.draw.rect(WIN, "blue", localPlayer.rect)
        for player in OtherPlayers.values():
            pg.draw.rect(WIN, "red", player.rect)
        pg.display.update()

        for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    return

mainLoop()
server.close()
pg.quit()
