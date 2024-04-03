from socket import socket
from time import sleep
import pygame as p
from random import randint
import pickle
from player import Player

print('trying to connect to server')
server = socket()
server.connect( ('127.0.0.1', 16384) )
print('connected')

p.init()
WIN = p.display.set_mode((500,500))

OtherPlayers : dict[int, Player] = {}

debugMode = False
run = True
def mainLoop():
    global run
    global OtherPlayers

    attackSpeed = 0.5
    attackSpeedTimer = 1
    localPlayer : Player = pickle.loads(server.recv(2048))
    while run:

        attackSpeedTimer += attackSpeed/60
        if attackSpeedTimer >= 1:
            localPlayer.shoot()

        for bullet in localPlayer.shootedBullets:
            bullet.updateValues()
            bullet.move()
        localPlayer.move()
        localPlayer.updateValues()

        server.send(pickle.dumps(localPlayer))
        if debugMode:print('player sent to server')

        msg = server.recv(2048)        
        OtherPlayers = {}
        if msg != b'0':
            data : dict[int,Player] = pickle.loads(msg)
            if debugMode:print(data)
            for player in data.values():
                OtherPlayers[player.num] = player
            if debugMode:print('players recieved from server')
        else : 
            if debugMode:print('no other player from server')

        if debugMode:print(len(OtherPlayers))
        
        
       # if serverMessage:
       #     otherPlayer = Player()


        WIN.fill('black')
        p.draw.rect(WIN, "blue", localPlayer.rect)
        for player in OtherPlayers.values():
            p.draw.rect(WIN, "red", player.rect)
        for bullet in localPlayer.shootedBullets:
            p.draw.rect(WIN,'green',bullet.rect)
        p.draw.line(WIN,'blue',localPlayer.pos, p.mouse.get_pos())
        p.display.update()

        for event in p.event.get():
                if event.type == p.QUIT:
                    run = False
                    return

mainLoop()
server.close()
p.quit()
